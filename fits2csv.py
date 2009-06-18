import pyfits

# This has now been profiled and made around 40 times faster than before!

def fits2csv(infilename, outfilename, sep=',', linesep='\n', maxlength=32,
             selectednames=None, limit=None):
    d = pyfits.getdata(infilename)
    if limit is not None:
        d = d[eval(limit)]
    if selectednames is None:
        names = d.names
    else:
        names = [n for n in d.names if n in selectednames]
    columns = [(d.field(n)).astype('S%i'%maxlength) for n in names]
    fout = file(outfilename, 'w')
    fout.write(sep.join(names)+linesep)
    for row in range(len(d)):
	s = [c[row] for c in columns]
	fout.write(sep.join(s)+linesep)
    fout.close()
