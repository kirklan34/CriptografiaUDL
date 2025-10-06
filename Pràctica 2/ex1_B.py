def euclides_extendido(d, n):
    d_orig, n_orig = d, n
    d = abs(d)
    n = abs(n)
    
    x0, x1 = 1, 0
    y0, y1 = 0, 1
    
    d_temp, n_temp = d, n
    while n_temp != 0:
        cociente = d_temp // n_temp
        resto = d_temp % n_temp
        x0, x1 = x1, x0 - cociente * x1
        y0, y1 = y1, y0 - cociente * y1
        d_temp = n_temp
        n_temp = resto
    
    mcd = d_temp
    x_final, y_final = x0, y0
    if d_orig < 0:
        x_final = -x_final
    if n_orig < 0:
        y_final = -y_final
    return mcd, x_final, y_final


def inverso_modular(d, n):
    if n <= 0:
        return None
    d = d % n
    if d == 0:
        return None
    mcd, x, y = euclides_extendido(d, n)
    if mcd != 1:
        return None
    inverso = x % n
    return inverso


def main():
    d = int(input("Introduce d: "))
    n = int(input("Introduce n: "))
    
    mcd, x, y = euclides_extendido(d, n)
    
    if mcd == 1:
        inverso = inverso_modular(d, n)
        print(f"{d} y {n} son coprimos")
        print(f"Inverso de {d} modulo {n}: {inverso}")
    else:
        print(f"{d} y {n} no son coprimos")


if __name__ == "__main__":
    main()