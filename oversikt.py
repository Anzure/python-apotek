from scipy import stats
import matplotlib.pyplot as plt
import os.path
from datetime import datetime

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


regnskap = hent_regnskap()
label = []
data = []
for rad in regnskap:
    salg = float(rad[3])
    tid = datetime.strptime(rad[1], "%d.%m.%y %H:%M:%S")
    ukenummer = int(tid.isocalendar()[1])
    match = False
    for i in range(0, len(label)):
        y = label[i]
        if y == ukenummer:
            data[i] = data[i] + salg
            match = True
    if not match:
        label.append(ukenummer)
        data.append(salg)
print(label)
print(data)

plt.plot(label, data)
plt.xlabel('x - Dager')
plt.ylabel('y - Salg')
plt.title('Salg pr dag')
plt.show()
