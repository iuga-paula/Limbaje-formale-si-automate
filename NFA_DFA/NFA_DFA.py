def conversie_NFA_DFA(D, n, alfabet, F, q0):
    # pasul 1: eliminarea nedeterminismului
    stari_comasate = []
    queue = [q0]
    vizitat = [0 for _ in range(n)]
    for stare in queue:
        for litera in alfabet:
            multime_stari = []
            if type(stare) != set:
                for i in range(len(D[litera])):
                    if D[litera][i][0] == stare:
                        multime_stari.append(D[litera][i][1])
            else:
                for elem in stare:
                    for i in range(len(D[litera])):
                        if D[litera][i][0] == elem:
                            multime_stari.append(D[litera][i][1])

            multime_stari = set(multime_stari)
            if len(multime_stari) > 1:

                if multime_stari not in queue:
                    queue.append(multime_stari)
                    stari_comasate.append(multime_stari)
            elif len(multime_stari) == 1:
                x = list(multime_stari)
                if x[0] not in queue:
                    queue.append(x[0])

    print("starile noului DFA: ")
    print(queue)
    # print("stari comasate:", stari_comasate)

    Dnou = {}
    for litera in alfabet:
        Dnou[litera] = []

    matrice = []
    for stare in queue:
        for litera in alfabet:
            multime_stari = []
            if stare in stari_comasate:
                poz = stari_comasate.index(stare)
                for elem in stari_comasate[poz]:
                    for j in range(len(D[litera])):
                        if D[litera][j][0] == elem:
                            multime_stari.append(D[litera][j][1])
                    if len(multime_stari) > 1:
                        multime_stari_noi = set(multime_stari)
                        if multime_stari_noi in queue:
                            t = tuple((stare, multime_stari_noi))
                            if t not in Dnou[litera]:
                                Dnou[litera].append(t)
                    else:
                        for elem1 in multime_stari:
                            t = tuple((stare, elem1))
                            if t not in Dnou[litera]:
                                Dnou[litera].append(t)
            else:
                for j in range(len(D[litera])):
                    if D[litera][j][0] == stare:
                        multime_stari.append(D[litera][j][1])

                multime_stari_noi = set(multime_stari)
                if len(multime_stari) > 1:
                    if multime_stari_noi in queue:
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
                    t = tuple((stare, multime_stari[0]))
                    if t not in Dnou[litera]:
                        Dnou[litera].append(t)

    print("DFA-ul inainte de renumerotarea starilor:")
    print(Dnou)

    # pasul 2: calcularea starilor finale
    stari_finale = []
    for stare in queue:
        if type(stare) == set:  # daca este stare compusa vad daca in ea se afla vreo stare finala

            if len(stare.intersection(set(F))):
                stari_finale.append(stare)

        elif stare in F:
            stari_finale.append(stare)

    print("starile finale ale DFA-ului sunt:")
    print(stari_finale)

    # pasul 3: redenumirea starilor
    n_nou = n  # numarul nou de stari
    stari_redenumite = []  # starile DFA-ului redenumite
    for stare in queue:
        if type(stare) == set:
            stari_redenumite.append(n_nou)
            n_nou += 1
        else:
            stari_redenumite.append(stare)
    n_nou -= 1

    for i in range(len(stari_finale)):  # daca este necesar redenumim si starile finale
        if type(stari_finale[i]) == set:
            poz = queue.index(stari_finale[i])
            stari_finale[i] = stari_redenumite[poz]

    print("starile redenumite ale DFA-ului:")
    print(stari_redenumite)
    print("starile finale redenumite ale DFA-ului:")
    print(stari_finale)

    for litera in alfabet:
        for i in range(len(Dnou[litera])):
            if type(Dnou[litera][i][0]) == set:  # vedem daca e stare compusa in dictionar si o renumerotam
                poz = queue.index(Dnou[litera][i][0])
                t = tuple((stari_redenumite[poz], Dnou[litera][i][1]))
                Dnou[litera][i] = t
            if type(Dnou[litera][i][1]) == set:  # vedem daca e stare compusa in dictionar si o renumerotam
                poz = queue.index(Dnou[litera][i][1])
                t = tuple((Dnou[litera][i][0], stari_redenumite[poz]))
                Dnou[litera][i] = t

    print("DFA-ul dupa redenumirea starilor este: ")
    print(Dnou)
    return n_nou, stari_finale, Dnou


def creare_fisier_output(D, n, alfabet, F, q0):
    nr_stari, stari_finale, DFA = conversie_NFA_DFA(D, n, alfabet, F, q0)
    g = open("DFA", "w")
    g.write(str(nr_stari) + "\n") #numarul de stari

    for litera in alfabet:
        g.write(str(litera) + " ")  #afisare alfabetul care e la fel
    g.write("\n")

    g.write(str(q0) + "\n")  #starea initiala care ramane la fel

    for stare in stari_finale:
        g.write(str(stare) + " ")  #noile stari finale pt NFA
    g.write("\n")

    nr_tranzitii = 0

    for litera in DFA.keys():
        nr_tranzitii += len(DFA[litera])
    g.write(str(nr_tranzitii) + "\n")

    for litera in DFA.keys():
        for i in range(len(DFA[litera])):
            g.write(str(DFA[litera][i][0]) + " " + str(litera) + " " + str(DFA[litera][i][1]) + "\n")

    g.close()



f = open("data2.in")
n = int(f.readline())   #numar stari
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

for elem in alfabet:
    if elem not in D.keys():
        D[elem] = []

print("NFA inital:")
print(D)
creare_fisier_output(D, n, alfabet, F, q0)
