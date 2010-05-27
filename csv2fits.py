import numpy as N
import pyfits
from string import join

def csv2fits(infilename, outfilename, sep=',', linesep='\n', columns=None):
    lss = [[i.strip('"\'').strip() for i in ls] for ls in (l.split(sep) for l in file(infilename))]
    if columns is None:
        columns = lss[0]
    print columns
    data = lss[1:]
    cols = []
    for i, c in enumerate(columns):
        d = N.array([l[i] for l in data])
        try:
            e = N.where(d != '', d, '-999')
            d = e.astype(N.int)
            maxd = N.absolute(d).max()
            if maxd > 2**31:
                t = 'K'
            elif maxd > 2**15:
                t = 'J'
            else:
                t = 'I'
        except ValueError:
            try:
                e = N.where(d != '', d, '-999')
                d = e.astype(N.float)
                t = 'E'
            except ValueError:
                maxlength = N.array([len(j) for j in d]).max()
                t = 'A%i'%max(1,maxlength)
        cols.append(pyfits.Column(name=c, format=t, array=d))
    tbhdu=pyfits.new_table(cols)
    tbhdu.writeto(outfilename, clobber=True)
