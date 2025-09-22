# Programa d'anàlisi de longitud de clau (Vigenère-like)
# S'executa sobre el text proporcionat a la conversa. Mostra:
# 1) Índex de coincidència (IC)
# 2) Estimació de Friedman de la longitud de la clau
# 3) Resultats de Kasiski (repeticions i factors de distàncies)
# 4) IC mitjà per longitud de clau candidata (1..20)
# 5) Suggeriments ordenats de longituds probables

from collections import Counter, defaultdict
import re
import math
import pandas as pd

cipher_text = """
tl fmmcse dilwhkb mg qgiibhocaeqlw iafjx qdnxonh rof i xlpmxv ws zalqlyx o izhjp dx
stgxsdq xg jn fmmcse imk oiavik sas qqyfptzml rt snjlhxtnkbc eoeqtzuaummwra vwf sa
xbnkoigx lx jxgxvxft
ajcxgi mxbhrt dxc xz hen vha p lhnbqxae xkihsbi yfxewzbqw ktabgzi jcx sa vt xnpaivik sa
1863 pxzh gtmutt vpvxz xgiam lxgroumkh se figsga bvwseeglxbi pxz vvpreml ppbuizs ya xt
1846
xb tll fbtgamoxg se lcugiimcvwd phtboaftjxhxcl wg sas ttyoqema ws huuamwiuvqh sh tkqxb
bimrtbtagb eih d’nvt dprtceo rltc esmafmg rt ktabgzi imkatt t cg qgiibhocaeqlhp dxlnwg lt
thbvimcw rt lt xtfpuei vzpu
nv vce dxavcqekbt zp lhvzwiuw lx zp ptztiaa vtti tl vzbdiotvtzxsmi tzxnxi xz ieqb qwurtb xb
c chtnacel wg b ts ei eccgbbnr se ei iogantt qaan
ieshhhzxg rawi vcaufvt sh phb mfpcmik qdm xt msmt qqyfpt wcg lxfkim rt snjlhxtnkbe
bogwtzuaunmwra
vwf o iae ktrp chtnaca iwm gtr tbtqpdt ifp pnttbgx dx nksfuxvvwp Dx tt aptxqqo bagmko
futv lvp umqewiztb nbp mtynwca wm qwurtbzs se vwkftnm lx fdthz tejelb fsiowm ici pxzf-
sirx lxrjik tt zdnzqmis dxtl fdthzl wcdbdbrjaea
dohilsb sh vt iwccak lx ztxbamsccbi ws eakinzts kmisiiwml sc ee bxli xbnkoi ee yns hizvbtxct
otwgeum taq thbt dgouiuwaimim eje tynshtxa iogantxg co gwfsh ekmg zp mtbxwma tjtbh
dxt qwurtb lwco jcx o bel tt qaan khwccblbo tn ei foiebft ddsbkbc tn eml rjel wvigrxvvwts
liusct ettjdrl yns aa wqlhpnvqt sctkm iogantxg geimmwsel ml ajlmqizt dx tt zdnzqmis dx
tt qaan mko fuxamwd dx kxfrak lbttrxvmg eakinzts jcx sh rxxxhxslqg w irhjtf tl lmn apxbu
vcbu wqowhok xxf sajcxgia figsga mzhppr nv fiatbxes erhxxf p lt thbvimcw rt lt keoj
lt thbvimcw rt lt keoj sxzt ofuxam bdmuzx c plzcg tpcmwk dgifmk rpqnmlh
jn vwi rtsvwusgtt tt zdnzqmis dx tt qaan ifp fux ml jp xbnkog ee lhqjmxvm bdmxa voa
dbdbrxr xt msmt xv uzdcl lx zp mtbxwma fqwo fux tt zdnzqmis dx tt qaan q tdaivik samxbhrt elbtrxsmqv hgawqvwdntt wsa xbnkoigx lx qtstz
"""

# Normalització: mantenim només lletres A-Z en majúscules
clean = re.sub(r'[^A-Za-z]', '', cipher_text).upper()

def index_of_coincidence(text):
    N = len(text)
    if N <= 1:
        return 0.0
    freqs = Counter(text)
    s = sum(v*(v-1) for v in freqs.values())
    return s / (N*(N-1))

def friedman_estimate(text):
    N = len(text)
    ic = index_of_coincidence(text)
    # constants for English reference; formula may vary slightly
    # Using standard Friedman formula:
    # K ≈ (0.027 * N) / ((N - 1) * IC - 0.038 * N + 0.065)
    denom = (N - 1) * ic - 0.038 * N + 0.065
    if denom == 0:
        return None, ic
    K = (0.027 * N) / denom
    return K, ic

def kasiski_examination(text, min_len=3, max_len=6):
    repeats = defaultdict(list)
    text_len = len(text)
    for L in range(min_len, max_len+1):
        seen = {}
        for i in range(0, text_len - L + 1):
            chunk = text[i:i+L]
            if chunk in seen:
                prev = seen[chunk]
                repeats[chunk].append(i - prev)
                # update prev to first occurrence to gather multiple distances
                # keep the original first index to collect distances from it
            else:
                seen[chunk] = i
    # collect factors of distances
    factor_counts = Counter()
    for chunk, dists in repeats.items():
        for d in dists:
            # factorize d (consider factors up to 30)
            for f in range(2, 31):
                if d % f == 0:
                    factor_counts[f] += 1
    return repeats, factor_counts

def average_ic_by_keylength(text, max_key=20):
    results = []
    for keylen in range(1, max_key+1):
        ics = []
        for offset in range(keylen):
            subseq = text[offset::keylen]
            ics.append(index_of_coincidence(subseq))
        avg_ic = sum(ics) / len(ics)
        results.append((keylen, avg_ic))
    return results

# Run analyses
friedman_K, ic = friedman_estimate(clean)
repeats, factor_counts = kasiski_examination(clean, min_len=3, max_len=6)
avg_ics = average_ic_by_keylength(clean, max_key=20)

# Present findings
print("Text net (només lletres) longitud:", len(clean))
print("Índex de coincidència (IC): {:.6f}".format(ic))
if friedman_K:
    print("Estimació de Friedman (longitud de clau aproximada): {:.2f}".format(friedman_K))
else:
    print("Estimació de Friedman: no aplicable")

print("\nKasiski: mostres repetides trobades (chunk -> nombres de distàncies):")
# Show up to 12 repeated chunks (if any)
count = 0
for chunk, dists in sorted(repeats.items(), key=lambda kv: (-len(kv[1]), kv[0])):
    print(f"  {chunk} -> distàncies: {dists}")
    count += 1
    if count >= 12:
        break
if not repeats:
    print("  Cap repetició de longitud 3..6 trobada.")

print("\nFactors de les distàncies (freqüències) — suggeriments de claus (factors més comuns):")
for f, c in factor_counts.most_common(10):
    print(f"  Factor {f}: {c} vegades")

# Dataframe per mostrar IC mitjana per longitud candidata
df = pd.DataFrame(avg_ics, columns=["key_length", "avg_IC"]).set_index("key_length")
print(df.to_string(float_format="{:.6f}".format))


# Sorted suggestions by avg_IC (descending)
sorted_by_ic = sorted(avg_ics, key=lambda x: -x[1])[:8]
print("\nLongituds candidates ordenades per IC mitja (més probable primer):")
for k, a in sorted_by_ic:
    print(f"  {k}: avg IC = {a:.6f}")

# Heurística final: combinar Kasiski factors and Friedman estimate and IC peaks
candidates = [k for k,_ in sorted_by_ic]
kasiski_candidates = [f for f,_ in factor_counts.most_common(6)]
print("\nSuggerència final combinada (heurística):")
combined = []
# add kasiski candidates first if present and <=20
for f in kasiski_candidates:
    if f <= 20 and f not in combined:
        combined.append(f)
# then add top IC candidates
for k in candidates:
    if k not in combined:
        combined.append(k)
# then include rounded friedman if in range
kf = None
if friedman_K:
    kf = round(friedman_K)
    if 1 <= kf <= 20 and kf not in combined:
        combined.insert(0, kf)

print("  Probables longituds de clau (ordre suggerit):", combined[:10])

