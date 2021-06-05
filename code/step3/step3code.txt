# SageMath code (using SnapPy) to accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# (arXiv:1908.01693)
# by Felipe Castellano-Macias and Nicholas Owad

import snappy
import csv

# Inputs the file knotinfo_full.csv from KnotInfo
mylist = []
with open('knotinfo_full.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        mylist.append(row)
del mylist[0]

# Inputs the file knotorious_full_fixed.csv from Knotorious
knotorious = []
with open('knotorious_full_fixed.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        knotorious.append(row)
del knotorious[0]

# Changes format
for k in knotorious:
    if '12a' in k[0]:
        while k[0][4] == '0':
            k[0] = k[0].replace('_0','_')
    elif '12n' in k[0]:
        while k[0][4] == '0':
            k[0] = k[0].replace('_0','_')
for k in knotorious:
    if len(k[3]) > 1:
        k[3] = k[3].replace(' or ','')
        k[3] = [int(i) for i in k[3]]
    else:
        k[3] = int(k[3])

# Defines a function that checks for an item within a list of lists
def checklist(knotname, listoflists):
    for i in listoflists:
        if i[0] == knotname:
            return listoflists.index(i)

# Adds Nakanishi indices from knotorious to mylist
for k in mylist:
    if k[4] == '':
        i = mylist.index(k)
        k[4] = knotorious[i][3]

# Inputs the file montesinos_all_final.csv
allmontesinos = []
with open('montesinos_all_final.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        allmontesinos.append(row)
del allmontesinos[0]
del allmontesinos[0]

# Changes format
for k in allmontesinos:
    k[2] = k[2].replace('[','')
    k[2] = k[2].replace(']','')
    k[2] = k[2].replace(' ','')
    montelist = k[2].split(',')
    if montelist[0] == '0':
        del montelist[0]
    k[2] = montelist

# Adds to each knot in mylist whether it is a Montesinos knot
# and its Montesinos fraction (if applicable)
for k in mylist:
    i = mylist.index(k)
    k.append(allmontesinos[i][1])
    k.append(allmontesinos[i][2])

# Inputs the file step2output.csv
MSYtheorem = []
with open('step2output.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        MSYtheorem.append(row)
del MSYtheorem[0]

# Changes format
for k in MSYtheorem:
    if '12a' in k[0]:
        while k[0][4] == '0':
            k[0] = k[0].replace('_0','_')
    elif '12n' in k[0]:
        while k[0][4] == '0':
            k[0] = k[0].replace('_0','_')

# Implements Morimoto, Sakuma, and Yokota's theorem
# about tunnel number one Montesinos knots
for k in mylist:
    if k[5] == '' and k[8] == 'Y':
        i = checklist(k[0],MSYtheorem)
        k[5] = MSYtheorem[i][3]

# Implements the theorem about strong inversions
for k in mylist:
    if k[5] == '':
        if k[6] == 'chiral' or k[6] == 'negative amphicheiral':
            k[5] = 2

# Implements the proposition about Nakanishi indices
for k in mylist:
    if k[5] == '':
        if type(k[4]) is int:
            if k[4]>1:
                k[5] = 2
        else:
            if all(l > 1 for l in k[4]):
                k[5] = 2

# Outputs mylist
mylist.insert(0, ['Name','Unknotting','Genus','Bridge','Nakanishi','Tunnel','Symmetry type','Symmetry group','Montesinos?','Montesinos fractions'])
with open('step3output.csv', 'w') as filecsv:
    writer = csv.writer(filecsv)
    writer.writerows(mylist)
filecsv.close()
