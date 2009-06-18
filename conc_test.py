import numpy as N
from math import pi, log10
from ppgplot_spb import *

pgend()

def conc_test_exp():
    r = N.arange(10000) / 50.0  # 0 to 200" in steps of 0.02 arcsec
    # exponential SB profile with 15" scalelength
    print 'normal exponential'
    rs = 15.0
    g1 = 75.0*N.exp(-r/rs)  # exponential SB profile with rs=15"
    conc(r, g1)
    # increase SB in outer region by 50 per cent
    print 'exponential with increased outer'
    g2 = increase(r, g1, 3*rs, 10*rs, 1.50)
    conc(r, g2)
    # increase SB in middle region by 50 per cent
    print 'exponential with increased middle'
    g3 = increase(r, g1, 1*rs, 3*rs, 1.50)
    conc(r, g3)
    # increase SB in central region by 50 per cent
    print 'exponential with increased centre'
    g4 = increase(r, g1, 0*rs, 1*rs, 1.50)
    conc(r, g4)
    # plot
    plot_conc(r, (g1, g2, g3, g4), 'exp_conc_test')

def conc_test_dev():
    r = N.arange(10000) / 10.0  # 0 to 1000" in steps of 0.1 arcsec
    # deV SB profile with 15" effective radius
    print 'normal deV'
    re = 15.0
    g1 = 5*N.exp(-7.67*((r/re)**0.25 - 1))  # deV SB profile with re=15"
    conc(r, g1)
    # increase SB in outer region by 50 per cent
    print 'deV with increased outer'
    g2 = increase(r, g1, 3.0*re, 10*re, 1.50)
    conc(r, g2)
    # increase SB in middle region by 50 per cent
    print 'deV with increased middle'
    g3 = increase(r, g1, 0.5*re, 3*re, 1.50)
    conc(r, g3)
    # increase SB in central region by 50 per cent
    print 'deV with increased centre'
    g4 = increase(r, g1, 0*re, 0.5*re, 1.50)
    conc(r, g4)
    # plot
    plot_conc(r, (g1, g2, g3, g4), 'dev_conc_test')

def increase(r, g, minr, maxr, factor):
    gnew = g.copy()
    gnew[r.searchsorted(minr):r.searchsorted(maxr)] *= factor
    return gnew

def conc(r, g, plot=True):
    gw = integrate_profile(r, g)
    gws = gw/gw[-1]
    r20 = r[gws.searchsorted(0.2)]
    r80 = r[gws.searchsorted(0.8)]
    C = 5 * log10(r80/r20)
    print 'r20 = %.2f, r80 = %.2f, C = %.2f'%(r20, r80, C)

def integrate_profile(r, x):
    y = 2*pi*r*(r[1]-r[0])*x
    return [(y[:i].sum() + 0.5*y[i]) for i in range(len(y))]

def plot_conc(r, g, f):
    pgopen('%s.ps/cps'%f)
    pgsetup(2)
    col = ['black', 'red', 'blue', 'green']
    pgenv(0.0, 100.0, -2.0, 2.0)
    pglab('r', 'log surface brightness profile', '')
    for i, gi in enumerate(g):
        pgxsci(col[i])
        pgline(r, N.log10(gi)-0.5*i)
        pgsci(1)
    pgenv(0.0, 100.0, 0.0, 1.1)
    pglab('r', 'fractional luminosity inside r', '')
    gw = [integrate_profile(r, gi) for gi in g]
    gws = [gwi/gwi[-1] for gwi in gw]
    for i, gwsi in enumerate(gws):
        pgxsci(col[i])
        pgline(r, gwsi)
        r20 = r[gwsi.searchsorted(0.2)]
        r80 = r[gwsi.searchsorted(0.8)]
        C = 5 * log10(r80/r20)
        pgtext(75, 0.75-0.1*i, 'C = %.2f'%C)
        pgxsls('dotted')
        pgline(N.array([r20, r20]), N.array([0.0, 1.5]))
        pgline(N.array([r80, r80]), N.array([0.0, 1.5]))
        pgxsls('solid')
        pgsci(1)
    pgclos()
