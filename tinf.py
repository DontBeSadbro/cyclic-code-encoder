import sys
import re


def check_d(d, k):
    """Pomocna funkcija koja provjerava ispravnost unosa d"""
    if re.compile(r'[^01]').search(d):
        raise BaseException("Nedozovoljeni znakovi u d")
    if len(d) != k:
        raise BaseException("Duljina d mora odgovarati k")


def xor_row(base, row):
    """Pomocna funkcija koja radi xor 2 reda matrice"""
    xored = []
    for i in range(len(row)):
        if base[i] == row[i]:
            xored.append(0)
        else:
            xored.append(1)
    return xored


def g_pol(matrix):
    """Funkcija za generiranje matrice polinoma"""
    g = []

    """Inicijaliziraj matricu"""
    for i in range(matrix.count("R")):
        g.append(0)

    """Stavi 1 radi x^0"""
    g.append(1)

    pol = 0

    """1 na potenciju prije zbrajala"""
    for i in range(len(matrix)):
        if matrix[i] == "Z":
            g[pol] = 1
        else:
            pol += 1

    """Okreni matricu kako bi se dobile potencije sa vise na manje"""
    g.reverse()

    return g


def calculate_r_k(n, matrix):
    """Funkcija za izracun r i k"""
    r = matrix.count("R")
    k = n - r
    return r, k


def g_matrix(n, k, r, g):
    """Funkcija za stvaranje generirajuce matrice"""
    g_extended = g.copy()

    """Prosirivanje originalne matrice"""
    for i in range(n):
        if i >= len(g):
            g_extended.append(0)

    """Napravi generirajucu matricu u ne-standardnom obliku"""
    g_mat = []
    for i in range(k):
        g_mat.append(g_extended.copy())
        g_extended.insert(0, g_extended.pop())

    """Pretvori generirajucu matricu u standardni oblik"""
    for i in range(len(g_mat)):
        ones = 0
        for j in range(len(g_mat[i]) - r):
            if g_mat[-(i + 1)][j] == 1:
                ones += 1
            if ones > 1 and g_mat[-(i + 1)][j] == 1:
                g_mat[-(i + 1)] = xor_row(g_mat[j], g_mat[-(i + 1)]).copy()
    return g_mat


def encode(d, g, n, k):
    """Funkcija za kodiranje slijeda bitova"""
    d_added = []
    for element in list(d):
        d_added.append(int(element))
    c = d_added.copy()

    """Mnozenje d sa potencijom od n-k"""
    for i in range(n - k):
        d_added.append(0)

    """Dijeljenje polinoma kako bi dobili crc"""
    while len(g) <= len(d_added) and d_added:
        if d_added[0] == 1:
            for i in range(len(g)):
                if d_added[i] == g[i]:
                    d_added[i] = 0
                else:
                    d_added[i] = 1
        d_added.pop(0)

    """Dodaj CRC na d te vrati kodnu rijec"""
    c.extend(d_added)
    return c


def main():
    arg_len = len(sys.argv) - 1
    d = None

    """Rucni unos parametara|parametri preko poziva programa|krivi broj parametara"""
    if arg_len == 0:
        print("Unesite shemu kodera (npr. ZRRZRZRR) te n:")
        unos = input()
        unos = unos.split()
        if len(unos) != 2:
            raise BaseException("Krivo uneseni parametri")
        matrix = unos[0]
        n = unos[1]
    elif arg_len == 3:
        matrix = sys.argv[1]
        n = sys.argv[2]
        d = sys.argv[3]
    elif arg_len == 2:
        matrix = sys.argv[1]
        n = sys.argv[2]
    else:
        raise BaseException("Krivi broj parametara")

    """Provjera ispravnosti parametara"""
    if re.compile(r'[^RZ]').search(matrix) or re.compile(r'[^0-9]').search(n):
        raise BaseException("Nedozovoljeni znakovi")
    n = int(n)
    r, k = calculate_r_k(n, matrix)
    if n == 0 or r == 0 or k <= 0:
        raise BaseException("Krivo unesena matrica i/ili n")

    print("Shema kodera: {}".format(matrix))
    print()

    print("n: {}".format(n))
    print("k: {}".format(k))
    print()
    g = g_pol(matrix)
    print("Polinom: {}".format(g))
    print()

    generator_matrix = g_matrix(n, k, r, g)
    print("Generirajuca matrica u standardnom obliku:")
    for row in generator_matrix:
        print(row)
    print()

    """Petlja unosa d ukoliko nije stavljen kao parametar programa"""
    if not d:
        question = "y"
        while question == "y":
            print("Zelite li kodirati slijed bitova d? y(Da), n(Ne)")
            question = input().lower()
            if question == "y":
                pass
            elif question == "n":
                sys.exit(0)
            else:
                question = "y"
                continue
            print("Unesite slijed bitova d: ")
            d = input()
            print()
            check_d(d, k)
            c = encode(d, g, n, k)
            print("Kodna rijec c je: {}".format(c))
            print()
    check_d(d, k)
    c = encode(d, g, n, k)
    print("Kodna rijec c je: {}".format(c))


main()
