######################################
# Egenvalgt oppgave i Programmering  #
# Laget av André Mathisen i FDPN2    #
# Sist oppdatert 21. desember 2021   #
######################################
# Apoteksystem - hoved program       #
# PIN kode er: 4567                  #
######################################
from lib.status import Status
from lib.tastatur import krev_tall, krev_svar
from lib.autentisering import krev_innlogging
from lib.utskrift import vis_varelager, vis_handlekurv, skriv_ut_kvittering
from lib.varelager import hent_varelager
from lib.regnskap import lagre_til_regnskap
from datetime import datetime

apotek_stauts = Status.OPPSTART
apotek_pin_hash = "bb4e331a72336b0c49f49541c426768d3e4afa20"
apotek_pin_salt = "JtAUW8G8WB"
varelager = []


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
        vis_handlekurv(handlekurv, total_mva, total_pris)

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
innlogging = krev_innlogging(apotek_pin_hash, apotek_pin_salt)
if not innlogging:
    print("Innlogging feilet.")
    exit()

# Registrer varer
apotek_stauts = Status.HANDLEKURV
vis_varelager(varelager)
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
tid = datetime.now().strftime("%d.%m.%y %H:%M:%S")
skriv_ut_kvittering(tid, handlekurv, total_mva, total_pris)
lagre_til_regnskap(tid, total_mva, total_pris)
print("Handel fullført, se kvittering.")
