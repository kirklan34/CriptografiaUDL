texto = """

 """

def limpiar_texto(texto):
    clean = re.sub(r'[^A-Za-z]', '', texto).upper()
"""
Dividim el text en subcadenes
Calculem l'índex de coincidencia que és igual a la freqüència.
Si aquest esta aprop del 0.068 podem tenir la clau
"""
def indice_coincidencia(texto):
    long = len(texto)
    if long <= 1:
        return 0.0
    freqs = Counter(texto)

def estimar_longitud_clave(texto, max_long=20):
    resultados = []
    for m in range(1, max_long+1):
        ics = []
        for i in range(m):


def analizar_columna(columna):
    # comparar frecuencias con las del idioma (ej: español o inglés)
    # devolver posible desplazamiento
    pass

# 5. Reconstruir clave
def reconstruir_clave(texto, longitud):
    pass

# 6. Descifrar con clave
def descifrar_vigenere(texto, clave):
    pass

# 7. Programa principal
def main():
    texto_cifrado = "AQUÍ_PONES_EL_TEXTO"
    
    texto = limpiar_texto(texto_cifrado)
    
    # Paso 1: Estimar longitud de clave
    longitudes = kasiski(texto)
    long_candidata = estimar_longitud_clave(texto)
    
    # Paso 2: Reconstruir clave
    clave = reconstruir_clave(texto, long_candidata)
    
    # Paso 3: Descifrar
    mensaje = descifrar_vigenere(texto, clave)
    
    print("Clave encontrada:", clave)
    print("Mensaje descifrado:", mensaje)

if __name__ == "__main__":
    main()
