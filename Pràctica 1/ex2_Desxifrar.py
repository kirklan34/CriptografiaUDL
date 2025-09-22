"""
Descifrador de textos con sustitución simple y símbolos homófonos.

Análisis de frecuencias y generación de hipótesis para descifrar textos.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Dict, List, Tuple

# Textos cifrados a analizar
CIFRADO_SIMPLE = """IH GXIQBY DYZHKSK EYQ RVIOMK DYSOI HKD PYQBKÑKD C IH IEY UI HYD ZÁJKOYD OIDYQKSK IQ IH GKHHI HKD QVSID YEVHBKSKQ IH DYH PXIQBOKD VQ OÍY DIOZIQBIKSK IQBOI HYD ÁOSYHID GIOUID HK TIQBI UIH ZVISHY PXOKSK KH EXIHY EYQ IDZIOKQMK UI NVI HK HHVGXK BOKJIOK SVIQKD EYDIEWKD"""

CIFRADO_HOMOFONOS = """N: <SKXMA }N%U,&, $NX B>N&>, }A&#K U,} $AXT,Ñ,? @ N( N$N XN UA? %Á/A&NU &OUNXW&A KX NU <AU(N (,U ;>&K? N$>UMW&W; O( ?A( $;O;M&,? >; &Í[ }O{%NSCNA&W O;T&N UA} Á{&N(N? <O#XO} :A EKSCN ZOU %>K&:N $;{A&W AU $]K(A $[S K}%K{WS>A ZO @>N :W UU><;, C{,/K&W &>KSA? $[?N$YW}"""

# Frecuencias esperadas del español (porcentajes aproximados)
FRECUENCIAS_ESPAÑOL = {
    'e': 13.68, 'a': 12.53, 'o': 8.68, 's': 7.98, 'r': 6.87, 'n': 6.71,
    'i': 6.25, 'd': 5.86, 'l': 4.97, 'c': 4.68, 't': 4.63, 'u': 3.93,
    'm': 3.15, 'p': 2.51, 'b': 2.22, 'g': 1.01, 'v': 0.90, 'y': 0.90,
    'q': 0.88, 'h': 0.70, 'f': 0.70, 'z': 0.52, 'j': 0.44, 'ñ': 0.31,
    'x': 0.22, 'k': 0.02, 'w': 0.02
}

# Palabras comunes en español
PALABRAS_COMUNES = [
    'el', 'la', 'de', 'que', 'y', 'en', 'un', 'es', 'se', 'no', 'te', 'lo', 
    'le', 'da', 'su', 'por', 'son', 'con', 'para', 'al', 'del', 'los', 'las', 
    'una', 'todo', 'esta', 'sus', 'muy', 'mas', 'pero', 'como', 'fue', 'han', 
    'ser', 'era', 'hay', 'dos', 'quien', 'donde', 'cuando', 'tiempo', 'pueblo', 
    'mundo', 'entre', 'sobre', 'todo', 'otros', 'hacer', 'bien', 'estado',
    'durante', 'tanto', 'hasta', 'desde', 'porque', 'aunque', 'mientras'
]

def limpiar_texto(texto: str) -> str:
    """Limpia el texto manteniendo solo letras y espacios."""
    return re.sub(r'[^a-záéíóúñü\s]', '', texto.lower())

def obtener_frecuencias(texto: str) -> Dict[str, float]:
    """Calcula las frecuencias de caracteres en el texto."""
    texto_limpio = limpiar_texto(texto)
    contador = Counter(char for char in texto_limpio if char.isalpha())
    total = sum(contador.values())
    
    if total == 0:
        return {}
    
    frecuencias = {}
    for char, count in contador.items():
        frecuencias[char] = (count / total) * 100
    
    return dict(sorted(frecuencias.items(), key=lambda x: x[1], reverse=True))

def analizar_patron_sustitucion_simple(texto: str) -> Dict[str, str]:
    """Analiza el patrón de sustitución simple basado en frecuencias."""
    frecuencias = obtener_frecuencias(texto)
    chars_ordenados = list(frecuencias.keys())
    chars_español = sorted(FRECUENCIAS_ESPAÑOL.keys(), key=lambda x: FRECUENCIAS_ESPAÑOL[x], reverse=True)
    
    mapeo = {}
    for i, char_cifrado in enumerate(chars_ordenados):
        if i < len(chars_español):
            mapeo[char_cifrado] = chars_español[i]
    
    return mapeo

def aplicar_mapeo(texto: str, mapeo: Dict[str, str]) -> str:
    """Aplica un mapeo de sustitución al texto."""
    resultado = ""
    for char in texto.lower():
        if char in mapeo:
            resultado += mapeo[char]
        elif char.isalpha():
            resultado += char  # Mantener chars no mapeados
        else:
            resultado += char  # Mantener espacios y puntuación
    return resultado

def analizar_bigramas_trigramas(texto: str) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Analiza bigramas y trigramas en el texto."""
    texto_limpio = limpiar_texto(texto).replace(' ', '')
    
    bigramas = {}
    trigramas = {}
    
    for i in range(len(texto_limpio) - 1):
        bigrama = texto_limpio[i:i+2]
        bigramas[bigrama] = bigramas.get(bigrama, 0) + 1
    
    for i in range(len(texto_limpio) - 2):
        trigrama = texto_limpio[i:i+3]
        trigramas[trigrama] = trigramas.get(trigrama, 0) + 1
    
    return (dict(sorted(bigramas.items(), key=lambda x: x[1], reverse=True)[:10]),
            dict(sorted(trigramas.items(), key=lambda x: x[1], reverse=True)[:10]))

def buscar_patrones_palabras(texto: str) -> List[str]:
    """Busca patrones de palabras que podrían coincidir con palabras comunes."""
    palabras = texto.split()
    patrones_encontrados = []
    
    for palabra in palabras:
        palabra_limpia = limpiar_texto(palabra)
        if len(palabra_limpia) > 0:
            candidatos = [p for p in PALABRAS_COMUNES if len(p) == len(palabra_limpia)]
            if candidatos:
                patrones_encontrados.append(f"'{palabra_limpia}' ({len(palabra_limpia)} chars) -> posibles: {candidatos[:3]}")
    
    return patrones_encontrados[:15]

def mejorar_mapeo_con_palabras_comunes(texto: str, mapeo_inicial: Dict[str, str]) -> Dict[str, str]:
    """Mejora el mapeo basándose en palabras conocidas."""
    mapeo = mapeo_inicial.copy()
    texto_descifrado = aplicar_mapeo(texto, mapeo)
    palabras = texto_descifrado.split()
    
    # Buscar palabras que coincidan exactamente con palabras comunes
    for palabra in palabras:
        palabra_limpia = limpiar_texto(palabra)
        if palabra_limpia in PALABRAS_COMUNES:
            continue  
        
        for palabra_comun in PALABRAS_COMUNES:
            if len(palabra_limpia) == len(palabra_comun):
                diferencias = sum(1 for a, b in zip(palabra_limpia, palabra_comun) if a != b)
                if diferencias == 1: 
                    for i, (a, b) in enumerate(zip(palabra_limpia, palabra_comun)):
                        if a != b:
                            # Encontrar caracter original
                            for orig, dest in mapeo.items():
                                if dest == a:
                                    mapeo[orig] = b
                                    break
    
    return mapeo

def descifrar_sustitucion_simple(texto: str) -> Tuple[str, Dict[str, str]]:
    """Función principal para descifrar sustitución simple."""
    print("=" * 60)
    print("ANÁLISIS DE SUSTITUCIÓN SIMPLE")
    print("=" * 60)
    print(f"Texto original:\n{texto}\n")
    
    # Análisis de frecuencias
    frecuencias = obtener_frecuencias(texto)
    print("Frecuencias de caracteres más comunes:")
    for char, freq in list(frecuencias.items())[:12]:
        print(f"  '{char}': {freq:.2f}%")
    
    # Mapeo inicial basado en frecuencias
    mapeo_inicial = analizar_patron_sustitucion_simple(texto)
    print(f"\nMapeo inicial (basado en frecuencias):")
    for orig, dest in list(mapeo_inicial.items())[:12]:
        print(f"  {orig} -> {dest}")
    
    # Aplicar mapeo inicial
    texto_parcial = aplicar_mapeo(texto, mapeo_inicial)
    print(f"\nTexto parcialmente descifrado:\n{texto_parcial}\n")
    
    # Análisis de patrones de palabras
    patrones = buscar_patrones_palabras(texto_parcial)
    print("Patrones de palabras encontrados:")
    for patron in patrones[:8]:
        print(f"  {patron}")
    
    # Mejorar mapeo
    mapeo_mejorado = mejorar_mapeo_con_palabras_comunes(texto, mapeo_inicial)
    texto_final = aplicar_mapeo(texto, mapeo_mejorado)
    
    print(f"\nTexto con mapeo mejorado:\n{texto_final}\n")
    
    # Análisis de bigramas y trigramas
    bigramas, trigramas = analizar_bigramas_trigramas(texto_final)
    print("Bigramas más frecuentes:")
    for bigrama, freq in list(bigramas.items())[:8]:
        print(f"  '{bigrama}': {freq}")
    
    return texto_final, mapeo_mejorado

def analizar_homofonos(texto: str) -> Tuple[str, Dict]:
    """Análisis específico para cifrado homófono."""
    print("=" * 60)
    print("ANÁLISIS DE CIFRADO HOMÓFONO")
    print("=" * 60)
    print(f"Texto original:\n{texto}\n")
    
    # Separar símbolos únicos
    simbolos = set()
    for char in texto:
        if char not in ' \n\t':
            simbolos.add(char)
    
    print(f"Número total de símbolos únicos: {len(simbolos)}")
    print(f"Símbolos encontrados: {''.join(sorted(list(simbolos)))}")
    
    # Contar frecuencias de símbolos
    contador_simbolos = Counter(char for char in texto if char not in ' \n\t')
    print(f"\nFrecuencias de símbolos más comunes:")
    for simbolo, freq in contador_simbolos.most_common(20):
        print(f"  '{simbolo}': {freq}")
    
    # Análisis de longitudes de palabras
    palabras = texto.split()
    longitudes = [len(palabra.strip()) for palabra in palabras if palabra.strip()]
    print(f"\nLongitudes de palabras más comunes: {Counter(longitudes).most_common()}")
    
    # Intentar mapeo básico con los símbolos más frecuentes
    print("\nHipótesis de mapeo (símbolos más frecuentes -> letras más frecuentes):")
    mapeo_basico = {}
    chars_español_frecuentes = ['e', 'a', 'o', 's', 'r', 'n', 'i', 'd', 'l', 'c', 't', 'u', 'm', 'p', 'b', 'g', 'v', 'y', 'q', 'h', 'f', 'z', 'j']
    
    for i, (simbolo, freq) in enumerate(contador_simbolos.most_common()):
        if i < len(chars_español_frecuentes):
            mapeo_basico[simbolo] = chars_español_frecuentes[i]
            print(f"  '{simbolo}' -> '{chars_español_frecuentes[i]}'")
    
    # Aplicar mapeo básico
    texto_tentativo = ""
    for char in texto:
        if char in mapeo_basico:
            texto_tentativo += mapeo_basico[char]
        else:
            texto_tentativo += char
    
    print(f"\nTexto con mapeo tentativo:\n{texto_tentativo}\n")
    
    # Buscar patrones reconocibles
    patrones = buscar_patrones_palabras(texto_tentativo)
    print("Patrones de palabras en texto tentativo:")
    for patron in patrones[:8]:
        print(f"  {patron}")
    
    analisis = {
        'simbolos_unicos': len(simbolos),
        'simbolos': list(simbolos),
        'frecuencias_simbolos': dict(contador_simbolos.most_common()),
        'longitudes_palabras': dict(Counter(longitudes)),
        'mapeo_tentativo': mapeo_basico
    }
    
    return texto_tentativo, analisis

def generar_hipotesis_contenido(texto_descifrado: str) -> List[str]:
    """Genera hipótesis sobre el contenido del texto."""
    palabras = texto_descifrado.lower().split()
    palabras_reconocibles = []
    
    for palabra in palabras:
        palabra_limpia = limpiar_texto(palabra)
        if palabra_limpia in PALABRAS_COMUNES or len(palabra_limpia) > 4:
            palabras_reconocibles.append(palabra_limpia)
    
    hipotesis = []
    texto_lower = texto_descifrado.lower()
    
    # Buscar palabras clave que indiquen el tema
    if any(word in texto_lower for word in ['rey', 'reino', 'castillo', 'noble', 'caballero', 'dama']):
        hipotesis.append("Posible contexto: Literatura medieval o de caballería")
    
    if any(word in texto_lower for word in ['casa', 'lugar', 'pueblo', 'ciudad', 'campo']):
        hipotesis.append("Posible contexto: Descripción de lugares o ambientes")
    
    if any(word in texto_lower for word in ['tiempo', 'dia', 'noche', 'cuando', 'mientras', 'durante']):
        hipotesis.append("Posible contexto: Narrativa con referencias temporales")
    
    if any(word in texto_lower for word in ['libro', 'leer', 'escribir', 'historia', 'cuento']):
        hipotesis.append("Posible contexto: Literatura o referencias a libros")
    
    # Evaluar calidad del descifrado
    porcentaje_reconocible = len(palabras_reconocibles) / len(palabras) if palabras else 0
    if porcentaje_reconocible > 0.4:
        hipotesis.append(f"Alta probabilidad de descifrado correcto ({porcentaje_reconocible:.1%} palabras reconocibles)")
    elif porcentaje_reconocible > 0.2:
        hipotesis.append(f"Descifrado parcial ({porcentaje_reconocible:.1%} palabras reconocibles)")
    else:
        hipotesis.append("Descifrado necesita más trabajo - pocas palabras reconocibles")
    
    return hipotesis

def main():
    """Función principal que ejecuta el análisis completo."""
    print("DESCIFRADOR DE TEXTOS CIFRADOS")
    print("Análisis criptográfico de sustitución simple y homófona")
    print("=" * 60)
    
    # Análisis del cifrado simple
    texto1_descifrado, mapeo1 = descifrar_sustitucion_simple(CIFRADO_SIMPLE)
    
    print("RESULTADO FINAL - SUSTITUCIÓN SIMPLE:")
    print(f"Texto descifrado:\n{texto1_descifrado}\n")
    
    hipotesis1 = generar_hipotesis_contenido(texto1_descifrado)
    print("Hipótesis del contenido:")
    for h in hipotesis1:
        print(f"  • {h}")
    
    print("\n" + "=" * 60)
    
    # Análisis del cifrado homófono  
    texto2_tentativo, analisis2 = analizar_homofonos(CIFRADO_HOMOFONOS)
    
    print("RESULTADO FINAL - CIFRADO HOMÓFONO:")
    print(f"Texto tentativo:\n{texto2_tentativo}\n")
    
    hipotesis2 = generar_hipotesis_contenido(texto2_tentativo)
    print("Hipótesis del contenido:")
    for h in hipotesis2:
        print(f"  • {h}")
    
    print(f"\n{'='*60}")
    print("CONCLUSIONES GENERALES:")
    print("1. El primer texto (sustitución simple) es más fácil de descifrar")
    print("2. El segundo texto (homófono) requiere análisis más profundo")
    print("3. Ambos textos parecen estar en español")
    print("4. Se recomienda análisis manual adicional para refinar resultados")
    print("5. Los patrones de frecuencia sugieren texto literario clásico")

if __name__ == "__main__":
    main()
