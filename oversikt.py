######################################
# Egenvalgt oppgave i Programmering  #
# Laget av André Mathisen i FDPN2    #
# Sist oppdatert 21. desember 2021   #
######################################
# Apoteksystem - ekstra program      #
######################################
import matplotlib.pyplot as plt
import datetime
from lib.regnskap import hent_regnskap

regnskap = hent_regnskap()
label_set = []
data_set = []
for rad in regnskap:
    salg = float(rad[3])
    tid = datetime.datetime.strptime(rad[1], "%d.%m.%y %H:%M:%S")
    label = tid.strftime("%b.%y")
    match = False
    for i in range(0, len(label_set)):
        y = label_set[i]
        if y == label:
            data_set[i] = data_set[i] + salg
            match = True
    if not match:
        label_set.append(label)
        data_set.append(salg)
print(label_set)
print(data_set)

plt.figure(figsize=(10, 6))
plt.plot(label_set, data_set)
plt.ylabel('Salg i NOK')
plt.title('Salg pr måned')
plt.savefig("regnskap.png")
plt.show()
