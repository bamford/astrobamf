from cStringIO import StringIO
import numpy

def tablefromcsv(fname, h5file, group, tablename, tabledesc,
                 names=True, dtype=None, converters=None, linechunk=10000):
    """ Create a table in a HDF5 file from a CSV file.

    Uses memory efficiently by iteratively reading 'linechunk' lines from CSV
    and writing into HDF5 table, instead of reading entire CSV file into memory.
    """
    fin = file(fname)
    first = True
    while True:
        lines = ''.join(fin.readline() for i in range(linechunk))
        if len(lines) == 0: break
        lines = lines.replace('"', '')
        rec = numpy.genfromtxt(StringIO(lines), names=names, delimiter=',',
                               dtype=dtype, converters=converters)
        if first:
            first = False
            table = h5file.createTable(group, tablename, rec, tabledesc)
        else:
            table.append(rec)
    table.flush()
