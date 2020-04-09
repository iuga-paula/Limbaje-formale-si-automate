f = open("data3.in")
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

print("DFA inital:")
print(D)

#pasul 1: Determinarea starilor echivalente
matrice_echivalenta = [[True for _ in range(n)] for _ in range(n)]
print("matrice echivlenta initial: ")
for i in range(n):
    for j in range(i):
        print(matrice_echivalenta[i][j], end=" ")
    print()

modificare = True
while modificare:  #cat timp mai apar modificari

