def funct_lambda(stari):
    global D
    stari_noi =  set([])

    for stare in stari:
        for j in range(len(D['$'])):

            if stare == D['$'][j][0]:  # vedem in ce stare putem ajunge cu lambda
                stari_noi.add(D['$'][j][1])  # adaugam in multime starea la care putem ajunge cu lambda\

    return stari_noi


def apeleaza_funct_lambda(stari):
    while stari != (stari | funct_lambda(stari)):
        stari = (stari | funct_lambda(stari))

    return  stari




def eval(cuvant, stare_initiala):
    global F, D;
    multime_stari = apeleaza_funct_lambda((set([stare_initiala])))
    F = set(F)

    for i in cuvant:  # pt fiecare litera a cuvantului
        multime_stari_noi = set()
        for stare in multime_stari:
            if i in D.keys():
                for k in range(len(D[i])):
                    if D[i][k][0] == stare:
                         multime_stari_noi.add(D[i][k][1])

        multime_stari = apeleaza_funct_lambda(multime_stari_noi)

    if len(multime_stari & F) != 0:
        return True
    return False


f = open("D:\documente\LFA\lambda-NFA\data2.in")
n = int(f.readline())  # numar stari
alfabet = f.readline()
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

cuv = []  # lista de cuvinte, fiecare urmeaza a fi testat daca este acceptat de DFA sau nu
s = f.readline()
while s != "":
    s = s.strip()
    cuv.append(s)
    s = f.readline()

f.close()

#print(D)
#print(cuv)

for elem in cuv:
    if eval(elem, q0):
        print("cuvantul " + elem + " este acceptat de lambda-NFA")
    else:
        print("cuvantul " + elem + " NU este acceptat de lambda-NFA")


#print(apeleaza_funct_lambda(set([q0])))
