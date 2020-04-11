def redenumire_stari(Dnou, n, stari_finale, stare_initiala, lista_stari_DFA_min):
    n_nou = n  # numarul nou de stari
    stari_redenumite = []  # starile DFA-ului redenumite
    for stare in lista_stari_DFA_min:
        if type(stare) == set:
            stari_redenumite.append(n_nou)
            n_nou += 1
        else:
            stari_redenumite.append(stare)
    n_nou -= 1

    if type(stare_initiala) == set:
        poz = lista_stari_DFA_min.index(stare_initiala)
        stare_initiala = stari_redenumite[poz]


    for i in range(len(stari_finale)):  # daca este necesar redenumim si starile finale
        if type(stari_finale[i]) == set:
            poz = lista_stari_DFA_min.index(stari_finale[i])
            stari_finale[i] = stari_redenumite[poz]


    print("starile redenumite ale DFAmin:")
    print(stari_redenumite)
    print("starile finale redenumite ale DFAmin:")
    print(stari_finale)
    print("starea initiala redenumita a DFAmin este:")
    print(stare_initiala)

    for litera in alfabet:
        for i in range(len(Dnou[litera])):
            if type(Dnou[litera][i][0]) == set:  # vedem daca e stare compusa in dictionar si o renumerotam
                poz = lista_stari_DFA_min.index(Dnou[litera][i][0])
                t = tuple((stari_redenumite[poz], Dnou[litera][i][1]))
                Dnou[litera][i] = t
            if type(Dnou[litera][i][1]) == set:  # vedem daca e stare compusa in dictionar si o renumerotam
                poz = lista_stari_DFA_min.index(Dnou[litera][i][1])
                t = tuple((Dnou[litera][i][0], stari_redenumite[poz]))
                Dnou[litera][i] = t

    print("DFA-ul dupa redenumirea starilor este: ")
    print(Dnou)
    n_nou = len(stari_redenumite)
    return n_nou, stari_redenumite, stari_finale, stare_initiala, Dnou


def drumuri(k):
    global x, vizitat, Dnou, n_nou, lista_stari_DFA_min,stari_finale,ma
    for stare in lista_stari_DFA_min:
        if vizitat[ma-stare] == 0 and stare != x[0]:
            x[k] = stare
            vizitat[ma-stare] = 1
            for litera in alfabet:
                for i in range(len(Dnou[litera])):
                        if Dnou[litera][i][0] == x[k-1] and Dnou[litera][i][1] == x[k]:
                            #if k < n_nou:
                            if x[k] in stari_finale:
                                return True
                            else:
                                drumuri(k+1)
            vizitat[ma-stare] = 0
    return False


def DFS(stare):
    global vizitat, lista_stari_DFA_min, DFA
    vizitat[stare] = 1
    for litera in alfabet:
        for i in range(len(DFA[litera])):
            if DFA[litera][i][0] == stare and vizitat[DFA[litera][i][1]] == 0:
                DFS(DFA[litera][i][1])


def creare_fisier_output(D, n, alfabet, stari_finale, stare_initiala):

    g = open("DFAmin", "w")
    g.write(str(n) + "\n") #numarul de stari

    for litera in alfabet:
        g.write(str(litera) + " ")  #afisare alfabetul care e la fel
    g.write("\n")

    g.write(str(stare_initiala) + "\n")  #starea initiala

    for stare in stari_finale:
        g.write(str(stare) + " ")  #noile stari finale pt NFA
    g.write("\n")

    nr_tranzitii = 0

    for litera in D.keys():
        nr_tranzitii += len(D[litera])
    g.write(str(nr_tranzitii) + "\n")  #numar tranzitii

    for litera in D.keys():
        for i in range(len(D[litera])):
            g.write(str(D[litera][i][0]) + " " + str(litera) + " " + str(D[litera][i][1]) + "\n")

    g.close()





f = open("data3.in")
n = int(f.readline())  # numar stari
alfabet = f.readline()  # alfabetul
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

for elem in alfabet:
    if elem not in D.keys():
        D[elem] = []

print("DFA inital:")
print(D)

# pasul 1: 1.1Determinarea starilor echivalente
matrice_echivalenta = [[True for _ in range(n)] for _ in range(n)]

#1.2 Marcam cu FALSE toate perechile (q,r), unde q stare ﬁnala si r stare neﬁnala:
for i in range(n):
    for j in range(i):
        if (i in F and j not in F) or (i not in F and j in F):  # daca una este stare finala si cealalta nu
            matrice_echivalenta[i][j] = False
            matrice_echivalenta[j][i] = False

#1.3 Marcam cu FALSE toate perechile (q,r) pentru care (δ(q,α),δ(r,α)) sunt marcate cu FALSE, ∀α ∈ Σ si repetam 1.3 pana cand nu mai apar modificari
modificare = True
while modificare:  # cat timp mai apar modificari
    modificare = False
    for i in range(n):
        for j in range(i):
            for litera in alfabet:
                stare1 = stare2 = -1
                for k in range(len(D[litera])):
                    if D[litera][k][0] == i:
                        stare1 = D[litera][k][1]
                        for l in range(len(D[litera])):
                            if D[litera][l][0] == j and stare1 != -1:
                                stare2 = D[litera][l][1]
                                if stare1 > stare2 and matrice_echivalenta[stare1][stare2] is False and matrice_echivalenta[i][j] is True:
                                    matrice_echivalenta[i][j] = False
                                    matrice_echivalenta[j][i] = False
                                    modificare = True


print("matricea echivalenta dupa modificari : ")
for i in range(n):
    for j in range(i):
        print(matrice_echivalenta[i][j], end=" ")
    print()

#Pasul 2: 2.1Gruparea starilor echivalente
lista_stari_echivalente = []
for i in range(n):
    stari_echivalente = set([])
    for j in range(n):
        if matrice_echivalenta[i] == matrice_echivalenta[j] and i != j:
            stari_echivalente.update([i, j])
    if stari_echivalente not in lista_stari_echivalente and len(stari_echivalente) > 1:
        lista_stari_echivalente.append(stari_echivalente)

print("lista starilor echivalente grupate:")
print(lista_stari_echivalente)

#2.2  calcularea functiei de tranzitie δ∗
stari = [x for x in range(n)]
lista_stari_DFA_min = []
for stare1 in stari:
    ok = False
    for stare_compusa in lista_stari_echivalente:
        if stare1 in stare_compusa:
            ok = True
    if ok is False:
        lista_stari_DFA_min.append(stare1) #adaugam starile simple
lista_stari_DFA_min.extend(lista_stari_echivalente) #adaugam starile compuse
print("starile noului DFA min sunt:")
print(lista_stari_DFA_min)

Dnou = {}
for litera in alfabet:
    Dnou[litera] = []

for stare in lista_stari_DFA_min:
    for litera in alfabet:
        multime_stari = []
        if stare in lista_stari_echivalente:
            poz = lista_stari_echivalente.index(stare)
            for elem in lista_stari_echivalente[poz]:
                for j in range(len(D[litera])):
                    if D[litera][j][0] == elem:
                        multime_stari.append(D[litera][j][1])
                if len(multime_stari) > 1:
                    multime_stari_noi = set(multime_stari)
                    if multime_stari_noi in lista_stari_DFA_min:
                        t = tuple((stare, multime_stari_noi))
                        if t not in Dnou[litera]:
                            Dnou[litera].append(t)
                else:
                    for stare_compusa in lista_stari_echivalente:
                        if multime_stari[0] in stare_compusa:
                            t = tuple((stare, stare_compusa))
                            if t not in Dnou[litera]:
                                Dnou[litera].append(t)
                            break
                    else:
                        if multime_stari[0] in lista_stari_DFA_min:
                            t = tuple((stare, multime_stari[0]))
                            if t not in Dnou[litera]:
                                Dnou[litera].append(t)
        else:
            for j in range(len(D[litera])):
                if D[litera][j][0] == stare:
                    multime_stari.append(D[litera][j][1])

            multime_stari_noi = set(multime_stari)
            if len(multime_stari) > 1:
                if multime_stari_noi in lista_stari_DFA_min:
                    t = tuple((stare, multime_stari_noi))
                    if t not in Dnou[litera]:
                        Dnou[litera].append(t)

                else:
                    for elem in multime_stari:
                        t = tuple((stare, elem))
                        if t not in Dnou[litera]:
                            Dnou[litera].append(t)

            elif len(multime_stari) == 1:
                multime_stari = list(multime_stari)
                for stare_compusa in lista_stari_echivalente:
                    if multime_stari[0] in stare_compusa:
                        t = tuple((stare, stare_compusa))
                        if t not in Dnou[litera]:
                            Dnou[litera].append(t)
                        break
                else:
                    if multime_stari[0] in lista_stari_DFA_min:
                        t = tuple((stare, multime_stari[0]))
                        if t not in Dnou[litera]:
                            Dnou[litera].append(t)
print("Noul DFA_min cu starile echivalent fara numerotare:")
print(Dnou)

#pasul 3: Calcularea starilor finale si initiale
stare_initiala = q0
for stare in lista_stari_DFA_min:
    if (type(stare) == set and q0 in stare) or (q0 == stare and type(stare) != set):
        stare_initiala = stare
        break
print("starea initala a DFAmin este: ")
print(stare_initiala)

stari_finale = []
F = set(F)

for stare in lista_stari_DFA_min:
    if type(stare) == set and stare.issubset(F):
        stari_finale.append(stare)

print("starile finale ale DFAmin sunt: ")
print(stari_finale)

#pasul 4: Eliminarea starilor dead-end
#intai renumerotam starile
n_nou, lista_stari_DFA_min, stari_finale, stare_initiala, Dnou = redenumire_stari(Dnou, n, stari_finale, stare_initiala, lista_stari_DFA_min)
ma = max(lista_stari_DFA_min)
dead_end = []
for stare in lista_stari_DFA_min:
    if stare not in stari_finale:
        x = [0 for _ in range(n_nou)]
        vizitat = [0 for _ in range(n_nou)]
        x[0] = stare
        vizitat[ma - stare] = 1
        if drumuri(1) is False: #cautam starile dead-end
            dead_end.append(stare)
print("starile dead-end sunt:")
print(dead_end)


DFA = {} #eliminam starile dead-end
n_nou = n_nou - len(dead_end)
for stare in dead_end:
    lista_stari_DFA_min.remove(stare)
for litera in alfabet:
    DFA[litera] = []
    for i in range(len(Dnou[litera])):
        if Dnou[litera][i][0] not in dead_end and Dnou[litera][i][1] not in dead_end:
            DFA[litera].append(Dnou[litera][i])

print("noul DFA dupa eliminarea starilor dead-end este: ")
print(DFA)

#pasul 5:eliminarea starilor neaccesibile:
stari_neaccesibile = []
vizitat = [0 for _ in range(max(lista_stari_DFA_min)+1)]
DFS(stare_initiala)
for i in range(min(lista_stari_DFA_min), len(vizitat)):
    if vizitat[i] == 0 and i in lista_stari_DFA_min:
        stari_neaccesibile.append(i)

print("starile neaccesibile sunt:")
print(stari_neaccesibile)

DFAmin = {} #eliminarea stari neaccesibile
n_nou = n_nou - len(stari_neaccesibile)
for stare in stari_neaccesibile:
    lista_stari_DFA_min.remove(stare)
for litera in alfabet:
    DFAmin[litera] = []
    for i in range(len(DFA[litera])):
        if DFA[litera][i][0] not in stari_neaccesibile and DFA[litera][i][1] not in stari_neaccesibile:
            DFAmin[litera].append(DFA[litera][i])

print("DFAmin final este:")
print(DFAmin)

creare_fisier_output(DFAmin, n_nou, alfabet, stari_finale, stare_initiala)





