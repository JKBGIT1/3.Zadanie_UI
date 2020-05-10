import heapq
import copy

class Pravidlo:
    def __init__(self, cisloPravidla, nazov, podmienky, akcie):
        self.cisloPravidla = cisloPravidla
        self.nazov = nazov
        self.podmienky = podmienky
        self.akcie = akcie
    def __lt__(self, other):  # potrebna funkcia na porovnovanie v heape. ficura pythonu
        return self.cisloPravidla < other.cisloPravidla
    def vymenZaOvplyvnujuceAkcie(self, akcie):
        self.akcie = akcie


class PridanaOsoba:
    def __init__(self, pismenko, meno):
        self.pismenko = pismenko
        self.meno = meno


osoby = [] # vsetky osoby, ktore sa budu nachadzat vo faktoch pridam do tohto listu
pracovnaPamat = [] # do tejto pamate sa na zaciatku nacitaju vsetky fakty, s ktorymi budem pracovat
instanciePravidla = [] # v tomto liste sa nachadzaju pravidla, ktorym podmienky platia a idem zistit, ci ich akcie ovplyvnia pracovnu pamat
ovplyvniaPracovnuPamat = [] # toto je min halda, v ktorej sa budu nachadzat iba instancie pravidla, ktore ovplyvnia pracovnu pamat, su usporiadane podla cislaPravidla
nacitanePravidla = [] # do tohto listu nacitam vsetky pravidla, ktore si reprezentujem classou

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
            nacitanePravidla.append(Pravidlo(cisloPravidla, nazovPravidla, podmienkyPravidla.replace("(", ""), akciePravidla.replace("(", "")))
            cisloPravidla = cisloPravidla + 1
            pocitadloRiadkov = 0
        pocitadloRiadkov = pocitadloRiadkov + 1

    nacitanePravidla.append(Pravidlo(cisloPravidla, nazovPravidla, podmienkyPravidla.replace("(", ""), akciePravidla.replace("(", "")))


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
        if (bolPridany == False and osoba != osobaMeno):  # osoba, ktorej meno prechadzam v cykle este nie je v pridanych
            starePridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
            pomocnePridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
            pomocnaZlozena = copy.deepcopy(zlozenaPodmienka)
            pomocnaZlozena[cisloPodmienky] = pomocnaZlozena[cisloPodmienky].replace(trebaVymenit, osoba, 1)
            vytvorPodmienkyPravidla(osobaMeno, starePridaneOsoby, cisloPravidla, nazovPravidla, pomocnaZlozena, akcie, cisloPodmienky)


def platnaElementarnaPodmienka(elementarnaPodmienka):
    # o to aby sa na kazde pismenko pridala ina osoba sa postara list pridaneOsoby vo vytvorPodmienkyPravidla
    # takze vzdy ked sa nachadza v elementarnej podmienka znak nerovnosti, tak mozem vratit true, pretoze sa dosadene osoby nebudu rovnat
    if (elementarnaPodmienka.find("<>") != -1):
        return True
    for fakt in pracovnaPamat: # ak sa nejedna o znak nerovnosti, tak musim prehladat pracovnu pamat aby som zistil, ci je elementarna podmienka pravdiva
        if (elementarnaPodmienka == fakt): # ak sa podmienka v pracovnej pamati nachadza, tak je fakt, teda vratim True
            return True
    return False # presiel som celu pracovnu pamat, ale elementarnu podmienku som vo faktoch nenasiel, takze vratim False


def naviazAkcie(akcie, pridaneOsoby):
    naviazaneAkcie = []
    for akcia in akcie:
        while(akcia.find("?") != -1):
            trebaVymenit = "?" + akcia[akcia.find("?") + 1]
            for pridanaOsoba in pridaneOsoby:
                if (trebaVymenit[1] == pridanaOsoba.pismenko):
                    akcia = akcia.replace(trebaVymenit, pridanaOsoba.meno, 1)
                    break
        naviazaneAkcie.append(akcia)
    return naviazaneAkcie


# !!! MOZNO BUDE TREBA ZMENIT PISMENKO X V PRAVIDLE SURODENCI NA PISMENKO Y
def vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky):
    if (cisloPodmienky == len(zlozenaPodmienka)):
        vytvorenePravidlo = Pravidlo(cisloPravidla, nazovPravidla, zlozenaPodmienka, naviazAkcie(akcie, pridaneOsoby))
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
    for osoba in osoby:
        for pravidlo in nacitanePravidla:
            zlozenaPodmienka = pravidlo.podmienky.split(")")[:len(pravidlo.podmienky.split(")")) - 1]
            splitnuteAkcie = pravidlo.akcie.split(")")[:len(pravidlo.akcie.split(")")) - 1]
            vytvorPodmienkyPravidla(osoba, [], pravidlo.cisloPravidla, pravidlo.nazov, zlozenaPodmienka, splitnuteAkcie, 0)


def vytvorKonecnuAkciu(akcia):
    novaAkcia = ""
    for slovo in akcia.split()[1:len(akcia.split())]:  # tuto spravne funguje vytvorenie akcie, s ktorou sa ma nieco spravit
        novaAkcia = novaAkcia + " " + slovo
    return novaAkcia[1:]



def zistiOvplyvneniePridajVykonaj(pridajAkcia):
    spravnyTvarAkcie = vytvorKonecnuAkciu(pridajAkcia)
    for fakt in pracovnaPamat:
        if (fakt == spravnyTvarAkcie):
            return False

    return True


def zistiOvplyvnenieZmazVykonaj(zmazAkcia):
    spravnyTvarAkcie = vytvorKonecnuAkciu(zmazAkcia)
    for fakt in pracovnaPamat:
        if (fakt == spravnyTvarAkcie):
            return True

    return False


def zistiOvplyvnujuceAkcie(instanciaPravidla):
    spravy = []
    ovplyvnujuceAkcie = []
    for akcia in instanciaPravidla.akcie:
        ovplyvnenie = False
        if (akcia.split()[0] == "pridaj"):
            ovplyvnenie = zistiOvplyvneniePridajVykonaj(akcia)
        elif (akcia.split()[0] == "vymaz"):
            ovplyvnenie = zistiOvplyvnenieZmazVykonaj(akcia)
        elif (akcia.split()[0] == "sprava"):
            spravy.append(akcia)

        if (ovplyvnenie):
            ovplyvnujuceAkcie.append(akcia)

    if (len(ovplyvnujuceAkcie) > 0):
        for sprava in spravy:
            ovplyvnujuceAkcie.append(sprava)
        return ovplyvnujuceAkcie

    return ovplyvnujuceAkcie


def akOvplyvniaPridajDoHaldy():
    for instanciaPravidla in instanciePravidla: # prebehnem vsetky vytvorene instancie pravidiel
        ovplyvnujuceAkcie = zistiOvplyvnujuceAkcie(instanciaPravidla)
        # ak existuje aspon jedna akcia pridaj alebo zmaz, ktora ovplyvni pracovnu pamat,
        # tak bude vratena v liste ovplyvnujuceAkcie spolocne so vsetkymi spravami, vytvorenej instancie pravidla
        if(len(ovplyvnujuceAkcie) > 0):
            instanciaPravidla.vymenZaOvplyvnujuceAkcie(ovplyvnujuceAkcie) # nahradim vsetky akcie pravidla iba tymi, ktore ovplyvnia pracovnu pamat
            heapq.heappush(ovplyvniaPracovnuPamat, instanciaPravidla) # do min haldy vhodim instanciu pravidla uz iba s akciami, ktore ovplyvnia pracovnu pamat


def vykonajAkciu(akcia):
    if (akcia.split()[0] == "sprava"):
        print(vytvorKonecnuAkciu(akcia))
    elif (akcia.split()[0] == "pridaj"):
        pracovnaPamat.append(vytvorKonecnuAkciu(akcia))
    elif (akcia.split()[0] == "vymaz"):
        pracovnaPamat.remove(vytvorKonecnuAkciu(akcia))


def vykonajAkcieJednejInstanciePravidla():
    try:
        vytiahnutaInstancia = heapq.heappop(ovplyvniaPracovnuPamat)
        for akcia in vytiahnutaInstancia.akcie:
            vykonajAkciu(akcia)
        return True
    except IndexError:
        return False


nacitajFakty()
nacitajPravidla()
pocet = 1
prebehloOvplyvnenie = True
while(prebehloOvplyvnenie):
    vytvorZoznamMoznychInstancii()
    akOvplyvniaPridajDoHaldy()
    prebehloOvplyvnenie = vykonajAkcieJednejInstanciePravidla()
    ovplyvniaPracovnuPamat.clear()

file = open("fakty_vystup.txt", "w")
for fakt in pracovnaPamat:
    file.write(fakt + "\n")






