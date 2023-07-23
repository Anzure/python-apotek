import os.path


def hent_regnskap():
    regnskap = []
    try:
        les_fil = open("regnskap.csv", "r")
        linjenummer = 0
        for linje in les_fil:
            rad = linje.split(";")
            if linjenummer > 0:
                regnskap.append(rad)
            linjenummer += 1
        les_fil.close()
    except FileNotFoundError:
        print("Regnskapsfil finnes ikke. Ny fil opprettes.")
    except IOError:
        print("Feil under lesing fra fil, sjekk tilganger.")
    except:
        print("Ukjent feil under lesing fra fil, kontakt IT.")
    return regnskap


def lagre_til_regnskap(tid, betalt_mva, salgssum):
    # Finn neste ID ved å lese fil
    id = 0
    regnskap = hent_regnskap()
    for rad in regnskap:
        id = int(rad[0]) + 1
    # Lagre salg til regnskapsfil
    try:
        ny_fil = not os.path.isfile("regnskap.csv")
        skriv_fil = open("regnskap.csv", mode='a')
        if ny_fil:
            skriv_fil.write("ID;Tidspunkt;Betalt MVA;Salgssum\n")
        skriv_fil.write(f"{id};{tid};{betalt_mva};{salgssum}\n")
        skriv_fil.close()
    except IOError:
        print("Feil under skriving til fil, sjekk tilganger.")
    except:
        print("Ukjent feil under skriving til fil, kontakt IT.")

# if len(hent_regnskap()) == 0:
#    for month in range(1, 13):
#        for tilfeldig in range(1, 20):
#            date = datetime.date(2021, month, randint(1, 28))
#            time = datetime.time(randint(10, 16), randint(0, 59), 0, 0)
#            tid = datetime.datetime.combine(date, time)
#            tid = tid.strftime("%d.%m.%y %H:%M:%S")
#            pris = float(randint(50, 2000))
#            mva = pris * 0.25
#            lagre_til_regnskap(tid, mva, pris)
