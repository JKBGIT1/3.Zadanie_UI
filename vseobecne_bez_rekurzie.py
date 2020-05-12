import heapq
import copy

class Pravidlo:
    def __init__(self, cisloPravidla, nazov, podmienky, akcie):
        self.cisloPravidla = cisloPravidla # podla toho, v akom poradi bolo zo suboru pravidla.txt nacitane pravidlo bude mat svoje cislo
        self.nazov = nazov # nazov pravidla sa vypisuje v pripade krokovania riesenie, kvoli tomu aby pouzivatel vedel, akcie ktoreho pravidla sa vykonali
        self.podmienky = podmienky # zlozena podmieka, ktora musi po naviazani platit aby sa vykonali akcie pravidla
        self.akcie = akcie # akcie pravidla, ktore sa vykonaju v pripade, ze plati podmienka a ovplyvnia pracovnu pamat
    def __lt__(self, other):  # potrebna funkcia na porovnovanie v heape -> nazov objektu min heapu ovplyvniaPracovnuPamat
        return self.cisloPravidla < other.cisloPravidla
    # po platnosti podmienky zistim, ktore akcie pravidla ovplyvnuju pracovnu pamat a nahradim ich povodnymi, pretoze je mozne, ze ich budem vykonavat
    def vymenZaOvplyvnujuceAkcie(self, akcie):
        self.akcie = akcie

# reprezentuje meno osoby, ktore som v podmienka naviazal na vybrane pismenko,
# potrebne z dovodu aby jedno meno nenaviazovalo na viac ako jedno pismenko
class PridanaOsoba:
    def __init__(self, pismenko, meno):
        self.pismenko = pismenko
        self.meno = meno


osoby = [] # mena vsetkych osob, ktore sa budu nachadzat vo fakty.txt pridam do tohto listu
pracovnaPamat = [] # do tejto pamate sa na zaciatku nacitaju vsetky fakty, s ktorymi budem pracovat
instanciePravidla = [] # v tomto liste sa nachadzaju pravidla, ktorym podmienky platia a idem zistit, ci ich akcie ovplyvnia pracovnu pamat
ovplyvniaPracovnuPamat = [] # toto je min halda, v ktorej sa budu nachadzat iba instancie pravidla, ktore ovplyvnia pracovnu pamat, su usporiadane podla cislaPravidla
nacitanePravidla = [] # do tohto listu nacitam vsetky pravidla, ktore si reprezentujem classou Pravidlo

# ak meno osoby, ktora sa nachadza vo fakte este nieje nacitane v liste osoby, tak ho tam pridam
def skusPridatMeno(meno):
    for osoba in osoby:
        if (osoba == meno):
            return
    osoby.append(meno)


def nacitajFakty():
    file = open("fakty.txt", "r")

    for line in file: # zo suboru nacitam fakty po riadkoch
        pracovnaPamat.append(line[:-1]) # fakty pridavam do pracovnej pamata nad ktorou budem vykonavat akcie
        for word in line.split(): # nacitany riadok si rozdelim na slova
            if (word[0].isupper()): # ak sa slovo zacina na pismenko, tak viem, ze je to meno
                skusPridatMeno(word) # pridam nacitane meno z faktu do listu osoby, ak sa tam este nenachadza

    file.close()

# v tejto funkcii nacitam jednotlive pravidla postupne, pricom im priradim cislo, podla ktoreho ich budem vyberat z haldy
# pravidlo nemoze byt na viac ako 3 riadky
def nacitajPravidla():
    cisloPravidla = 1
    nazovPravidla = ""
    podmienkyPravidla = ""
    akciePravidla = ""
    file = open("pravidla.txt", "r")

    pocitadloRiadkov = 1
    for line in file:
        if (pocitadloRiadkov == 1): # na prvom riadku pravidla sa nachadza jeho nazov
            nazovPravidla = line[0:len(line) - 2] # nazov pravidla ulozim bez dvojbodky a noveho riadku
        elif (pocitadloRiadkov == 2): # na druhom riadku sa nachadzaju podmienky pravidla so zaciatocnym slovom AK
            # podmineky pravidla ulozim bez
            # prveho slova AK, zbytocnych zaciatocnych medzier,
            # poslednej uzatvaracej zatvorky a noveho riadku
            podmienkyPravidla = line[4:len(line) - 2]
        elif (pocitadloRiadkov == 3): # na tretom riadku sa nachadzaju akcie pravidla so zaciatocnym slovom POTOM
            # akcie pravidla ulozim bez
            # prveho slova POTOM, zbytocnych zaciatocnych medzier
            # poslednej uzatvaracej zatvorky a noveho riadku
            akciePravidla = line[7:len(line) - 2] #
        else: # ked som nacital 3 riadky zo suboru, tak program to berie tak, ze uz ma nacitane vsetky potrebne veci pre pravidlo a nasleduje prazdny riadok
            # z podmienko pravidla aj z akcii pravidla vymazane "(", pre dalsie ucely
            nacitanePravidla.append(Pravidlo(cisloPravidla, nazovPravidla, podmienkyPravidla.replace("(", ""), akciePravidla.replace("(", "")))
            cisloPravidla = cisloPravidla + 1
            pocitadloRiadkov = 0
        pocitadloRiadkov = pocitadloRiadkov + 1
    # po skonceni suboru som este nepridal posledne nacitane pravidlo, takze tak musim urobit pred skoncenim funkcie
    nacitanePravidla.append(Pravidlo(cisloPravidla, nazovPravidla, podmienkyPravidla.replace("(", ""), akciePravidla.replace("(", "")))
    file.close()

# ak sa znova vyskytlo pismenko, za ktore som uz nahradil meno, tak nebudem hladat nove naviazanie, ale pouzijem to, co som vyuzil predtym
def uzNahradenePismeno(pismenkoOsoby, pridaneOsoby):
    for i in range(len(pridaneOsoby)):
        if (pridaneOsoby[i].pismenko == pismenkoOsoby):
            return i
    return -1


def vyskusajVsetkyOsoby(trebaVymenit, osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky):
    pomocnePridaneOsoby = copy.deepcopy(pridaneOsoby) # do tohto listu pridavam mena vsetkych osob, ktore sa uz v behu tejto funkcii naviazali
    for osoba in osoby: # prejdem mena osob v liste osoby
        bolPridany = False
        starePridaneOsoby = copy.deepcopy(pridaneOsoby)
        for pridanaOsoba in pomocnePridaneOsoby: # v cykle zistujem, ci som uz nahodou meno danej osoby nenaviazal na pismenko
            if (osoba == pridanaOsoba.meno):  # bol pridany, takze znamena, ze uz ho nebudem pridavat
                bolPridany = True
        if (bolPridany == False and osoba != osobaMeno):  # osoba, ktorej meno som prechadzal v cykle este nie je v pridanych
            starePridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba)) # nahradim meno osoby namiesto otazniku a pismenka
            pomocnePridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osoba)) # pridam meno osoby do listu, aby som ju znova nenaviazal
            pomocnaZlozena = copy.deepcopy(zlozenaPodmienka)
            # v pomocnej zlozenej podmienke naviazem meno osoby, ktora este nebola naviazana
            # cyklus naviazania na aktualne pismenko bude pokracovat, ale zavola sa funkcia na pokracovania naviazovania zlozenej podmienky
            # pricom pismenko, ktore skusam navazovat v cykle v nej bude nahradene za meno osoby
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

# podla toho na ake pismenka som naviazoval mena osob podmienkach naviazem mena osob v akciach vzniknutej instancie pravidla
def naviazAkcie(akcie, pridaneOsoby):
    naviazaneAkcie = []
    for akcia in akcie: # prejdem vsetky akcie pravidla
        while(akcia.find("?") != -1): # ak najdem ?, tak viem, ze treba vykonat naviazanie
            trebaVymenit = "?" + akcia[akcia.find("?") + 1] # z akcie vyberiem znak ? a velke pismenko, za ktore idem nahradit meno
            for pridanaOsoba in pridaneOsoby: # prejdem vsetky pridaneOsoby, ktore som vyuzil v podmienkach pravidla
                if (trebaVymenit[1] == pridanaOsoba.pismenko): # ak sa pismenko v akcii rovna pismenku pridanej osobe v podmienke, tak na hradim jej meno za pismenko v akcii
                    akcia = akcia.replace(trebaVymenit, pridanaOsoba.meno, 1)
                    break
        naviazaneAkcie.append(akcia)
    return naviazaneAkcie



def vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky):
    if (cisloPodmienky == len(zlozenaPodmienka)): # naviazalo som mena osob v celej zlozenej podmienka, ktora plati, takze vytvorim novu instanciu pravidla
        vytvorenePravidlo = Pravidlo(cisloPravidla, nazovPravidla, zlozenaPodmienka, naviazAkcie(akcie, pridaneOsoby))
        instanciePravidla.append(vytvorenePravidlo)
    else:
        if (zlozenaPodmienka[cisloPodmienky].find("?") != -1): # ak sa v elementarnej podmienke nachadza otaznik, tak je potrebne vykonat naviazanie
            trebaVymenit = "?" + zlozenaPodmienka[cisloPodmienky][zlozenaPodmienka[cisloPodmienky].find("?") + 1] # nacitam otaznik a pismenko za nim
            if (trebaVymenit[1] == "X"): # ak je pismenko X, tak budem nahradzat meno v premenej osobaMeno
                zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, osobaMeno, 1) # vymenit ? s pismenkom za hodnotu v premenej osobaMeno
                if (uzNahradenePismeno(trebaVymenit[1], pridaneOsoby) == -1): # osobaMeno sa nenachadza v liste pridaneOsoby, takze ju tam pridam
                    pridaneOsoby.append(PridanaOsoba(trebaVymenit[1], osobaMeno))
                # pokracujem v navazovani zlozenej podmienky pravidla
                vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
            else:
                # zistim ci som za aktualne pismenko uz nahradil meno nejakej osoby
                indexPridaneho = uzNahradenePismeno(trebaVymenit[1], pridaneOsoby)
                if (indexPridaneho != -1): # osoba uz bola pridana, takze naviazem meno z listu pridaneOsoby, ktore danemu pismenku patri
                    zlozenaPodmienka[cisloPodmienky] = zlozenaPodmienka[cisloPodmienky].replace(trebaVymenit, pridaneOsoby[indexPridaneho].meno, 1)  # osoba uz bola pridana, takze ju nebudem davat do listu
                    vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
                else: # aktualnemu pismenku este neprislucha meno ziadnej osoby, takze naviazem vsetky mena, ktore nie su v liste priadneOsoby
                    vyskusajVsetkyOsoby(trebaVymenit, osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky)
        else: # ak sa v elementarnej podmienke nenachadza otaznik, tak musim zisti, ci je pravdiva
            if (platnaElementarnaPodmienka(zlozenaPodmienka[cisloPodmienky])): # ak je elementarna podmienka pravdiva, tak pokracujem v navazovani zlozenej podmienky
                vytvorPodmienkyPravidla(osobaMeno, pridaneOsoby, cisloPravidla, nazovPravidla, zlozenaPodmienka, akcie, cisloPodmienky + 1)


def vytvorZoznamMoznychInstancii():
    for osoba in osoby: # osoba z tohto cyklu sa bude vzdy nahradzat za pismenko X v podmienke aj akciach
        for pravidlo in nacitanePravidla: # prejdem vsetky pravidla, pricom v nich bude navazovat za X stale tu istu osobu
            zlozenaPodmienka = pravidlo.podmienky.split(")")[:len(pravidlo.podmienky.split(")")) - 1] # odstranim nepotrebne veci
            splitnuteAkcie = pravidlo.akcie.split(")")[:len(pravidlo.akcie.split(")")) - 1] # odstranim nepotrebne veci
            # zacnem navazovat aktualnu osobu na podmienky pravidla
            vytvorPodmienkyPravidla(osoba, [], pravidlo.cisloPravidla, pravidlo.nazov, zlozenaPodmienka, splitnuteAkcie, 0)

# z akcie vytvorim fakt
def vytvorKonecnuAkciu(akcia):
    novaAkcia = ""
    for slovo in akcia.split()[1:len(akcia.split())]:
        novaAkcia = novaAkcia + " " + slovo
    return novaAkcia[1:]


# zistim, ci akcia pridaj ovplyvni pracovnu pamat
def zistiOvplyvneniePridajVykonaj(pridajAkcia):
    spravnyTvarAkcie = vytvorKonecnuAkciu(pridajAkcia)
    for fakt in pracovnaPamat:
        if (fakt == spravnyTvarAkcie):
            return False

    return True

# zistim, ci akcia mazania ovplyvni pracovnu pamat
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
        if (akcia.split()[0] == "pridaj"): # ak sa ma vykonat akcia pridaj, tak musim zistit, ci ovplyvni pracovnu pamat
            ovplyvnenie = zistiOvplyvneniePridajVykonaj(akcia)
        elif (akcia.split()[0] == "vymaz"): # ak sa ma vykonat akcia vymaz, tak musim zisti, ci ovplyvni pracovnu pamat
            ovplyvnenie = zistiOvplyvnenieZmazVykonaj(akcia)
        elif (akcia.split()[0] == "sprava"): # sprava neovplyvnuje pracovnu pamat, preto si ich zatedy ukladam do samostatneho listu
            spravy.append(akcia)

        if (ovplyvnenie): # nasla sa akcia, ktora ovplyvni pamat, takze ju pridam do listu akcii, ktore ovplyvnuju pamat
            ovplyvnujuceAkcie.append(akcia)

    if (len(ovplyvnujuceAkcie) > 0): # ak sa v liste nachadza aspon jedna akcia, ktora ovplyvnuje pracovnu pamat, tak k nej pridam spravy pravidla
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
    if (akcia.split()[0] == "sprava"): # viem, ze sa v halde nachadzali iba instancie pravidla, ktorych akcie ovplyvnia pamat, takze ich spravy vypisem tiez
        print("\n" + vytvorKonecnuAkciu(akcia))
    elif (akcia.split()[0] == "pridaj"): # pridam fakt do pracovnej pamate
        pracovnaPamat.append(vytvorKonecnuAkciu(akcia))
    elif (akcia.split()[0] == "vymaz"): # vymazem fakt z pracovnej pamati
        pracovnaPamat.remove(vytvorKonecnuAkciu(akcia))


def vykonajAkcieJednejInstanciePravidla(postupVykonania):
    try:
        vytiahnutaInstancia = heapq.heappop(ovplyvniaPracovnuPamat) # vytiahnem prvok z haldy
        # v pripade, ze sa riesenie vykonava po krokoch, tak vypisem nazov pravidla a aj jeho akcie, ktore som vykonal
        if (postupVykonania != "2"):
            print("VYKONANE AKCIE PRAVIDLA: " + vytiahnutaInstancia.nazov)
        for akcia in vytiahnutaInstancia.akcie:
            if (postupVykonania != "2"):
                print(akcia)
            vykonajAkciu(akcia)
        return True # pretoze bola zmenena pracovna pamat, tak program pokracuje v rieseni
    except IndexError: # ak je halda prazdna, tak vyhodi podmienku a ja vratim False, pretoze pracovna pamat nebola zmenena a program skonci
        return False


nacitajFakty() # nacitam fakty do listu pracovnaPamat
nacitajPravidla() # nacitam pravidla do listu nacitanePravidla

postupVykonania = ""
prebehloOvplyvnenie = True
while(prebehloOvplyvnenie):
    if (postupVykonania != "2"): # rozhoduje, ci sa bude vykonavat riesenie po krocho s vypisom alebo az do konca
        postupVykonania = input("Jeden krok(1), Do konca(2): ")
    vytvorZoznamMoznychInstancii() # vytvorim vsetky instancie pravidla, ktorym platia podmienky
    akOvplyvniaPridajDoHaldy() # tie pravidla, ktorych akcie ovplyvnia pracovnu pamat pridam do min haldy
    # vyberiem z min haldy pravidlo, ktore je na vrchu a vykonam jeho akcie, ak je halda prazdna, tak skonci cyklus
    prebehloOvplyvnenie = vykonajAkcieJednejInstanciePravidla(postupVykonania)
    ovplyvniaPracovnuPamat.clear() # je potrebne vyprazdnit haldu
    if (postupVykonania != "2"): # ak sa riesenie vykonava po krokoch, tak vypisem pracovnu pamat, aby som videl, ktory fakt bol do nej pridany
        print("\nAKTUALNA PRACOVNA PAMAT:")
        for fakt in pracovnaPamat:
            print(fakt)
        print("")

# po skonceni hlavneho cyklu sa zapisu fakty v pracovnej pamati do suboru fakty_vystup.txt
print("\nFINALNY VYSLEDOK ZAPISANY V fakty_vystup.txt")
file = open("fakty_vystup.txt", "w")
for fakt in pracovnaPamat:
    file.write(fakt + "\n")
file.close()






