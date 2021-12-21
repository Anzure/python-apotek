from ..modeller.produkt import Produkt


def hent_varelager():
    varer = []
    try:
        les_fil = open("varelager.csv", "r")
        linjenummer = 0
        for x in les_fil:
            if linjenummer > 0:
                y = x.split(";")
                varenummer = int(y[0])
                navn = str(y[1])
                enhetspris = float(y[2])
                reseptbelagt = int(y[3]) == 1
                hylle = int(y[4])
                produkt = Produkt(varenummer, navn, enhetspris, reseptbelagt, hylle)
                varer.append(produkt)
            linjenummer += 1
        les_fil.close()
    except FileNotFoundError:
        print("Filen finnes ikke, sjekk filsti.")
    except IOError:
        print("Feil under lesing av fil, sjekk tilganger.")
    return varer
