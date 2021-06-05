# Python code (using SnapPy) to accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# (arXiv:1908.01693)
# by Felipe Castellano-Macias and Nicholas Owad.
# Code used to find all Montesinos knots with 14 or fewer crossings.

from __future__ import division
import snappy
from fractions import Fraction
import sys
sys.setrecursionlimit(1000000000)
import copy
import csv
import itertools
import math
from collections import deque
from fractions import gcd

# Finds all integer partitions of the positive integer n.
# Each partition will be a list of positive integers.
def partitions(n):
    newlist = []
    if n == 1:
        newlist.append([1])
        return newlist
    else:
        for i in range(1, n + 1):
            if i == n:
                a = [n]
                newlist.append(a)
            else:
                for j in partitions(n-i):
                    a = [i]
                    for e in j:
                        a.append(e)
                    newlist.append(a)
        return newlist

# Finds all integer partitions of length m of the positive integer n.
# Each partition will be a list of length m of positive integers.
def partitionsmterms(n, m):
    newlist = []
    for i in partitions(n):
        if len(i) == m:
            newlist.append(i)
    return newlist

# Removes duplicates from a list without altering the order.
def remove_duplicates(mylist):
    newlist = []
    for i in mylist:
        if i in newlist:
            pass
        else:
            newlist.append(i)
    return newlist

# mylist needs to be a list of fractions.
# Removes fractions from mylist with denominator equal to ±1.
def removen1(mylist):
    output = []
    for i in mylist:
        if i.denominator != 1 and i.denominator != -1:
            output.append(i)
    return output

# Outputs a list of continued fractions that can be built from partitions of n.
def continuedfractionlist(n):
    fractionlist = []
    for i in partitions(n):
        if len(i) == 1:
            fractionlist.append(Fraction(i[0],1))
        else:
            a = i[0]
            for j in i[1:]:
                a = j + Fraction(1,a)
            fractionlist.append(a)
    return remove_duplicates(fractionlist)

# Outputs a list of continued fractions that can be built from partitions of n,
# including the inverse and negative of each fraction, excluding duplicates.
def continuedfractionlistinvdupneg(n):
    y = continuedfractionlist(n)
    z = []
    for i in y:
        z.append(i)
        z.append(Fraction(i.denominator,i.numerator))
        z.append(Fraction(-i.denominator,i.numerator))
    return remove_duplicates(z)

# Outputs a list of all rational tangles with n crossings,
# possibly including duplicates or rational tangles with fewer than n crossings.
def rattanlist(n):
    mylist = []
    if n == 0:
        mylist.append(snappy.RationalTangle(0))
        mylist.append(snappy.RationalTangle(1,0))
    else:
        x = removen1(continuedfractionlistinvdupneg(n))
        for i in x:
            T = snappy.RationalTangle(i.numerator,i.denominator)
            mylist.append(T)
    return mylist

# mylist needs to be a list of knots. Removes duplicate knots from mylist.
def knotduplicates(mylist):
    namelist = []
    knotlist = []
    for k in mylist:
        name = k.exterior().identify()
        if name not in namelist:
            namelist.append(name)
            knotlist.append(k)
    return knotlist

# mylist is a list of lists, where the first entry of each list is a knot.
# Removes duplicate knots from mylist by comparing the first entries.
def knotduplicates_fraction(mylist):
    namelist = []
    knotlist = []
    for k in mylist:
        name = k[0].exterior().identify()
        if name not in namelist:
            namelist.append(name)
            knotlist.append(k)
    return knotlist

# Outputs all cyclic permutations of a list a.
def cyclicpermlist(a):
    outputlist = []
    d = deque(a)
    for _ in range(len(a)):
        d.rotate()
        outputlist.append(list(d))
    return outputlist

# Outputs a collection of lists, ordered up to cyclic permutation.
def uptocyclicperm(listoflists):
    for A in listoflists:
        C = cyclicpermlist(A)
        for x in C:
            if x != A and x in listoflists:
                listoflists.remove(x)
    return listoflists

# Outputs precisely all Montesinos knots with n crossings and
# number of rational tangles equal to 'terms', with no duplicates. Each item
# in the output is a list: its first entry is the name of the Montesinos knot,
# and its second entry is a list containing the fractions associated to each
# rational tangle in the Montesinos knot.
def montesinosall(n,terms):
    tangledict = {}
    for i in range(2,n+1):
        tangledict[i] = rattanlist(i)
    partitionslist = []
    part = uptocyclicperm(partitionsmterms(n,terms))
    for i in part:
        for k in i:
            if k == 1:
                a = 1
        if a != 1:
            partitionslist.append(i)
        a = 0
    newdict = {}
    key = 0
    newdict[0] = []
    newdict[0].append([snappy.RationalTangle(0), [snappy.RationalTangle(0).fraction] ])
    outputlist = []
    for p in partitionslist:
        for t in p:
            key = key +1
            newdict[key] = []
            for f in newdict[key-1]:
                for g in tangledict[t]:
                    ind = newdict[key-1].index(f)
                    newdict[key].append([f[0]+g, newdict[key-1][ind][1] + [g.fraction]])
        for tangle in newdict[key]:
            knot = [tangle[0].numerator_closure(),tangle[1]]
            if len(knot[0].exterior().link().crossings) == n and len(knot[0].link_components) == 1:
                outputlist.append(knot)
        key = 0
    final = []
    for knot in knotduplicates_fraction(outputlist):
        final.append([knot[0].exterior().identify(), knot[1]])
    finalfinal = []
    for b in final:
        if len(snappy.Manifold(str(b[0][-1])).link().crossings) == n:
            finalfinal.append(b)
    return finalfinal

# Creates a list of all Montesinos knots with 8 crossings.
m8 = montesinosall(8,3) + montesinosall(8,4)

# Creates a list of all Montesinos knots with 9 crossings.
m9 = montesinosall(9,3) + montesinosall(9,4)

# Creates a list of all Montesinos knots with 10 crossings.
m10 = montesinosall(10,3) + montesinosall(10,4) + montesinosall(10,5)

# Creates a list of all Montesinos knots with 11 crossings.
m11 = montesinosall(11,3) + montesinosall(11,4) + montesinosall(11,5)

# Creates a list of all Montesinos knots with 12 crossings.
m12 = montesinosall(12,3) + montesinosall(12,4) + montesinosall(12,5) + montesinosall(12,6)

# Creates a list of all Montesinos knots with 13 crossings.
m13 = montesinosall(13,3) + montesinosall(13,4) + montesinosall(13,5) + montesinosall(13,6)

# Creates a list of all Montesinos knots with 14 crossings.
m14 = montesinosall(14,3) + montesinosall(14,4) + montesinosall(14,5) + montesinosall(14,6) + montesinosall(14,7)

# Converts the name of a knot k to a string.
def naming(k): # e.g. k = [o9_37732(0,0), 10_133(0,0), K9_591(0,0), K10n4(0,0)]
    return str(k)

# Combines all Montesinos knots with 14 crossings or fewer,
# together with their associated fractions,
# into the list sortedmontesinos.
montesinoslist = []
for knot in m8:
    montesinoslist.append([naming(knot[0]), knot[1]])
for knot in m9:
    montesinoslist.append([naming(knot[0]), knot[1]])
for knot in m10:
    montesinoslist.append([naming(knot[0]), knot[1]])
for knot in m11:
    montesinoslist.append([naming(knot[0]), knot[1]])
for knot in m12:
    montesinoslist.append([naming(knot[0]), knot[1]])
for knot in m13:
    montesinoslist.append([naming(knot[0]), knot[1]])
for knot in m14:
    montesinoslist.append([naming(knot[0]), knot[1]])
sortedmontesinos = sorted(montesinoslist)
sortedmontesinos.insert(0, ['Name','Montesinos fraction'])

# Outputs a csv file called montesinosoutput.csv containing all Montesinos
# knots with 14 crossings or fewer, together with their associated fractions.
with open('montesinosoutput.csv', 'w') as filecsv:
    writer = csv.writer(filecsv)
    writer.writerows(sortedmontesinos)
filecsv.close()
