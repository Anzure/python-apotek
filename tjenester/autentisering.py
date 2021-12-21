import hashlib
from .tastatur import krev_tall


def krev_innlogging(pin_hash, pin_salt):
    print("Ny økt krever innlogging.")
    pin_test = 3
    while pin_test > 0:
        pin_kode = krev_tall("PIN-kode")
        if sjekk_pin_kode(pin_kode, pin_hash, pin_salt):
            print("Takk for din innlogging, ha en fin dag på jobb!")
            return True
        else:
            pin_test -= 1
            print(f"Feil PIN-kode oppgitt, du har {pin_test} forsøk igjen!")
    return False


def sjekk_pin_kode(pin_kode, apotek_pin_hash, apotek_pin_salt):
    test_kode = f"{pin_kode}{apotek_pin_salt}"
    sha_1 = hashlib.sha1()
    for x in range(0, 999999):
        sha_1.update(test_kode.encode('utf-8'))
    pin_hash = sha_1.hexdigest()
    resultat = pin_hash == apotek_pin_hash
    return resultat
