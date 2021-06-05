# SageMath code (using SnapPy and Heegaard) to accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# (arXiv:1908.01693)
# by Felipe Castellano-Macias and Nicholas Owad

import snappy
import heegaard
import csv

# Inputs step4output.csv
mylist = []
with open('step4output.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        mylist.append(row)

# Deletes the first item of mylist
del mylist[0]

# Adds an extra entry to each list in mylist
for k in mylist:
    k.append('')

# Implements the method to compute tunnel number by finding
# a presentation of the knot group (uses the program Heegaard);
# we recommend repeating this step many times (or setting the
# number of randomizations to a larger number)
for k in mylist:
    if k[5] == '':
        M = snappy.Manifold(k[0].replace('_',''))
        for i in range(1000):
            G = M.fundamental_group()
            if G.num_generators() == 2:
                if heegaard.is_realizable(G.relators()):
                    k[5] = 1
                    k[11] = G.num_generators()
                    break
            else:
                M.randomize()
for k in mylist:
    if k[5] == '1':
        if k[11] == '2':
            pass
        elif 'a' in k[0] or 'n' in k[0]:
            M = snappy.Manifold(k[0].replace('_',''))
            for i in range(1000):
                G = M.fundamental_group()
                if heegaard.is_realizable(G.relators()) and G.num_generators() == 2:
                    k[11] = 2
                    break
                else:
                    M.randomize()
        else:
            M = snappy.Manifold(k[0])
            for i in range(1000):
                G = M.fundamental_group()
                if heegaard.is_realizable(G.relators()) and G.num_generators() == 2:
                    k[11] = 2
                    break
                else:
                    M.randomize()

# Outputs mylist
mylist.insert(0, ['Name','Unknotting','Genus','Bridge','Nakanishi','Tunnel','Symmetry type','Symmetry group','Montesinos?','Montesinos fractions','Kohno','Min num gen (Heegaard realizable)'])
with open('step5output.csv', 'w') as filecsv:
    writer = csv.writer(filecsv)
    writer.writerows(mylist)
filecsv.close()
