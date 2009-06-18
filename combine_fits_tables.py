import pyfits
import numpy as N
import os.path

def combine_fits_tables(tables, outfile, idfield='OBJID'):
    cols = []
    matches = {}
    lengths = []
    for t in tables:
        columns = t[1].columns
        data = t[1].data
        lengths.append(len(data))
        uniqidx, uniqid = N.unique1d(data.field(idfield), True)
        repeatedidx = N.ones(len(data), N.bool)
        repeatedidx[uniqidx] = False
        repeatedid = data.field(idfield)[repeatedidx]
        if len(repeatedid) > 0:
            print 'Repeated ids:', repeatedid
            print 'The repeats have been discarded'
            data = data[uniqidx]
        order = N.argsort(data.field(idfield))
        for c in columns:
            name = c.name.upper()
            if name not in [ci.name for ci in cols]:
                cols.append(pyfits.Column(name=name, format=c.format,
                                          array=data.field(name)[order]))
            else:
                matches[name] = data.field(name)[order]
    print 'Table lengths, with repeats:',
    print lengths
    tbhdu=pyfits.new_table(cols)
    data = tbhdu.data
    # check that repeated columns are identical
    print 'Repeated columns:',
    print matches.keys()
    for name in matches.keys():
        if N.any(data.field(name) != matches[name]):
            print 'Warning!  Repeated columns (%s) differ.'%name
            print data.field(name)[:5]
            print matches[name][:5]
    file_exists = os.path.isfile(outfile)
    if file_exists:
        os.remove(outfile)
    tbhdu.writeto(outfile)
