t = tuple((1,2))
print(t[0])

D = {1: [tuple((1, 2)), tuple((2,3))]}
print(D[1][0])
print(D[1][0][0]) #D[litera][stare_curenta][strare_gen]


print(len(D[1]))
s = 'abdcro0kvrj'
for i in range(len(s)):
    if s[i] not in D.keys():
        print("NU", s[i])