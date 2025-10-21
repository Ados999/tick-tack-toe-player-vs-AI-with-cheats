import random
import sys

def uvodni_obrazek():
    obrazek = r"""
     _____ _         _____             _____
    |_   _(_) ___   |_   _|_,_  ___   |_   _|__   ___
      | | | |/ __|    | |/ _  |/ __|    | |/ _ \ / _ \ 
      | | | | (__     | | (_| | (__     | | (_) |  __/
      |_| |_|\___|    |_|\__,_|\___|    |_|\___/ \___|
    """
    print(obrazek)
    print("Vitam te ve hre piskvorky, bacha neni to jednoducha hra jak se muze zdat")
    print()

def tah_hrace(velikost_pole,hraci_pole,obtiznost,cheaty):
    if cheaty == "ano":
        nejlepsi_pozicka = vyber_nejlepsi_tah(hraci_pole,0, float('-inf'), float('inf'), True, "O",cheaty)
        print("Nejlepsi policko bude",nejlepsi_pozicka) # printujeme nejlepsi pozici kam dat symbol
    policko_hrace = int(input(f"Napis na jake policko chces napsat symbol X, od 1 az {velikost_pole**2}: "))
    print()
    if policko_hrace > velikost_pole**2 or policko_hrace <= 0 or hraci_pole[(policko_hrace - 1) // velikost_pole][(policko_hrace - 1) % velikost_pole] != ".":
        print("Ty nezbedniku, zkus to znova") # kdyz hrac napise spatne cislo tak musi psat znova
        tah_hrace(velikost_pole,hraci_pole,obtiznost,cheaty)
    else:
        hraci_pole[(policko_hrace - 1) // velikost_pole][(policko_hrace - 1) % velikost_pole] = "X"
        print("Tvuj tah:") # kdyz napise spravny cislo tak symbol tam napiseme a vytiskneme
        printi(hraci_pole,velikost_pole)
        kontrola_vitezstvi(hraci_pole,velikost_pole,obtiznost,0,"X",cheaty)

def tah_pocitace(hraci_pole,velikost_pole,obtiznost,cheaty):
    if obtiznost == 1: # kdyz obtiznost bude 1 tak generujeme pouze nahodna cisla
        nahodny_index = random.randint(1, velikost_pole**2)
        if hraci_pole[(nahodny_index - 1) // velikost_pole][(nahodny_index - 1) % velikost_pole] != ".":
            tah_pocitace(hraci_pole,velikost_pole,obtiznost,cheaty)
        if hraci_pole[(nahodny_index - 1) // velikost_pole][(nahodny_index - 1) % velikost_pole] == ".":
            hraci_pole[(nahodny_index - 1) // velikost_pole][(nahodny_index - 1) % velikost_pole] = "O"
            
    if obtiznost == 2: # kdyz obtiznost bude 2 tak se strida generovani nahodnych cisel a minimax algoritmu
        global posledni_tah
        posledni_tah = "minimax"
        if posledni_tah == "minimax":
            nejlepsi_pozicka = vyber_nejlepsi_tah(hraci_pole,0, float('-inf'), float('inf'), True, "O",cheaty)
            hraci_pole[(nejlepsi_pozicka-1) // velikost_pole][(nejlepsi_pozicka-1) % velikost_pole] = "O"
            posledni_tah = "nahoda"
        elif posledni_tah == "nahoda":
            nahodny_index = random.randint(1, velikost_pole**2)
            if hraci_pole[(nahodny_index - 1) // velikost_pole][(nahodny_index - 1) % velikost_pole] != ".":
                tah_pocitace(hraci_pole,velikost_pole,obtiznost,cheaty)
            if hraci_pole[(nahodny_index - 1) // velikost_pole][(nahodny_index - 1) % velikost_pole] == ".":
                hraci_pole[(nahodny_index - 1) // velikost_pole][(nahodny_index - 1) % velikost_pole] = "O"
            posledni_tah = "minimax"
    
    if obtiznost == 3: # kdyz obtiznost je 3 tak pocitac pouziva jenom minimax algoritmus
        nejlepsi_pozicka = vyber_nejlepsi_tah(hraci_pole,0, float('-inf'), float('inf'), True, "O",cheaty)
        hraci_pole[(nejlepsi_pozicka-1) // velikost_pole][(nejlepsi_pozicka-1) % velikost_pole] = "O"
        
    if obtiznost == 4: # kdyz obtiznost je 4 tak pocitac pouziva dvakrat za sebou minimax algoritmus
        nejlepsi_pozicka = vyber_nejlepsi_tah(hraci_pole,0, float('-inf'), float('inf'), True, "O",cheaty)
        hraci_pole[(nejlepsi_pozicka-1) // velikost_pole][(nejlepsi_pozicka-1) % velikost_pole] = "O"
        nejlepsi_pozicka = vyber_nejlepsi_tah(hraci_pole,0, float('-inf'), float('inf'), True, "O",cheaty)
        hraci_pole[(nejlepsi_pozicka-1) // velikost_pole][(nejlepsi_pozicka-1) % velikost_pole] = "O"
           
    print("Pocitace tah:")
    printi(hraci_pole,velikost_pole)
    kontrola_vitezstvi(hraci_pole,velikost_pole,obtiznost,0,"O",cheaty) # kontrolujeme konec hry
    tah_hrace(velikost_pole,hraci_pole,obtiznost,cheaty)
 
def kontrola_vitezstvi(hraci_pole,velikost_pole,obtiznost,delka_vyherni_kombinace,symbol,cheaty):
    delka_vyherni_kombinace = vyherni_kombinace(velikost_pole)
    if symbol == "X": # kdyz na tahu byl hrac, mam to jenom proto abych mohl printovat jiny text v zavislosti kdo a jak vyhral
        for radek in hraci_pole: # kontrolujeme radky
            for i in range(len(radek) - delka_vyherni_kombinace + 1):
                vitezstvi = True
                for j in range(delka_vyherni_kombinace):
                    if radek[i + j] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_hrac(obtiznost)
                    hrat_znova()
        for sloupec in range(velikost_pole): # kontrolujeme sloupce
            for i in range(len(hraci_pole) - delka_vyherni_kombinace + 1):
                vitezstvi = True
                for j in range(delka_vyherni_kombinace):
                    if hraci_pole[i + j][sloupec] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_hrac(obtiznost)
                    hrat_znova()
        for i in range(len(hraci_pole) - delka_vyherni_kombinace + 1):
            for j in range(velikost_pole - delka_vyherni_kombinace + 1):
                vitezstvi = True # Diagonala zleva nahoru doprava dolu
                for k in range(delka_vyherni_kombinace):
                    if hraci_pole[i + k][j + k] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_hrac(obtiznost)
                    hrat_znova()
                vitezstvi = True # Diagonala zleva dolu doprava nahoru
                for k in range(delka_vyherni_kombinace):
                    if hraci_pole[i + k][j + delka_vyherni_kombinace - 1 - k] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_hrac(obtiznost)
                    hrat_znova()        
        vsechny_bez_tecky = 0 # kotrolujeme remizu az na konec vzdy
        for i in hraci_pole:
            if "." in i:
                vsechny_bez_tecky = False
                break
            else:
                vsechny_bez_tecky = True
        if vsechny_bez_tecky:
            printeni_remizy(obtiznost)
            hrat_znova()
        tah_pocitace(hraci_pole,velikost_pole,obtiznost,cheaty) # hraje hrac
        
    if symbol == "O": # tady uplne to same pro pocitac
        for radek in hraci_pole:
            for i in range(len(radek) - delka_vyherni_kombinace + 1):
                vitezstvi = True
                for j in range(delka_vyherni_kombinace):
                    if radek[i + j] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_pocitac(obtiznost)
                    hrat_znova()
        for sloupec in range(velikost_pole):
            for i in range(len(hraci_pole) - delka_vyherni_kombinace + 1):
                vitezstvi = True
                for j in range(delka_vyherni_kombinace):
                    if hraci_pole[i + j][sloupec] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_pocitac(obtiznost)
                    hrat_znova()
        for i in range(len(hraci_pole) - delka_vyherni_kombinace + 1):
            for j in range(velikost_pole - delka_vyherni_kombinace + 1):
                # Diagonala zleva nahoru doprava dolu
                vitezstvi = True
                for k in range(delka_vyherni_kombinace):
                    if hraci_pole[i + k][j + k] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_pocitac(obtiznost)
                    hrat_znova()
                # Diagonala zleva dolu doprava nahoru
                vitezstvi = True
                for k in range(delka_vyherni_kombinace):
                    if hraci_pole[i + k][j + delka_vyherni_kombinace - 1 - k] != symbol:
                        vitezstvi = False
                        break
                if vitezstvi:
                    printeni_viteztvi_pocitac(obtiznost)
                    hrat_znova()
        vsechny_bez_tecky = 0
        for i in hraci_pole:
            if "." in i:
                vsechny_bez_tecky = False
                break
            else:
                vsechny_bez_tecky = True
        if vsechny_bez_tecky:
            printeni_remizy(obtiznost)
            hrat_znova()
        tah_hrace(velikost_pole,hraci_pole,obtiznost,cheaty)
        
def vyherni_kombinace(velikost_pole):
    if velikost_pole == 3: # zjistujeme kolik symbolu je potreba pro vyhru
        return 3
    if velikost_pole == 4 or velikost_pole == 5:
        return 4
    if velikost_pole == 6 or velikost_pole == 7 or velikost_pole == 8:
        return 5
    if velikost_pole == 9 or velikost_pole == 10:
        return 6  

def printeni_viteztvi_hrac(obtiznost):
    if obtiznost == 1: # printujeme kdyz vyhral hrac
        print("Vyhral si!, zkus si zvolit tezsi obtiznost a porazim te")
    if obtiznost == 2:
        print("Vyhral si!, okey jde ti to")
    if obtiznost == 3:
        print("Vyhral si!, tak to jses ultimatni god ze si me porazil na levelu impossible!")
    if obtiznost == 4:
        print("Vyhral si!, tak to nejsem uz god, si dnes vypotreboval stesti na celej zivot")

def printeni_viteztvi_pocitac(obtiznost):
    if obtiznost == 1: # printujeme kdyz vyhral pocitac
        print("Prohral si!, tak to jses solidni bot")
    if obtiznost == 2:
        print("Prohral si!, musis se vice snazit hele")
    if obtiznost == 3:
        print("Prohral si!, nic si z toho nedelej, trosku cheatuju")
    if obtiznost == 4:
        print("Prohral si!, v klidu, muzu delat 2 tahy za sebou")

def printeni_remizy(obtiznost):
    if obtiznost == 1: # printujeme kdyz byla remiza
        print("Remiza!, haha ani nad nahodnymi cisly si nevyhral")
    if obtiznost == 2:
        print("Remiza!, hele tak neprohral si coz je solidni uspech")
    if obtiznost == 3:
        print("Remiza!, tak to jses dobrej ze si na level impossible neprohral, necheatujes trosku?")
    if obtiznost == 4:
        print("Remiza!, njn to se mi to hraje kdyz mam 2 tahy haha")
    
def printi(hraci_pole,velikost_pole):
    for i in range(velikost_pole): # printujeme hraci pole hezky radek na radku
        print(*hraci_pole[i])
    print()

def nova_hra(hraci_pole,velikost_pole,obtiznost):
    uvodni_obrazek() # printujeme tic tac toe
    velikost_pole = int((input("Napis jedno cislo jakou velikost bude mit hraci pole, napr. 3 a pouze cisla 3 az 10: ")))
    if velikost_pole > 10 or velikost_pole < 3:
        print("Spatne cislo velikosti pole, co to jako zkousis za tricky na me?, zkus to znova")
        nova_hra(0,0,0)
    obtiznost = int(input("Napis obtiznost, lehka=1 nebo stredni=2 nebo impossible=3 nebo god=4: "))
    if obtiznost == 1 or obtiznost == 2 or obtiznost == 3 or obtiznost == 4:
        pass
    else:
        print("Spatne cislo obtiznosti, co to jako zkousis za tricky na me?, zkus to znova")
        nova_hra(0,0,0)
    hraci_pole = [["."]*velikost_pole for _ in range(velikost_pole)]
    kombinace = vyherni_kombinace(velikost_pole)
    print()
    print("Na vyherni kombinaci (radky, sloupce, diagonaly) je potreba mit",kombinace,"symbolu")
    print()
    print("startovni pole: ")
    printi(hraci_pole,velikost_pole)
    cheaty = input("Vidim ze se docela bojis, chces zapnout cheaty? ano/ne: ")
    if cheaty == "ano": # zapinamne cheaty
        print("Cheaty se zapinaji, pred kazdym tahem ti napisu jake policko mas hrat tak aby si nikdy neprohral")
        print()
    if cheaty == "ne":
        print("Si veris tak gl")
        print()
    if cheaty != "ano" and cheaty != "ne":
        print("Nauc se psat uz pls, znova to udelej")
        nova_hra(0,0,0)
    tah_hrace(velikost_pole,hraci_pole,obtiznost,cheaty)
  
def hrat_znova():
    vysledek = input("Chces hrat znova? ano/ne: ") # jakmile hra skonci tak muzeme hrat znova
    if vysledek == "ano":
        nova_hra(0,0,0)
    if vysledek == "ne":
        print("Tak nekdy priste")
        print()
        sys.exit()
    else:
        print("Spatna odpoved, napis to znova")
        hrat_znova()

def vyber_nejlepsi_tah(hraci_pole,hloubka,alpha,beta,maximizing_player,symbol,cheaty):
    nejvyssi_hodnota = float('-inf')
    nejlepsi_tah = None

    for sloupec in range(len(hraci_pole)):
        for radek in range(len(hraci_pole)):
            if hraci_pole[radek][sloupec] == ".":
                hraci_pole[radek][sloupec] = symbol
                hodnota = minimax(hraci_pole,hloubka,alpha,beta,not maximizing_player,symbol,cheaty)
                hraci_pole[radek][sloupec] = "."  # Vraceni puvodniho stavu pole

                if hodnota > nejvyssi_hodnota:
                    nejvyssi_hodnota = hodnota
                    nejlepsi_tah = radek * len(hraci_pole) + sloupec + 1 # prevedeme z (radek,sloupec) na jedno cislo pozice

    return nejlepsi_tah

def ohodnoceni(hraci_pole,symbol):
    vitezne_pozice = [] # 2D seznam do ktereho ukladame mozne vitezne tahy
    for radek in hraci_pole: # Kontrola radku
        for i in range(len(radek) - vyherni_kombinace(len(radek)) + 1):
            vitezne_pozice.append(radek[i:i + vyherni_kombinace(len(radek))])
    # Kontrola sloupcu
    for sloupec in range(len(hraci_pole[0])):
        for i in range(len(hraci_pole) - vyherni_kombinace(len(hraci_pole)) + 1):
            vitezne_pozice.append([hraci_pole[j][sloupec] for j in range(i, i + vyherni_kombinace(len(hraci_pole)))])
    # Kontrola diagoaál zleva nahoru doprava dolu
    for i in range(len(hraci_pole) - vyherni_kombinace(len(hraci_pole)) + 1):
        for j in range(len(hraci_pole[0]) - vyherni_kombinace(len(hraci_pole[0])) + 1):
            vitezne_pozice.append([hraci_pole[i + k][j + k] for k in range(vyherni_kombinace(len(hraci_pole)))])
    # Kontrola diagonal zleva dolu doprava nahoru
    for i in range(len(hraci_pole) - vyherni_kombinace(len(hraci_pole)) + 1):
        for j in range(len(hraci_pole[0]) - 1, vyherni_kombinace(len(hraci_pole[0])) - 2, -1):
            vitezne_pozice.append([hraci_pole[i + k][j - k] for k in range(vyherni_kombinace(len(hraci_pole)))])
    ohodnoceni_hry = 0

    for pozice in vitezne_pozice:
        obsazeno_hracsymbolem = pozice.count(symbol)
        if symbol == "X":
            protihraci_symbol = "O"
        else:
            protihraci_symbol = "X"
        obsazeno_protihracsymbolem = pozice.count(protihraci_symbol)

        if obsazeno_hracsymbolem == vyherni_kombinace(len(pozice)):
            ohodnoceni_hry += 100
        elif obsazeno_hracsymbolem == vyherni_kombinace(len(pozice))-1 and obsazeno_protihracsymbolem == 0:
            ohodnoceni_hry += 10
        elif obsazeno_hracsymbolem == 1 and obsazeno_protihracsymbolem == 0:
            ohodnoceni_hry += 1
        elif obsazeno_protihracsymbolem == vyherni_kombinace(len(pozice)):
            ohodnoceni_hry -= 100
        elif obsazeno_protihracsymbolem == vyherni_kombinace(len(pozice))-1 and obsazeno_hracsymbolem == 0:
            ohodnoceni_hry -= 10
        elif obsazeno_protihracsymbolem == 1 and obsazeno_hracsymbolem == 0:
            ohodnoceni_hry -= 1

    return ohodnoceni_hry

def minimax(hraci_pole,hloubka,alpha,beta,maximizing_player,symbol,cheaty):
    ohodnoceni_hry = ohodnoceni(hraci_pole,symbol)

    if ohodnoceni_hry != 0:  # Kontrola koncovych stavu
        return ohodnoceni_hry

    if maximizing_player:
        nejvyssi_hodnota = float('-inf')  # Nejvyssi hodnota pro hrace "O"
        for radek in range(len(hraci_pole)):
            for sloupec in range(len(hraci_pole)):
                if hraci_pole[radek][sloupec] == ".":
                    hraci_pole[radek][sloupec] = "O"
                    hodnota = minimax(hraci_pole,hloubka-1,alpha,beta,False,symbol,cheaty)
                    hraci_pole[radek][sloupec] = "."  # Vraceni puvodniho stavu pole
                    nejvyssi_hodnota = max(nejvyssi_hodnota,hodnota)
                    alpha = max(alpha,hodnota)
                    if beta <= alpha:
                        break  # Oriznuti vetve
        return nejvyssi_hodnota
    else:
        nejnizsi_hodnota = float('inf')  # Nejnizsi hodnota pro hrace "X"
        for radek in range(len(hraci_pole)):
            for sloupec in range(len(hraci_pole)):
                if hraci_pole[radek][sloupec] == ".":
                    hraci_pole[radek][sloupec] = "X"
                    hodnota = minimax(hraci_pole,hloubka-1,alpha,beta,True,symbol,cheaty)
                    hraci_pole[radek][sloupec] = "."  # Vraceni puvodniho stavu pole
                    nejnizsi_hodnota = min(nejnizsi_hodnota,hodnota)
                    beta = min(beta,hodnota)
                    if beta <= alpha:
                        break  # Oriznuti vetve
        return nejnizsi_hodnota

nova_hra(0,0,0)



