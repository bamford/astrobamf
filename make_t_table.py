import Numeric as N
import nr
import sys
import pickle

ndof = 51
nt = 50000
bigdof = 1000

def prob(df, t):
    return (1 - nr.betai(0.5*df,0.5,df/(df+t**2))/2)


class t_table:
    def __init__(self, ndof=ndof, nt=nt):
        self.ndof = int(ndof)
        self.nt = int(nt)
        self.table = make_t_table(self.ndof, self.nt)
    def t(self, dof, prob):
        ipfloat = (prob - 0.5) * 200.0
        ip = int(round(ipfloat))
        prob_nearest = ip / 200.0 + 0.5
        prob_diff = abs(prob - prob_nearest)
        if prob_diff > 0.001:
            print 'Warning: requested probability of %5.3f differs from nearest'%prob
            print '         entry in table by 5.3%f. Using prob=%5.3f'%(prob_diff, prob_nearest)
        return self.table[self.index(dof, prob)][2]

    def index(self, dof, prob):
        "Returns the index corresponding closest to given dof and prob"
        # get index of dof
        if int(dof) == bigdof:
            idof = self.ndof - 1
        else:
            idof = int(round(dof - 1))
            if idof >= self.ndof - 1:
                #print 'Warning: t-table does not extend up to the specified degree'
                #print '         of freedom, dof=%i used instead.' % bigdof
                idof = self.ndof - 1
        # get index of prob
        ip = int(round((prob - 0.5) * 200.0))
        return idof, ip
    def accuracy(self, dof):
        tacc = 10.0 * 1.0 / self.nt
        if dof >= self.ndof:
            #print 'Warning: t-table does not extend up to the specified degree'
            #print '         of freedom, dof=%i used instead.' % bigdof
            dof = bigdof
        if dof == 1:
            tacc *= 10.0
        return tacc
    def save(self, filename = '/tmp/t_table.pickle'):
        pickle.dump(self, file(filename, 'w'), 1)


def make_t_table(ndof, nt):
    print 'Making t-table.  This may take a while...'
    p = N.zeros((ndof,nt), N.Float32)
    d = N.zeros((ndof))
    t = N.zeros((ndof,nt), N.Float32)
    print 'df(0-%i):'%(ndof-1),
    for df in range(ndof):
        print df,
        sys.stdout.flush()
        if df == ndof-1:
            dof = bigdof
        else:
            dof = df+1
        d[df] = dof
        for ti in range(0, nt):
            tin = 10.0 * ti/float(nt)
            if dof == 1:
                tin *= 10.0
            p[df,ti] = prob(dof, tin)
            t[df,ti] = tin
    print
    print 'df(0-%i):'%(ndof-1),
    pdiff = 0.01
    table = N.zeros((ndof, 100, 3), N.Float32)
    for df in range(ndof):
        print df,
        sys.stdout.flush()
        if df == ndof-1: dof = bigdof
        else: dof = df+1
        sorted_indices = N.argsort(p[df])
        pthis = N.take(p[df], sorted_indices)
        tthis = N.take(t[df], sorted_indices)
        pindex = 0
        for pcurrentindex in range(100):
            if pindex >= nt:
                table[df, pcurrentindex] = (-99.9, -99.9, -99.9)
                continue
            pcurrent = pcurrentindex/200.0 + 0.5
            pdelta_old = 100.0
            while 1:
                #print 'pindex =', pindex
                ptest = pthis[pindex]
                pdelta = abs(ptest - pcurrent)
                #print 'pdelta, pdelta_old', pdelta, pdelta_old
                #print 'dof, pcurrent, pthis[pindex] =', dof, pcurrent, pthis[pindex]
                if pdelta < pdiff and pdelta < pdelta_old:
                    #print 'table[df, pcurrentindex] =', table[df, pcurrentindex]
                    #print 'pcurrent, pthis[pindex], tthis[pindex] =', pcurrent, pthis[pindex], tthis[pindex]
                    table[df, pcurrentindex] = (dof, pthis[pindex], tthis[pindex])
                    pindex += 1
                else:
                    pindex += 1
                    if pdelta > pdelta_old:
                        pindex = max(0, pindex-2)
                        break
                if pdelta < pdelta_old:
                    pdelta_old = pdelta
                if pindex >= nt: break
    print
    #print 't(2, 0.8)  = table[1, 60] =', table[1, 60]
    #print 't(3, 0.95) = table[2, 90] =', table[2, 90]
    #print 't(17, 0.99) = table[16, 98] =', table[16, 98]
    #print 't(22, 0.65) = table[21, 30] =', table[21, 30]
    return table
