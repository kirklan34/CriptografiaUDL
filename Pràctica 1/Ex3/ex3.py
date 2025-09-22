import re
from collections import Counter
import math

# Text xifrat
ciphertext = """
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
dbdbrxr xt msmt xv uzdcl lx zp mtbxwma fqwo fux tt zdnzqmis dx tt qaan q tdaivik sa
mxbhrt elbtrxsmqv hgawqvwdntt wsa xbnkoigx lx qtstz a
"""

#Netejar el text dels espais i números
ciphertext = re.sub(r'[^a-zA-Z]', '', ciphertext).lower()

# --- FREQÜÈNCIES CATALÀ ---
spanish_freq = {
    'a':12.53,'b':1.49,'c':4.68,'d':5.86,'e':13.68,'f':0.52,'g':1.01,
    'h':0.70,'i':6.25,'j':0.44,'k':0.11,'l':8.37,'m':3.15,'n':7.01,
    'o':8.68,'p':2.51,'q':0.88,'r':6.87,'s':7.88,'t':4.63,'u':3.93,
    'v':0.90,'w':0.04,'x':0.22,'y':0.90,'z':0.47
}
# Arrodonir les freqüències perquè si les sumem donin 100.
# Serveix per poder poder utilitzar en text de diferents tamanys
total = sum(spanish_freq.values())
spanish_freq = {k: v/total for k,v in spanish_freq.items()}

# Mirem la concentració de les lletres repetides
# El nostre objectiu es 0,07
def index_coincidence(text):
    N = len(text)#Llargada text
    freqs = Counter(text)#Cops que es repeteix una lletra
    #f es la freqüència de cada lletra i apliquem un sumatori fi(fi-1)/N(N-1)
    return sum(f*(f-1) for f in freqs.values()) / (N*(N-1)) if N > 1 else 0

#Funció per saber la llargada de la clau
#Separa el text i el separa en K textos.
#Calcula l'índex de coincidéncia del subtext i fa la mitjana
#retorna la k més llarga
def kasiski_guess_keylen(text, max_len=20):
    results = {}
    for key_len in range(1, max_len+1):
        ic_values = []
        for i in range(key_len):
            subtext = text[i::key_len]
            ic_values.append(index_coincidence(subtext))
        results[key_len] = sum(ic_values) / len(ic_values)
    return results
#Compara freqüències amb els subtextos
#Comota quantes vegades surt una lletra i ho compara amb el que serie esperavle
#Fórmula (observat - espetat)²/esperat
def chi_squared_stat(subtext, shift):
    # Desplaça el subtext
    shifted = ''.join(chr((ord(c)-ord('a')-shift) % 26 + ord('a')) for c in subtext)
    freqs = Counter(shifted)
    N = len(shifted)
    chi2 = 0 
    for ch in spanish_freq:
        observed = freqs.get(ch, 0)
        expected = spanish_freq[ch] * N
        chi2 += (observed-expected)**2 / expected if expected>0 else 0
    return chi2
#Troba la clau lletra per lletra.
#Divideix el text en subalfabets i prova els 26 desplaçaments
#tria el més petit 
def guess_key_spanish(text, key_len):
    key = ""
    for i in range(key_len):
        subtext = text[i::key_len]
        best_shift, best_chi2 = None, 1e9
        for shift in range(26):
            chi2 = chi_squared_stat(subtext, shift)
            if chi2 < best_chi2:
                best_chi2, best_shift = chi2, shift
        key += chr(ord('a') + best_shift)
    return key
#Desencripta
def vigenere_decrypt(text, key):
    plain = []
    key = key.lower()
    klen = len(key)
    for i, ch in enumerate(text):
        if ch.isalpha():
            shift = ord(key[i % klen]) - ord('a')
            p = (ord(ch) - ord('a') - shift) % 26
            plain.append(chr(ord('a') + p))
    return ''.join(plain)


ic_results = kasiski_guess_keylen(ciphertext, 20)
key_len = max(ic_results, key=ic_results.get)

print("Longitud de clau probable:", key_len)

key = guess_key_spanish(ciphertext, key_len)
print("Clau refinada:", key)

plaintext = vigenere_decrypt(ciphertext, key)
print("\nText desxifrat:")
print(plaintext)
