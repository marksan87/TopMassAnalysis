#!/usr/bin/env python
from ROOT import *
from array import array
import pickle

masses = [165.5, 169.5, 171.5, 172.5, 173.5, 175.5, 178.5]
#toppt_m1_rec = [ (69.488562, 0.094977), (70.242693, 0.097783), (70.588405, 0.100271), (70.792389, 0.101122), (71.181537, 0.102683), (71.555042, 0.104888), (72.101318, 0.108589) ]
#toppt_m2_rec = [ (6041.681366, 15.517344), (6150.125760, 16.052418), (6213.443249, 16.523008), (6245.093778, 16.680706), (6312.259246, 17.011982), (6374.307679, 17.424556), (6467.385716, 18.162967) ]

moments = pickle.load(open("moments_Mll_sys_TopPtReweight_cut_300.pkl",'rb'))
toppt_m1_rec = moments["sysUp"]["m1"]["rec"]
toppt_m2_rec = moments["sysUp"]["m2"]["rec"]

mt = array('f',masses)
zeros = array('f',[0.] * len(masses))
m1rec = array('f', [toppt_m1_rec[i][0] for i in xrange(len(toppt_m1_rec))] )
m1rec_err = array('f', [toppt_m1_rec[i][1] for i in xrange(len(toppt_m1_rec))] )
m2rec = array('f', [toppt_m2_rec[i][0] for i in xrange(len(toppt_m2_rec))] )
m2rec_err = array('f', [toppt_m2_rec[i][1] for i in xrange(len(toppt_m2_rec))] )
m1G = TGraphErrors(len(masses), mt, m1rec, zeros, m1rec_err)
m2G = TGraphErrors(len(masses), mt, m2rec, zeros, m2rec_err)

m1G.Fit("pol1")
m2G.Fit("pol1")
f1 = m1G.GetFunction("pol1")
f2 = m2G.GetFunction("pol1")


m1_p0 = f1.GetParameter(0)
m1_p1 = f1.GetParameter(1)

m2_p0 = f2.GetParameter(0)
m2_p1 = f2.GetParameter(1)

# Moments of mt1725 nominal 
nominal_m1 = 112.867940 
nominal_m2 = 16257.580313 

# Extracted masses from mt1725 nominal
# ptll
#mass_m1 = 172.236189
#mass_m2 = 172.142386
# Mll
mass_m1 = 172.656479
mass_m2 = 172.552005


topptsys_m1 = (nominal_m1 - m1_p0) / m1_p1
topptsys_m2 = (nominal_m2 - m2_p0) / m2_p1

unc_m1 = mass_m1 - topptsys_m1
unc_m2 = mass_m2 - topptsys_m2

print "toppt systematic uncertainty"
print "moment 1:  %f" % unc_m1
print "moment 2:  %f" % unc_m2



#puUp_m1 = 74.145409
#puUp_m2 = 7260.422952
#puDn_m1 = 74.083493
#puDn_m2 = 7248.710121
#nom_m1_p0 = 27.2881
#nom_m1_p1 = 0.268818
#nom_m2_p0 = -1563.65
#nom_m2_p1 = 51.0489

"""
puUp_m1 = 70.985732 
puUp_m2 = 6283.977842
puDn_m1 = 70.943465
puDn_m2 = 6276.327963

nom_m1_p0 = 33.143572 
nom_m1_p1 = 0.219585
nom_m2_p0 = 57.068095
nom_m2_p1 = 36.150362

puUp_sys_m1 = (puUp_m1 - nom_m1_p0) / nom_m1_p1
puUp_sys_m2 = (puUp_m2 - nom_m2_p0) / nom_m2_p1

puDn_sys_m1 = (puDn_m1 - nom_m1_p0) / nom_m1_p1
puDn_sys_m2 = (puDn_m2 - nom_m2_p0) / nom_m2_p1

print "pileupUp m1 extracted mt:", puUp_sys_m1
print "pileupDn m1 extracted mt:", puDn_sys_m1

print "pileupUp m2 extracted mt:", puUp_sys_m2
print "pileupDn m2 extracted mt:", puDn_sys_m2


puUpUnc_m1 = puUp_sys_m1 - mass_m1
puUpUnc_m2 = puUp_sys_m2 - mass_m2

puDnUnc_m1 = puDn_sys_m1 - mass_m1
puDnUnc_m2 = puDn_sys_m2 - mass_m2

print "pileup uncertainty\tup / down"
print "moment 1:  %f / %f" % (puUpUnc_m1, puDnUnc_m1)
print "moment 2:  %f / %f" % (puUpUnc_m2, puDnUnc_m2)
"""
