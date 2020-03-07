def evaluate(cuvant, stare_initiala):
    global F, D
    F = set(F)  #multime stari finale

    lista_aux = []
    lista_aux.append(stare_initiala)
    multime_stari = set(lista_aux)  #creez o multime (un set) pt a retine fara duplicate starile curente
    cuv_nou = ""

    for stare in multime_stari:  #pt fiecare stare
        lista_noua = []

        flag = False   #pt a verifica daca cuvantul pe care il formam nu s-a blocat
        for j in range(len(D['$'])):

            if stare == D['$'][j][0]:    #vedem in ce stare putem ajunge cu lambda
                lista_noua.append(D['$'][j][1])   #adaugam in multime starea la care putem ajunge cu lambda
                flag = True
        for k in range(len(cuvant)): #vedem in ce stare putem ajunge cu vreo litera din cuvant
            flag_litera = False
            if cuvant[k] in D.keys():
                for i in range(len(D[cuvant[k]])):
                    if stare == D[cuvant[k]][i][0]:
                        lista_noua.append(D[cuvant[k]][i][0]) #adaugam in multime starea la care putem ajunge cu litera din cuvant
                        flag_litera = True
                        flag = True
            if flag_litera: #daca am gasit o noua stare la care putem ajunge cu litera din cuvant dintr-o stare a multimii curente atunci
                cuv_nou += cuvant[k]  #o adaugam la cuvantul nou

            if cuv_nou == cuvant and len(multime_stari & F) != 0: #daca am obtinut cuv cerut iar multimea de stari intersectata cu F e diferita de multimea vida
                return True
            if cuv_nou == cuvant and len(multime_stari & F) == 0 and flag is not True:
                print("1")
                return False

            if flag is False and cuv_nou != cuvant:
                print("2")
                return False

        multime_stari = set(lista_noua)     #noile stari din care putem pleca




    #print(cuv_nou)
    #return True




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
    if evaluate(elem,q0):
        print("cuvantul " + elem + " este acceptat de lambda-NFA")
    else:
        print("cuvantul " + elem + " NU este acceptat de lambda-NFA")