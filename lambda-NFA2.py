
def evaluate(cuvant, stare_initiala):
    global F, D
    F = set(F)  # multime stari finale

    lista_aux = []
    lista_aux.append(stare_initiala)
    multime_stari = set(lista_aux)  # creez o multime (un set) pt a retine fara duplicate starile curente

    cuv_nou = ""
    for i in range(len(cuvant)):  #pt fiecare litera a cuvantului
        flag = False
        flag_litera = False
        for j in range(len(D['$'])): #vedem in ce stare putem ajunge cu lambda
            if D['$'][j][0] in multime_stari:
                multime_stari.add(D['$'][j][1])   #adaugam in multime starea la care putem ajunge cu lambda
                flag = True
        if cuvant[i] in D.keys():
            for k in range(len(D[cuvant[i]])):
                if D[cuvant[i]][k][0] in multime_stari:
                    multime_stari.add(D[cuvant[i]][k][1])
                    flag = True
                    if flag_litera is not True:
                        cuv_nou += cuvant[i]
                        flag_litera = True

        else:
            print("1")
            return False  #litera din cuvant nu apartine alfabetului

        if flag is False and i != len(cuv) - 1 and len(multime_stari & F) == 0:
            print("2")
            return False

    if cuv_nou != cuvant:
        print(cuv_nou)
        print("3")
        return False
    elif cuv_nou == cuvant and len(multime_stari & F) == 0:
        print("4")
        return False

    return True







f = open("data.in")
n = int(f.readline())   #numar stari
alfabet = f.readline()
alfabet = alfabet.split()

D = {}   #dictionar in care cheile sunt literele din alfabet iar valorile sunt tiste de tupluri(x,y)
         #cu semnificatia ca din (cu) litera (pe post de cheie) se poate ajunge din starea x in starea y

q0 = int(f.readline()) #stare initala
s = f.readline()
F = [int(x) for x in s.split()] #lista de stari finale
l = int(f.readline())  #nr translatari
while l > 0:
    s = f.readline()
    s = s.split() #stare 1 = s[0] , lit = s[1], stare 2 = s[2]
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

cuv = []   #lista de cuvinte, fiecare urmeaza a fi testat daca este acceptat de DFA sau nu
s = f.readline()
while s != "":
    s = s.strip()
    cuv.append(s)
    s = f.readline()

f.close()

print(D)
print(cuv)

for elem in cuv:
    if evaluate(elem, q0):
        print("cuvantul " + elem + " este acceptat de lambda-NFA")
    else:
        print("cuvantul " + elem + " NU este acceptat de lambda-NFA")