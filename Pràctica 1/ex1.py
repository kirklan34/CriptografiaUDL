"""
Anàlisi de freqüències per al xifratge de Cèsar
Pràctica 1 - Criptografia
EX1
"""

from collections import Counter

# Freqüències de lletres en anglès (en percentatge)
FREQUENCIES_ENGLISH = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
    'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
    'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
    'P': 1.9, 'B': 1.3, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

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

def calcular_chi_quadrat(frequencies_observades, total_lletres):
    """
    Calcula l'estadístic chi-quadrat per comparar amb les freqüències de l'anglès.
    
    Args:
        frequencies_observades (dict): Freqüències observades en el text
        total_lletres (int): Total de lletres en el text
    
    Returns:
        float: Valor de chi-quadrat (menor valor indica millor ajust a l'anglès)
    """
    chi_quadrat = 0.0
    
    for lletra in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        # Freqüència observada
        observada = frequencies_observades.get(lletra, 0)
        
        # Freqüència esperada segons l'anglès
        esperada = (FREQUENCIES_ENGLISH[lletra] / 100.0) * total_lletres
        
        # Evitar divisió per zero
        if esperada > 0:
            chi_quadrat += ((observada - esperada) ** 2) / esperada
    
    return chi_quadrat

def mostrar_frequencies_anglès():
    """
    Mostra les freqüències de lletres en anglès ordenades.
    """
    print("FREQÜÈNCIES TÍPIQUES EN ANGLÈS:")
    print("=" * 35)
    
    # Ordenar per freqüència (major a menor)
    sorted_english = sorted(FREQUENCIES_ENGLISH.items(), key=lambda x: x[1], reverse=True)
    
    for char, freq in sorted_english:
        print(f"{char}: {freq:4.1f}%")

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
    
    print()
    
    # Mostrar freqüències de l'anglès per comparació
    mostrar_frequencies_anglès()
    
    # Analitzar tots els desplaçaments i trobar el millor
    print("\nANÀLISI DE TOTS ELS DESPLAÇAMENTS:")
    print("=" * 50)
    
    millor_desplaçament = 0
    millor_chi_quadrat = float('inf')
    resultats_analisi = []
    
    for i in range(1, 26):
        desxifrat = desxifrat_cesar(text_xifrat, -i)
        freq_desxifrat = comptar_lletres(desxifrat)
        total_lletres = sum(freq_desxifrat.values())
        
        chi_quadrat = calcular_chi_quadrat(freq_desxifrat, total_lletres)
        resultats_analisi.append((i, chi_quadrat, desxifrat))
        
        if chi_quadrat < millor_chi_quadrat:
            millor_chi_quadrat = chi_quadrat
            millor_desplaçament = i
    
    # Ordenar per chi-quadrat (millor ajust primer)
    resultats_analisi.sort(key=lambda x: x[1])
    
    print("MILLORS CANDIDATS (ordenats per similitud amb l'anglès):")
    print("-" * 60)
    for i, (desplaçament, chi_val, text_desxifrat) in enumerate(resultats_analisi[:5]):
        print(f"{i+1}. Desplaçament {desplaçament:2d} (χ² = {chi_val:8.2f}):")
        # Mostrar només les primeres línies per estalviar espai
        primera_linia = text_desxifrat.split('\n')[0]
        print(f"   {primera_linia}...")
        print()
    
    print(f"MILLOR CANDIDAT: Desplaçament {millor_desplaçament}")
    print("=" * 50)
    millor_text = desxifrat_cesar(text_xifrat, -millor_desplaçament)
    print(millor_text)
    
    # Provar tots els desplaçaments
    print("\n\nTOTS ELS POSSIBLES DESXIFRATGES:")
    print("=" * 50)
    
    for i in range(1, 26):
        desxifrat = desxifrat_cesar(text_xifrat, -i)
        print(f"Desplaçament {i:2d}: {desxifrat}")

if __name__ == "__main__":
    main()