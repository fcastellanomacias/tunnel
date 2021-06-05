# SageMath code (using SnapPy) to accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# (arXiv:1908.01693)
# by Felipe Castellano-Macias and Nicholas Owad

import snappy
import csv

# Inputs step5output.csv
mylst = []
with open('step5output.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row != []:
            mylst.append(row)

# Deletes the first item of mylst
del mylst[0]

# Adds an extra entry to each list in mylst
for k in mylst:
    k.append('')

# Indicates that non-Montesinos knots do not satisfy
# the conditions of Lustig and Moriah's theorem
for k in mylst:
    if k[8] == 'N':
        k[12] = 'n/a'

# Outputs the gcd of a list of integers
def GCD_list(milista):
    g = milista[0]
    for i in milista[1:]:
        g = gcd(g,i)
    return g

# Defines a function that changes the format of a list of fractions
def stringtolist(s): # e.g. s = '[(1, 2), (2, 3), (2, 3), (5, 12)]'
    mys = s[1:len(s)-1]
    mys1 = mys.replace(' ','')
    mys2 = mys1.replace('(','')
    mys3 = mys2.replace(')','')
    s2 = mys3.split(',')
    midlst = [int(l) for l in s2]
    c = 0
    outlst = []
    while c < len(s2):
        outlst.append(Rational(int(midlst[c])/int(midlst[c+1])))
        c = c+2
    return outlst # e.g. outlst = [1/2, 2/3, 2/3, 5/12]

# Defines a function that checks whether a Montesinos knot satisfies
# the conditions of Lusting and Moriah's theorem
def LM(s): # e.g. s = "['1/2', '1/3', '3/7']"
    mys = s[1:len(s)-1]
    mys1 = mys.replace(' ','')
    mys2 = mys1.replace("'",'')
    s2 = mys2.split(',')
    fractions = [Rational(f) for f in s2]
    denoms = [f.denominator() for f in fractions]
    alpha = GCD_list(denoms)
    if alpha != 1:
        return True
    else:
        return False

# Indicates whether a Montesinos knot satisfies
# the conditions of Lusting and Moriah's theorem
for k in mylst:
    if k[8] == 'Y':
        if LM(k[9]):
            k[12] = 'Y'
        elif not LM(k[9]):
            k[12] = 'N'

# Defines a function that changes the format of a list of fractions
def cleanfract(s): # s = "['1/2', '1/3', '3/7']"
    return s.replace("'",'')

# Cleans up the format of the fractions of Montesinos knots
for k in mylst:
    if k[8] == 'Y':
        k[9] = cleanfract(k[9])

# Outputs mylst
mylst.insert(0, ['Name','Unknotting','Genus','Bridge','Nakanishi','Tunnel','Symmetry type','Symmetry group','Montesinos?','Montesinos fractions','Kohno','Min num gen (Heegaard realizable)','alpha'])
with open('step6output.csv', 'w') as filecsv:
    writer = csv.writer(filecsv)
    writer.writerows(mylst)
filecsv.close()
