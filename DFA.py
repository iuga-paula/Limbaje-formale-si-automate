def evaluate(cuvant, stare_curenta):
    global F, D
    for i in range(len(cuvant)):

        flag = 0
        if cuvant[i] in D.keys():

            for j in range(len(D[cuvant[i]])):
                if D[cuvant[i]][j][0] == stare_curenta:
                    stare_curenta = D[cuvant[i]][j][1]
                    flag = 1
                    break
            if flag == 0: #nu s-a gasit starea curenta in nicio tranzitie care contine litera a
                return False

        else:
            return False #litera din cuvantul introdus nu se afla in alfabet
    if stare_curenta not in F: #daca ultima stare la care s-a ajuns in cuv este stare finala
        return False
    return True





f = open("data.txt")
n = int(f.readline())
alfabet = f.readline()    #numar stari
alfabet = alfabet.split()

D = {}   #dictionar in care cheile sunt literele din alfabet iar valorile sunt tiste de tupluri(x,y)
         #cu semnificatia ca din (cu) litera (pe post de cheie) se poate ajunge din starea x in starea y

q0 = int(f.readline().strip()) #stare initala
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

#print(cuv)
#print(D)

for elem in cuv:
    if evaluate(elem, q0) is True:
        print("cuvantul " + elem + " este acceptat de DFA")
    else:
        print("cuvantul " + elem + " NU este acceptat de DFA")


