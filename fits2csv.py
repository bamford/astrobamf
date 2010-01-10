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

def fits2csv_round(infilename, outfilename, sep=',', linesep='\n', maxlength=32,
                   selectednames=None, limit=None, round=4):
    d = pyfits.getdata(infilename)
    if limit is not None:
        d = d[eval(limit)]
    if selectednames is None:
        selectednames = d.names
    floatnames = [n[0] for n in d.dtype.descr
                  if (n[0] in selectednames) and ('f' in n[1])]
    othernames = [n[0] for n in d.dtype.descr
                  if (n[0] in selectednames) and ('f' not in n[1])]
    floatcolumns = [d.field(c) for c in floatnames]
    othercolumns = [d.field(c) for c in othernames]
    n = len(d)
    del d
    fout = file(outfilename, 'w')
    fout.write(sep.join(othernames+floatnames)+linesep)
    roundformat = '%.' + '%if'%round
    for row in range(n):
	s = ['%s'%(c[row]) for c in othercolumns]
	s += [roundformat%(c[row]) for c in floatcolumns]
	fout.write(sep.join(s)+linesep)
    fout.close()
