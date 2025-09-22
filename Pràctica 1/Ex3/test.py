import re
from collections import Counter
import string

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
dbdbrxr xt msmt xv uzdcl lx zp mtbxwma fqwo fux tt zdnzqmis dx tt qaan q tdaivik samxbhrt elbtrxsmqv hgawqvwdntt wsa xbnkoigx lx qtstz
"""

# --- PREPROCESSING ---
ciphertext = re.sub(r'[^a-zA-Z]', '', ciphertext).lower()

# --- FUNCIONS ---
def index_coincidence(text):
    N = len(text)
    freqs = Counter(text)
    return sum(f*(f-1) for f in freqs.values()) / (N*(N-1)) if N > 1 else 0

def kasiski_guess_keylen(text, max_len=20):
    results = {}
    for key_len in range(1, max_len+1):
        ic_values = []
        for i in range(key_len):
            subtext = text[i::key_len]
            ic_values.append(index_coincidence(subtext))
        results[key_len] = sum(ic_values) / len(ic_values)
    return results

def guess_key(text, key_len, most_common_plain='e'):
    key = ""
    for i in range(key_len):
        subtext = text[i::key_len]
        freqs = Counter(subtext)
        if not freqs:
            key += '?'
            continue
        most_common_cipher, _ = freqs.most_common(1)[0]
        shift = (ord(most_common_cipher) - ord(most_common_plain)) % 26
        key_letter = chr(ord('a') + shift)
        key += key_letter
    return key

# --- ESTIMACIÓ ---
ic_results = kasiski_guess_keylen(ciphertext, 20)
print("Índex de coincidència per longitud de clau:")
for k, v in ic_results.items():
    print(f"Llargada {k}: IC = {v:.3f}")

# Triem la llargada amb IC més alt
key_len = max(ic_results, key=ic_results.get)
print(f"\nLongitud de clau més probable: {key_len}")

# Deduïm la clau
key = guess_key(ciphertext, key_len, most_common_plain='e')
print(f"\nClau probable: {key}")
