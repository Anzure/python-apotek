def krev_svar(text):
    while True:
        bool_input = input(f"{text} ")
        if bool_input.upper() == "Y":
            return True
        if bool_input.upper() == "N":
            return False


def krev_tall(inndata):
    while True:
        try:
            tall_input = input(f"Skriv inn {inndata}: ")
            tall_output = int(tall_input)
            return tall_output
        except ValueError:
            print(f"Ugydlig {inndata} oppgitt, prøv på nytt!")
