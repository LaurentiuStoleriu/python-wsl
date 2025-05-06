

fisier = open("pete_solare.txt", "r")

for linie in fisier.readlines():
    continut = linie.split('\t')
    idx = int(continut[0])
    nr = float(continut[1])
    print(f"În luna a {idx}-a de la începutul măsurătorilor s-au observat în medie {nr} pete")

fisier.close()