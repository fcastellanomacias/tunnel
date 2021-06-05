# SageMath code (using SnapPy) to accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# (arXiv:1908.01693)
# by Felipe Castellano-Macias and Nicholas Owad

import snappy
import csv

# Inputs step3output.csv
mylst = []
with open('step3output.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        mylst.append(row)

# Adds an extra entry to each list in mylst
for k in mylst:
    k.append('')

# Implements the theorem about the Jones polynomial
c = float(2*cos(pi/5)^2)
count = 0
for k in mylst:
    if k[5] == '':
        M = snappy.Manifold(k[0].replace('_',''))
        L = M.link()
        P = L.jones_polynomial()
        p = P(e^(2*pi*i/5))
        f = float(sqrt(p.real()^2+ p.imag()^2))
        if f>2.149:
            k[5] = 2
            count += 1
for k in mylst:
    if 'a' in k[0] or 'n' in k[0]:
        M = snappy.Manifold(k[0].replace('_',''))
        L = M.link()
        P = L.jones_polynomial()
        p = P(e^(2*pi*i/5))
        f = float(sqrt(p.real()^2+ p.imag()^2))
        k[10] = f
    else:
        M = snappy.Manifold(k[0])
        L = M.link()
        P = L.jones_polynomial()
        p = P(e^(2*pi*i/5))
        f = float(sqrt(p.real()^2+ p.imag()^2))
        k[10] = f

# Outputs mylst
mylst.insert(0, ['Name','Unknotting','Genus','Bridge','Nakanishi','Tunnel','Symmetry type','Symmetry group','Montesinos?','Montesinos fractions','Kohno'])
with open('step4output.csv', 'w') as filecsv:
    writer = csv.writer(filecsv)
    writer.writerows(mylst)
filecsv.close()
