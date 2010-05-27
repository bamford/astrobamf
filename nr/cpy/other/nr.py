# This file was created automatically by SWIG.
# Don't modify this file, modify the SWIG interface instead.
# This file is compatible with both classic and new-style classes.

import _nr

def _swig_setattr(self,class_type,name,value):
    if (name == "this"):
        if isinstance(value, class_type):
            self.__dict__[name] = value.this
            if hasattr(value,"thisown"): self.__dict__["thisown"] = value.thisown
            del value.thisown
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    self.__dict__[name] = value

def _swig_getattr(self,class_type,name):
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError,name

import types
try:
    _object = types.ObjectType
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0
del types


class fcomplex(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, fcomplex, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, fcomplex, name)
    def __repr__(self):
        return "<C fcomplex instance at %s>" % (self.this,)
    __swig_setmethods__["r"] = _nr.fcomplex_r_set
    __swig_getmethods__["r"] = _nr.fcomplex_r_get
    if _newclass:r = property(_nr.fcomplex_r_get, _nr.fcomplex_r_set)
    __swig_setmethods__["i"] = _nr.fcomplex_i_set
    __swig_getmethods__["i"] = _nr.fcomplex_i_get
    if _newclass:i = property(_nr.fcomplex_i_get, _nr.fcomplex_i_set)
    def __init__(self, *args):
        _swig_setattr(self, fcomplex, 'this', _nr.new_fcomplex(*args))
        _swig_setattr(self, fcomplex, 'thisown', 1)
    def __del__(self, destroy=_nr.delete_fcomplex):
        try:
            if self.thisown: destroy(self)
        except: pass

class fcomplexPtr(fcomplex):
    def __init__(self, this):
        _swig_setattr(self, fcomplex, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, fcomplex, 'thisown', 0)
        _swig_setattr(self, fcomplex,self.__class__,fcomplex)
_nr.fcomplex_swigregister(fcomplexPtr)

class arithcode(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, arithcode, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, arithcode, name)
    def __repr__(self):
        return "<C arithcode instance at %s>" % (self.this,)
    __swig_setmethods__["ilob"] = _nr.arithcode_ilob_set
    __swig_getmethods__["ilob"] = _nr.arithcode_ilob_get
    if _newclass:ilob = property(_nr.arithcode_ilob_get, _nr.arithcode_ilob_set)
    __swig_setmethods__["iupb"] = _nr.arithcode_iupb_set
    __swig_getmethods__["iupb"] = _nr.arithcode_iupb_get
    if _newclass:iupb = property(_nr.arithcode_iupb_get, _nr.arithcode_iupb_set)
    __swig_setmethods__["ncumfq"] = _nr.arithcode_ncumfq_set
    __swig_getmethods__["ncumfq"] = _nr.arithcode_ncumfq_get
    if _newclass:ncumfq = property(_nr.arithcode_ncumfq_get, _nr.arithcode_ncumfq_set)
    __swig_setmethods__["jdif"] = _nr.arithcode_jdif_set
    __swig_getmethods__["jdif"] = _nr.arithcode_jdif_get
    if _newclass:jdif = property(_nr.arithcode_jdif_get, _nr.arithcode_jdif_set)
    __swig_setmethods__["nc"] = _nr.arithcode_nc_set
    __swig_getmethods__["nc"] = _nr.arithcode_nc_get
    if _newclass:nc = property(_nr.arithcode_nc_get, _nr.arithcode_nc_set)
    __swig_setmethods__["minint"] = _nr.arithcode_minint_set
    __swig_getmethods__["minint"] = _nr.arithcode_minint_get
    if _newclass:minint = property(_nr.arithcode_minint_get, _nr.arithcode_minint_set)
    __swig_setmethods__["nch"] = _nr.arithcode_nch_set
    __swig_getmethods__["nch"] = _nr.arithcode_nch_get
    if _newclass:nch = property(_nr.arithcode_nch_get, _nr.arithcode_nch_set)
    __swig_setmethods__["ncum"] = _nr.arithcode_ncum_set
    __swig_getmethods__["ncum"] = _nr.arithcode_ncum_get
    if _newclass:ncum = property(_nr.arithcode_ncum_get, _nr.arithcode_ncum_set)
    __swig_setmethods__["nrad"] = _nr.arithcode_nrad_set
    __swig_getmethods__["nrad"] = _nr.arithcode_nrad_get
    if _newclass:nrad = property(_nr.arithcode_nrad_get, _nr.arithcode_nrad_set)
    def __init__(self, *args):
        _swig_setattr(self, arithcode, 'this', _nr.new_arithcode(*args))
        _swig_setattr(self, arithcode, 'thisown', 1)
    def __del__(self, destroy=_nr.delete_arithcode):
        try:
            if self.thisown: destroy(self)
        except: pass

class arithcodePtr(arithcode):
    def __init__(self, this):
        _swig_setattr(self, arithcode, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, arithcode, 'thisown', 0)
        _swig_setattr(self, arithcode,self.__class__,arithcode)
_nr.arithcode_swigregister(arithcodePtr)

class huffcode(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, huffcode, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, huffcode, name)
    def __repr__(self):
        return "<C huffcode instance at %s>" % (self.this,)
    __swig_setmethods__["icod"] = _nr.huffcode_icod_set
    __swig_getmethods__["icod"] = _nr.huffcode_icod_get
    if _newclass:icod = property(_nr.huffcode_icod_get, _nr.huffcode_icod_set)
    __swig_setmethods__["ncod"] = _nr.huffcode_ncod_set
    __swig_getmethods__["ncod"] = _nr.huffcode_ncod_get
    if _newclass:ncod = property(_nr.huffcode_ncod_get, _nr.huffcode_ncod_set)
    __swig_setmethods__["left"] = _nr.huffcode_left_set
    __swig_getmethods__["left"] = _nr.huffcode_left_get
    if _newclass:left = property(_nr.huffcode_left_get, _nr.huffcode_left_set)
    __swig_setmethods__["right"] = _nr.huffcode_right_set
    __swig_getmethods__["right"] = _nr.huffcode_right_get
    if _newclass:right = property(_nr.huffcode_right_get, _nr.huffcode_right_set)
    __swig_setmethods__["nch"] = _nr.huffcode_nch_set
    __swig_getmethods__["nch"] = _nr.huffcode_nch_get
    if _newclass:nch = property(_nr.huffcode_nch_get, _nr.huffcode_nch_set)
    __swig_setmethods__["nodemax"] = _nr.huffcode_nodemax_set
    __swig_getmethods__["nodemax"] = _nr.huffcode_nodemax_get
    if _newclass:nodemax = property(_nr.huffcode_nodemax_get, _nr.huffcode_nodemax_set)
    def __init__(self, *args):
        _swig_setattr(self, huffcode, 'this', _nr.new_huffcode(*args))
        _swig_setattr(self, huffcode, 'thisown', 1)
    def __del__(self, destroy=_nr.delete_huffcode):
        try:
            if self.thisown: destroy(self)
        except: pass

class huffcodePtr(huffcode):
    def __init__(self, this):
        _swig_setattr(self, huffcode, 'this', this)
        if not hasattr(self,"thisown"): _swig_setattr(self, huffcode, 'thisown', 0)
        _swig_setattr(self, huffcode,self.__class__,huffcode)
_nr.huffcode_swigregister(huffcodePtr)


addint = _nr.addint

airy = _nr.airy

amebsa = _nr.amebsa

amoeba = _nr.amoeba

amotry = _nr.amotry

amotsa = _nr.amotsa

anneal = _nr.anneal

anorm2 = _nr.anorm2

arcmak = _nr.arcmak

arcode = _nr.arcode

arcsum = _nr.arcsum

asolve = _nr.asolve

atimes = _nr.atimes

avevar = _nr.avevar

balanc = _nr.balanc

banbks = _nr.banbks

bandec = _nr.bandec

banmul = _nr.banmul

bcucof = _nr.bcucof

bcuint = _nr.bcuint

beschb = _nr.beschb

bessi = _nr.bessi

bessi0 = _nr.bessi0

bessi1 = _nr.bessi1

bessik = _nr.bessik

bessj = _nr.bessj

bessj0 = _nr.bessj0

bessj1 = _nr.bessj1

bessjy = _nr.bessjy

bessk = _nr.bessk

bessk0 = _nr.bessk0

bessk1 = _nr.bessk1

bessy = _nr.bessy

bessy0 = _nr.bessy0

bessy1 = _nr.bessy1

beta = _nr.beta

betacf = _nr.betacf

betai = _nr.betai

bico = _nr.bico

bksub = _nr.bksub

bnldev = _nr.bnldev

brent = _nr.brent

broydn = _nr.broydn

bsstep = _nr.bsstep

caldat = _nr.caldat

chder = _nr.chder

chebev = _nr.chebev

chebft = _nr.chebft

chebpc = _nr.chebpc

chint = _nr.chint

chixy = _nr.chixy

choldc = _nr.choldc

cholsl = _nr.cholsl

chsone = _nr.chsone

chstwo = _nr.chstwo

cisi = _nr.cisi

cntab1 = _nr.cntab1

cntab2 = _nr.cntab2

convlv = _nr.convlv

copy = _nr.copy

correl = _nr.correl

cosft = _nr.cosft

cosft1 = _nr.cosft1

cosft2 = _nr.cosft2

covsrt = _nr.covsrt

crank = _nr.crank

cyclic = _nr.cyclic

daub4 = _nr.daub4

dawson = _nr.dawson

dbrent = _nr.dbrent

ddpoly = _nr.ddpoly

decchk = _nr.decchk

derivs = _nr.derivs

df1dim = _nr.df1dim

dfour1 = _nr.dfour1

dfpmin = _nr.dfpmin

dfridr = _nr.dfridr

dftcor = _nr.dftcor

dftint = _nr.dftint

difeq = _nr.difeq

dlinmin = _nr.dlinmin

dpythag = _nr.dpythag

drealft = _nr.drealft

dsprsax = _nr.dsprsax

dsprstx = _nr.dsprstx

dsvbksb = _nr.dsvbksb

dsvdcmp = _nr.dsvdcmp

eclass = _nr.eclass

eclazz = _nr.eclazz

ei = _nr.ei

eigsrt = _nr.eigsrt

elle = _nr.elle

ellf = _nr.ellf

ellpi = _nr.ellpi

elmhes = _nr.elmhes

erfcc = _nr.erfcc

erff = _nr.erff

erffc = _nr.erffc

eulsum = _nr.eulsum

evlmem = _nr.evlmem

expdev = _nr.expdev

expint = _nr.expint

f1 = _nr.f1

f1dim = _nr.f1dim

f2 = _nr.f2

f3 = _nr.f3

factln = _nr.factln

factrl = _nr.factrl

fasper = _nr.fasper

fdjac = _nr.fdjac

fgauss = _nr.fgauss

fill0 = _nr.fill0

fit = _nr.fit

fitexy = _nr.fitexy

fixrts = _nr.fixrts

fleg = _nr.fleg

flmoon = _nr.flmoon

fmin = _nr.fmin

four1 = _nr.four1

fourew = _nr.fourew

fourfs = _nr.fourfs

fourn = _nr.fourn

fpoly = _nr.fpoly

fred2 = _nr.fred2

fredin = _nr.fredin

frenel = _nr.frenel

frprmn = _nr.frprmn

ftest = _nr.ftest

gamdev = _nr.gamdev

gammln = _nr.gammln

gammp = _nr.gammp

gammq = _nr.gammq

gasdev = _nr.gasdev

gaucof = _nr.gaucof

gauher = _nr.gauher

gaujac = _nr.gaujac

gaulag = _nr.gaulag

gauleg = _nr.gauleg

gaussj = _nr.gaussj

gcf = _nr.gcf

golden = _nr.golden

gser = _nr.gser

hpsel = _nr.hpsel

hpsort = _nr.hpsort

hqr = _nr.hqr

hufapp = _nr.hufapp

hufdec = _nr.hufdec

hufenc = _nr.hufenc

hufmak = _nr.hufmak

hunt = _nr.hunt

hypdrv = _nr.hypdrv

hypgeo = _nr.hypgeo

hypser = _nr.hypser

icrc = _nr.icrc

icrc1 = _nr.icrc1

igray = _nr.igray

iindexx = _nr.iindexx

indexx = _nr.indexx

interp = _nr.interp

irbit1 = _nr.irbit1

irbit2 = _nr.irbit2

jacobi = _nr.jacobi

jacobn = _nr.jacobn

julday = _nr.julday

kendl1 = _nr.kendl1

kendl2 = _nr.kendl2

kermom = _nr.kermom

ks2d1s = _nr.ks2d1s

ks2d2s = _nr.ks2d2s

ksone = _nr.ksone

kstwo = _nr.kstwo

laguer = _nr.laguer

lfit = _nr.lfit

linbcg = _nr.linbcg

linmin = _nr.linmin

lnsrch = _nr.lnsrch

load = _nr.load

load1 = _nr.load1

load2 = _nr.load2

locate = _nr.locate

lop = _nr.lop

lubksb = _nr.lubksb

ludcmp = _nr.ludcmp

machar = _nr.machar

matadd = _nr.matadd

matsub = _nr.matsub

medfit = _nr.medfit

memcof = _nr.memcof

metrop = _nr.metrop

mgfas = _nr.mgfas

mglin = _nr.mglin

midexp = _nr.midexp

midinf = _nr.midinf

midpnt = _nr.midpnt

midsql = _nr.midsql

midsqu = _nr.midsqu

miser = _nr.miser

mmid = _nr.mmid

mnbrak = _nr.mnbrak

mnewt = _nr.mnewt

moment = _nr.moment

mp2dfr = _nr.mp2dfr

mpadd = _nr.mpadd

mpdiv = _nr.mpdiv

mpinv = _nr.mpinv

mplsh = _nr.mplsh

mpmov = _nr.mpmov

mpmul = _nr.mpmul

mpneg = _nr.mpneg

mppi = _nr.mppi

mprove = _nr.mprove

mpsad = _nr.mpsad

mpsdv = _nr.mpsdv

mpsmu = _nr.mpsmu

mpsqrt = _nr.mpsqrt

mpsub = _nr.mpsub

mrqcof = _nr.mrqcof

mrqmin = _nr.mrqmin

newt = _nr.newt

odeint = _nr.odeint

orthog = _nr.orthog

pade = _nr.pade

pccheb = _nr.pccheb

pcshft = _nr.pcshft

pearsn = _nr.pearsn

period = _nr.period

piksr2 = _nr.piksr2

piksrt = _nr.piksrt

pinvs = _nr.pinvs

plgndr = _nr.plgndr

poidev = _nr.poidev

polcoe = _nr.polcoe

polcof = _nr.polcof

poldiv = _nr.poldiv

polin2 = _nr.polin2

polint = _nr.polint

powell = _nr.powell

predic = _nr.predic

probks = _nr.probks

psdes = _nr.psdes

pwt = _nr.pwt

pwtset = _nr.pwtset

pythag = _nr.pythag

pzextr = _nr.pzextr

qgaus = _nr.qgaus

qrdcmp = _nr.qrdcmp

qromb = _nr.qromb

qromo = _nr.qromo

qroot = _nr.qroot

qrsolv = _nr.qrsolv

qrupdt = _nr.qrupdt

qsimp = _nr.qsimp

qtrap = _nr.qtrap

quad3d = _nr.quad3d

quadct = _nr.quadct

quadmx = _nr.quadmx

quadvl = _nr.quadvl

ran0 = _nr.ran0

ran1 = _nr.ran1

ran2 = _nr.ran2

ran3 = _nr.ran3

ran4 = _nr.ran4

rank = _nr.rank

ranpt = _nr.ranpt

ratint = _nr.ratint

ratlsq = _nr.ratlsq

ratval = _nr.ratval

rc = _nr.rc

rd = _nr.rd

realft = _nr.realft

rebin = _nr.rebin

red = _nr.red

relax = _nr.relax

relax2 = _nr.relax2

resid = _nr.resid

revcst = _nr.revcst

reverse = _nr.reverse

rf = _nr.rf

rj = _nr.rj

rk4 = _nr.rk4

rkck = _nr.rkck

rkdumb = _nr.rkdumb

rkqs = _nr.rkqs

rlft3 = _nr.rlft3

rofunc = _nr.rofunc

rotate = _nr.rotate

rsolv = _nr.rsolv

rstrct = _nr.rstrct

rtbis = _nr.rtbis

rtflsp = _nr.rtflsp

rtnewt = _nr.rtnewt

rtsafe = _nr.rtsafe

rtsec = _nr.rtsec

rzextr = _nr.rzextr

savgol = _nr.savgol

score = _nr.score

scrsho = _nr.scrsho

select = _nr.select

selip = _nr.selip

shell = _nr.shell

shoot = _nr.shoot

shootf = _nr.shootf

simp1 = _nr.simp1

simp2 = _nr.simp2

simp3 = _nr.simp3

simplx = _nr.simplx

simpr = _nr.simpr

sinft = _nr.sinft

slvsm2 = _nr.slvsm2

slvsml = _nr.slvsml

sncndn = _nr.sncndn

snrm = _nr.snrm

sobseq = _nr.sobseq

solvde = _nr.solvde

sor = _nr.sor

sort = _nr.sort

sort2 = _nr.sort2

sort3 = _nr.sort3

spctrm = _nr.spctrm

spear = _nr.spear

sphbes = _nr.sphbes

splie2 = _nr.splie2

splin2 = _nr.splin2

spline = _nr.spline

splint = _nr.splint

spread = _nr.spread

sprsax = _nr.sprsax

sprsin = _nr.sprsin

sprspm = _nr.sprspm

sprstm = _nr.sprstm

sprstp = _nr.sprstp

sprstx = _nr.sprstx

stifbs = _nr.stifbs

stiff = _nr.stiff

stoerm = _nr.stoerm

svbksb = _nr.svbksb

svdcmp = _nr.svdcmp

svdfit = _nr.svdfit

svdvar = _nr.svdvar

toeplz = _nr.toeplz

tptest = _nr.tptest

tqli = _nr.tqli

trapzd = _nr.trapzd

tred2 = _nr.tred2

tridag = _nr.tridag

trncst = _nr.trncst

trnspt = _nr.trnspt

ttest = _nr.ttest

tutest = _nr.tutest

twofft = _nr.twofft

vander = _nr.vander

vegas = _nr.vegas

voltra = _nr.voltra

wt1 = _nr.wt1

wtn = _nr.wtn

wwghts = _nr.wwghts

zbrac = _nr.zbrac

zbrak = _nr.zbrak

zbrent = _nr.zbrent

zrhqr = _nr.zrhqr

zriddr = _nr.zriddr

zroots = _nr.zroots

