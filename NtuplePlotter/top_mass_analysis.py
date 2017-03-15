#!/usr/bin/env python
from array import array
import optparse
import operator
import os,sys
import json
import pickle
import random
import ROOT
from ROOT import TH1F, TLorentzVector
#from pileup import *
from PyleupRW import PyleupRW
from subprocess import Popen, PIPE

# Needed for b tagging efficency
#ROOT.gSystem.Load('libCondFormatsBTagObjects')
#ROOT.gROOT.ProcessLine('.L plugins/BTagCalibrationStandalone.cc+')
#calib = ROOT.BTagCalibration("csvv2", "CSVv2.csv")

# Second option can be 0, 1, or 2 corresponding to loose, medium, and tight operating points
#reader = ROOT.BTagCalibrationReader(calib, 1, "mujets", "central")
#print reader.eval(0, 1.2, 60)
random.seed()
#ROOT.gSystem.Load('libCondFormatsBTagObjects') 

debug = False 
debug_iter = 100


use_strict_lep_selection = True	    # Require the leading leptons to be an eu pair



def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

STYPE = enum('DOWN', 'NORM', 'UP')
OP = enum('LOOSE', 'MEDIUM', 'TIGHT')
JER_var_type = STYPE.NORM


# Selection Cuts
ele_pt_cut = 25
ele_eta_cut = 2.4

mu_pt_cut = 25
mu_eta_cut = 2.4
mu_relIso_cut = 0.15	# Tight (loose) iso cut = 0.15 (0.25)

jet_pt_cut = 30
jet_eta_cut = 2.4

# TODO: Un-hardcode this...

# Total integrated luminosity for Sep2016 Rereco B-H
luminosity = 35861.0 # 1/pb


###################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/BtagRecommendation80X  #
# B tagging discriminator WPs
# Loose:  0.460   Mistag rate: 10%
# Medium: 0.800   Mistag rate: 1%
# Tight:  0.935   Mistag rate: 0.1%
btag_disc = 0.800

####################################################################################################################
# Cut-based Electron ID Medium WP
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
# 
# cut[barrel, endcap]
# barrel: |eta supercluster| <= 1.479
# endcap: 1.479 < |eta supercluster| < 2.5     
ele_full5x5_sigmaIetaIeta_cut = [0.00998, 0.0298];
ele_dEtaIn_cut = [0.00311, 0.00609];
ele_dPhiIn_cut = [0.103, 0.045];
ele_HoverE_cut = [0.253, 0.0878];
ele_relIso_cut = [0.0695, 0.0821];
ele_ooEmooP_cut = [0.134, 0.13];
ele_d0_cut = [0.05, 0.10];
ele_dz_cut = [0.10, 0.20];
ele_missingInnerHits_cut = [1, 1];
####################################################################################################################

# Region 0: barrel
# Region 1: endcap
def detector_region(SCEta):
    return 0 if abs(SCEta) <= 1.479 else 1

# Veto all electrons whose eta supercluster falls in the transition region
def transition_region_veto(SCEta):
    return False if abs(SCEta) > 1.4442 and abs(SCEta) < 1.5660 else True


# kEleGammaAndNeutralHadronIso03
# Summer16 80X effective areas
# https://github.com/ikrav/cmssw/blob/egm_id_80X_v1/RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt 
def ele_effective_area(SCEta):
    eta = abs(SCEta)
    if eta < 1.0:     return 0.1703
    elif eta < 1.479: return 0.1715
    elif eta < 2.0:   return 0.1213
    elif eta < 2.2:   return 0.1230
    elif eta < 2.3:   return 0.1635
    elif eta < 2.4:   return 0.1937
    else:             return 0.2393


# https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetResolution#JER_Scaling_factors_and_Uncertai
# Core resolution scaling factor SF (measured data/MC resolution ration) for the JER scaling 
# correction method for smearing reconstructed jets
def JER_SF(jetEta, sys_type):
    eta = abs(jetEta)

    corr   = [1.122, 1.167, 1.168, 1.029, 1.115, 1.041, 1.167, 1.094, 1.168]
    corrUp = [1.148, 1.215, 1.214, 1.095, 1.118, 1.103, 1.253, 1.187, 1.288]
    corrDn = [1.096, 1.119, 1.122, 0.963, 1.112, 0.979, 1.081, 1.001, 1.048]

    region = 0
    if eta >= 0.5: region += 1
    if eta >= 0.8: region += 1
    if eta >= 1.1: region += 1
    if eta >= 1.3: region += 1
    if eta >= 1.7: region += 1
    if eta >= 1.9: region += 1
    if eta >= 2.1: region += 1
    if eta >= 2.3: region += 1

    if   sys_type == STYPE.NORM: return corr[region]
    elif sys_type == STYPE.UP:   return corrUp[region]
    elif sys_type == STYPE.DOWN: return corrDn[region]
    else: 
	print "No systematic type selected!"
	return -1

# https://twiki.cern.ch/twiki/bin/view/CMS/JetResolution
def doJER(tree, sys_type):
    # Correct MET when jets are smeared
    tMET = TLorentzVector()
    tMET.SetPtEtaPhiM(tree.pfMET, 0.0, tree.pfMETPhi, 0.0)
    #if debug: print "before correction MET: pfMET = %s\tpfMETPhi = %s" % (tree.pfMET, tree.pfMETPhi)

    # Scale jets
    for jetInd in xrange(0, tree.nJet):
	if tree.jetPt[jetInd] < 10: continue
	# if tree.jetGenJetIndex[jetInd] > 0:  
	if tree.jetGenJetPt[jetInd] > 0:
	    tjet = TLorentzVector()
	    tjet.SetPtEtaPhiM(tree.jetPt[jetInd], tree.jetEta[jetInd], tree.jetPhi[jetInd], 0.0)
	    tMET += tjet
	    oldPt = tree.jetPt[jetInd]
	    genPt = tree.jetGenJetPt[jetInd]

	    #print "jet %s: pt before = %s" % (jetInd, oldPt)
	    eta = tree.jetEta[jetInd]
	    tree.jetPt[jetInd] = max(0.0, genPt + JER_SF(eta, sys_type)*(oldPt - genPt))
	    tjet.SetPtEtaPhiM(tree.jetPt[jetInd], tree.jetEta[jetInd], tree.jetPhi[jetInd], 0.0)
	    tMET -= tjet
	    #print "jet %s: pt after = %s" % (jetInd, tree.jetPt[jetInd])
    
    # Save updated MET values
    tree.pfMET = tMET.Pt()
    tree.pfMETPhi = tMET.Phi()
    #if debug: print "after correction MET: pfMET = %s   pfMETPhi = %s" % (tree.pfMET, tree.pfMETPhi)


def make_hist(name, title, bins, xlabel="", ylabel=""):
    h = TH1F(name, title, len(bins)-1, array('d', bins))
    h.GetXaxis().SetTitle(xlabel)
    h.GetYaxis().SetTitle(ylabel)
    h.SetTitle(title)
    return h

def runAnalysis(inFileDir, inFileName, file_index, outFileURL, mc_file_list, pileupFile, xsec=None, n_mc_events=None):
    """
    Perform the analysis on a single file
    """
    print '...analysing %s' % inFileName                                           
    jet_mult_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    vertex_mult_bins = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
    eta_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4]
    pt_bins = [20,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    eta_signed_bins = [-3.0, -2.8, -2.6, -2.4, -2.2, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
    lepton_mult_bins = [0, 1, 2, 3, 4, 5]
    lepton_high_mult_bins = [3, 4, 5] 
    energy_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    invariant_mass_bins = [ 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    e_sum_bins = [20, 50, 80, 110, 140, 170, 200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500]
    pt_sum_bins = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    flavor_bins = [0, 1, 2, 3]
    #pileup_weight_bins = [-1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    pileup_weight_bins = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]


    histos = {}
   
    # Diagnostic plots
    histos["diag_lepton_mult"] = make_hist("diag_lepton_mult", "Lepton multiplicity (diag)", lepton_mult_bins, "Lepton multiplicity", "Events/bin")
    histos["diag_lepton_high_mult"] = make_hist("diag_lepton_high_mult", "Lepton multiplicity > 2 (diag)", lepton_high_mult_bins, "Lepton multiplicity", "Events/bin")
    histos["diag_flavor_mult"] = make_hist("diag_flavor_mult", "Lepton flavor multiplicity (diag)", flavor_bins, "Lepton flavor (eu, ee, uu)", "Events/bin")
    
    histos["diag_vertex_mult"] = make_hist("diag_vertex_mult", "Vertex multiplicity (diag)", vertex_mult_bins, "Vertex multiplicity", "Events/bin")  
    
    histos["diag_mu_pt"] = make_hist("diag_mu_pt", "Muon p_{T} (diag)", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["diag_mu_eta"] = make_hist("diag_mu_eta", "Muon #void8#eta#void8 (diag)", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["diag_mu_eta_signed"] = make_hist("diag_mu_eta_signed", "Muon #eta (diag)", eta_signed_bins, "#eta", "Events/bin")
    histos["diag_ele_pt"] = make_hist("diag_ele_pt", "Electron p_{T} (diag)", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["diag_ele_eta"] = make_hist("diag_ele_eta", "Electron #void8#eta#void8 (diag)", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["diag_ele_eta_signed"] = make_hist("diag_ele_eta_signed", "Electron #eta (diag)", eta_signed_bins, "#eta", "Events/bin")
    histos["diag_ele_sc_eta"] = make_hist("diag_ele_sc_eta", "Electron #void8#eta_{SC}#void8 (diag)", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["diag_ele_sc_eta_signed"] = make_hist("diag_ele_sc_eta_signed", "Electron #eta_{SC} (diag)", eta_signed_bins, "#eta", "Events/bin")
    histos["diag_jet_pt"] = make_hist("diag_jet_pt", "Jet p_{T} (diag)", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["diag_jet_eta"] = make_hist("diag_jet_eta", "Jet #void8#eta#void8 (diag)", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["diag_jet_mult"] = make_hist("diag_jet_mult", "Jet multiplicity (diag)", jet_mult_bins, "Jet multiplicity", "Events/bin")
    histos["diag_bjet_pt"] = make_hist("diag_bjet_pt", "Bjet p_{T} (diag)", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["diag_bjet_eta"] = make_hist("diag_bjet_eta", "Bjet #void8#eta#void8 (diag)", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["diag_bjet_mult"] = make_hist("diag_bjet_mult", "Bjet multiplicity (diag)", jet_mult_bins, "Bjet multiplicity", "Events/bin")

    # Selection cut plots:
    #
    # Step 1: After lepton selection (Pt > 20, |eta| <= 2.5)
    # Step 2: After jet selection (Pt > 30, |eta| <= 2.5)
    # Step 3: After bjet selection (at least 1 bjet)

    histos["mu_pt"] = make_hist("mu_pt", "Muon p_{T}", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["mu_eta"] = make_hist("mu_eta", "Muon #void8#eta#void8", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["mu_eta_signed"] = make_hist("mu_eta_signed", "Muon #eta", eta_signed_bins, "#eta", "Events/bin")
    histos["ele_pt"] = make_hist("ele_pt", "Electron p_{T}", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["ele_eta"] = make_hist("ele_eta", "Electron #void8#eta#void8", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["ele_eta_signed"] = make_hist("ele_eta_signed", "Electron #eta", eta_signed_bins, "#eta", "Events/bin")
    histos["ele_sc_eta"] = make_hist("ele_sc_eta", "Electron #void8#eta_{SC}#void8", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["ele_sc_eta_signed"] = make_hist("ele_sc_eta_signed", "Electron #eta_{SC}", eta_signed_bins, "#eta", "Events/bin")    
    histos["jet_pt"] = make_hist("jet_pt", "Jet p_{T}", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["jet_eta"] = make_hist("jet_eta", "Jet #void8#eta#void8", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["jet_mult"] = make_hist("jet_mult", "Jet multiplicity", jet_mult_bins, "Jet multiplicity", "Events/bin")
    histos["bjet_pt"] = make_hist("bjet_pt", "Bjet p_{T}", pt_bins, "p_{T} [GeV]", "Events/bin")
    histos["bjet_eta"] = make_hist("bjet_eta", "Bjet #void8#eta#void8", eta_bins, "#void8#eta#void8", "Events/bin")
    histos["bjet_mult"] = make_hist("bjet_mult", "Bjet multiplicity", jet_mult_bins, "Bjet multiplicity", "Events/bin")
    histos["lepton_mult"] = make_hist("lepton_mult", "Lepton count", lepton_mult_bins, "Lepton multiplicity", "Events/bin")
    histos["lepton_high_mult"] = make_hist("lepton_high_mult", "Lepton multiplicity > 2", lepton_high_mult_bins, "Lepton multiplicity", "Events/bin")
    histos["vertex_mult"] = make_hist("vertex_mult", "Vertex multiplicity", vertex_mult_bins, "Vertex multiplicity", "Events/bin")
    histos["vertex_mult_raw"] = make_hist("vertex_mult_raw", "Vertex multiplicity (before offline cuts)", vertex_mult_bins, "Vertex multiplicity", "Events/bin")
    histos["pileup_weights"] = make_hist("pileup_weights", "Pileup weights", pileup_weight_bins, "Pileup weights", "Events/bin")

    # Kinematic distributions
    histos["pt_pos"] = make_hist("pt_pos", "p_{T}(l^{+})", pt_bins, "p_{T}(l^{+}) [GeV]", "Events/bin")
    histos["pt_ll"] = make_hist("pt_ll", "p_{T}(l^{+}l^{-})", pt_bins, "p_{T}(l^{+}l^{-}) [GeV]", "Events/bin")
    histos["E_pos"] = make_hist("E_pos", "E(l^{+})", energy_bins, "E(l^{+}) [GeV]", "Events/bin") 
    histos["M_ll"] = make_hist("M_ll", "M(l^{+}l^{-})", invariant_mass_bins, "M(l^{+}l^{-}) [GeV]", "Events/bin")
    histos["Ep_Em"] = make_hist("Ep_Em", "E(l^{+}) + E(l^{-})", e_sum_bins,"E(l^{+}) + E(l^{-}) [GeV]", "Events/bin")
    histos["ptp_ptm"] = make_hist("ptp_ptm", "p_{T}(l^{+}) + p_{T}(l^{-})", pt_sum_bins, "p_{T}(l^{+}) + p_{T}(l^{-}) [GeV]", "Events/bin")


    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)

    #inFileURL = "root://cmsxrootd.fnal.gov/%s/%s.root" % (inFileDir, inFileName)
    
#    if trigger == TRIGGERS.DILEPTON_AND_DZ: trig_name = "all_dilepton_trig.root"
#    elif trigger == TRIGGERS.DILEPTON: trig_name ="dilepton_trig"
#    elif trigger == TRIGGERS.DZ: trig_name="DZ_trig"
#    else: trigger == ""
    inFileURL = "%s/%s/%s_%d.root" % (inFileDir, inFileName, inFileName, file_index)
				    
    print "About to open file %s" % (inFileURL)
   
    fIn=ROOT.TFile.Open(inFileURL)

    print "%s opened successfully!" % (inFileURL)

    tfile_dir = fIn.Get("ggNtuplizer")
    tree=tfile_dir.Get("EventTree")

  #  print "Tree obtained!"

    # If xsec == None then this is a data file, otherwise it is mc
    isData = True if xsec == None else False


    # For MC only:
    if mc_file_list is not None: pileupWeighter = PyleupRW(mc_file_list=mc_file_list, pileupFile=pileupFile)

    

    # Total of all selected leptons/jets after all cuts are applied
    totalEle = []
    totalMu = []
    totalJets = []
    nJets, nBtags, nElectrons, nMuons, weighted_jets, weighted_bjets, weighted_electrons, weighted_muons = 0, 0, 0, 0, 0, 0, 0, 0  
    totalGoodEntries = 0
    # For b-tagging efficiency
    # nUpgradedJets: num of non b-tagged jets that get upgraded to b-tagged jets
    # nDowngradedJets: num of b-tagged jets that get downgraded to non b-tagged jets
    nUpgradedJets, nDowngradedJets = 0,0 

    puWeightSum = 0
    puEvents = 0

    totalEntries=tree.GetEntriesFast()
    print "Total entries in %s: %s" % (inFileURL, totalEntries)
    totalIterations = min(debug_iter, totalEntries) if debug else totalEntries
#    print "pileupWeighter.getAvgWeight() = ", pileupWeighter.getAvgWeight()
   
    tree.GetEntry(0)
    if tree.isData:
        weight = 1
    else:
        xsec_weight = 1.0 * luminosity * xsec / n_mc_events
        if inFileURL == "/uscms_data/d1/msaunder/skims_2016/full/mc_spring16_TT.root" and debug == True:
	    print "TT  xsec %s     n_mc_events %s    luminosity %s" % ( xsec, n_mc_events, luminosity )
	    print "TT xsec_weight = ", xsec_weight
    
    for i in xrange(0, totalIterations):   
	if i%100==0 : 
	    sys.stdout.write('\r [ %d/100 ] done' %(int(float(100.*i)/float(totalEntries))) )
	    sys.stdout.flush()
	
	tree.GetEntry(i)
	
	# Apply Jet Resoution corrections (mc only)
	if not isData: doJER(tree, JER_var_type)
	
	# Good lepton/jet candidates, ordered by descending pt
	goodEleList =[]  
	goodMuList = []
	goodJetList = []
	goodBJetList = []
	
	# Intermediate values. Use the above lists to access good leptons/jets
	# Dictionary format  { index: pt }
	# Ex: { 0: 97.5, 1: 36.2, 2: 79.4, 3: 34.9, 4: 124.8 )
	_eleDict = {}
	_muDict = {}
	_jetDict = {}
	_bjetDict = {}

	weight = 1

	    #print "About to calculate pileup weight with ", pileupWeighter
	    
	    #p_vi_assign(_puBX, tree.puBX)
	    #p_vf_assign(_puTrue, tree.puTrue)

	    #pileup_weight = pileupWeighter.getWeight(tree.nPUInfo, _puBX, _puTrue)
	if not tree.isData:
	    pileup_weight = pileupWeighter.getWeight(tree.nPUInfo, tree.puBX, tree.puTrue)
	    if pileup_weight != 1.0:
		puWeightSum += pileup_weight
		puEvents += 1
	

	    weight = pileup_weight * xsec_weight
	
	
	histos["vertex_mult_raw"].Fill(tree.nVtx, weight)

	ele = TLorentzVector()
	mu = TLorentzVector()
	jet = TLorentzVector()

	e_ind = -1	# Index of leading electron
	mu_ind = -1	# Index of leading muon
	lepton_mult = 0    # total of e that pass ele cuts and u that pass mu cuts  


	# Process electrons
	for ele_n in xrange(0, tree.nEle):
	    region = detector_region(tree.eleSCEta[ele_n])
	    ele_relIso = tree.elePFChIso[ele_n] + max(0., tree.elePFNeuIso[ele_n] \
		+ tree.elePFPhoIso[ele_n] - max(0., tree.rho) * ele_effective_area(tree.eleSCEta[ele_n])) / tree.elePt[ele_n] 
	    
	    # Impose selection cuts	
	    if (tree.elePt[ele_n] > ele_pt_cut
		and ROOT.TMath.Abs(tree.eleEta[ele_n]) < ele_eta_cut 
		and bool(tree.eleIDbit[ele_n]>>2 & 1)  # Medium ele cut
	        and ele_relIso < ele_relIso_cut[region]):
		
		    nElectrons += 1
		    lepton_mult += 1	
		    _eleDict.update( {ele_n:tree.elePt[ele_n]} ) 


	# For dict  { key:value }  itemgetter(0) for key, itemgetter(1) for value
	if len(_eleDict) > 0:
	    # Found a good electron
	    goodEleList = sorted(_eleDict.items(), key=operator.itemgetter(1))  # Returns a list of the dictionary items sorted by value (pt)
	    goodEleList.reverse()	# Sort in descending pt order
	    e_ind = (goodEleList[0])[0]	 # Index of leading pt electron



	# Process muons
	for mu_n in xrange(0, tree.nMu):
	    mu_relIso = ( tree.muPFChIso[mu_n] + max(0., tree.muPFNeuIso[mu_n] + tree.muPFPhoIso[mu_n] - 0.5 * tree.muPFPUIso[mu_n]) ) / tree.muPt[mu_n]

	    if (tree.muPt[mu_n] > mu_pt_cut
	        and ROOT.TMath.Abs(tree.muEta[mu_n]) < mu_eta_cut
	        and bool(tree.muIDbit[mu_n]>>2 & 1)	# Tight muon cut
	        and mu_relIso < mu_relIso_cut):
		
		    nMuons += 1
		    lepton_mult += 1

		    _muDict.update( {mu_n:tree.muPt[mu_n]} )


	if len(_muDict) > 0:
	    goodMuList = sorted(_muDict.items(), key=operator.itemgetter(1))
	    goodMuList.reverse()
	    mu_ind = (goodMuList[0])[0]

 	
	# Process jets
	for jet_n in xrange(0, tree.nJet):
	    jet.SetPtEtaPhiM(tree.jetPt[jet_n], tree.jetEta[jet_n], tree.jetPhi[jet_n], 0.)
	    if jet.Pt > jet_pt_cut and ROOT.TMath.Abs(jet.Eta()) < jet_eta_cut:
		nJets += 1

		_jetDict.update( {jet_n:tree.jetPt[jet_n]} )
	
		if tree.jetCSV2BJetTags[jet_n] > btag_disc:
		    _bjetDict.update( {jet_n:tree.jetPt[jet_n]} )
 
		totalJets.append(jet)
	

	if len(_jetDict) > 0: 
	    # At least 1 jet
	    goodJetList = sorted(_jetDict.items(), key=operator.itemgetter(1))
	    goodJetList.reverse()

	if len(_bjetDict) > 0:
	    # At least 1 bjet	
	    goodBJetList = sorted(_bjetDict.items(), key=operator.itemgetter(1))
	    goodBJetList.reverse()

	
	##########################
	###  Diagnostic plots  ###
	##########################
	if len(goodEleList) + len(goodMuList) > 1:
	    e0_pt = 0
	    mu0_pt = 0
	    e1_pt = 0
            mu1_pt = 0
	    eu_pt = 0
	    ee_pt = 0
	    uu_pt = 0

            if len(goodEleList) > 0:
                e0_pt = (goodEleList[0])[1] # Leading ele pt (if exists)
            if len(goodMuList) > 0:
                mu0_pt = (goodMuList[0])[1] # Sub-leading mu pt (if exists)

            if len(goodEleList) > 1:
                e1_pt = (goodEleList[1])[1] # Sub-leading ele pt (if exists)
            if len(goodMuList) > 1:
                mu1_pt = (goodMuList[1])[1] # Sub-leading mu pt (if exists)

	    eu_pt = e0_pt + mu0_pt
	    ee_pt = e0_pt + e1_pt
	    uu_pt = mu0_pt + mu1_pt

	    if eu_pt > ee_pt and eu_pt > uu_pt:
		histos["diag_flavor_mult"].Fill(0, weight)
		None

	    elif ee_pt > uu_pt:
		histos["diag_flavor_mult"].Fill(1, weight)
		None

	    else:
		histos["diag_flavor_mult"].Fill(2, weight)
		None

	    numEle = len(goodEleList)
	    numMu = len(goodMuList)
	    histos["diag_lepton_mult"].Fill(numEle + numMu, weight)
	    if numEle + numMu > 2:
		histos["diag_lepton_high_mult"].Fill(numEle + numMu, weight)
		None

	    histos["diag_vertex_mult"].Fill(tree.nVtx, weight)

	    ev = TLorentzVector()
	    mv = TLorentzVector()
	    jv = TLorentzVector()
	    bv = TLorentzVector()

	    if len(goodEleList) > 0:
		for e in goodEleList:
		    ev.SetPtEtaPhiM(tree.elePt[e[0]], tree.eleEta[e[0]], tree.elePhi[e[0]], 0.)

		    histos["diag_ele_pt"].Fill(ev.Pt(), weight)
		    histos["diag_ele_eta"].Fill(ROOT.TMath.Abs(ev.Eta()), weight)
		    histos["diag_ele_eta_signed"].Fill(ev.Eta(), weight)
		    histos["diag_ele_sc_eta"].Fill(ROOT.TMath.Abs(tree.eleSCEta[e[0]]), weight)
		    histos["diag_ele_sc_eta_signed"].Fill(tree.eleSCEta[e[0]], weight)

	    if len(goodMuList) > 0:
		for m in goodMuList:
		    mv.SetPtEtaPhiM(tree.muPt[m[0]], tree.muEta[m[0]], tree.muPhi[m[0]], 0.)

		    histos["diag_mu_pt"].Fill(mv.Pt(), weight)
		    histos["diag_mu_eta"].Fill(ROOT.TMath.Abs(mv.Eta()), weight)
		    histos["diag_mu_eta_signed"].Fill(mv.Eta(), weight)

	    jmult = 0
	    if len(goodJetList) > 0:
		for j in goodJetList:
		    jv.SetPtEtaPhiM(tree.jetPt[j[0]], tree.jetEta[j[0]], tree.jetPhi[j[0]], 0.)
		    jmult += 1

		    histos["diag_jet_pt"].Fill(jv.Pt(), weight)
		    histos["diag_jet_eta"].Fill(jv.Eta(), weight)

		histos["diag_jet_mult"].Fill(jmult, weight)

	    bjmult = 0
	    if len(goodBJetList) > 0:
		for bj in goodBJetList:
		    bv.SetPtEtaPhiM(tree.jetPt[bj[0]], tree.jetEta[bj[0]], tree.jetPhi[bj[0]], 0.)
		    bjmult += 1
		    
		    histos["diag_bjet_pt"].Fill(bv.Pt(), weight)
		    histos["diag_bjet_eta"].Fill(bv.Eta(), weight)

		histos["diag_bjet_mult"].Fill(bjmult, weight)
	    

	#############################
	###  Begin selction cuts  ###
	#############################
	if e_ind > -1 and mu_ind > -1:	# There is a good leading electron and muon  
	    # Set lepton TLorentz vectors 
	    ele.SetPtEtaPhiM(tree.elePt[e_ind], tree.eleEta[e_ind], tree.elePhi[e_ind], 0.)	
	    mu.SetPtEtaPhiM(tree.muPt[mu_ind], tree.muEta[mu_ind], tree.muPhi[mu_ind], 0.)

	    lp = TLorentzVector()  # Positive lepton
	    lm = TLorentzVector()  # Negative lepton
	    ll = TLorentzVector()  # l+l- pair

	    if use_strict_lep_selection:
		if len(goodEleList) + len(goodMuList) > 2:
		    continue

		e0_pt = (goodEleList[0])[1]	# Leading ele pt
		mu0_pt = (goodMuList[0])[1]	# Leading mu pt

		e1_pt = 0
		mu1_pt = 0

		if len(goodEleList) > 1:
		    e1_pt = (goodEleList[1])[1]	# Sub-leading ele pt (if exists)
		if len(goodMuList) > 1:
		    mu1_pt = (goodMuList[1])[1] # Sub-leading mu pt (if exists)

		if e0_pt + mu0_pt > e0_pt + e1_pt and e0_pt + mu0_pt > mu0_pt + mu1_pt and \
		   tree.eleCharge[e_ind] * tree.muCharge[mu_ind] < 0:
		    if tree.eleCharge[e_ind] > 0:
			lp = ele
			lm = mu
		    else:
			lp = mu
			lm = ele

		    ll = lp + lm

		else:
		    continue

	    else:
		if tree.eleCharge[e_ind] > 0: 
		    lp = ele    # e+
		elif tree.muCharge[mu_ind] > 0:
		    lp = mu     # u+
		else: 
		    # No positive lepton, veto event
		    continue

		if tree.eleCharge[e_ind] < 0:
		    lm = ele    # e-
		elif tree.muCharge[mu_ind] < 0:
		    lm = mu	    # u-
		else:
		    # No negative lepton, veto event
		    continue
		ll = lp + lm   # eu pair (l+l-)


	    if ll.M() > 20:    # Cut on invariant mass of the lepton pair	
		if len(goodJetList) > 0:	    # At least 1 jet
		    if len(goodBJetList) > 0:  # At least 1 b tagged jet 

			totalGoodEntries += 1
			histos["pt_pos"].Fill(lp.Pt(), weight)
			histos["pt_ll"].Fill(ll.Pt(), weight)
			histos["E_pos"].Fill(lp.E(), weight)
			histos["M_ll"].Fill(ll.M(), weight)
			histos["Ep_Em"].Fill(lp.E() + lm.E(), weight)
			histos["ptp_ptm"].Fill(lp.Pt() + lm.Pt(), weight)
			    
			totalEle.append(ele)
			totalMu.append(mu)

			histos["ele_pt"].Fill(ele.Pt(), weight)
			histos["ele_eta"].Fill(ROOT.TMath.Abs(ele.Eta()), weight)
			histos["ele_eta_signed"].Fill(ele.Eta(), weight)
			histos["ele_sc_eta"].Fill(ROOT.TMath.Abs(tree.eleSCEta[e_ind]), weight)
			histos["ele_sc_eta_signed"].Fill(tree.eleSCEta[e_ind], weight)
			histos["mu_pt"].Fill(mu.Pt(), weight)
			histos["mu_eta"].Fill(ROOT.TMath.Abs(mu.Eta()), weight)
			histos["mu_eta_signed"].Fill(mu.Eta(), weight)

			for jet_ind in xrange(0, len(goodJetList)):
			    jet.SetPtEtaPhiM(tree.jetPt[jet_ind], tree.jetEta[jet_ind], tree.jetPhi[jet_ind], 0.)
			    totalJets.append(jet)
			    histos["jet_pt"].Fill(jet.Pt(), weight)
			    histos["jet_eta"].Fill(jet.Eta(), weight)
						
			for bjet_ind in xrange(0, len(goodBJetList)):
			    histos["bjet_pt"].Fill(tree.jetPt[bjet_ind], weight)
			    histos["bjet_eta"].Fill(tree.jetEta[bjet_ind], weight)

			histos["jet_mult"].Fill(len(goodJetList), weight)
			histos["bjet_mult"].Fill(len(goodBJetList), weight)
			
			n_leptons = len(goodEleList) + len(goodMuList)	
			histos["lepton_mult"].Fill(n_leptons, weight) 
			if n_leptons > 2:
			    #print "\nlepton_mult = %s\n" % (lepton_mult)
			    histos["lepton_high_mult"].Fill(n_leptons, weight)
			
			histos["vertex_mult"].Fill(tree.nVtx, weight)
			if not isData: histos["pileup_weights"].Fill(pileup_weight, 1)
    # end of main for loop 
    
    #print "pileup average weight: "
    sys.stdout.write('\r [ 100/100 ] done\n' )
    sys.stdout.flush()
    # All done with this file
    fIn.Close()
    print "Total good events in %s  %s" % (inFileName, totalGoodEntries) 
    if not isData:
    	print "Average pileup weight for events in %s  %s" % (inFileName, pileupWeighter.getAvgWeight())

    # Save histograms to file
    fOut=ROOT.TFile.Open(outFileURL,'RECREATE')
    for key in histos: histos[key].Write()
    fOut.Close()


"""
Wrapper to be used when run in parallel
"""
def runAnalysisPacked(args):
    try:
        return runAnalysis(inFileDir=args[0],
				 inFileName=args[1],
                                 file_index=args[2],
				 outFileURL=args[3],
				 mc_file_list=args[4],
				 pileupFile=args[5],
                                 xsec=args[6],
				 n_mc_events=args[7])
    except :
        print 50*'<'
        print "  Problem  (%s) with %s continuing without"%(sys.exc_info()[1],args[0])
        print 50*'<'
        return False


def call_it(instance, name, args=(), kwargs=None):
    "indirect caller for instance methods and multiprocessing"
    if kwargs is None:
	kwargs = {}
    return getattr(instance, name)(*args, **kwargs)

"""
steer the script
"""
def main():
    #global pileupWeighter
    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-j', '--json',        dest='json'  ,      help='json with list of files',      default=None,        type='string')
    parser.add_option('-i', '--inDir',       dest='inDir',       help='input directory with files',   default=None,        type='string')
    parser.add_option('-o', '--outDir',      dest='outDir',      help='output directory',             default='analysis',  type='string') 
    parser.add_option('-p', '--puF',	     dest='puF',         help='path to pilup histogram file', default=None,        type='string')
    parser.add_option('-n', '--njobs',       dest='njobs',       help='# jobs to run in parallel',    default=0,           type='int')
    (opt, args) = parser.parse_args()

    #read list of samples
    #print "About to open json file %s" % (opt.json)
    jsonFile = open(opt.json,'r')
    #print "Retrieving sample list"
    samplesList=json.load(jsonFile,encoding='utf-8').items()
    jsonFile.close()

    #prepare output
    if len(opt.outDir)==0    : opt.outDir='./'
    os.system('mkdir -p %s' % opt.outDir)
        
    #create the analysis jobs
    taskList = []
    mc_file_list = []
    num_files_in_sample = []

    # Get the list of mc files to create the pileup weighter
    for sample, sampleInfo in samplesList:
	p1 = Popen(["ls", "-alh", "%s/%s/" % (opt.inDir, sample)], stdout=PIPE)
	p2 = Popen(["grep", "root"], stdin=p1.stdout, stdout=PIPE)
	p3 = Popen(["wc", "-l"], stdin=p2.stdout, stdout=PIPE)
	num_files = int(p3.communicate()[0])
	num_files_in_sample.append(num_files)

	if sampleInfo[1] != 0:
	    # Don't add data files to the mc list
	    continue
        inFileURL = "%s/%s/%s_0.root" % (opt.inDir, sample, sample)
        mc_file_list.append(inFileURL)
	

#	for n in xrange(0, num_files):
#	    inFileURL = "%s/%s/%s_%d.root" % (opt.inDir, sample, sample, n)
#	    mc_file_list.append(inFileURL)


    ### Only needed for swig library class
    # mc_file_list is a list of unicode strings. convert to list of ascii strings before passing to PUReweight constructor
    # mc_ascii_list = []
    # for entry in mc_file_list: mc_ascii_list.append(entry.encode('ascii', 'replace'))
    
    #puWeighter = PUReweight(len(mc_ascii_list), mc_ascii_list, opt.puF)
    #pileupWeighter = None
    #puWeighter = PyleupRW(mc_file_list, opt.puF)
    #print puWeighter
    #h = puWeighter.getPUweightHist()
    #print h
    #newWeighter = PUReweight(p_th1d_value(h))
    #print newWeighter
    #h = p_th1d_value(puWeighter.getPUweightHist())
    #print h.GetEntries()
    #print h

    for index, (sample, sampleInfo) in enumerate(samplesList):
        #inFileURL  = "%s/%s.root" % (opt.inDir,sample)
        #if not os.path.isfile(inFileURL): continue
        xsec=sampleInfo[0] if sampleInfo[1]==0 else None
	n_mc_events=sampleInfo[5] if sampleInfo[1]==0 else None 
	
	for n in xrange(0, num_files_in_sample[index]):
	    outFileURL = "%s/%s_%d.root" % (opt.outDir, sample, n)
	    taskList.append( (opt.inDir, sample, n, outFileURL, mc_file_list, opt.puF, xsec, n_mc_events) )
    
    # Run the analysis jobs
    if opt.njobs == 0:
        for inFileDir, inFileName, outFileURL, mc_file_list, xsec, n_mc_events in taskList:
            runAnalysis(inFileDir=inFileDir, inFileName=inFileName, numFiles=1, outFileURL=outFileURL, pileupFile=opt.puF, xsec=xsec, n_mc_events=n_mc_events)
    else:
	from multiprocessing import Pool
	#from multiprocessing.pool import ApplyResult
	#pool = Pool(opt.njobs)
	#async_results = [pool.apply_async(runAnalysis, t) for t in taskList]
	#pool.close()
	#map(ApplyResult.wait, async_results)
        #lst_results = [r.get() for r in async_results]
	pool = Pool(opt.njobs)	
	pool.map(runAnalysisPacked,taskList)

    #all done here
    print 'Analysis results are available in %s' % opt.outDir
    exit(0)



"""
for execution from another script
"""
if __name__ == "__main__":
    sys.exit(main())
