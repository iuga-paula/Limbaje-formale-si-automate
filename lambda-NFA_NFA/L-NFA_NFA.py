

def funct_lambda_inchidere(stari):
    global li, D
    stari_noi = set(stari)
    for i in stari:
        for j in range(len(D['$'])):
            if i == D['$'][j][0]:  # vedem in ce stare putem ajunge cu lambda
                stari_noi.add(D['$'][j][1])  # adaugam in multime starea la care putem ajunge cu lambda\

    return stari_noi


def apeleaza_funct_lambda_inchidere(stari):
    while stari != (stari | funct_lambda_inchidere(stari)):
        stari = (stari | funct_lambda_inchidere(stari))
    return stari


def conversie_L_NFA_NFA(D, F, n, alfabet, stari_finale_noi):
    # pasul 1: lambda inchidere:
    li = {}  # pt fiecare nod cu lambda unde pot merge
    for i in range(n):
        li[i] = set([i])

    # print(li)
    # for i in range(n):
    # li[i] = apeleaza_funct_lambda_inchidere(li[i])
    # print(li)

    # pasul 2 +3 : Calcularea functiei de tranzitie + stari finale :
    f = set(F)
    Dnou = {}
    for litera in alfabet:
        for i in range(n):
            li[i] = apeleaza_funct_lambda_inchidere(li[i])  # l-closure
        # print(li)
        for stare in li.keys():
            multime_noua = set([])
            for i in li[stare]:
                for j in range(len(D[litera])):
                    if D[litera][j][0] == i:
                        multime_noua.add(D[litera][j][1])  # alfa
            li[stare] = multime_noua
        # print(li)
        for i in range(n):
            li[i] = apeleaza_funct_lambda_inchidere(li[i])  # l-closure
        # print(li)
        Dnou[litera] = []  # dictionar nou pt NFA
        for stare in li.keys():
            if len(li[stare] | f):  # vedem care sunt starile finale in noul automat
                stari_finale_noi.add(stare)
            for j in li[stare]:
                t = tuple((stare, j))
                Dnou[litera].append(t)

    print("automatul nou NFA dupa calcularea functiei de tranzitie:")
    print(Dnou)
    # print(stari_finale)
    # pas 4: elimiarea starilor redundante:
    # Doua stari sunt identice daca au tranzitiile sunt identice pentru orice caracter din alfabet si daca amandoua sunt sau nu sunt stari ﬁnal
    Dstari = {}
    stari_identice = set([])
    matstari = []
    for stare in range(n):
        # cream o lista de liste pt ficare stare
        # adica in lista mare exista o lista cu tranzitiile pt fiecare litera
        Dstari[stare] = []
        for litera in alfabet:
            listastarilitera = []
            for i in range(len(Dnou[litera])):
                if Dnou[litera][i][0] == stare:
                    listastarilitera.append(Dnou[litera][i][1])
            Dstari[stare].append(listastarilitera)

    # print(Dstari)
    for stare1 in Dstari.keys():
        for stare2 in Dstari.keys():
            if Dstari[stare1] == Dstari[stare2] and stare1 != stare2:
                stari_identice.add(stare2)

    print("starile indentice sunt :", stari_identice)
    stari_identice = list(stari_identice)
    for stare in stari_identice[1:]:
        del Dstari[stare]

    NFA = {}
    for litera in alfabet:
        NFA[litera] = []
        for i in range(len(Dnou[litera])):
            if Dnou[litera][i][0] not in stari_identice[1:] and Dnou[litera][i][1] not in stari_identice[1:]:
                NFA[litera].append(Dnou[litera][i])

    print("noul NFA dupa eliminarea starilor identice este: ")
    print(NFA)
    stari_identice = set(stari_identice[1:])
    return NFA, stari_finale_noi, stari_identice


def creare_fisier_output(D, F, stari_finale_noi, n, alfabet, q0): #se creeaza fisier de output similar cu cel de input
    g = open("NFA", "w")
    NFA, stari_finale, stari_identice = conversie_L_NFA_NFA(D, F, n, alfabet, stari_finale_noi)
    stari = set([x for x in range(n)]) | stari_identice    #starile noi pt NFA
    g.write(str(len(stari)) + "\n") #nr de stari pt NFA

    for litera in alfabet:
        g.write(str(litera) + " ")  #afisare alfabetul care e la fel
    g.write("\n")

    g.write(str(q0) + "\n")  #starea initiala care ramane la fel
    for stare in stari_finale:
        g.write(str(stare) + " ")  #noile stari finale pt NFA
    g.write("\n")

    nr_tranzitii = 0
    for litera in NFA.keys():
        nr_tranzitii += len(NFA[litera])
    g.write(str(nr_tranzitii) + "\n")

    for litera in NFA.keys():
        for i in range(len(NFA[litera])):
            g.write(str(NFA[litera][i][0]) + " " + str(litera) + " " + str(NFA[litera][i][1]) + "\n")

    g.close()



f = open("lambda-NFA")
n = int(f.readline())  # numar stari
alfabet = f.readline()  #alfabetul
alfabet = alfabet.split()

D = {}  # dictionar in care cheile sunt literele din alfabet iar valorile sunt tiste de tupluri(x,y)
# cu semnificatia ca din (cu) litera (pe post de cheie) se poate ajunge din starea x in starea y

q0 = int(f.readline())  # stare initala
s = f.readline()
F = [int(x) for x in s.split()]  # lista de stari finale
l = int(f.readline())  # nr translatari
while l > 0:
    s = f.readline()
    s = s.split()  # stare 1 = s[0] , lit = s[1], stare 2 = s[2]
    if s[1] not in D.keys():
        D[s[1]] = []
        t = tuple((int(s[0]), int(s[2])))
        D[s[1]].append(t)
    else:
        t = tuple((int(s[0]), int(s[2])))
        D[s[1]].append(t)

    l -= 1
f.close()
for elem in alfabet:
    if elem not in D.keys():
        D[elem] = []

stari_finale_noi = set([])
print("lambda NFA inital:")
print(D)

#Dict, Stari,stari2 =  conversie_L_NFA_NFA(D, F, stari_finale_noi)
# print(Dict)
#print(Stari)
#print(stari2)
creare_fisier_output(D, F, stari_finale_noi, n, alfabet, q0)

