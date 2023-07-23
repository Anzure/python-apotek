def skriv_ut_kvittering(tid, handlekurv, total_mva, total_pris):
    try:
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
        skriv_fil.write("%-70s" % f"\n| Tidspunkt: {tid}")
        skriv_fil.write("|")
        skriv_fil.write("%-70s" % f"\n| MVA beløp: {format(total_mva, '.2f')} kr")
        skriv_fil.write("|")
        skriv_fil.write("%-70s" % f"\n| Sum betalt: {format(total_pris, '.2f')} kr")
        skriv_fil.write("|")
        skriv_fil.write("\n|--------------------------------------------------------------------|")
        skriv_fil.close()
    except IOError:
        print("Feil under skriving til fil, sjekk tilganger.")
    except:
        print("Ukjent feil under skriving til fil, kontakt IT.")


def vis_varelager(varelager):
    print("%-5s" % f"ID", end="")
    print("%-30s" % f"Produkt", end="")
    print("%-10s" % f"Pris")
    for produkt in varelager:
        print("%-5s" % produkt.varenummer, end="")
        print("%-30s" % produkt.navn, end="")
        print("%-10s" % f"{format(produkt.pris, '.2f')} kr")


def vis_handlekurv(handlekurv, total_mva, total_pris):
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
