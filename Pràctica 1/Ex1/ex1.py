"""
Anàlisi de freqüències per al xifratge de Cèsar
Pràctica 1 - Criptografia
EX1
"""

from collections import Counter

def comptar_lletres(text):
    """
    Compta les lletres del text.
    
    Args:
        text (str): Text a analitzar
    
    Returns:
        dict: Diccionari amb el comptatge de cada lletra
    """
    # Convertir a majúscules i mantenir només lletres
    text_net = ''.join([c for c in text.upper() if c.isalpha()])
    
    # Comptar freqüències
    frequencies = Counter(text_net)
    
    return frequencies

def mostrar_comptatge(frequencies):
    """
    Mostra el comptatge de lletres ordenat.
    
    Args:
        frequencies (dict): Diccionari amb el comptatge de lletres
    """
    print("COMPTATGE DE LLETRES:")
    print("=" * 30)
    
    # Ordenar per freqüència (major a menor)
    sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
    
    for char, count in sorted_freq:
        print(f"{char}: {count}")

def desxifrat_cesar(text, desplaçament):
    """
    Desxifra un text utilitzant el xifratge de Cèsar.
    
    Args:
        text (str): Text xifrat
        desplaçament (int): Desplaçament a aplicar (negatiu del xifratge original)
    
    Returns:
        str: Text desxifrat
    """
    result = ""
    
    for char in text:
        if char.isalpha():
            # Determinar si és majúscula o minúscula
            is_upper = char.isupper()
            char = char.upper()
            
            # Aplicar desplaçament
            shifted = chr((ord(char) - ord('A') + desplaçament) % 26 + ord('A'))
            
            # Mantenir el cas original
            if not is_upper:
                shifted = shifted.lower()
            
            result += shifted
        else:
            result += char
    
    return result

def main():
    # Text xifrat
    text_xifrat = """T SLGP DPPY ESTYRD JZF APZAWP HZFWO YZE MPWTPGP, LEELNV DSTAD
ZY QTCP ZQQ ESP DSZFWOPC ZQ ZCTZY, T HLENSPO N-MPLXD RWTEEPC
TY ESP OLCV YPLC ESP ELYYSLFDPC RLEP. LWW ESZDP XZXPYED HTWW
MP WZDE TY ETXP, WTVP EPLCD TY CLTY. ETXP EZ OTP."""
    
    print("TEXT XIFRAT:")
    print("=" * 40)
    print(text_xifrat)
    print()
    
    # Comptatge de lletres
    frequencies = comptar_lletres(text_xifrat)
    
    print(f"Total de lletres: {sum(frequencies.values())}")
    print()
    
    # Mostrar comptatge
    mostrar_comptatge(frequencies)
    
    # Provar tots els desplaçaments
    print("\nTOTS ELS POSSIBLES DESXIFRATGES:")
    print("=" * 50)
    
    for i in range(1, 26):
        desxifrat = desxifrat_cesar(text_xifrat, -i)
        print(f"Desplaçament {i:2d}: {desxifrat}")

if __name__ == "__main__":
    main()