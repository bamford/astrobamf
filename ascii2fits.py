import numpy as N
import pyfits
import os

def ascii2fits(infilename, outfilename, sep=None, header=None):
    f = file(infilename)
    if header is None:
        l = f.readline()
        ls = l.split(sep)
        columns = [i.strip() for i in ls]
    else:
        h = file(header)
        l = h.readline()
        ls = l.split(sep)
        columns = [i.strip() for i in ls]
        h.close()
    lines = f.readlines()
    lines = [i.split(sep) for i in lines]
    data = {}
    cols = []
    for i, c in enumerate(columns):
        example = lines[0][i]
        if '.' in example:
            t = float
            tn = N.float
            tp = 'E'
        elif len(example) < 4:
            t = int
            tn = N.int16
            tp = 'I'
        elif len(example) < 10:
            t = int
            tn = N.int32
            tp = 'J'
        else:
            t = long
            tn = N.int64
            tp = 'K'
        d = [t(l[i]) for l in lines]
        data[c] = N.array(d, tn)
        cols.append(pyfits.Column(name=c, format=tp, array=data[c]))
    tbhdu=pyfits.new_table(cols)
    file_exists = os.path.isfile(outfilename)
    if file_exists:
	os.remove(outfilename)
    tbhdu.writeto(outfilename)
	
