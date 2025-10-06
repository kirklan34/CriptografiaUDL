def exponenciacion_binaria(m, e, n):
    """
    Calcula m^e mod n usando el método de exponenciación binaria.
    
    Args:
        m (int): Base
        e (int): Exponente
        n (int): Módulo
    
    Returns:
        int: El resultado de m^e mod n
    """
    if n == 1:
        return 0
    
    if e == 0:
        return 1 % n
    
    if e < 0:
        return None
    
    # Inicialización
    resultado = 1
    base = m % n
    
    # Procesar cada bit del exponente de derecha a izquierda
    while e > 0:
        if e % 2 == 1:  # Si el bit menos significativo es 1
            resultado = (resultado * base) % n
        
        e = e // 2  # Desplazar bits a la derecha
        base = (base * base) % n  # Elevar la base al cuadrado
    
    return resultado





def main():
    """Función principal del programa"""
    try:
        # Solicitar entrada del usuario
        m = int(input("Introduce la base (m): "))
        e = int(input("Introduce el exponente (e): "))
        n = int(input("Introduce el módulo (n): "))
        
        if n <= 0:
            print("Error: El módulo debe ser un número positivo")
            return
        
        if e < 0:
            print("Error: Este programa no maneja exponentes negativos")
            return
        
        # Calcular usando exponenciación binaria
        resultado = exponenciacion_binaria(m, e, n)
        
        if resultado is not None:
            print(f"{m}^{e} mod {n} = {resultado}")
    
    except ValueError:
        print("Error: Por favor, introduce números enteros válidos")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
