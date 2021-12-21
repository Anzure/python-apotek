######################################
# Egenvalgt oppgave i Programmering  #
# Laget av André Mathisen i FDPN2    #
# Sist oppdatert 28. november 2021   #
######################################
# PIN kode er: 4567                  #
######################################
from enum import Enum
from datetime import datetime
import hashlib


class Status(Enum):
    OPPSTART = 1
    INNLOGGING = 2
    HANDLEKURV = 3
    BETALING = 4


apotek_stauts = Status.OPPSTART
apotek_pin_hash = "bb4e331a72336b0c49f49541c426768d3e4afa20"
apotek_pin_salt = "JtAUW8G8WB"
varelager = []


class Produkt:
    def __init__(self, varenummer, navn, pris, reseptbelagt, hylle):
        self.varenummer = int(varenummer)
        self.navn = str(navn)
        self.pris = float(pris)
        self.reseptbelagt = bool(reseptbelagt)
        self.hylle = int(hylle)


def sjekk_pin_kode(pin_kode):
    test_kode = f"{pin_kode}{apotek_pin_salt}"
    sha_1 = hashlib.sha1()
    for x in range(0, 999999):
        sha_1.update(test_kode.encode('utf-8'))
    pin_hash = sha_1.hexdigest()
    resultat = pin_hash == apotek_pin_hash
    return resultat


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


def krev_tall(inndata):
    while True:
        try:
            tall_input = input(f"Skriv inn {inndata}: ")
            tall_output = int(tall_input)
            return tall_output
        except ValueError:
            print(f"Ugydlig {inndata} oppgitt, prøv på nytt!")


def krev_svar(text):
    while True:
        bool_input = input(f"{text} ")
        if bool_input.upper() == "Y":
            return True
        if bool_input.upper() == "N":
            return False


def krev_innlogging():
    print("Ny økt krever innlogging.")
    pin_test = 3
    while pin_test > 0:
        pin_kode = krev_tall("PIN-kode")
        if sjekk_pin_kode(pin_kode):
            print("Takk for din innlogging, ha en fin dag på jobb!")
            return True
        else:
            pin_test -= 1
            print(f"Feil PIN-kode oppgitt, du har {pin_test} forsøk igjen!")
    return False


def skriv_ut_kvittering(handlekurv, total_mva, total_pris):
    timestamp = datetime.now().strftime("%d.%m.%y %H:%M:%S")
    skriv_fil = open("kvittering.txt", mode='w')
    skriv_fil.write("|--------------------------------------------------------------------|")
    skriv_fil.write("\n|---------------------------- KVITTERING ----------------------------|")
    skriv_fil.write("\n|--------------------------------------------------------------------|")
    skriv_fil.write("%-30s" % f"\n| Produkt")
    skriv_fil.write("%-14s" % f"Enhetspris")
    skriv_fil.write("%-12s" % f"Antall")
    skriv_fil.write("%-14s" % f"Pris")
    skriv_fil.write("|")
    for x in handlekurv:
        produkt = x[0]
        antall = x[1]
        pris = x[2]
        skriv_fil.write("%-30s" % f"\n| {produkt.navn}")
        skriv_fil.write("%-14s" % f"{format(produkt.pris, '.2f')} kr")
        skriv_fil.write("%-12s" % f"{antall}")
        skriv_fil.write("%-14s" % f"{format(pris, '.2f')} kr")
        skriv_fil.write("|")
    skriv_fil.write("\n|--------------------------------------------------------------------|")
    skriv_fil.write("%-70s" % f"\n| Tidspunkt: {timestamp}")
    skriv_fil.write("|")
    skriv_fil.write("%-70s" % f"\n| MVA beløp: {format(total_mva, '.2f')} kr")
    skriv_fil.write("|")
    skriv_fil.write("%-70s" % f"\n| Sum betalt: {format(total_pris, '.2f')} kr")
    skriv_fil.write("|")
    skriv_fil.write("\n|--------------------------------------------------------------------|")
    skriv_fil.close()


def print_varelager():
    print("%-5s" % f"ID", end="")
    print("%-30s" % f"Produkt", end="")
    print("%-10s" % f"Pris")
    for produkt in varelager:
        print("%-5s" % produkt.varenummer, end="")
        print("%-30s" % produkt.navn, end="")
        print("%-10s" % f"{format(produkt.pris, '.2f')} kr")

def print_handlekurv(handlekurv, total_mva, total_pris):
    print("%-5s" % f"ID", end="")
    print("%-28s" % f"Produkt", end="")
    print("%-14s" % f"Enhetspris", end="")
    print("%-10s" % f"Antall", end="")
    print("%-12s" % f"Pris")
    for x in handlekurv:
        produkt = x[0]
        antall = x[1]
        pris = x[2]
        print("%-5s" % produkt.varenummer, end="")
        print("%-28s" % produkt.navn, end="")
        print("%-14s" % f"{format(produkt.pris, '.2f')} kr", end="")
        print("%-10s" % antall, end="")
        print("%-12s" % f"{format(pris, '.2f')} kr")
    print(f"Beregnet MVA beløp: {format(total_mva, '.2f')} kr")
    print(f"Beregnet beløp å betale: {format(total_pris, '.2f')} kr")


def krev_handlekurv():
    handlekurv = []
    total_mva = 0
    total_pris = 0
    while apotek_stauts == Status.HANDLEKURV:
        varenummer = krev_tall("varenummer")
        produkt = varelager[varenummer]
        print(f"{produkt.navn}")
        print(f"- Reseptbelagt: {produkt.reseptbelagt}")
        print(f"- Pris: {format(produkt.pris, '.2f')} kr")
        print(f"- Hylle: {produkt.hylle}")

        if produkt.reseptbelagt:
            resept_status = krev_svar("Er resept gydlig (Y/N)?")
            if not resept_status:
                exit()

        antall = krev_tall("antall")
        pris = produkt.pris * antall
        if produkt.reseptbelagt:
            pris = 0

        total_pris += pris
        total_mva += pris * 0.25
        handlekurv.append([produkt, antall, pris])
        print_handlekurv(handlekurv, total_mva, total_pris)

        handlekurv_status = krev_svar("Skal kunden ha flere varer (Y/N)?")
        if not handlekurv_status:
            break
    handlevogn = [handlekurv, total_mva, total_pris]
    return handlevogn


# Oppstart
print("Velkommen til apoteket!")
varelager = hent_varelager()

# Innlogging
apotek_stauts = Status.INNLOGGING
innlogging = krev_innlogging()
if not innlogging:
    print("Innlogging feilet.")
    exit()

# Registrer varer
apotek_stauts = Status.HANDLEKURV
print_varelager()
handlevogn = krev_handlekurv()
handlekurv = handlevogn[0]
total_mva = handlevogn[1]
total_pris = handlevogn[2]

# Prosesser betaling
apotek_stauts = apotek_stauts.BETALING
print(f"MVA beløp: {format(total_mva, '.2f')} kr")
print(f"Total pris: {format(total_pris, '.2f')} kr")
betalt_status = krev_svar("Har kunden betalt (Y/N)?")
if not betalt_status:
    print("Betaling avbrutt.")
    exit()
skriv_ut_kvittering(handlekurv, total_mva, total_pris)
print("Handel fullført, se kvittering.")
