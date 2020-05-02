class PravidloAkcie:
    def __init__(self, pridaj, vymaz, sprava):
        self.pridaj = pridaj
        self.vymaz = vymaz
        self.sprava = sprava

osoby = [] # vsetky osoby, ktore sa budu nachadzat vo faktoch pridam do tohto listu
pracovnaPamat = []
rodinnePravidlaInstancie = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []} # zoznam instancii aplikovatelnych pravidiel na rodinne vztahy

def pridajRodicovskyFakt(line, splitnutyLine):
    rodicIndex = None
    dietaIndex = None
    rodic = splitnutyLine[0]
    dieta = splitnutyLine[3]

    for i in range(len(osoby)):
        if (osoby[i] == rodic):
            rodicIndex = i
        elif (osoby[i] == dieta):
            dietaIndex = i

    if (rodicIndex != None): # zaznam o rodicovi je v liste pre osoby
        osoby.append(dieta)
    elif (dietaIndex != None): # zaznam o dietati je v liste pre osoby
        osoby.append(rodic)
    else: # zaznam o dietati a ani o rodicovin nie je v liste
        osoby.append(rodic)
        osoby.append(dieta)

    pracovnaPamat.append(line)


def pridajPohlavieMuzFakt(line, splitnutyLine):
    muz = splitnutyLine[1]

    for i in range(len(osoby)):
        if (osoby[i] == muz):
            pracovnaPamat.append(line)
            return

    osoby.append(muz)
    pracovnaPamat.append(line)


def pridajPohlavieZenaFakt(line, splitnutyLine):
    zena = splitnutyLine[1]

    for i in range(len(osoby)):
        if (osoby[i] == zena):
            pracovnaPamat.append(line)
            return

    osoby.append(zena)
    pracovnaPamat.append(line)


def pridajManzeliaFakt(line, splitnutyLine):
    manzelia1Index = None
    manzelia2Index = None
    manzelia1 = splitnutyLine[1]
    manzelia2 = splitnutyLine[2]

    for i in range(len(osoby)):
        if (osoby[i] == manzelia1):
            manzelia1Index = i
        elif (osoby[i] == manzelia2):
            manzelia2Index = i

    if (manzelia1Index != None): # zaznam o rodicovi je v liste pre osoby
        osoby.append(manzelia2)
    elif (manzelia2Index != None): # zaznam o dietati je v liste pre osoby
        osoby.append(manzelia1)
    else: # zaznam o dietati a ani o rodicovin nie je v liste
        osoby.append(manzelia1)
        osoby.append(manzelia2)

    pracovnaPamat.append(line)


def nacitajFakty():
    file = open("fakty.txt", "r")

    for line in file:
        for word in line.split():
            if (word == "rodic"):
                pridajRodicovskyFakt(line, line.split())
            elif (word == "muz"):
                pridajPohlavieMuzFakt(line, line.split())
            elif (word == "zena"):
                pridajPohlavieZenaFakt(line, line.split())
            elif (word == "manzelia"):
                pridajManzeliaFakt(line, line.split())

    file.close()


def vyskusajAplikaciuDruhyRodic(osoba, iterovanaOsoba):
    elementarnaPodmienka = osoba + " je rodic " + iterovanaOsoba + "\n"
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka == fakt):
            for fakt2 in pracovnaPamat:
                splitnutyFakt2 = fakt2.split()
                if (splitnutyFakt2[0] == "manzelia" and splitnutyFakt2[1] == osoba):
                    rodinnePravidlaInstancie.get(1).append(PravidloAkcie(splitnutyFakt2[2] + " je rodic " + iterovanaOsoba + "\n", None, None))
                elif (splitnutyFakt2[0] == "manzelia" and splitnutyFakt2[2] == osoba):
                    rodinnePravidlaInstancie.get(2).append(PravidloAkcie(splitnutyFakt2[1] + " je rodic " + iterovanaOsoba + "\n", None, None))


def vyskusajAplikaciuOtecMatka(osoba, iterovanaOsoba):
    elementarnaPodmienka = osoba + " je rodic " + iterovanaOsoba + "\n"
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka == fakt):
            for fakt2 in pracovnaPamat:
                splitnutyFakt2 = fakt2.split()
                if (splitnutyFakt2[0] == "muz" and splitnutyFakt2[1] == osoba):
                    rodinnePravidlaInstancie.get(3).append(PravidloAkcie(osoba + " je otec " + iterovanaOsoba + "\n", None, None))
                elif (splitnutyFakt2[0] == "zena" and splitnutyFakt2[1] == osoba):
                    rodinnePravidlaInstancie.get(4).append(PravidloAkcie(osoba + " je matka " + iterovanaOsoba + "\n", None, None))


def vyskusajAplikaciuSurodenci(osoba, iterovanaOsoba):
    elementarnaPodmienka1 = osoba + " je rodic " + iterovanaOsoba + "\n"
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka1 == fakt):
            for i in range(len(osoby)):
                elementarnaPodmienka2 = osoba + " je rodic " + osoby[i] + "\n"
                for fakt2 in pracovnaPamat:
                    if (elementarnaPodmienka2 == fakt2 and osoby[i] != iterovanaOsoba):
                        rodinnePravidlaInstancie.get(5).append(PravidloAkcie(iterovanaOsoba + " a " + osoby[i] + " su surodenci\n", None, None))


def vyskusajAplikaciuBrat(osoba, iterovanaOsoba):
    elementarnaPodmienka = osoba + " a " + iterovanaOsoba + " su surodenci\n"
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka == fakt):
            for fakt2 in pracovnaPamat:
                splitnutyFakt2 = fakt2.split()
                if (splitnutyFakt2[0] == "muz" and splitnutyFakt2[1] == osoba):
                    rodinnePravidlaInstancie.get(6).append(PravidloAkcie(osoba + " je brat " + iterovanaOsoba + "\n", None, None))


def vyskusajAplikaciuStryko(osoba, iterovanaOsoba):
    elementarnaPodmienka1 = osoba + " je brat " + iterovanaOsoba + "\n"
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka1 == fakt):
            for i in range(len(osoby)):
                elementarnaPodmienka2 = iterovanaOsoba + " je rodic " + osoby[i] + "\n"
                for fakt2 in pracovnaPamat:
                    if (elementarnaPodmienka2 == fakt2):
                        rodinnePravidlaInstancie.get(7).append(PravidloAkcie(osoba + " je stryko " + osoby[i] + "\n", None, osoby[i] + " ma stryka"))


def vyskusajAplikaciuTestMazania(osoba, iterovanaOsoba):
    elementarnaPodmienka = osoba + " je stryko " + iterovanaOsoba + "\n"
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka == fakt):
            for fakt2 in pracovnaPamat:
                splitnutyFakt2 = fakt2.split()
                if (splitnutyFakt2[0] == "zena" and splitnutyFakt2[1] == iterovanaOsoba):
                    rodinnePravidlaInstancie.get(8).append(PravidloAkcie(None, "zena " + iterovanaOsoba + "\n", None))


def vytvorZoznamAplikovatelnychInstanciiPravidiel(osoba):
    for i in range(len(osoby)):
        vyskusajAplikaciuDruhyRodic(osoba, osoby[i]) # pravidlo DruhyRodic1 a pravidlo DruhyRodic2
        vyskusajAplikaciuOtecMatka(osoba, osoby[i]) # pravidlo Otec a pravidlo Matka
        vyskusajAplikaciuSurodenci(osoba, osoby[i]) # Pravidlo Surodenci
        vyskusajAplikaciuBrat(osoba, osoby[i]) # Pravidlo Brat
        vyskusajAplikaciuStryko(osoba, osoby[i]) # Pravidlo Stryko
        vyskusajAplikaciuTestMazania(osoba, osoby[i]) # Pravidlo Test Mazania


def vyfilTrujPravidla():
    for i in range(1, 9): # je 8 pravidiel, v dictionary su ocislovane od 1 po 8, preto ich vsetky prejdem v tomto cykle
        for pravidloAkcie in reversed(rodinnePravidlaInstancie.get(i)):
            vymazCelePravidlo = False
            if (pravidloAkcie.pridaj != None):
                for fakt in pracovnaPamat:  # v tomto cykle zistujem, ci akcia pravidla ovplyvni pracovnu pamat
                    if (pravidloAkcie.pridaj == fakt): # fakt sa v pamati nachadza, takze ho nebudem pridavat -> vymazem akciu
                        pravidloAkcie.pridaj = None
                        vymazCelePravidlo = True
            else:
                vymazCelePravidlo = True
            if (pravidloAkcie.vymaz != None):
                existujeFakt = False
                for fakt in pracovnaPamat:
                    if (pravidloAkcie.vymaz == fakt): # fakt sa v pracovnej pamati nachcadza, takze ho pravidlo moze vymazat
                        existujeFakt = True
                if (existujeFakt == False): # zistil som, ze sa fakt nenachazda v pracovnej pamati, takze ho pravidlo nemoze vymazat, tym padom vymazem akciu
                    pravidloAkcie.vymaz = None
                    if (vymazCelePravidlo):
                        rodinnePravidlaInstancie.get(i).remove(pravidloAkcie)
            elif (vymazCelePravidlo):
                rodinnePravidlaInstancie.get(i).remove(pravidloAkcie)


def zapisPravidloDoPracovnejPamati():
    global vykonane

    for i in range(1, 9): # je 8 pravidiel, v dictionary su ocislovane od 1 po 8, preto ich vsetky prejdem v tomto cykle
        for pravidloAkcie in rodinnePravidlaInstancie.get(i):
            if (vykonane):
                break
            elif (pravidloAkcie.pridaj != None and pravidloAkcie.vymaz != None):
                pracovnaPamat.append(pravidloAkcie.pridaj)
                pracovnaPamat.remove(pravidloAkcie.vymaz)
                if (pravidloAkcie.sprava != None):
                    print(pravidloAkcie.sprava)
                vykonane = True
            elif (pravidloAkcie.pridaj != None):
                pracovnaPamat.append(pravidloAkcie.pridaj)
                if (pravidloAkcie.sprava != None):
                    print(pravidloAkcie.sprava)
                vykonane = True
            elif (pravidloAkcie.vymaz != None):
                pracovnaPamat.remove(pravidloAkcie.vymaz)
                if (pravidloAkcie.sprava != None):
                    print(pravidloAkcie.sprava)
                vykonane = True
        rodinnePravidlaInstancie.get(i).clear()


nacitajFakty()

vykonane = True
while(vykonane):
    vykonane = False
    for i in range(len(osoby)):
        vytvorZoznamAplikovatelnychInstanciiPravidiel(osoby[i])
    vyfilTrujPravidla()
    zapisPravidloDoPracovnejPamati()

file = open("fakty_vystup.txt", "w")
for fakt in pracovnaPamat:
    file.write(fakt)






