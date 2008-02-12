# A demonstration of how to loop over multiple (equal-length) lists,
# such that every combination of items from the lists occurs once.

nval = 3
nparam = 7

p = [['p1_1', 'p1_2', 'p1_3'],
     ['p2_1', 'p2_2', 'p2_3'],
     ['p3_1', 'p3_2', 'p3_3'],
     ['p4_1', 'p4_2', 'p4_3'],
     ['p5_1', 'p5_2', 'p5_3'],
     ['p6_1', 'p6_2', 'p6_3'],
     ['p7_1', 'p7_2', 'p7_3']]

pout = [1]

for m in range(nparam):
    ptmp = []
    for i in range(len(pout)):
	for j in range(nval):
	    if m == 0:
		ptmp.append(p[m][j])
	    else:
		ptmp.append(pout[i]+','+p[m][j])
    pout = ptmp

print len(pout)
for i in pout:
    print i
