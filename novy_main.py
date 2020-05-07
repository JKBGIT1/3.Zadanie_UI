import heapq

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
minHeapPravidla = [] # do min heapu vkladam vsetky potencionalne pravidla, ktorych akcie sa mozno vykonaju
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


# def jeTamOtaznik(osoba, podmienka, pridaneOsoby, zlozenaPodmienka):
#     if (podmienka.find("?") != -1):
#         trebaVymenit = "?"
#
#
#
# def vytvorPodmienkyPravidla(osoba, pridaneOsoby, zlozenaPodmienka):
#     for podmienka in zlozenaPodmienka:
#         if (podmienka.find("<>") == -1): # ak sa nejedna o to, ci su nejake osoby rozne, tak bude dosadzat mena do podmienky
#             jeTamOtaznik(osoba, podmienka, pridaneOsoby, zlozenaPodmienka)
#             trebaVymenit = "?" + podmienka[podmienka.find("?") + 1]
#             if (trebaVymenit[1] == "X"):


# !!! MOZNO BUDE TREBA ZMENIT PISMENKO X V PRAVIDLE SURODENCI NA PISMENKO Y
def vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky):
    if (cisloPodmienky == len(zlozenaPodmienka)): # ak som dosadil osoby do celej zlozenej podmienky pravidla, tak zisti ju vratim
        # hodim do haldy pravidlo, ktoreho akcie sa mozu vykonavat, ak bude pravdiva podmienka, ktoru som vytvoril
        vytvorenePravidlo = Pravidlo(cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie,pridaneOsoby)
        heapq.heappush(minHeapPravidla, vytvorenePravidlo)
    else:
        if (zlozenaPodmienka[cisloPodmienky].find("<>") == -1): # to, ze nepridam 2 rovnake osoby mam zabezpecene pomocou listu pridaneOsoby
            trebaVymenit = "?" + zlozenaPodmienka[cisloPodmienky][(zlozenaPodmienka[cisloPodmienky].find("?") + 1)]
            if (trebaVymenit[1] == "X"): # za X sa vzdy nahradza hodnota, ktora je ulozena v premennej osoba, teda meno osoby, pre ktoru vytvram pravidla
                zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, osoba, 1)
                for i in range(len(pridaneOsoby)):
                    if (pridaneOsoby[i].pismenko == "X"): # hodnota premennej osoba uz bola raz pridana, takze ju nepridam do listu pridaneOsoby
                        if (zlozenaPodmienka[cisloPodmienky].find("?") == -1):
                            pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
                            vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)
                        else:
                            pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
                            vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
                if (zlozenaPodmienka[cisloPodmienky].find("?") == -1):
                    pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
                    vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)
                else:
                    pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
                    vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
            else:
                indexPridane = uzNahradenePismeno(trebaVymenit[1], pridaneOsoby)
                if (indexPridane != -1): # za toto pismenko som uz nahradil osobu, takze v dalsej podmienka nahradim tu istu
                    zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, pridaneOsoby[indexPridane].meno, 1) # osoba uz bola pridana, takze ju nebudem davat do listu
                    if (zlozenaPodmienka[cisloPodmienky].find("?") == -1):
                        pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
                        vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)
                    else:
                        pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba))
                        vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
                else: # za toto pismenko som este nenahradil osobu, takze pojdem nahradit novu
                    for i in range(len(osoby)): # vyberiem osobu, ktorej meno chcem nahradit pismenkom
                        bolPridany = False
                        if (osoby[i] == osoba): # premenu tejto osoby pridavam iba pod pismenko X
                            continue
                        j = 0
                        while(j < len(pridaneOsoby)):
                            # ak uz meno danej osoby bolo v nejakej podmienke nahradene skusim dalsiu osobu
                            if (osoby[i] != pridaneOsoby[j].meno):
                                bolPridany = True
                                zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, osoby[i], 1)
                                pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoby[i]))
                                # viacPridaneOsoby = pridaneOsoby
                                # pridaneOsoby.extend(viacPridaneOsoby)
                                if (zlozenaPodmienka[cisloPodmienky].find("?") == -1):
                                    vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)
                                    break
                                else:
                                    vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
                                    break
                            j = j + 1
                        if (bolPridany == False):
                            zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, osoby[i], 1)
                            pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoby[i]))
                            if (zlozenaPodmienka[cisloPodmienky].find("?") == -1):
                                vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)
                            else:
                                vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
        else: # v podmienke sa nachadza "<>", teda je potrebne porovnat, ci su pridavane osoby do podmienok rozdielne, zabezpeci sa mi to pomocou pridaneOsoby, takze sa len posunie rekurzia
            return vytvorPodmienkyPravidla(osoba, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)


def vytvorZoznamMoznychInstancii():
    for osoba in osoby:
        for pravidlo in nacitanePravidla:
            zlozenaPodmienka = pravidlo.podmienky.split(")")[:len(pravidlo.podmienky.split(")")) - 1]
            splitnuteAkcie = pravidlo.akcie.split(")")[:len(pravidlo.akcie.split(")")) - 1]
            vytvorPodmienkyPravidla(osoba, [], pravidlo.cisloPravidla, pravidlo.nazov, zlozenaPodmienka, splitnuteAkcie, 0)


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


def vykonajAkciePlatnehoPravidla():
    while (True):
        try:
            vytiahnutaInstancia = heapq.heappop(minHeapPravidla)
            if (zistiCiPlatnaPodmienka(vytiahnutaInstancia)):
               break
        except IndexError:
            break


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
nacitajPravidla()
vytvorZoznamMoznychInstancii()
vykonajAkciePlatnehoPravidla()
for fakt in pracovnaPamat:
    print(fakt)
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






