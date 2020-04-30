class Osoba:
    def __init__(self, meno):
        self.meno = meno
        self.rodicia = []
        self.otec = None
        self.mama = None
        self.stryko = []
        self.surodenci = []
        self.bratia = []
        self.sestry = []
        self.deti = []
        self.manzelia = None
        self.pohlavie = ""


osoby = [] # vsetky osoby, ktore sa budu nachadzat vo faktoch pridam do tohto listu


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
    osoby[manzelia1Index].manzelia = manzelia2Index
    osoby[manzelia2Index].manzelia = manzelia1Index


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

    file.close()


def skontrolujDalsieDeti(file, rodicIndex1, rodicIndex2):
    # zistim, ci druhy rodic nema pridelene dalsie deti , ktore ma prvy rodic
    for i in range(len(osoby[rodicIndex1].deti)):
        for j in range(len(osoby[rodicIndex2].deti)):
            if (osoby[rodicIndex1].deti[i] == osoby[rodicIndex2].deti[j]):
                break
            elif (j == len(osoby[rodicIndex2].deti) - 1):
                # druhy rodic nema pridelene dieta, ktore ma prvy, tym padom mu ho pridam a zapisem novy fakt do fakty.txt
                osoby[osoby[rodicIndex1].deti[i]].rodicia.append(osoby[rodicIndex2]) # dietatu pridam druheho rodica
                osoby[rodicIndex2].deti.append(osoby[rodicIndex1].deti[i]) # druhemu rodicovi pridam dieta
                file.write("(" + osoby[rodicIndex2].meno + " je rodic " + osoby[osoby[rodicIndex1].deti[i]].meno + ")\n")


def skusPridatDruhehoRodica(file, osoba, osobaIndex): # ak ma osoba rodica, tak je mozne, ze je jej rodic vo vztahu manzelsko, tym padom ma osoba aj druheho rodica
    if (len(osoba.rodicia) != 0 and osoby[osoba.rodicia[0]].manzelia != None): # ak ma osoba rodica a rodic je vo vztahu manzelskom, tak jej pridam dalsieho rodica
        # jeden rodic je vo vztahu manzelskom, tym padom je mozne, ze osobe budem pridavat dalsieho rodica, ak tam nie je
        if (len(osoba.rodicia) == 1 or osoby[osoba.rodicia[0]].manzelia != osoba.rodicia[1]): # ak je uz rodic priradeny k osobe, tak sa nebude pridavat novy fakt ani vztah osoby
            # ak rodic osoby je vo vztahu manzelskom a osoba ma iba jedneho rodica, tak sa jej prida druhy a zaroven sa prida novy fakt do suboru fakty.txt
            osoba.rodicia.append(osoby[osoba.rodicia[0]].manzelia)
            osoby[osoba.rodicia[1]].deti.append(osobaIndex)
            file.write("(" + osoby[osoba.rodicia[1]].meno + " je rodic " + osoba.meno + ")\n")
            # je mozne, ze prvy rodic ma viac deti, tym padom bude mat aj druhy rodic viacej deti
            skontrolujDalsieDeti(file, osoba.rodicia[0], osoba.rodicia[1])


def zistiCiMaOtcaMatku(file, osoba):
    for i in range(len(osoba.rodicia)): # osobe prejdem vsetkych rodicov a zistim, ci je mozne urcit presne mamu alebo otca
        if (osoby[osoba.rodicia[i]].pohlavie == "muz"): # tento rodic je muz, takze bude otec danej osoby
            if (osoba.rodicia[i] != osoba.otec): # ak rodic nema prideleny vztah otec ku danej osobe, tak pridam novy fakt do fakty.txt a vytvorim novy vztah
                osoba.otec = osoba.rodicia[i] # otec je tak isto index v liste osoby
                file.write("(" + osoby[osoba.otec].meno + " je otec " + osoba.meno + ")\n")
        elif (osoby[osoba.rodicia[i]].pohlavie == "zena"): # tento rodic je zena, takze bude mama danej osoby
            if (osoba.rodicia[i] != osoba.mama): # ak rodic nema prideleny vztah mama ku danej osobe, tak pridam novy fakt do fakty.txt a vytvorim novy vztah
                osoba.mama = osoba.rodicia[i] # mama je tiez index v liste osoby
                file.write("(" + osoby[osoba.mama].meno + " je mama " + osoba.meno + ")\n")


def pridajOsobu(osoba, osobaIndex, indexSurodenec):
    if (osoba.pohlavie == "muz"):
        osoby[indexSurodenec].bratia.append(osobaIndex)
    # else:
    #     osoby[indexSurodenec].sestry.append(osobaIndex)

# v cykle prejdem vsetkych surodencov danej osoby, aby som zistil, ci uz sa dieta rodica nenachadza ako surodenec danej osoby
def skusPridatSurodenca(file, osoba, osobaIndex, surodenecIndex):
    for i in range(len(osoba.surodenci)):
        if (osoba.surodenci[i] != surodenecIndex and i == len(osoba.surodenci) - 1):
            # dieta rodica sa nema prideleny vztah surodenca ku danej osobe, takze mozem pridat novy fakt do fakty.txt a vytvorit surodenecky vztah
            file.write("("+ osoba.meno + " " + osoby[surodenecIndex].meno + " su surodenci)\n")
            osoba.surodenci.append(surodenecIndex)
            if (osoby[surodenecIndex].pohlavie == "muz"): # ak je surodenec muz, tak pridam novy fakt do fakty.txt a vytvorim bratsky vztah
                osoba.bratia.append(surodenecIndex)
                file.write("(" + osoby[surodenecIndex].meno + " je brat " + osoba.meno + ")\n")
                pridajOsobu(osoba, osobaIndex, surodenecIndex)
            # elif (osoby[osoby[i].deti[j]].pohlavie == "zena"):
            #     osoba.sestry.append(osoby[i].deti[j])
            #     pridajOsobu(osoba, osobaIndex, osoby[i].deti[j])


def zistiSurodencov(file, osoba, osobaIndex):
    for i in range(len(osoba.rodicia)):
        for j in range(len(osoby[i].deti)): # dieta ma rodica a idem zistit, ci ma surodencov
            if (osoby[i].deti[j] != osobaIndex): # rodic ma dieta a nie je to to, ktore skumam
                skusPridatSurodenca(file, osoba, osobaIndex, osoby[i].deti[j])


def skusPridatStryka(file, osoba, osobaIndex, indexSurodencaOsoby):
    for i in range(len(osoby[indexSurodencaOsoby].deti)):
        for j in range(len(osoby[i].stryko)): # zistim, ci uz nahodou nie je vytvoreny vztah stryka s dietatom
            if (osoby[i].stryko[j] != osobaIndex and j ==len(osoby[i].stryko) - 1):
                osoby[i].stryko.append(osobaIndex)
                print("sprava " + osoby[i].meno + " ma stryka")
                file.write("(" + osoba.meno + " je stryko " + osoba[i].meno + ")\n")


def zistiStryka(file, osoba, osobaIndex):
    for i in range(len(osoby)):
        for j in range(len(osoby[i].bratia)):
            if (osoby[i].bratia[j] == osobaIndex): # vybrana osoba je niekoho brat, tym padom moze byt stryko
                skusPridatStryka(file, osoba, osobaIndex, i)


def testMazania(osoba):
    for i in range(len(osoba.stryko)):
        if (osoby[i].pohlavie == "zena"):
            with open("fakty.txt", "r") as f:
                lines = f.readlines()
            with open("fakty.txt", "w") as f:
                for line in lines:
                    if line != "(zena " + osoby[i].meno + ")":
                        f.write(line)
            f.close()


def vyskusajPravidla(file, osoba, osobaIndex):
    skusPridatDruhehoRodica(file, osoba, osobaIndex)
    zistiCiMaOtcaMatku(file, osoba)
    zistiSurodencov(file, osoba, osobaIndex)
    zistiStryka(file, osoba, osobaIndex)
    testMazania(osoba)


nacitajFakty()

file = open("fakty.txt", "a")
for i in range(len(osoby)):
    vyskusajPravidla(file, osoby[i], i)

file.close()
# for i in range(len(osoby)):
#     print(osoby[i].meno)
#     print(osoby[i].rodicia)
#     print(osoby[i].bratia)
#     print(osoby[i].sestry)
#     print(osoby[i].deti)
#     print(osoby[i].manzelia)
#     print(osoby[i].pohlavie)




