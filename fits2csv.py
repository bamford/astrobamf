import pyfits

# This has now been profiled and made around 40 times faster than before!

def fits2csv(infilename, outfilename, sep=',', linesep='\n', maxlength=32,
             selectednames=None, limit=None):
    d = pyfits.getdata(infilename)
    if limit is not None:
        d = d[eval(limit)]
    names = d.names
    if selectednames is None:
        columns = [(d.field(n)).astype('S%i'%maxlength) for n in names]
        selectednames = names
    else:
        columns = [(d.field(n)).astype('S%i'%maxlength)
                   for n in names if n in selectednames]
    fout = file(outfilename, 'w')
    fout.write(sep.join(selectednames)+linesep)
    for row in range(len(d)):
	s = [c[row] for c in columns]
	fout.write(sep.join(s)+linesep)
    fout.close()
