import json
from pathlib import Path


def encode(vhod: list) -> tuple[list, list]:
    """
    Izvede kodiranje vhodnega sporocila z algoritmom BPE.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih znakov ASCII.

    Returns
    -------
    (izhod, izhodS) : tuple[list, list]
        izhod : list
            Kodirano vhodno sporocilo v obliki indeksov.
        izhodS : list
            Seznam ASCII kod in parov indeksov.
    """
    seznamSIdx=255
    seznamS = []
    for i in range(256):
        seznamS.append(i)
    # print(seznamS)


    # print(vhod)
    for i, znak in enumerate(vhod):
        vhod[i] = ord(vhod[i])
    # print(vhod)

    while(True):

        # print(vhod)

        # to bo slovar za pare v obliki z generiki : <Par, integer>
        slovar = {}

        for i in range(0, len(vhod) - 1):
            curr = (vhod[i], vhod[i + 1])
            # print("Par {}".format(curr))
            # print(curr)
            slovar[curr] = slovar.get(curr, 0) + 1

        
        # for k, v in slovar.items():
        #     print(f"Par {k} se pojavi {v}")

        maks=0
        maksId=0
        for k, v in slovar.items():
            if(v > maks):
                maks = v
                maksId = k
        
        if(slovar[maksId] < 2 or seznamSIdx >= 4096):
            break

        # print("Maks par: {} => {}".format(maksId, slovar[maksId]))
        seznamS.append(maksId)
        seznamSIdx += 1

        novVhod = []
        i = 0
        while i < len(vhod):
            if i < len(vhod) - 1 and (vhod[i], vhod[i+1]) == maksId:
                novVhod.append(seznamSIdx)
                i += 2 
            else:
                novVhod.append(vhod[i])
                i += 1 
        vhod = novVhod
   
    # print(vhod)
    # print(seznamS)

    return (vhod, seznamS)


def decode(vhod: list, S: list) -> list:
    """
    Izvede dekodiranje vhodnega zaporedja indeksov z algoritmom BPE.

    Parameters
    ----------
    vhod : list
        Seznam vhodnih indeksov.
    S : list
        Seznam ASCII kod in parov indeksov.

    Returns
    -------
    izhod : list
        Dekodirano vhodno sporocilo v obliki ASCII znakov.

    """

    i = len(S) - 1
    while(i > 255):
        # print(S[i])
        novVhod = []
        for el in vhod:
            if(el == i):
                novVhod.append(S[i][0])
                novVhod.append(S[i][1])
            else:
                novVhod.append(el)
        i -=1
        vhod = novVhod

    niz = []
    i = 0
    for el in vhod:
        niz.append(chr(el))
        i += 1

    return niz 


def compute_compression_ratio(vhod: list, izhod: list ) -> float:
    """
    Izracuna kompresijsko razmerje.

    Parameters
    ----------
    vhod : list
        Vhodno zaporedje.
    izhod : list
        Izhodno zaporedje.
    

    Returns
    -------
    R : float
        Kompresijsko razmerje.
    """

    R = (len(vhod) * 8) / (len(izhod) * 12)
    return R


def read_raw_text(path: str) -> list:
    """
    Prebere besedilno datoteko in vrne seznam znakov.

    Parameters
    ----------
    path : str
        Pot do vhodne datoteke .txt.

    Returns
    -------
    list
        Seznam znakov iz datoteke.
    """
    return list(Path(path).read_text(encoding="ascii"))


def write_raw_text(path: str, znaki: list) -> None:
    """
    Zapise seznam znakov v besedilno datoteko.

    Parameters
    ----------
    path : str
        Pot do izhodne datoteke .txt.
    znaki : list
        Seznam znakov za zapis.
    """
    Path(path).write_text("".join(znaki), encoding="ascii")


def read_coded_msg(path: str) -> tuple[list, list]:
    """
    Prebere JSON datoteko z izhodoma funkcije encode.

    Parameters
    ----------
    path : str
        Pot do vhodne datoteke .json.

    Returns
    -------
    tuple[list, list]
        Par seznamov (izhod, izhodS).
    """
    data = json.loads(Path(path).read_text(encoding="ascii"))
    return data["izhod"], data["izhodS"]

# odstrani f: float !!!! pred oddajo !!!!, če ne bo drugače
def write_coded_msg(path: str, izhod: list, izhodS: list) -> None:
    """
    Zapise izhoda funkcije encode v JSON datoteko.

    Parameters
    ----------
    path : str
        Pot do izhodne datoteke .json.
    izhod : list
        Kodirano sporocilo.
    izhodS : list
        Seznam ASCII kod in parov indeksov.
    """
    data = {
        "izhod": izhod,
        "izhodS": izhodS,
        # "R": r
    }
    Path(path).write_text(
        json.dumps(data, ensure_ascii=False, indent=4),
        encoding="ascii",
    )


# zakomentiraj te klice funkcij pred oddajo !!!

# encode(read_raw_text("primeri/1.txt"))
# vhod, vhodS = encode(read_raw_text("primeri/6.txt"))
# niz = decode(vhod, vhodS)
# write_raw_text("primeri/6Decode.txt", niz)
# R = compute_compression_ratio(niz, vhod)
# write_coded_msg("primeri/test06.json", vhod, vhodS, R)


#### test max testiranje ####

# vhod, vhodS = encode(read_raw_text("testMax.txt"))
# print(vhod)
# print(vhodS)
# niz = decode(vhod, vhodS)
# R = compute_compression_ratio(niz, vhod)
# write_coded_msg("testMax.json", vhod, vhodS)
# print(R)
# write_raw_text("testMaxOut.txt", niz)