#!/usr/bin/env python
from ROOT import * 
from numpy import mean, std
from array import array
import sys
import os

def createToyMoments(tree, obs, cut, npoints = 50000, ntoys = 10000, m = "172_5"):
    rand = TRandom3(0)
    maxEvt = tree.GetEntriesFast()
    toyPts = {}

    m1_rec = 0.
    m1_rec_unc = 0.
    m2_rec = 0.
    m2_rec_unc = 0.
    m4_rec = 0.
    weight = 0.
    h = TH1D("mt%s" % m, "", 4, -0.5, 3.5)
    #h.Sumw2()
    while len(toyPts) < npoints:
        evt = rand.Integer(maxEvt) + 1
        if evt not in toyPts:
            tree.GetEntry(evt)
            if eval("tree.rec_%s" % obs) > cut: continue
            exec("toyPts[evt] = {'%s':tree.rec_%s, 'weight':tree.weight}" % (obs,obs))
            m1_rec += eval("toyPts[evt]['%s'] * toyPts[evt]['weight']" % obs)
            m2_rec += eval("toyPts[evt]['%s']**2 * toyPts[evt]['weight']" % obs)
            m4_rec += eval("toyPts[evt]['%s']**4 * toyPts[evt]['weight']" % obs)
            weight += toyPts[evt]["weight"]

            h.Fill(0, toyPts[evt]["weight"])
            h.Fill(1, eval("toyPts[evt]['%s'] * toyPts[evt]['weight']" % obs))
            h.Fill(2, eval("toyPts[evt]['%s']**2 * toyPts[evt]['weight']" % obs))

    m1_rec /= weight
    m2_rec /= weight
    m4_rec /= weight

    m1_rec_unc = ( (m2_rec - m1_rec**2) / weight)**0.5
    m2_rec_unc = ( (m4_rec - m2_rec**2) / weight)**0.5

    print "len(toyPts) = ", len(toyPts) 

    print "\tSums\t\t\t\tHist"
    print "Weight\t%f\t\t\t%f" % (weight, h.GetBinContent(1))
    h.Scale(1. / h.GetBinContent(1))
    print "m1\t%f   +- %f\t\t%f   +- %f" % (m1_rec, m1_rec_unc, h.GetBinContent(2), h.GetBinError(2))
    print "m2\t%f +- %f\t%f +- %f" % (m2_rec, m2_rec_unc, h.GetBinContent(3), h.GetBinError(3))
   
    m1toys = TH1D("mt%s-moment1"%m, "mt %s moment1 toys" % m.replace("_","."), 100, -5., 5.)
    m2toys = TH1D("mt%s-moment2"%m, "mt %s moment2 toys" % m.replace("_","."), 100, -5., 5.)

    m1toylist = []
    m2toylist = []
    for n in xrange(ntoys):
        m1toylist.append(rand.Gaus(m1_rec, m1_rec_unc))
        m2toylist.append(rand.Gaus(m2_rec, m2_rec_unc))

        m1toys.Fill((m1toylist[-1] - m1_rec) / m1_rec_unc)
        m2toys.Fill((m2toylist[-1] - m2_rec) / m2_rec_unc)
    
    print "\nToys"
    print "Residual m1: %f  +- %f" % (mean(m1toylist) - m1_rec, std(m1toylist))
    print "Residual m2: %f  +- %f" % (mean(m2toylist) - m2_rec, std(m2toylist))

    return m1toys,m2toys, [m1_rec, m1_rec_unc], [m2_rec, m2_rec_unc]


def createToyMomentsOld(tree, obs, cut, npoints = 50000, ntoys = 10000, m = "172_5"):
    rand = TRandom3(0)
    maxEvt = tree.GetEntriesFast()
    toyPts = {}

    m1_rec = 0.
    m1_rec_unc = 0.
    m2_rec = 0.
    m2_rec_unc = 0.
    m4_rec = 0.
    weight = 0.
    h = TH1D("mt%s" % m, "", 4, -0.5, 3.5)
    #h.Sumw2()
    while len(toyPts) < npoints:
        evt = rand.Integer(maxEvt) + 1
        if evt not in toyPts:
            tree.GetEntry(evt)
            if eval("tree.rec_%s" % obs) > cut: continue
            exec("toyPts[evt] = {'%s':tree.rec_%s, 'weight':tree.weight}" % (obs,obs))
            m1_rec += eval("toyPts[evt]['%s'] * toyPts[evt]['weight']" % obs)
            m2_rec += eval("toyPts[evt]['%s']**2 * toyPts[evt]['weight']" % obs)
            m4_rec += eval("toyPts[evt]['%s']**4 * toyPts[evt]['weight']" % obs)
            weight += toyPts[evt]["weight"]

            h.Fill(0, toyPts[evt]["weight"])
            h.Fill(1, eval("toyPts[evt]['%s'] * toyPts[evt]['weight']" % obs))
            h.Fill(2, eval("toyPts[evt]['%s']**2 * toyPts[evt]['weight']" % obs))

    m1_rec /= weight
    m2_rec /= weight
    m4_rec /= weight

    m1_rec_unc = ( (m2_rec - m1_rec**2) / weight)**0.5
    m2_rec_unc = ( (m4_rec - m2_rec**2) / weight)**0.5

    print "len(toyPts) = ", len(toyPts) 

    print "\tSums\t\t\t\tHist"
    print "Weight\t%f\t\t\t%f" % (weight, h.GetBinContent(1))
    h.Scale(1. / h.GetBinContent(1))
    print "m1\t%f   +- %f\t\t%f   +- %f" % (m1_rec, m1_rec_unc, h.GetBinContent(2), h.GetBinError(2))
    print "m2\t%f +- %f\t%f +- %f" % (m2_rec, m2_rec_unc, h.GetBinContent(3), h.GetBinError(3))
   
    m1toys = TH1D("mt%s-moment1"%m, "mt %s moment1 toys" % m.replace("_","."), 100, -5., 5.)
    m2toys = TH1D("mt%s-moment2"%m, "mt %s moment2 toys" % m.replace("_","."), 100, -5., 5.)

    m1toylist = []
    m2toylist = []
    for n in xrange(ntoys):
        m1toylist.append(rand.Gaus(m1_rec, m1_rec_unc))
        m2toylist.append(rand.Gaus(m2_rec, m2_rec_unc))

        m1toys.Fill((m1toylist[-1] - m1_rec) / m1_rec_unc)
        m2toys.Fill((m2toylist[-1] - m2_rec) / m2_rec_unc)
    
    print "\nToys"
    print "Residual m1: %f  +- %f" % (mean(m1toylist) - m1_rec, std(m1toylist))
    print "Residual m2: %f  +- %f" % (mean(m2toylist) - m2_rec, std(m2toylist))

    return m1toys,m2toys, [m1_rec, m1_rec_unc], [m2_rec, m2_rec_unc]
