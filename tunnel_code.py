# To accompany the paper
# 'The tunnel number of all 11 and 12 crossing alternating knots'
# by F. Castellano-Macias and N. Owad

from __future__ import division
import snappy
from fractions import Fraction
import sys
sys.setrecursionlimit(1000000000)
from collections import OrderedDict
import copy
import _csv
import itertools
import math
from collections import deque
from fractions import gcd

# Finds all integer partitions of the positive integer n. Each partition will
# be a list of positive integers.
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

# Finds all integer partitions of length m of the positive integer n. Each
# partition will be a list of length m of positive integers.
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

# mylist needs to be a list of fractions. Removes fractions from mylist with
# denominator equal to ±1.
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

# Outputs a list of all rational tangles with n crossings, possibly including
# duplicates or rational tangles with less than n crossings.
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

# Outputs a list of all rational tangles with n crossings built out of
# fractions with odd denominator, possibly including duplicates or rational
# tangles with less than n crossings.
def rattanlistodd(n):
    mylist = []
    if n == 0:
        mylist.append(snappy.RationalTangle(0))
        mylist.append(snappy.RationalTangle(0,0))
    else:
        x = removen1(continuedfractionlistinvdupneg(n))
        for i in x:
            if i.denominator % 2 == 1:
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

# mylist is an array, where the first entry of each item is a knot. Removes
# duplicate knots from mylist by comparing the first entry from each item.
def knotduplicates_fraction(mylist):
    namelist = []
    knotlist = []
    for k in mylist:
        name = k[0].exterior().identify()
        if name not in namelist:
            namelist.append(name)
            knotlist.append(k)
    return knotlist

# Ouputs all clasp Montesinos knots of the form M(e;±1/2,b1/a1,b2/a2) with
# n crossings, where a1 and a2 are odd, possibly including duplicates, links,
# or Montesinos knots with fewer than n crossings.
def montesinos(n):
    newlist = []
    t = n - 2
    mydict = {}
    for l in range(2,t-1):
        mydict[l] = rattanlistodd(l)
    for i in range(2,t-1):
        j = t - i
        for a in mydict[i]:
            for b in mydict[j]:
                T1 = a + snappy.RationalTangle(1,2) + b
                T2 = a + snappy.RationalTangle(-1,2) + b
                L1 = T1.numerator_closure()
                L2 = T2.numerator_closure()
                newlist.append(L1)
                newlist.append(L2)
    return knotduplicates(newlist)

# Ouputs all alternating clasp Montesinos knots of the form
# M(e;±1/2,b1/a1,b2/a2), where a1 and a2 are odd, with no links or knots with
# fewer than n crossings.
def montesinosnew(n):
    outputlist = []
    for i in montesinos(n):
        if i.is_alternating() and len(i.link_components) == 1:
            b = i.exterior().identify()
            if len(snappy.Manifold(str(b[-1])).link().crossings) == n:
                outputlist.append(i)
    return outputlist

# Ouputs all nonalternating clasp Montesinos knots of the form
# M(e;±1/2,b1/a1,b2/a2), where a1 and a2 are odd, with no links or knots with
# fewer than n crossings.
def montesinosnewnonalt(n):
    outputlist = []
    for i in montesinos(n):
        if len(i.link_components) == 1 and i.is_alternating() == False:
            b = i.exterior().identify()
            if len(snappy.Manifold(str(b[-1])).link().crossings) == n:
                outputlist.append(i)
    return outputlist

# Outputs the set of names of all alternating clasp Montesinos knots of the
# form M(e;±1/2,b1/a1,b2/a2), where a1 and a2 are odd, with no links or knots
# with fewer than n crossings.
def montesinos_set(n):
    newset = set()
    for i in montesinosnew(n):
        x = i.exterior().identify()
        newset.add(str(x))
    return newset

# Outputs the set of names of all nonalternating clasp Montesinos knots of the
# form M(e;±1/2,b1/a1,b2/a2), where a1 and a2 are odd, with no links or knots
# with fewer than n crossings.
def montesinos_setnonalt(n):
    newset = set()
    for i in montesinosnewnonalt(n):
        x = i.exterior().identify()
        newset.add(str(x))
    return newset

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

# Outputs precisely all alternating Montesinos knots with n crossings and
# number of rational tangles equal to 'terms', with no duplicates. Each item
# in the output is a list: its first entry is the name of the Montesinos knot,
# and its second entry is a list containing the fractions associated to each
# rational tangle in the Montesinos knot.
def montesinosall_alt(n,terms):
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
            if len(knot[0].exterior().link().crossings) == n and len(knot[0].link_components) == 1 and knot[0].is_alternating():
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

# Outputs precisely all nonalternating Montesinos knots with n crossings and
# number of rational tangles equal to 'terms', with no duplicates. Each item
# in the output is a list: its first entry is the name of the Montesinos knot,
# and its second entry is a list containing the fractions associated to each
# rational tangle in the Montesinos knot.
def montesinosall_nonalt(n,terms):
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
            if len(knot[0].exterior().link().crossings) == n and len(knot[0].link_components) == 1 and knot[0].is_alternating() == False:
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

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_11(n):
    newlist = []
    for s in montesinos_set(n):
        start = s.find('a') - 2
        end = s.find('(', start)
        newlist.append(s[start:start+3] + '_' + s[start+3:end])
    return newlist

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_12(n):
    newlist = []
    for s in montesinos_set(n):
        start = s.find('a') - 2
        end = s.find('(', start)
        if len(s[start+3:end]) == 4:
            newlist.append(s[start:start+3] + '_' + s[start+3:end])
        elif len(s[start+3:end]) == 3:
            newlist.append(s[start:start+3] + '_0' + s[start+3:end])
        elif len(s[start+3:end]) == 2:
            newlist.append(s[start:start+3] + '_00' + s[start+3:end])
        elif len(s[start+3:end]) == 1:
            newlist.append(s[start:start+3] + '_000' + s[start+3:end])
    return newlist

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_11_nonalt(n):
    newlist = []
    for s in montesinos_setnonalt(n):
        start = s.find('n') - 2
        end = s.find('(', start)
        newlist.append(s[start:start+3] + '_' + s[start+3:end])
    return newlist

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_12_nonalt(n):
    newlist = []
    for s in montesinos_setnonalt(n):
        start = s.find('n') - 2
        end = s.find('(', start)
        if len(s[start+3:end]) == 4:
            newlist.append(s[start:start+3] + '_' + s[start+3:end])
        elif len(s[start+3:end]) == 3:
            newlist.append(s[start:start+3] + '_0' + s[start+3:end])
        elif len(s[start+3:end]) == 2:
            newlist.append(s[start:start+3] + '_00' + s[start+3:end])
        elif len(s[start+3:end]) == 1:
            newlist.append(s[start:start+3] + '_000' + s[start+3:end])
    return newlist

# Creates a list of the names of precisely all alternating Montesinos knots
# with 11 crossings.
m11_a = montesinosall_alt(11,3) + montesinosall_alt(11,4) + montesinosall_alt(11,5)

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_11_all_alt(n):
    newlist = []
    for s in m11_a:
        start = str(s[0][-1]).find('a') - 2
        end = str(s[0][-1]).find('(', start)
        newlist.append([str(s[0][-1])[start:start+3] + '_' + str(s[0][-1])[start+3:end], s[1]])
    return newlist

# Creates a list of the names of precisely all alternating Montesinos knots
# with 12 crossings.
m12_a = montesinosall_alt(12,3) + montesinosall_alt(12,4) + montesinosall_alt(12,5) + montesinosall_alt(12,6)

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_12_all_alt(n):
    newlist = []
    for s in m12_a:
        start = str(s[0][-1]).find('a') - 2
        end = str(s[0][-1]).find('(', start)
        if len(str(s[0][-1])[start+3:end]) == 4:
            newlist.append([str(s[0][-1])[start:start+3] + '_' + str(s[0][-1])[start+3:end], s[1]])
        elif len(str(s[0][-1])[start+3:end]) == 3:
            newlist.append([str(s[0][-1])[start:start+3] + '_0' + str(s[0][-1])[start+3:end], s[1]])
        elif len(str(s[0][-1])[start+3:end]) == 2:
            newlist.append([str(s[0][-1])[start:start+3] + '_00' + str(s[0][-1])[start+3:end], s[1]])
        elif len(str(s[0][-1])[start+3:end]) == 1:
            newlist.append([str(s[0][-1])[start:start+3] + '_000' + str(s[0][-1])[start+3:end], s[1]])
    return newlist

# Creates a list of the names of precisely all nonalternating Montesinos knots
# with 11 crossings.
m11_n = montesinosall_nonalt(11,3) + montesinosall_nonalt(11,4) + montesinosall_nonalt(11,5)

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_11_all_nonalt(n):
    newlist = []
    for s in m11_n:
        start = str(s[0][-1]).find('n') - 2
        end = str(s[0][-1]).find('(', start)
        newlist.append([str(s[0][-1])[start:start+3] + '_' + str(s[0][-1])[start+3:end], s[1]])
    return newlist

# Creates a list of the names of precisely all nonalternating Montesinos knots
# with 12 crossings.
m12_n = montesinosall_nonalt(12,3) + montesinosall_nonalt(12,4) + montesinosall_nonalt(12,5) + montesinosall_nonalt(12,6)

# Adjusts names of knots to match KnotInfo conventions.
def montesinos_name_12_all_nonalt(n):
    newlist = []
    for s in m12_n:
        start = str(s[0][-1]).find('n') - 2
        end = str(s[0][-1]).find('(', start)
        if len(str(s[0][-1])[start+3:end]) == 4:
            newlist.append([str(s[0][-1])[start:start+3] + '_' + str(s[0][-1])[start+3:end], s[1]])
        elif len(str(s[0][-1])[start+3:end]) == 3:
            newlist.append([str(s[0][-1])[start:start+3] + '_0' + str(s[0][-1])[start+3:end], s[1]])
        elif len(str(s[0][-1])[start+3:end]) == 2:
            newlist.append([str(s[0][-1])[start:start+3] + '_00' + str(s[0][-1])[start+3:end], s[1]])
        elif len(str(s[0][-1])[start+3:end]) == 1:
            newlist.append([str(s[0][-1])[start:start+3] + '_000' + str(s[0][-1])[start+3:end], s[1]])
    return newlist

# Opens the file knotinfo_data_complete.csv, taken from KnotInfo, and extracts
# from it the name of all knots with 11 or 12 crossings, their bridge numbers,
# and whether they are alternating or nonalternating. Creates the array
# knotlist; each item in knotlist will be a knot with some of its invariants.
with open('knotinfo_data_complete.csv') as csvfile:
    readCSV = _csv.reader(csvfile, delimiter=',')
    knotlist = []
    for row in readCSV:
        if "11a" in row[0]:
            knotlist.append([row[0], row[44], row[10]])
        elif "11n" in row[0]:
            knotlist.append([row[0], row[44], row[10]])
        elif "12a" in row[0]:
            knotlist.append([row[0], row[44], row[10]])
        elif "12n" in row[0]:
            knotlist.append([row[0], row[44], row[10]])

# Adds an entry to each item in knotlist.
for k in knotlist:
    k.append('?')

# Adds an entry to each item in knotlist.
for k in knotlist:
    k.append('Mont?')

# Adds an entry to each item in knotlist.
for k in knotlist:
    k.append('Fraction')

# Alternating 2-bridge knots have tunnel number 1.
for k in knotlist:
    if k[1] == '2' and k[2] == 'Y':
        k[3] = 1

# Creates some lists of Montesinos knots which will be used later.
montesinos_11_12 = montesinos_name_11(11) + montesinos_name_12(12)
montesinos_11_12_nonalt = montesinos_name_11_nonalt(11) + montesinos_name_12_nonalt(12)
montesinos_11_12_all_alt = montesinos_name_11_all_alt(11) + montesinos_name_12_all_alt(12)
montesinos_all_alt = []
for i in range(0,len(montesinos_11_12_all_alt)):
    montesinos_all_alt.append(montesinos_11_12_all_alt[i][0])
montesinos_11_12_all_nonalt = montesinos_name_11_all_nonalt(11) + montesinos_name_12_all_nonalt(12)
montesinos_all_nonalt = []
for i in range(0,len(montesinos_11_12_all_nonalt)):
    montesinos_all_nonalt.append(montesinos_11_12_all_nonalt[i][0])
montesinosall = montesinos_all_alt + montesinos_all_nonalt
montesinosall_fract = montesinos_11_12_all_alt + montesinos_11_12_all_nonalt

# mylist needs to be a list of integers. Outputs the gcd of mylist.
def GCD_list(mylist):
    g = mylist[1]
    for i in mylist[1:]:
        g = gcd(g,i)
    return g

# Creates a list of all Montesinos knots with 11 or 12 crossings satisfying
# Lustig and Moriah's theorem.
lustig_moriah_thm_list = []
for knot in montesinosall_fract:
    denominator_list = []
    for fraction in knot[1]:
        denominator_list.append(fraction[1])
    g = GCD_list(denominator_list)
    if g != 1:
        lustig_moriah_thm_list.append(knot[0])

# Alternating clasp Montesinos knots of the form M(e;±1/2,b1/a1,b2/a2),
# where a1 and a2 are odd, have tunnel number 1.
for k in knotlist:
    if k[2] == 'Y' and k[0] in montesinos_11_12:
        if k[3] == 1:
            pass
        else:
            k[3] = 1

# Alternating 3-bridge knots have tunnel number 2.
for k in knotlist:
    if k[1] == '3' and k[2] == 'Y':
        if k[3] != '?':
            pass
        else:
            k[3] = 2

# The knots 12a_0750 and 12a_0554 satisfy Lustig and Moriah's theorem.
for k in knotlist:
    if k[1] == '4' and k[2] == 'Y':
        if k[0] == '12a_0750' or k[0] == '12a_0554':
            k[3] = 3
        else:
            k[3] = 2

# Nonalternating clasp Montesinos knots of the form M(e;±1/2,b1/a1,b2/a2),
# where a1 and a2 are odd, have tunnel number 1.
for k in knotlist:
    if k[2] == 'N' and k[0] in montesinos_11_12_nonalt:
        k[3] = 1

# Indicates whether each 11 or 12 crossing knot is a Montesinos knot or not.
# If a knot is Montesinos, it also adds its fraction decomposition.
for k in knotlist:
    if k[0] in montesinosall:
        k[4] = 'Y'
        k[5] = montesinosall_fract[next(i for i,v in enumerate(montesinosall_fract) if k[0] in v)][1]
    else:
        k[4] = 'N'
        k[5] = 'n/a'

# Makes each bridge number an integer, instead of a string.
for k in knotlist:
    k[1] = int(k[1])

# Implements Lustig and Moriah's theorem for tunnel number.
for k in knotlist:
    if k[0] in lustig_moriah_thm_list and k[3] == '?':
        k[3] = k[1]-1

# Deletes the first fraction for each Montesinos knot, which was assigned
# to be 0/1.
for k in knotlist:
    if k[5] != 'n/a':
        del k[5][0]

# Adds an entry to each item in knotlist.
for k in knotlist:
    k.append('LM?alpha?')

# Indicates whether each 11 or 12 crossing knot satisfies the assumptions of
# Lustig and Moriah's theorem or not.
for k in knotlist:
    if k[0] in lustig_moriah_thm_list:
        k[6] = 'Y'
    else:
        k[6] = 'N'

# Inserts an index as the first item of knotlist
knotlist.insert(0, ['Name','Bridge number','Alternating?','Tunnel number','Montesinos?','Montesinos fraction','Lustig-Moriah?'])

# Outputs a csv file containing knotlist.
with open('new_tunnel_csv.csv', 'w') as filecsv:
    writer = _csv.writer(filecsv)
    writer.writerows(knotlist)
filecsv.close()
