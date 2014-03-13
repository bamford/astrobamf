import numpy
import pylab
from numpy.random import poisson, binomial
from scipy.stats import scoreatpercentile, beta
from numpy import median, searchsorted
import pylab
from math import sqrt

def check_yara_errors(Nb_true=5, Ntot_true=15, Nsamp=10000,
                      tot_first=True, gehrels_poisson=True, upper=False):

    Na_true = Ntot_true - Nb_true
    f_true = Nb_true/float(Ntot_true)

    if tot_first:
        # determine total number first using Poisson statistics,
        # then split between a and b using Binomial statistics
        Ntot = poisson(Na_true+Nb_true, Nsamp)
        Nb = numpy.zeros(Nsamp, numpy.float)
        ok = (Ntot > 0).nonzero()[0]
        Nok = len(ok)
        Nb[ok] = binomial(Ntot[ok], f_true, Nok).astype(numpy.float)
        Ntot = Ntot.astype(numpy.float)
        Na = Ntot - Nb
    else:
        # treat counts of a and b as independent Poisson processes
        Na = poisson(Na_true, Nsamp).astype(numpy.float)
        Nb = poisson(Nb_true, Nsamp).astype(numpy.float)
        Ntot = Na + Nb
        ok = (Ntot > 0).nonzero()[0]
        Nok = len(ok)

    # ignore events with no counts at all
    Na = Na[ok]
    Nb = Nb[ok]
    Ntot = Ntot[ok]
    
    f = Nb/Ntot  # measured fractions
    # measured rms uncertainty, using known true fraction:
    rmsf_empirical = numpy.sqrt(((f - f_true)**2).mean())
    # measured confidence interval uncertainty, using known true fraction:
    if upper:
        sf_empirical = scoreatpercentile(f, 84.13) - f_true
    else:
        sf_empirical = f_true - scoreatpercentile(f, 15.87)
    
    if gehrels_poisson:
        # use gehrels more accurate approximation to Poisson confidence intervals
        if upper:
            sNb = upper_limit_1_sigma(Nb) - Nb
            sNa = Na - lower_limit_1_sigma(Na)
            sNtot =  Ntot - lower_limit_1_sigma(Ntot)
        else:
            sNb = Nb - lower_limit_1_sigma(Nb)
            sNa = upper_limit_1_sigma(Na) - Na
            sNtot = upper_limit_1_sigma(Ntot) - Ntot
    else:
        # just use sqrt(N)
        sNb = numpy.sqrt(Nb)
        sNa = numpy.sqrt(Na)
        sNtot = numpy.sqrt(Ntot)

    if Nsamp <= 10:  # for debugging
        print Nb
        print Na
        print Ntot
        print sNb
        print sNa
        print sNtot

    # estimated uncertainty using gehrels Poisson+Binomial approximation:
    if upper:
        sf_gehrels = (fraction_upper_limit_1_sigma(Nb, Na) - f).mean()
    else:
        sf_gehrels = (f - fraction_lower_limit_1_sigma(Nb, Na)).mean()

    # estimated uncertainty using Yara's formula:
    sf_yara = f**2 * ((sNb/Nb)**2 + (sNtot/Ntot)**2 - 2*sNb*sNtot/(Nb*Ntot))
    sf_yara[Nb == 0] = 0
    sf_yara[sf_yara < 0] = 0
    sf_yara = numpy.sqrt(sf_yara).mean()

    # estimated uncertainty using Steven's formula treating a and b as independent:
    sf_steven = (numpy.sqrt(Nb**2*sNa**2 + Na**2*sNb**2)/(Na+Nb)**2).mean()

    return sf_empirical, sf_gehrels, sf_yara, sf_steven


# Approximations to Poisson upper and lower limits
# presently only for 1-sigma confidence limits
# from Gehrels 1986.
# Could extend to general CI using Ebeling 2003/4 (astro-ph/0301285),
# which builds from Gehrels 1986.

def upper_limit_1_sigma(n):
    return (n+1.0)*(1.0 - 1.0/(9.0*(n+1.0)) + 1.0/(3.0*numpy.sqrt(n+1.0)))**3    

def lower_limit_1_sigma(n):
    limit = n*(1.0 - 1.0/(9.0*n) - 1.0/(3.0*numpy.sqrt(n)))**3
    limit[n == 0] = 0
    return limit

def fraction_upper_limit_1_sigma(n1, n2):
    CL = 0.8413
    h = 2 / (1.0/(2*n2-1) + 1.0/(2*n1+1))
    l = (1 - 3)/6.0
    w = numpy.sqrt(h+l)/h + (1.0/(2*n2-1) - 1.0/(2*n1+1)) * (l + 5.0/6.0 - 2.0/(3.0*h))
    eps = 0.0
    limit = ((n1+1)*numpy.exp(2*w) + eps*n2) / ((n1+1)*numpy.exp(2*w) + n2)
    limit[n2 == 1] = CL**(1.0/(n1+n2))
    limit[n1 == 0] = 1-(1-CL)**(1.0/n2)
    limit[n2 == 0] = 1.0
    limit[n1+n2 == 0] = 0
    return limit

def fraction_lower_limit_1_sigma(n1, n2):
    limit = 1 - fraction_upper_limit_1_sigma(n2, n1)
    limit[n1 == 0] = 0
    return limit    

def check_gehrels():
    n = numpy.arange(1000)
    u = upper_limit_1_sigma(n) - n
    l = n - lower_limit_1_sigma(n)
    s = numpy.sqrt(n)
    pylab.plot(n, s, '-')
    pylab.plot(n, l, '--')
    pylab.plot(n, u, ':')

def exact_ci(obsNb, obsNtot, Nsamp=10000, plot=False):
    # numerically calculate the exact 1 and 2 sigma confidence
    # intervals for Nb/Ntot given observed values of Nb and Ntot
    sNtot = int(7*sqrt(obsNtot+1))
    sNb = int(7*sqrt(obsNb+1))
    weight = []
    frac = []
    for testNtot in range(max(1, obsNtot - sNtot), obsNtot + sNtot):
        for testNb in range(max(0, obsNb - sNb), obsNb + sNb):
            if testNb > testNtot: continue
            f = testNb/float(testNtot)
            Ntot = poisson(testNtot, Nsamp)
            Nb = numpy.zeros(Nsamp, numpy.float)
            ok = (Ntot > 0).nonzero()[0]
            Nok = len(ok)
            Nb[ok] = binomial(Ntot[ok], f, Nok).astype(numpy.float)
            Ntot = Ntot.astype(numpy.float)
            match = ((obsNb == Nb) & (obsNtot == Ntot)).nonzero()[0]
            w = len(match)/float(Nsamp)
            frac.append(f)
            weight.append(w)
    weight = numpy.array(weight)
    frac = numpy.array(frac)
    args = numpy.argsort(frac)
    frac = frac[args]
    weight = weight[args]
    cumweight = weight.cumsum()
    cumweight /= cumweight[-1]
    arglow = searchsorted(cumweight, 0.1587)
    arghigh = searchsorted(cumweight, 0.8413)
    flow1 = frac[arglow]
    fhigh1 = frac[arghigh]
    arglow = searchsorted(cumweight, 0.0228)
    arghigh = searchsorted(cumweight, 0.9772)
    flow2 = frac[arglow]
    fhigh2 = frac[arghigh]
    if plot:
        pylab.figure()
        h = pylab.hist(frac, 50, weights=weight, histtype='step')
        ymax = h[0].max()
        pylab.vlines(flow, 0, ymax, linestyles='dashed')
        pylab.vlines(fhigh, 0, ymax, linestyles='dashed')
    return flow1, fhigh1, flow2, fhigh2
    
def plot_check(Ntot=9):
    f = numpy.zeros(Ntot+1)
    l = numpy.zeros((3, Ntot+1, 4))
    u = numpy.zeros((3, Ntot+1, 4))
    le = numpy.zeros((2, Ntot+1))
    ue = numpy.zeros((2, Ntot+1))
    lb = numpy.zeros((2, Ntot+1))
    ub = numpy.zeros((2, Ntot+1))
    Nb = numpy.arange(Ntot+1)
    for i in Nb:
        f[i] = float(i)/Ntot
        l[0, i] = check_yara_errors(Nb_true=i, Ntot_true=Ntot, tot_first=True,
                                 gehrels_poisson=True, upper=False)
        l[0, i] = f[i] - l[0, i]
        u[0, i] = check_yara_errors(Nb_true=i, Ntot_true=Ntot, tot_first=True,
                                 gehrels_poisson=True, upper=True)
        u[0, i] = f[i] + u[0, i]
        l[1, i] = check_yara_errors(Nb_true=i, Ntot_true=Ntot, tot_first=True,
                                 gehrels_poisson=False, upper=False)
        l[1, i] = f[i] - l[1, i]
        u[1, i] = check_yara_errors(Nb_true=i, Ntot_true=Ntot, tot_first=True,
                                 gehrels_poisson=False, upper=True)
        u[1, i] = f[i] + u[1, i]
        l[2, i] = check_yara_errors(Nb_true=i, Ntot_true=Ntot, tot_first=False,
                                 gehrels_poisson=True, upper=False)
        l[2, i] = f[i] - l[2, i]
        u[2, i] = check_yara_errors(Nb_true=i, Ntot_true=Ntot, tot_first=False,
                                 gehrels_poisson=True, upper=True)
        u[2, i] = f[i] + u[2, i]
        le[0,i], ue[0,i], le[1,i], ue[1,i] = exact_ci(i, Ntot)
        lb[0,i] = beta.ppf(0.1587, i+1, Ntot-i+1)
        ub[0,i] = beta.ppf(0.8413, i+1, Ntot-i+1)
        lb[1,i] = beta.ppf(0.0228, i+1, Ntot-i+1)
        ub[1,i] = beta.ppf(0.9772, i+1, Ntot-i+1)

    pylab.figure()
    for i in Nb:
        pylab.plot([i-0.3, i+0.3], [f[i], f[i]], '-k')
        pylab.plot([i-0.3, i+0.3], [le[0,i], le[0,i]], '--k')
        pylab.plot([i-0.3, i+0.3], [ue[0,i], ue[0,i]], '--k')
        pylab.plot([i-0.3, i+0.3], [le[1,i], le[1,i]], ':k')
        pylab.plot([i-0.3, i+0.3], [ue[1,i], ue[1,i]], ':k')
        
    yara_sqrt = pylab.plot(Nb, l[1,:,2], 'o',
               markeredgecolor='green', markerfacecolor='white') # yara sqrt
    pylab.plot(Nb, u[1,:,2], 'o',
               markeredgecolor='green', markerfacecolor='white') # yara sqrt
    steven_sqrt = pylab.plot(Nb, l[1,:,3], 's',
               markeredgecolor='blue', markerfacecolor='white') # steven sqrt
    pylab.plot(Nb, u[1,:,3], 's',
               markeredgecolor='blue', markerfacecolor='white') # steven sqrt
    yara_asym = pylab.plot(Nb, l[0,:,2], 'og') # yara asym
    pylab.plot(Nb, u[0,:,2], 'og') # yara asym
    steven_asym = pylab.plot(Nb, l[0,:,3], 'sb') # steven asym
    pylab.plot(Nb, u[0,:,3], 'sb') # steven asym
    empirical = pylab.plot(Nb, l[0,:,0], '*k') # empirical
    pylab.plot(Nb, u[0,:,0], '*k') # empirical
    gehrels = pylab.plot(Nb, l[0,:,1], 'xr') # gehrels
    pylab.plot(Nb, u[0,:,1], 'xr') # gehrels
    betafn = pylab.plot(Nb, lb[0], 'v',
                        markeredgecolor='purple', markerfacecolor='purple') # beta
    pylab.plot(Nb, ub[0], 'v',
               markeredgecolor='purple', markerfacecolor='purple') # beta
    betafn2s = pylab.plot(Nb, lb[1], 'v',
                          markeredgecolor='purple', markerfacecolor='white') # beta
    pylab.plot(Nb, ub[1], 'v',
               markeredgecolor='purple', markerfacecolor='white') # beta

    leg = pylab.legend((empirical, gehrels, steven_asym, yara_asym,
                        steven_sqrt, yara_sqrt, betafn),
                       ('empirical', 'gehrels', 'steven asym', 'yara asym',
                        'steven sqrt', 'yara sqrt', 'beta'),
                       numpoints=1, loc='upper left', frameon=False,
                       labelspacing=0.2, handletextpad=0.0, borderaxespad=0.2)
    for t in leg.get_texts():
        t.set_fontsize('small')
        t.set_y(6.0)
    pylab.axis((-1, Ntot+1, -0.2, 1.2))
    pylab.savefig('check_yara_errors.pdf')
