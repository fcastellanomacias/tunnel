# SageMath code (using SnapPy) to accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# (arXiv:1908.01693)
# by Felipe Castellano-Macias and Nicholas Owad

import snappy
import csv

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

# Inputs the file step1output.csv
tunnellist = []
with open('tunnel_data.csv') as csvfile:
    readCSV = _csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        if row != []:
            tunnellist.append(row)
del tunnellist[0]

# Changes format of some items in tunnellist
for row in tunnellist:
    row[1] = int(row[1])
    if row[3] != '':
        row[3] = int(row[3])
    if row[5] != 'n/a':
        row[5] = stringtolist(row[5])

# Given a fraction, outputs the value of that fraction mod 1
def modulo1(f): # e.g. f = 43/27
    if f == 0:
        return f
    elif f == 1:
        return 0
    elif f < 1 and f>0:
        return f
    elif f > 1:
        r = f-f.floor()
        return r
    elif f<0:
        t = f-f.floor()
        return t

# Implements Morimoto, Sakuma, and Yokota's theorem
# about tunnel number one Montesinos knots
count = 0
count2 = 0
count3 = 0
for k in tunnellist:
    if k[4] == 'Y' and k[3] == '':
        if len(k[5]) == 3:
            l = k[5]
            if (denominator(l[0]) == 2 and denominator(l[1])%2 == 1 and denominator(l[2])%2 == 1) or (denominator(l[1]) == 2 and denominator(l[0])%2 == 1 and denominator(l[2])%2 == 1) or (denominator(l[2]) == 2 and denominator(l[1])%2 == 1 and denominator(l[0])%2 == 1):
                k[3] = 1
                count2 = count2 + 1
for k in tunnellist:
    if k[4] == 'Y' and k[3] == '':
        if len(k[5]) == 3:
            l = k[5]
            esum = -sum(l)
            e1p = 1/(3*denominator(l[0]))
            e1m = -1/(3*denominator(l[0]))
            e2p = 1/(3*denominator(l[1]))
            e2m = -1/(3*denominator(l[1]))
            e3p = 1/(3*denominator(l[2]))
            e3m = -1/(3*denominator(l[2]))
            if (modulo1(l[1]) == 1/3 or modulo1(l[1]) == 2/3) and (modulo1(l[2]) == 1/3 or modulo1(l[2]) == 2/3) and (esum == e1p or esum == e1m):
                k[3] = 1
                print(k)
                count = count+1
            elif (modulo1(l[0]) == 1/3 or modulo1(l[0]) == 2/3) and (modulo1(l[2]) == 1/3 or modulo1(l[2]) == 2/3) and (esum == e2p or esum == e2m):
                k[3] = 1
                print(k)
                count = count+1
            elif (modulo1(l[0]) == 1/3 or modulo1(l[0]) == 2/3) and (modulo1(l[1]) == 1/3 or modulo1(l[1]) == 2/3) and (esum == e3p or esum == e3m):
                k[3] = 1
                print(k)
                count = count+1
for k in tunnellist:
    if k[4] == 'Y' and k[3] == '':
        k[3] = 2
        count3 = count3+1

# Inserts an index as the first item of tunnellist
tunnellist.insert(0, ['Name','Bridge number','Alternating?','Tunnel number','Montesinos?','Montesinos fraction','Lustig-Moriah?'])

# Outputs a csv file containing tunnellist
with open('step2output.csv', 'w') as filecsv:
    writer = _csv.writer(filecsv)
    writer.writerows(tunnellist)
filecsv.close()
