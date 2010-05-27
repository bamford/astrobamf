# Approximations to Poisson upper and lower limits
# presently only for 1-sigma confidence limits
# from Gehrels 1986.
# Could extend to general CI using Ebeling 2003/4 (astro-ph/0301285),
# which builds from Gehrels 1986.

import numpy as N

def upper_limit_1_sigma(n):
    return (n+1.0)*(1.0 - 1.0/(9.0*(n+1.0)) + 1.0/(3.0*N.sqrt(n+1.0)))**3    

def lower_limit_1_sigma(n):
    return n*(1.0 - 1.0/(9.0*n) - 1.0/(3.0*N.sqrt(n)))**3

# def ebeling_upper_limit(n, S):
#     bi = N.array([)
#     c01 = 0.50688
#     c02 = 2.27532
#     c1i = N.array([...])
#     c2i = N.array([...])
#     c3i = N.array([...])
#     c4i = N.array([...])
#     b = 0.0
#     for i in range(8):
#     	b += bi[i] * S**i
#     c = 0.0
#     if S <= S01:
# 	for i in range(4):
# 	    c += c1i[i] * (1.0/(S-S01))**i
#     if S > S01 and S <= 1.2:
# 	for i in range(4):
# 	    c += c2i[i] * (N.log10(S-S01))**i
#     if S > 1.2 and S <= S02:
# 	for i in range(3):
# 	    c += c3i[i] * (1.0/(S-S02))**i
#     if S > S02:
# 	for i in range(7):
# 	    c += c4i[i] * (N.log10(S-S02))**i
#     return (n+1)*(1 - 1/(9*(n+1)) + S/(3*sqrt(n+1)) + b*(n+1)**c)**3
