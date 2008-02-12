import pyfits

# This has now been profiled and made around 40 times faster than before!

def fits2csv(infilename, outfilename, sep=',', linesep='\n', maxlength=32):
    d = pyfits.getdata(infilename)
    names = d.names
    columns = [(d.field(n)).astype('S%i'%maxlength) for n in names]
    fout = file(outfilename, 'w')
    fout.write(sep.join(names)+linesep)
    for row in range(len(d)):
	s = [c[row] for c in columns]
	fout.write(sep.join(s)+linesep)
    fout.close()
