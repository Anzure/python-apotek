class Produkt:
    def __init__(self, varenummer, navn, pris, reseptbelagt, hylle, antall):
        self.varenummer = int(varenummer)
        self.navn = str(navn)
        self.pris = float(pris)
        self.reseptbelagt = bool(reseptbelagt)
        self.hylle = int(hylle)
        self.antall = int(antall)
