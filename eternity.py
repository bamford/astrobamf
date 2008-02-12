import numpy as N
u = N.random.uniform


def r(n):
    # create 4 random integer numbers between 0 and n-1 inclusive
    return u(0, n, 4).astype(N.int)


def generate_all(n):
    # discover all possible configurations of n*n different elements
    # in an n*n array by brute force
    a = N.arange(n*n)
    a = a.reshape((n,n))
    c = []
    print 'Starting array:'
    print a
    nrepeat = 0
    ntry = 0
    nnotify = 100
    while True:
        ntry += 1
        if ntry/float(nnotify) - int(ntry/nnotify) < 1.0/(nnotify+1):
            print 'Tried %i, found %i'%(ntry, len(c))
        # swap two random elements
        i1, i2, j1, j2 = r(n)
        tmp = a[j1, j2]
        a[j1, j2] = a[i1, i2]
        a[i1, i2] = tmp
        repeat = False
        for b in c:
            if N.all(a==b):
                repeat=True
                break
        if repeat:
            nrepeat += 1
            if nrepeat > max(n**3, ntry/2):
                break
        else:
            c.append(a.copy())
            nrepeat = 0
    print 'Found %i configurations'%len(c),
    print 'in %i tries'%ntry
