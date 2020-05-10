import heapq
import copy

class PravidloAkcie:
    def __init__(self, pridaj, vymaz, sprava):
        self.pridaj = pridaj
        self.vymaz = vymaz
        self.sprava = sprava


class Pravidlo:
    def __init__(self, cisloPravidla,  nazov, podmienky, akcie, pridaneOsoby):
        self.cisloPravidla = cisloPravidla
        self.nazov = nazov
        self.podmienky = podmienky
        self.akcie = akcie
        self.pridaneOsoby = pridaneOsoby
    def __lt__(self, other):  # potrebna funkcia na porovnovanie v heape. ficura pythonu
        return self.cisloPravidla < other.cisloPravidla


class PridanaOsoba:
    def __init__(self, pismenko, meno):
        self.pismenko = pismenko
        self.meno = meno


osoby = [] # vsetky osoby, ktore sa budu nachadzat vo faktoch pridam do tohto listu
pracovnaPamat = [] # do tejto pamate sa na zaciatku nacitaju vsetky fakty, s ktorymi budem pracovat
instanciePravidla = []
nacitanePravidla = [] # do tohto listu nacitam vsetky pravidla, ktore si reprezentujem classou
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

    pracovnaPamat.append(line[:-1])


def pridajPohlavieMuzFakt(line, splitnutyLine):
    muz = splitnutyLine[1]

    for i in range(len(osoby)):
        if (osoby[i] == muz):
            pracovnaPamat.append(line[:-1])
            return

    osoby.append(muz)
    pracovnaPamat.append(line[:-1])


def pridajPohlavieZenaFakt(line, splitnutyLine):
    zena = splitnutyLine[1]

    for i in range(len(osoby)):
        if (osoby[i] == zena):
            pracovnaPamat.append(line[:-1])
            return

    osoby.append(zena)
    pracovnaPamat.append(line[:-1])


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

    pracovnaPamat.append(line[:-1])


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


def nacitajPravidla():
    cisloPravidla = 1
    nazovPravidla = ""
    podmienkyPravidla = ""
    akciePravidla = ""
    file = open("pravidla.txt", "r")

    pocitadloRiadkov = 1
    for line in file:
        if (pocitadloRiadkov == 1):
            nazovPravidla = line[0:len(line) - 2]
        elif (pocitadloRiadkov == 2):
            podmienkyPravidla = line[4:len(line) - 2]
        elif (pocitadloRiadkov == 3):
            akciePravidla = line[7:len(line) - 2]
        else:
            nacitanePravidla.append(Pravidlo(cisloPravidla, nazovPravidla, podmienkyPravidla.replace("(", ""), akciePravidla.replace("(", ""), []))
            cisloPravidla = cisloPravidla + 1
            pocitadloRiadkov = 0
        pocitadloRiadkov = pocitadloRiadkov + 1

    nacitanePravidla.append(Pravidlo(cisloPravidla, nazovPravidla, podmienkyPravidla.replace("(", ""), akciePravidla.replace("(", ""), []))


def uzNahradenePismeno(pismenkoOsoby, pridaneOsoby):
    for i in range(len(pridaneOsoby)):
        if (pridaneOsoby[i].pismenko == pismenkoOsoby):
            return i
    return -1


def vyskusajVsetkyOsoby(trebaVymenit, osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky):
    pomocnePridaneOsoby = copy.deepcopy(pridaneOsoby)
    for osoba in osoby:
        bolPridany = False
        starePridaneOsoby = copy.deepcopy(pridaneOsoby)
        for pridanaOsoba in pomocnePridaneOsoby:
            if (osoba == pridanaOsoba.meno):  # bol pridany, takze znamena, ze uz ho nebudem pridavat
                bolPridany = True
        if (
                bolPridany == False and osoba != osobaMeno):  # osoba, ktorej meno prechadzam v cykle este nie je v pridanych
            starePridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
            pomocnePridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
            pomocnaZlozena = copy.deepcopy(zlozenaPodmienka)
            pomocnaZlozena[cisloPodmienky] = pomocnaZlozena[cisloPodmienky].replace(trebaVymenit, osoba, 1)
            vytvorPodmienkyPravidla(osobaMeno, starePridaneOsoby, cisloPravidla, nazovPravidla, pomocnaZlozena, akcie, cisloPodmienky)


def platnaElementarnaPodmienka(elementarnaPodmienka):
    for fakt in pracovnaPamat:
        if (elementarnaPodmienka == fakt):
            return True
    return False

# !!! MOZNO BUDE TREBA ZMENIT PISMENKO X V PRAVIDLE SURODENCI NA PISMENKO Y
def vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky):
    if (cisloPodmienky == len(zlozenaPodmienka)):
        vytvorenePravidlo = Pravidlo(cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, pridaneOsoby)
        instanciePravidla.append(vytvorenePravidlo)
    else:
        if (zlozenaPodmienka[cisloPodmienky].find("?") != -1):
            trebaVymenit = "?" + zlozenaPodmienka[cisloPodmienky][zlozenaPodmienka[cisloPodmienky].find("?") + 1] # nacitam otaznik a pismenko za nim
            if (trebaVymenit[1] == "X"): # ak je pismenko X, tak budem nahradzat meno v premenej osoba
                zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, osobaMeno, 1)
                if (uzNahradenePismeno(trebaVymenit[1], pridaneOsoby) == -1): # osoba uz bola pridana
                    pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osobaMeno))
                vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
            else: # inak bude nahradzat meno, ktore este nie je pridane
                indexPridaneho = uzNahradenePismeno(trebaVymenit[1], pridaneOsoby)
                if (indexPridaneho != -1): # osoba uz bola pridana
                    zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, pridaneOsoby[indexPridaneho].meno, 1)  # osoba uz bola pridana, takze ju nebudem davat do listu
                    vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
                else: # osoba uz bola pridana
                    vyskusajVsetkyOsoby(trebaVymenit, osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
        else:
            if (platnaElementarnaPodmienka(zlozenaPodmienka[cisloPodmienky])):
                vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)

def vytvorZoznamMoznychInstancii():
    # for osoba in osoby:
        for pravidlo in nacitanePravidla:
            zlozenaPodmienka = pravidlo.podmienky.split(")")[:len(pravidlo.podmienky.split(")")) - 1]
            splitnuteAkcie = pravidlo.akcie.split(")")[:len(pravidlo.akcie.split(")")) - 1]
            vytvorPodmienkyPravidla(osoby[0], [], pravidlo.cisloPravidla, pravidlo.nazov, zlozenaPodmienka, splitnuteAkcie, 0)


def zistiDosadenie(pismenkoOsoby, instanciaPravidla):
    for pridanaOsoba in instanciaPravidla.pridaneOsoby:
        if (pismenkoOsoby == pridanaOsoba.pismenko):
            return pridanaOsoba.meno


def vytvorAkciu(akcia, instanciaPravidla):
    vytvorenaAkcia = ""
    for slovo in akcia.split()[1:]:
        if (slovo[0] == "?"):
            vytvorenaAkcia = vytvorenaAkcia + zistiDosadenie(slovo[1], instanciaPravidla) + " "
        else:
            vytvorenaAkcia = vytvorenaAkcia + slovo + " "

    if (vytvorenaAkcia[len(vytvorenaAkcia) - 1] == " "):
        return vytvorenaAkcia[:len(vytvorenaAkcia) - 1]
    else:
        return vytvorenaAkcia


def zistiOvplyvneniePridajVykonaj(pridajAkcia):
    for fakt in pracovnaPamat:
        if (fakt == pridajAkcia):
            return False

    pracovnaPamat.append(pridajAkcia)
    return True


def zistiOvplyvnenieZmazVykonaj(zmazAkcia):
    for fakt in pracovnaPamat:
        if (fakt == zmazAkcia):
            pracovnaPamat.remove(zmazAkcia)
            return True

    return False


def akOvplyvniaVykonajAkcie(instanciaPravidla):
    spravy = []
    ovplyvnenie = False
    for akcia in instanciaPravidla.akcie:
        if (akcia.split()[0] == "pridaj"):
            vytvorenaAkcia = vytvorAkciu(akcia, instanciaPravidla)
            ovplyvnenie = zistiOvplyvneniePridajVykonaj(vytvorenaAkcia)
        elif (akcia.split()[0] == "vymaz"):
            vytvorenaAkcia = vytvorAkciu(akcia, instanciaPravidla)
            ovplyvnenie = zistiOvplyvnenieZmazVykonaj(vytvorenaAkcia)
        elif (akcia.split()[0] == "sprava"):
            spravy.append(vytvorAkciu(akcia, instanciaPravidla))

    if (ovplyvnenie):
        for sprava in spravy:
            print(sprava)
        return True

    return False


def zistiCiPlatnaPodmienka(instanciaPravidla):
    print(instanciaPravidla.podmienky)
    for podmienka in instanciaPravidla.podmienky:
        platiPodmienka = False
        for fakt in pracovnaPamat:
            if (podmienka == fakt):
                platiPodmienka = True
        if (platiPodmienka == False):
            return False

    if(akOvplyvniaVykonajAkcie(instanciaPravidla)):
        return True
    else:
        return False


# def vykonajAkciePlatnehoPravidla():
#     while (True):
#         try:
#             vytiahnutaInstancia = heapq.heappop(minHeapPravidla)
#             if (zistiCiPlatnaPodmienka(vytiahnutaInstancia)):
#                break
#         except IndexError:
#             break


nacitajFakty()
nacitajPravidla()
vytvorZoznamMoznychInstancii()
for instancia in instanciePravidla:
    print(instancia.nazov, end=" ")
    print(instancia.podmienky)
    # for pridanaOsoba in instancia.pridaneOsoby:
    #     print(pridanaOsoba.pismenko + " " + pridanaOsoba.meno)
# vykonajAkciePlatnehoPravidla()
# for fakt in pracovnaPamat:
#     print(fakt)
# for pravidlo in pravidla:
#     print(pravidlo.cisloPravidla)
#     print(pravidlo.nazov)
#     print(pravidlo.podmienky)
#     print(pravidlo.akcie)

# vykonane = True
# while(vykonane):
#     vykonane = False
#     for i in range(len(osoby)):
#         vytvorZoznamAplikovatelnychInstanciiPravidiel(osoby[i])
#     vyfilTrujPravidla()
#     zapisPravidloDoPracovnejPamati()
#
# file = open("fakty_vystup.txt", "w")
# for fakt in pracovnaPamat:
#     file.write(fakt)






