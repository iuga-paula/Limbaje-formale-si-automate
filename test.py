
elem = 1
# multime = set(elem)
# print(multime)  NU MERGE

l = []
l.append(elem)
multime = set(l)
print(multime)  #merge

elem2 = 3
multime.add(elem)  #FARA  DUPLICATE
multime.add(elem2)
print(multime)

D = {1:[('a','b'), ('b','c')]}

for elem in multime:
        print(elem)
        if elem in D.keys():
            print(D[elem][0][0])


cuv = "anaare"
cuv_nou = ""
for i in range(len(cuv)):
    cuv_nou += cuv[i]

if cuv == cuv_nou:
    print(cuv_nou)
else:
    print("NU")

multime2 = set([3,0,9])
if len(multime & multime2) != 0:
    print(multime & multime2)

if 0 in multime2:
    print("da")

l = [1,2,34]
l = set(l)
print(l)
