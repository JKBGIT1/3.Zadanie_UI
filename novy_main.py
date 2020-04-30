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


def vytvorRodicovskyVztah(rodicIndex, dietaIndex, rodicObjekt, dietaObjekt):
    osoby[rodicIndex].deti.append(dietaObjekt)
    osoby[dietaIndex].rodicia.append(rodicObjekt)


def pridajRodicovskyVztah(line):
    rodicIndex = None
    dietaIndex = None
    rodic = line[0]
    dieta = line[3]

    for i in range(len(osoby)):
        if (osoby[i].meno == rodic):
            rodicIndex = i
        elif (osoby[i].meno == dieta):
            dietaIndex = i

    if (rodicIndex != None and dietaIndex != None): # zaznam o rodicovi aj o dietati je v liste pre osoby
        vytvorRodicovskyVztah(rodicIndex, dietaIndex, osoby[rodicIndex], osoby[dietaIndex])
    elif (rodicIndex != None): # zaznam o rodicovi je v liste pre osoby
        osoby.append(Osoba(dieta))
        vytvorRodicovskyVztah(rodicIndex, len(osoby) - 1, osoby[rodicIndex], osoby[len(osoby) - 1])
    elif (dietaIndex != None): # zaznam o dietati je v liste pre osoby
        osoby.append(Osoba(rodic))
        vytvorRodicovskyVztah(len(osoby) - 1, dietaIndex, osoby[len(osoby) - 1], osoby[dietaIndex])
    else: # zaznam o dietati a ani o rodicovin nie je v liste
        osoby.append(Osoba(rodic))
        osoby.append(Osoba(dieta))
        vytvorRodicovskyVztah(len(osoby) - 2, len(osoby) - 1, osoby[len(osoby) - 2], osoby[len(osoby) - 1])


def pridajPohlavieMuz(line):
    muz = line[1]

    for i in range(len(osoby)):
        if (osoby[i].meno == muz):
            osoby[i].pohlavie = "muz"
            return

    novaOsoba = Osoba(muz)
    novaOsoba.pohlavie = "muz"
    osoby.append(novaOsoba)


def pridajPohlavieZena(line):
    zena = line[1]

    for i in range(len(osoby)):
        if (osoby[i].meno == zena):
            osoby[i].pohlavie = "zena"
            return

    novaOsoba = Osoba(zena)
    novaOsoba.pohlavie = "zena"
    osoby.append(novaOsoba)


def vytvorManzelskyVztah(manzelia1Index, manzelia2Index, manzelia1Objekt, manzelia2Objekt):
    osoby[manzelia1Index].manzelia = manzelia2Objekt
    osoby[manzelia2Index].manzelia = manzelia1Objekt


def pridajManzelov(line):
    manzelia1Index = None
    manzelia2Index = None
    manzelia1 = line[1]
    manzelia2 = line[2]

    for i in range(len(osoby)):
        if (osoby[i].meno == manzelia1):
            manzelia1Index = i
        elif (osoby[i].meno == manzelia2):
            manzelia2Index = i

    if (manzelia1Index != None and manzelia2Index != None): # zaznam o rodicovi aj o dietati je v liste pre osoby
        vytvorManzelskyVztah(manzelia1Index, manzelia2Index, osoby[manzelia1Index], osoby[manzelia2Index])
    elif (manzelia1Index != None): # zaznam o rodicovi je v liste pre osoby
        osoby.append(Osoba(manzelia2))
        vytvorManzelskyVztah(manzelia1Index, len(osoby) - 1, osoby[manzelia1Index], osoby[len(osoby) - 1])
    elif (manzelia2Index != None): # zaznam o dietati je v liste pre osoby
        osoby.append(Osoba(manzelia1))
        vytvorManzelskyVztah(len(osoby) - 1, manzelia2Index, osoby[len(osoby) - 1], osoby[manzelia2Index])
    else: # zaznam o dietati a ani o rodicovin nie je v liste
        osoby.append(Osoba(manzelia1))
        osoby.append(Osoba(manzelia2))
        vytvorManzelskyVztah(len(osoby) - 2, len(osoby) - 1, osoby[len(osoby) - 2], osoby[len(osoby) - 2])


def nacitajFakty():
    file = open("fakty.txt", "r")

    for line in file:
        print(line)
        for word in line.split():
            if (word == "rodic"):
                pridajRodicovskyVztah(line.split())
            elif (word == "muz"):
                pridajPohlavieMuz(line.split())
            elif (word == "zena"):
                pridajPohlavieZena(line.split())
            elif (word == "manzelia"):
                pridajManzelov(line.split())

    file.close()


def skontrolujDalsieDeti(file, rodic1, rodic2):
    # zistim, ci druhy rodic nema pridelene dalsie deti , ktore ma prvy rodic
    for dietarodica1 in rodic1.deti:
        for dietarodica2 in rodic2.deti:
            if (dietarodica1 == dietarodica2):
                break
            elif (dietarodica2 == rodic2.deti[-1]):
                # druhy rodic nema pridelene dieta, ktore ma prvy, tym padom mu ho pridam a zapisem novy fakt do fakty.txt
                dietarodica1.rodicia.append(rodic2) # dietatu pridam druheho rodica
                rodic2.deti.append(dietarodica1) # druhemu rodicovi pridam dieta
                file.write(rodic2.meno + " je rodic " + dietarodica1.meno + "\n")


def skusPridatDruhehoRodica(file, osoba): # ak ma osoba rodica, tak je mozne, ze je jej rodic vo vztahu manzelsko, tym padom ma osoba aj druheho rodica
    if (len(osoba.rodicia) != 0 and osoba.rodicia[0].manzelia != None): # ak ma osoba rodica a rodic je vo vztahu manzelskom, tak jej pridam dalsieho rodica
        # jeden rodic je vo vztahu manzelskom, tym padom je mozne, ze osobe budem pridavat dalsieho rodica, ak tam nie je
        if (len(osoba.rodicia) == 1 or osoba.rodicia[0].manzelia != osoba.rodicia[1]): # ak je uz rodic priradeny k osobe, tak sa nebude pridavat novy fakt ani vztah osoby
            # ak rodic osoby je vo vztahu manzelskom a osoba ma iba jedneho rodica, tak sa jej prida druhy a zaroven sa prida novy fakt do suboru fakty.txt
            osoba.rodicia.append(osoba.rodicia[0].manzelia)
            osoba.rodicia[1].deti.append(osoba)
            file.write(osoba.rodicia[1].meno + " je rodic " + osoba.meno + "\n")
            # je mozne, ze prvy rodic ma viac deti, tym padom bude mat aj druhy rodic viacej deti
            skontrolujDalsieDeti(file, osoba.rodicia[0], osoba.rodicia[1])


def skusOtecDalsejOsoby(file, otec):
    for dieta in otec.deti:
        if (dieta.otec == None):
            dieta.otec = otec
            file.write(otec.meno + " je otec " + dieta.meno + "\n")


def skusMatkaDalsejOsoby(file, matka):
    for dieta in matka.deti:
        if (dieta.mama == None):
            dieta.mama = matka
            file.write(matka.meno + " je matka " + dieta.meno + "\n")


def zistiCiMaOtcaMatku(file, osoba):
    for rodic in osoba.rodicia: # osobe prejdem vsetkych rodicov a zistim, ci je mozne urcit presne mamu alebo otca
        if (rodic.pohlavie == "muz"): # tento rodic je muz, takze bude otec danej osoby
            if (rodic != osoba.otec): # ak rodic nema prideleny vztah otec ku danej osobe, tak pridam novy fakt do fakty.txt a vytvorim novy vztah
                osoba.otec = rodic
                file.write(rodic.meno + " je otec " + osoba.meno + "\n")
                skusOtecDalsejOsoby(file, rodic)
        elif (rodic.pohlavie == "zena"): # tento rodic je zena, takze bude mama danej osoby
            if (rodic != osoba.mama): # ak rodic nema prideleny vztah mama ku danej osobe, tak pridam novy fakt do fakty.txt a vytvorim novy vztah
                osoba.mama = rodic
                file.write(rodic.meno + " je matka " + osoba.meno + "\n")
                skusMatkaDalsejOsoby(file, rodic)

# v cykle prejdem vsetkych surodencov danej osoby, aby som zistil, ci uz sa dieta rodica nenachadza ako surodenec danej osoby
def skusPridatSurodenca(file, osoba, moznySurodenec):
    for surodenec in osoba.surodenci:
        if (surodenec == moznySurodenec):
            return

    # dieta rodica sa nema prideleny vztah surodenca ku danej osobe, takze mozem pridat novy fakt do fakty.txt a vytvorit surodenecky vztah
    osoba.surodenci.append(moznySurodenec)
    file.write(osoba.meno + " a " + moznySurodenec.meno + " su surodenci\n")
    # elif (osoby[osoby[i].deti[j]].pohlavie == "zena"):
    #     osoba.sestry.append(osoby[i].deti[j])
    #     pridajOsobu(osoba, osobaIndex, osoby[i].deti[j])


def zistiSurodencov(file, osoba):
    for rodic in osoba.rodicia:
        for surodenec in rodic.deti: # dieta ma rodica a idem zistit, ci ma surodencov
            if (surodenec != osoba): # rodic ma dieta a nie je to to, ktore skumam
                skusPridatSurodenca(file, osoba, surodenec)


def pridajOsobuBratSestra(osoba, surodenec):
    if (osoba.pohlavie == "muz"):
        surodenec.bratia.append(osoba)
    # else:
    #     osoby[indexSurodenec].sestry.append(osobaIndex)


def skusPridatBrata(file, osoba, surodenec):
    for brat in osoba.bratia:
        if (brat == surodenec):
            return

    if (osoba.pohlavie == "muz"):
        file.write(osoba.meno + " je brat " + surodenec.meno + "\n")
        pridajOsobuBratSestra(osoba, surodenec)
    file.write(surodenec.meno + " je brat " + osoba.meno + "\n")
    pridajOsobuBratSestra(surodenec, osoba)


def zistiBratov(file, osoba):
    for surodenec in osoba.surodenci:
        if (surodenec.pohlavie == "muz"):
            skusPridatBrata(file, osoba, surodenec)


def skusPridatStryka(file, osoba, dieta):
    for stryko in dieta.stryko: # zistim, ci uz nahodou nie je vytvoreny vztah stryka s dietatom
        if (stryko == osoba):
            return

    dieta.stryko.append(osoba)
    print("sprava " + dieta.meno + " ma stryka")
    file.write(osoba.meno + " je stryko " + dieta.meno + "\n")


def zistiStryka(file, osoba):
    for clovek in osoby:
        for brat in clovek.bratia:
            if (brat == osoba): # vybrana osoba je niekoho brat, tym padom moze byt stryko
                for dieta in clovek.deti:
                    skusPridatStryka(file, osoba, dieta)


def testMazania(osoba):
    for clovek in osoby:
        for stryko in clovek.stryko:
            if (stryko == osoba):
                with open("fakty.txt", "r") as f:
                    lines = f.readlines()
                with open("fakty.txt", "w") as f:
                    for line in lines:
                        if line != ("zena " + clovek.meno + "\n"):
                            f.write(line)
                f.close()


def vyskusajPravidla(file, osoba):
    skusPridatDruhehoRodica(file, osoba)
    zistiCiMaOtcaMatku(file, osoba)
    zistiSurodencov(file, osoba)
    zistiBratov(file, osoba)
    zistiStryka(file, osoba)
    testMazania(osoba)


nacitajFakty()

file = open("fakty.txt", "a")
for i in range(len(osoby)):
    vyskusajPravidla(file, osoby[i])

file.close()
# for i in range(len(osoby)):
#     print(osoby[i].meno)
#     print(osoby[i].rodicia)
#     print(osoby[i].bratia)
#     print(osoby[i].sestry)
#     print(osoby[i].deti)
#     print(osoby[i].manzelia)
#     print(osoby[i].pohlavie)




