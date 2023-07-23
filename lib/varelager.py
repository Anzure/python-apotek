from .produkt import Produkt


def oppdater_lager(varelager, handlekurv):
    try:
        skriv_fil = open("varelager.csv", mode='w')
        skriv_fil.write("ID;Produkt;Pris;Reseptbelagt;Hylle;Antall\n")
        for produkt in varelager:
            antall = produkt.antall
            for vare in handlekurv:
                if vare[0].varenummer == produkt.varenummer:
                    antall -= vare[1]
            skriv_fil.write(f"{produkt.varenummer};")
            skriv_fil.write(f"{produkt.navn};")
            skriv_fil.write(f"{produkt.pris};")
            skriv_fil.write(f"{produkt.reseptbelagt};")
            skriv_fil.write(f"{produkt.hylle};")
            skriv_fil.write(f"{antall}\n")
        skriv_fil.close()
    except IOError:
        print("Feil under skriving til fil, sjekk tilganger.")
    except:
        print("Ukjent feil under skriving til fil, kontakt IT.")


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
                reseptbelagt = y[3].lower() == "true" or y[3] == "1" or y[3] == 1
                hylle = int(y[4])
                antall = int(y[5])
                produkt = Produkt(varenummer, navn, enhetspris, reseptbelagt, hylle, antall)
                varer.append(produkt)
            linjenummer += 1
        les_fil.close()
    except FileNotFoundError:
        print("Filen finnes ikke, sjekk filsti.")
    except IOError:
        print("Feil under lesing fra fil, sjekk tilganger.")
    except:
        print("Ukjent feil under lesing fra fil, kontakt IT.")
    return varer
