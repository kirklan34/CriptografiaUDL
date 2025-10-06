def mcd_euclides(d, n):
    """
    Calcula el máximo común divisor de dos enteros d y n
    usando el algoritmo de Euclides.
    
    Args:
        d (int): Primer entero
        n (int): Segundo entero
    
    Returns:
        int: El máximo común divisor de d y n
    """
    # Convertir a valores absolutos para manejar números negativos
    d = abs(d)
    n = abs(n)
    
    # Asegurar que d >= n para el algoritmo
    if d < n:
        d, n = n, d
    
    print(f"Calculando MCD({d}, {n}) usando el algoritmo de Euclides:")
    
    # Algoritmo de Euclides
    while n != 0:
        resto = d % n
        print(f"{d} = {n} × {d // n} + {resto}")
        d = n
        n = resto
    
    return d


def mcd_euclides_extendido(d, n):
    """
    Versión extendida del algoritmo de Euclides que también calcula
    los coeficientes de Bézout.
    
    Args:
        d (int): Primer entero
        n (int): Segundo entero
    
    Returns:
        tuple: (mcd, x, y) donde mcd = d*x + n*y
    """
    # Guardar los valores originales
    d_orig, n_orig = d, n
    
    # Convertir a valores absolutos
    d = abs(d)
    n = abs(n)
    
    # Asegurar que d >= n
    if d < n:
        d, n = n, d
        intercambiado = True
    else:
        intercambiado = False
    
    # Inicializar coeficientes
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    print(f"\nCalculando MCD extendido de ({d_orig}, {n_orig}):")
    
    d_temp, n_temp = d, n
    while n_temp != 0:
        cociente = d_temp // n_temp
        resto = d_temp % n_temp
        
        print(f"{d_temp} = {n_temp} × {cociente} + {resto}")
        
        # Actualizar coeficientes
        x0, x1 = x1, x0 - cociente * x1
        y0, y1 = y1, y0 - cociente * y1
        
        d_temp = n_temp
        n_temp = resto
    
    mcd = d_temp
    
    # Ajustar coeficientes si se intercambiaron los números
    if intercambiado:
        x0, y0 = y0, x0
    
    # Ajustar signos según los valores originales
    if d_orig < 0:
        x0 = -x0
    if n_orig < 0:
        y0 = -y0
    
    print(f"\nResultado: MCD = {mcd}")
    print(f"Coeficientes de Bézout: {d_orig} × {x0} + {n_orig} × {y0} = {mcd}")
    
    return mcd, x0, y0


def main():
    """Función principal que solicita entrada del usuario y calcula el MCD"""
    print("=== Calculadora del Máximo Común Divisor ===")
    print("Algoritmo de Euclides\n")
    
    try:
        # Solicitar entrada del usuario
        d = int(input("Introduce el primer entero (d): "))
        n = int(input("Introduce el segundo entero (n): "))
        
        if d == 0 and n == 0:
            print("Error: Ambos números no pueden ser 0")
            return
        
        # Calcular MCD usando algoritmo básico
        print("\n" + "="*50)
        mcd = mcd_euclides(d, n)
        print(f"\nEl MCD({d}, {n}) = {mcd}")
        
        # Calcular MCD extendido
        print("\n" + "="*50)
        mcd_ext, x, y = mcd_euclides_extendido(d, n)
        
        # Verificar el resultado
        verificacion = d * x + n * y
        print(f"\nVerificación: {d} × {x} + {n} × {y} = {verificacion}")
        
        if verificacion == mcd_ext:
            print("✓ La verificación es correcta")
        else:
            print("✗ Error en el cálculo")
            
    except ValueError:
        print("Error: Por favor, introduce números enteros válidos")
    except Exception as e:
        print(f"Error inesperado: {e}")


if __name__ == "__main__":
    main()
