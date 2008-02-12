import numpy as N
import pyfits
from string import join

def csv2fits(infilename, outfilename, sep=',', linesep='\n'):
    f = file(infilename)
    lines = f.readlines()
    n = len(lines)-1
    f.close()
    lss = [[i.strip() for i in ls] for ls in (l.split(sep) for l in lines)]
    columns = lss[0]
    data = lss[1:]
    cols = []
    for i, c in enumerate(columns):
        # should really check for match to anything non-numeric using re
        if N.any(['"' in data[j][i] for j in range(n)]):
            d = N.array([l[i] for l in data])
            maxlength = N.array([len(j) for j in d]).max()
            t = 'A%i'%maxlength
        else:
            d = N.array([float(l[i]) for l in data])
            t = 'E'  # should check for double and integer
        cols.append(pyfits.Column(name=c, format=t, array=d))
    tbhdu=pyfits.new_table(cols)
    tbhdu.writeto(outfilename, clobber=True)
