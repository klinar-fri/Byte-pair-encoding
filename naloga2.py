"""
Naloga 2 - Ocena kanala in izracun kapacitete.

V tej datoteki so podani prototipi funkcij, ki jih morate implementirati.
Funkcije naj uporabljajo samo standardno knjiznico Python, modul math in numpy.
"""

import numpy as np
import math

def getProbability(y : int, x: int, X : list[int], Y : list[int], n: int, m: int) -> float:
    stXov = 0
    stYov = 0

    for i in range(len(X)):
        if(X[i] < 0 or X[i] >= m):
            raise ValueError
        if(X[i] == x):
            stXov += 1
            if(Y[i] < 0 or Y[i] >= n):
                raise ValueError
            if(Y[i] == y):
                stYov +=1

    if(stXov == 0.0):
        return 0.0

    return (stYov / stXov)

    
def estimate_channel(x: list[int], y: list[int], m: int, n: int) -> np.ndarray:
    """
    Oceni diskretni kanal iz opazovanih vhodnih in izhodnih simbolov.

    Parametri
    ----------
    x : list[int]
        Dovoljeni vhodni simboli so stevila od 0 do m-1.
    y : list[int]
        Dovoljeni izhodni simboli so stevila od 0 do n-1.
    m : int
        Stevilo moznih vhodnih simbolov.
    n : int
        Stevilo moznih izhodnih simbolov.

    Vrne
    -------
    W : np.ndarray
        Dvodimenzionalna matrika velikosti n x m z elementi W[y, x] = P(Y=y | X=x).

    Sprozi
    ------
    ValueError
        Ce sta x in y razlicnih dolzin ali se kaksen simbol pojavi zunaj dovoljenega obsega.
    """
    # Tukaj napisite svojo kodo.

    w = np.zeros((n, m))

    if(len(x) != len(y)):
        raise ValueError

    for j in range(n):
        for i in range(m):
            w[j][i] = getProbability(j, i, x, y, n, m)

    return w


def blahut_arimoto(W: np.ndarray, tol: float = 1e-9, max_iter: int = 1000,) -> np.ndarray:
    """
    Izracuna vhodno porazdelitev in kapaciteto kanala z algoritmom Blahut-Arimoto.

    Parametri
    ----------
    W : np.ndarray
        Dvodimenzionalna matrika velikosti n x m z elementi W[y, x] = P(Y=y | X=x).
    tol : float
        Toleranca za preverjanje konvergence.
    max_iter : int
        Najvecje stevilo iteracij.

    Vrne
    -------
    p_star : np.ndarray
        Priblizek optimalne vhodne porazdelitve dolzine m

    Sprozi
    ------
    ValueError
        Ce ima W kaksen stolpec ni veljavna porazdelitev.
    """
    # Tukaj napisite svojo kodo.
    velikost = W.shape
    p = np.zeros(velikost[1])
    for i in range(velikost[1]):
        p[i] = (1 / velikost[1])

    # print(p)

    #preverimo veljavnost W
    for stolpec in range(velikost[1]):
        sum = 0
        for vrstica in range(velikost[0]):
            if(W[vrstica][stolpec] < 0):
                raise ValueError
            sum += W[vrstica][stolpec]
        if(sum != 1):
            raise ValueError

    newMat = W
    i = 0
    while(i < max_iter):
        q = np.matmul(W, p)

        c = np.zeros(velikost[1])

        for k in range(velikost[1]):
            tmpC = 0
            for l in range(velikost[0]):
                if(W[l][k] > 0):
                    if(q[l] != 0):
                        tmpC += W[l][k] * math.log(W[l][k] / q[l])
            c[k] = tmpC

        # print("C:", c)
        # print("Stari p:", p)

        noviP = np.zeros(velikost[1])
        vsotaElementov = 0
        for k in range(velikost[1]):
            noviP[k] = p[k] * math.exp(c[k])
            vsotaElementov += noviP[k]

        # print("Novi p:", noviP)
        # normaliziramo -> delimo z vsoto elementov, lahko tud samo p / vsotaElementov, nekako deluje
        for k in range(velikost[1]):
            noviP[k] = noviP[k] / vsotaElementov

        # print("Normaliziran p:", noviP)

        maxDiff = 0.0
        for k in range(velikost[1]):
            currDif = abs(p[k] - noviP[k])
            if(currDif > maxDiff):
                maxDiff = currDif
        
        if(maxDiff < tol):
            break
        i += 1

        p = noviP

    # print(i)
    # print(p)

    return p


def compute_capacity(W: np.ndarray, p: np.ndarray) -> float:
    """
    Izracuna I(X;Y) za dan kanal W in vhodno porazdelitev p.

    Parametri
    ----------
    W : np.ndarray
        Dvodimenzionalna matrika velikosti n x m z elementi W[y, x] = P(Y=y | X=x).
    p : np.ndarray
        Enodimenzionalna vhodna porazdelitev dolzine m, kjer je p[x] = P(X=x).

    Vrne
    -------
    C_bits : float
        Vrednost I(X;Y) v bitih.
    """
    # Tukaj napisite svojo kodo.

    velikost = W.shape
    q = np.matmul(W, p)
    c = np.zeros(velikost[1])

    # print(q)
    for x in range(velikost[1]):
        tmpC = 0
        for y in range(velikost[0]):
            if(W[y][x] > 0):
                if(q[y] != 0):
                    tmpC += W[y][x] * math.log(W[y][x] / q[y])
        c[x] = tmpC

    # print(c)
    capaciteta = 0
    for x in range(velikost[1]):
        capaciteta += p[x] * c[x]


    return (capaciteta / math.log(2))


def estimate_capacity(
    x: list[int],
    y: list[int],
    m: int,
    n: int,
    tol: float = 1e-9,
    max_iter: int = 1000,
) -> float:
    """
    Oceni kanal iz podatkov in vrne njegovo kapaciteto.

    Parametri
    ----------
    x : list[int]
        Vhodni simboli so stevila od 0 do m-1.
    y : list[int]
        Izhodni simboli so stevila od 0 do n-1.
    m : int
        Stevilo moznih vhodnih simbolov.
    n : int
        Stevilo moznih izhodnih simbolov.
    tol : float
        Toleranca za algoritem Blahut-Arimoto.
    max_iter : int
        Najvecje stevilo iteracij algoritma Blahut-Arimoto.

    Vrne
    -------
    C_bits : float
        Ocenjena kapaciteta kanala v bitih.
    """
    # Tukaj napisite svojo kodo.
    w = estimate_channel(x, y, m, n)
    p = blahut_arimoto(w)
    capaciteta = compute_capacity(w, p)
    return capaciteta


def make_bsc_dataset(
    n: int,
    p: float,
    seed: int | None = None,
) -> tuple[list[int], list[int]]:
    """
    Ustvari nakljucne podatke za binarni simetricni kanal.

    Generira n vhodnih simbolov enakomerno iz {0, 1}. Vsak simbol se z
    verjetnostjo p obrne. Z izbiro seed dobite ponovljive podatke.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, size=n).tolist()
    flip = rng.random(n) < p
    y = [xi ^ int(f) for xi, f in zip(x, flip)]
    return x, y


def make_bec_dataset(
    n: int,
    epsilon: float,
    seed: int | None = None,
) -> tuple[list[int], list[int]]:
    """
    Ustvari nakljucne podatke za binarni kanal z brisanjem (BEC).

    Generira n vhodnih simbolov enakomerno iz {0, 1}. Vsak simbol se z
    verjetnostjo epsilon izbrise (izhodni simbol 2). Z izbiro seed dobite
    ponovljive podatke.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, size=n).tolist()
    erased = rng.random(n) < epsilon
    y = [2 if e else xi for xi, e in zip(x, erased)]
    return x, y


def make_zchannel_dataset(
    n: int,
    p: float,
    seed: int | None = None,
) -> tuple[list[int], list[int]]:
    """
    Ustvari nakljucne podatke za binarni Z-kanal.

    Generira n vhodnih simbolov enakomerno iz {0, 1}. Vhod 0 se vedno prenese
    kot 0. Vhod 1 se z verjetnostjo p prenese kot 0, sicer kot 1. Z izbiro
    seed dobite ponovljive podatke.
    """
    rng = np.random.default_rng(seed)
    x = rng.integers(0, 2, size=n).tolist()
    flip = rng.random(n) < p
    y = [0 if xi == 0 else (0 if f else 1) for xi, f in zip(x, flip)]
    return x, y


# vhod = make_bsc_dataset(200, 0.20, 10)

# vhod = make_bec_dataset(2000, 0.20, 10)

# vhod = make_zchannel_dataset(200, 0.123, 10)

# print(estimate_channel(vhod[0], vhod[1], 2, 2))
# w = estimate_channel(vhod[0], vhod[1], 2, 2)
# p = blahut_arimoto(w)
# capaciteta = compute_capacity(w, p)
# print(estimate_capacity(vhod[0], vhod[1], 2, 2))

# za bec
# print(estimate_capacity(vhod[0], vhod[1], 2, 2))
