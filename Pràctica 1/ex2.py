#!/usr/bin/env python3n/env python3
"""
Exercici 2 — Comparació substitució simple i símbols homòfons.

Compareu les freqüències d’aparició dels caràcters d’un i altre mètode.
"""
from __future__ import annotations

import math
import random
from collections import Counter, defaultdict
from typing import Dict, List, Tuple


PLAINTEXT = """
En un lugar de la Mancha, de cuyo nombre no quiero acordarme, no ha mucho
tiempo que vivía un hidalgo de los de lanza en astillero, adarga antigua, rocín flaco
y galgo corredor. Una olla de algo más vaca que carnero, salpicón las más noches,
duelos y quebrantos los sábados, lantejas los viernes, algún palomino de anadidura
los domingos, consumían las tres partes de su hacienda. El resto della concluían
sayo de velarte, calzas de velludo para las fiestas, con sus pantuflos de lo mesmo, y
los días de entresemana se honraba con su vellorí de lo más fino. Tenía en su casa
una ama que pasaba de los cuarenta, y una sobrina que no llegaba a los veinte, y un
mozo de campo y plaza, que así ensillaba el rocín como tomaba la podadera. Frisaba
la edad de nuestro hidalgo con los cincuenta anos; era de complexión recia, seco
de carnes, enjuto de rostro, gran madrugador y amigo de la caza. Quieren decir
que tenía el sobrenombre de Quijada, o Quesada, que en esto hay alguna diferencia
en los autores que deste caso escriben; aunque, por conjeturas verosímiles, se deja
entender que se llamaba Quejana. Pero esto importa poco a nuestro cuento; basta
que en la narración del no se salga un punto de la verdad.
Es, pues, de saber que este sobredicho hidalgo, los ratos que estaba ocioso, que eran
los más del ano, se daba a leer libros de caballerías, con tanta afición y gusto, que
olvidó casi de todo punto el ejercicio de la caza, y aun la administración de su
hacienda. Y llegó a tanto su curiosidad y desatino en esto, que vendió muchas
hanegas de tierra de sembradura para comprar libros de caballerías en que leer,
y así, llevó a su casa todos cuantos pudo haber dellos; y de todos, ningunos le parecían tan bien como los que compuso el famoso Feliciano de Silva, porque la
claridad de su prosa y aquellas entricadas razones suyas le parecían de perlas, y
más cuando llegaba a leer aquellos requiebros y cartas de desafíos, donde en muchas
partes hallaba escrito: La razón de la sinrazón que a mi razón se hace, de tal
manera mi razón enflaquece, que con razón me quejo de la vuestra fermosura. Y
también cuando leía: ...los altos cielos que de vuestra divinidad divinamente con
las estrellas os fortifican, y os hacen merecedora del merecimiento que merece la
vuestra grandeza.
"""


def get_letters(text: str) -> List[str]:
	"""Return list of unique alphabetic characters found in text (lowercased).

	We consider any character for which str.isalpha() is True as a symbol to
	be substituted. This preserves accents as distinct symbols.
	"""
	s = {c.lower() for c in text if c.isalpha()}
	return sorted(s)


def simple_substitution_map(letters: List[str], seed: int = 42) -> Dict[str, str]:
	rand = random.Random(seed)
	shuffled = letters.copy()
	rand.shuffle(shuffled)
	return {p: c for p, c in zip(letters, shuffled)}


def encrypt_simple(text: str, mapping: Dict[str, str]) -> str:
	out = []
	for ch in text:
		key = ch.lower()
		if key.isalpha() and key in mapping:
			sub = mapping[key]
			out.append(sub.upper() if ch.isupper() else sub)
		else:
			out.append(ch)
	return ''.join(out)


def allocate_homophones(letters: List[str], freqs: Dict[str, int], total_tokens: int, seed: int = 42) -> Dict[str, List[str]]:
	"""Allocate single-character homophone symbols among plaintext letters.

	The ciphertext alphabet is drawn from a pool of letters, digits, punctuation
	and a selection of accented letters. Each plaintext letter receives one or
	more single-character homophones. If the requested pool size is larger than
	the available symbol pool, it is reduced.
	"""
	rand = random.Random(seed)
	# candidate pool of single-character symbols (letters, digits, punctuation,
	# some accented letters). This should be large enough for typical total_tokens.
	candidate = list(
		"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
		"!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~¡¿áéíóúÁÉÍÓÚàèìòùñÑçÇœŒß"
	)
	# ensure unique
	candidate = sorted(set(candidate), key=lambda x: rand.random())
	if total_tokens > len(candidate):
		total_tokens = len(candidate)

	n = len(letters)
	if total_tokens < n:
		total_tokens = n

	# base assign 1 per letter
	allocation = {L: 1 for L in letters}
	remaining = total_tokens - n
	total_freq = sum(freqs.get(L, 0) for L in letters)
	if total_freq == 0:
		for i in range(remaining):
			allocation[letters[i % n]] += 1
	else:
		extras = []
		for L in letters:
			proportion = freqs.get(L, 0) / total_freq
			extras.append((L, proportion * remaining))
		assigned = 0
		for L, val in extras:
			add = int(math.floor(val))
			allocation[L] += add
			assigned += add
		leftovers = remaining - assigned
		if leftovers > 0:
			frac = [(L, (val - math.floor(val))) for L, val in extras]
			choices = []
			for L, f in frac:
				weight = int(round(f * 100))
				if weight <= 0:
					weight = 1
				choices.extend([L] * weight)
			for i in range(leftovers):
				pick = rand.choice(choices)
				allocation[pick] += 1

	# assign actual single-character symbols
	rand.shuffle(candidate)
	out: Dict[str, List[str]] = {}
	idx = 0
	for L in letters:
		cnt = allocation[L]
		out[L] = candidate[idx: idx + cnt]
		idx += cnt
	return out


def encrypt_homophonic(text: str, homo_map: Dict[str, List[str]], seed: int = 42) -> str:
	rand = random.Random(seed)
	out_chars: List[str] = []
	for ch in text:
		key = ch.lower()
		if key.isalpha() and key in homo_map:
			symbol = rand.choice(homo_map[key])
			out_chars.append(symbol)
		else:
			# preserve non-alpha characters (spaces, punctuation, digits) as-is
			out_chars.append(ch)
	return ''.join(out_chars)


def token_freqs_homophonic(ciphertext: str, pool: List[str]) -> Counter:
	# count occurrences of single-character homophone symbols drawn from pool
	pool_set = set(pool)
	return Counter(ch for ch in ciphertext if ch in pool_set)


def char_freqs_simple(ciphertext: str) -> Counter:
	return Counter(c.lower() for c in ciphertext if c.isalpha())


def entropy_from_counts(counter: Counter) -> float:
	total = sum(counter.values())
	if total == 0:
		return 0.0
	ent = 0.0
	for v in counter.values():
		p = v / total
		ent -= p * math.log2(p)
	return ent


def stddev_from_counts(counter: Counter) -> float:
	vals = list(counter.values())
	if not vals:
		return 0.0
	mean = sum(vals) / len(vals)
	var = sum((x - mean) ** 2 for x in vals) / len(vals)
	return math.sqrt(var)


def print_frequencies(counter: Counter, title: str) -> None:
    print(f'\n{title}:')
    total = sum(counter.values())
    for sym, cnt in counter.most_common():
        percentage = (cnt / total) * 100
        print(f'  {sym}: {cnt} ({percentage:.2f}%)')


def main() -> None:
    seed = 42
    text = PLAINTEXT
    letters = get_letters(text)

    # frequency of plaintext letters (lowercase)
    plain_letter_counts = Counter(c.lower() for c in text if c.isalpha())

    # --- simple substitution ---
    simple_map = simple_substitution_map(letters, seed=seed)
    simple_cipher = encrypt_simple(text, simple_map)
    freq_simple = char_freqs_simple(simple_cipher)

    # --- homophonic substitution ---
    # choose pool size (a few times the alphabet size) to allow flattening
    total_tokens = max(200, len(letters) * 6)
    homo_alloc = allocate_homophones(letters, plain_letter_counts, total_tokens, seed=seed)
    # flatten the pool list for later frequency counting
    pool_list = [sym for syms in homo_alloc.values() for sym in syms]
    homo_cipher = encrypt_homophonic(text, homo_alloc, seed=seed)
    freq_homo = token_freqs_homophonic(homo_cipher, pool_list)

    # stats
    ent_simple = entropy_from_counts(freq_simple)
    ent_homo = entropy_from_counts(freq_homo)
    sd_simple = stddev_from_counts(freq_simple)
    sd_homo = stddev_from_counts(freq_homo)

    # print everything to terminal
    print('== COMPARACIÓ DE XIFRATS: SUBSTITUCIÓ SIMPLE VS HOMÒFON ==\n')
    
    print('TEXT ORIGINAL:')
    print(text.strip())
    
    print('\n' + '='*80)
    print('TEXT XIFRAT AMB SUBSTITUCIÓ SIMPLE:')
    print(simple_cipher)
    
    print('\n' + '='*80)
    print('TEXT XIFRAT AMB MÈTODE HOMÒFON:')
    print(homo_cipher)
    
    print('\n' + '='*80)
    print_frequencies(freq_simple, 'FREQÜÈNCIES - SUBSTITUCIÓ SIMPLE')
    
    print('\n' + '='*80)
    print_frequencies(freq_homo, 'FREQÜÈNCIES - MÈTODE HOMÒFON')
    
    print('\n' + '='*80)
    print('COMPARACIÓ ESTADÍSTICA:')
    print(f'\nPlaintext:')
    print(f'  Únics símbols: {len(letters)}')
    
    print(f'\nSubstitució simple:')
    print(f'  Símbols en xifrat: {len(freq_simple)}')
    print(f'  Símbol més freqüent: {freq_simple.most_common(1)[0][0]} ({freq_simple.most_common(1)[0][1]} aparicions)')
    
    print(f'\nMètode homòfon:')
    if freq_homo:
        print(f'  Token més freqüent: {freq_homo.most_common(1)[0][0]} ({freq_homo.most_common(1)[0][1]} aparicions)')
    
if __name__ == '__main__':
	main()

