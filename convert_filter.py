from glob import glob

def dat2par(fglob):
    fnames = glob(fglob)
    header = file('parheader').readlines()
    for fname in fnames:
        fnameout = fname.replace('.dat', '.par')
        f = file(fname)
        fout = file(fnameout, 'w')
        fout.writelines(header)
        fout.write('\ntypedef struct {\n double lambda;\n double pass;\n} KFILTER_SIMPLE;\n\n')
        for l in f:
            fout.write('KFILTER_SIMPLE %s'%l)
        fout.close()

