class Osoba:
    def __init__(self, meno):
        self.meno = meno
        self.rodicia = []
        self.bratia = []
        self.sestry = []
        self.deti = []
        self.manzelia = []
        self.pohlavie = ""


osoby = []


def vytvorRodicovskyVztah(rodicIndex, dietaIndex):
    osoby[rodicIndex].deti.append(dietaIndex)
    osoby[dietaIndex].rodicia.append(rodicIndex)


def pridajRodicovskyVztah(line):
    rodicIndex = None
    dietaIndex = None
    rodic = (line[0])[1:]
    dieta = (line[3])[0: len(line[3]) - 1]

    for i in range(len(osoby)):
        if (osoby[i].meno == rodic):
            rodicIndex = i
        elif (osoby[i].meno == dieta):
            dietaIndex = i

    if (rodicIndex != None and dietaIndex != None): # zaznam o rodicovi aj o dietati je v liste pre osoby
        vytvorRodicovskyVztah(rodicIndex, dietaIndex)
    elif (rodicIndex != None): # zaznam o rodicovi je v liste pre osoby
        osoby.append(Osoba(dieta))
        vytvorRodicovskyVztah(rodicIndex, len(osoby) - 1)
    elif (dietaIndex != None): # zaznam o dietati je v liste pre osoby
        osoby.append(Osoba(rodic))
        vytvorRodicovskyVztah(len(osoby) - 1, dietaIndex)
    else: # zaznam o dietati a ani o rodicovin nie je v liste
        osoby.append(Osoba(rodic))
        osoby.append(Osoba(dieta))
        vytvorRodicovskyVztah(len(osoby) - 2, len(osoby) - 1)


def pridajPohlavieMuz(line):
    muz = (line[1])[0: len(line[1]) - 1]

    for i in range(len(osoby)):
        if (osoby[i].meno == muz):
            osoby[i].pohlavie = "muz"
            return

    novaOsoba = Osoba(muz)
    novaOsoba.pohlavie = "muz"
    osoby.append(novaOsoba)


def pridajPohlavieZena(line):
    zena = (line[1])[0: len(line[1]) - 1]

    for i in range(len(osoby)):
        if (osoby[i].meno == zena):
            osoby[i].pohlavie = "zena"
            return

    novaOsoba = Osoba(zena)
    novaOsoba.pohlavie = "zena"
    osoby.append(novaOsoba)


def vytvorManzelskyVztah(manzelia1Index, manzelia2Index):
    osoby[manzelia1Index].manzelia.append(manzelia2Index)
    osoby[manzelia2Index].manzelia.append(manzelia1Index)


def pridajManzelov(line):
    manzelia1Index = None
    manzelia2Index = None
    manzelia1 = line[1]
    manzelia2 = (line[2])[0: len(line[2]) - 1]

    for i in range(len(osoby)):
        if (osoby[i].meno == manzelia1):
            manzelia1Index = i
        elif (osoby[i].meno == manzelia2):
            manzelia2Index = i

    if (manzelia1Index != None and manzelia2Index != None): # zaznam o rodicovi aj o dietati je v liste pre osoby
        vytvorManzelskyVztah(manzelia1Index, manzelia2Index)
    elif (manzelia1Index != None): # zaznam o rodicovi je v liste pre osoby
        osoby.append(Osoba(manzelia2))
        vytvorManzelskyVztah(manzelia1Index, len(osoby) - 1)
    elif (manzelia2Index != None): # zaznam o dietati je v liste pre osoby
        osoby.append(Osoba(manzelia1))
        vytvorManzelskyVztah(len(osoby) - 1, manzelia2Index)
    else: # zaznam o dietati a ani o rodicovin nie je v liste
        osoby.append(Osoba(manzelia1))
        osoby.append(Osoba(manzelia2))
        vytvorManzelskyVztah(len(osoby) - 2, len(osoby) - 1)


def nacitajFakty():
    file = open("fakty.txt", "r")

    for line in file:
        print(line)
        for word in line.split():
            if (word == "rodic"):
                pridajRodicovskyVztah(line.split())
            elif (word == "(muz"):
                pridajPohlavieMuz(line.split())
            elif (word == "(zena"):
                pridajPohlavieZena(line.split())
            elif (word == "(manzelia"):
                pridajManzelov(line.split())


nacitajFakty()

for i in range(len(osoby)):
    print(osoby[i].meno)
    print(osoby[i].rodicia)
    print(osoby[i].bratia)
    print(osoby[i].sestry)
    print(osoby[i].deti)
    print(osoby[i].manzelia)
    print(osoby[i].pohlavie)




