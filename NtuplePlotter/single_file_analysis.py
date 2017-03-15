#!/usr/bin/env python
from array import array
import optparse
import operator
import os,sys
import json
import pickle
import random
import ROOT
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

debug = True
debug_iter = 1000


# Selection Cuts
ele_pt_cut = 20
ele_eta_cut = 2.4

mu_pt_cut = 20
mu_eta_cut = 2.4
mu_relIso_cut = 0.15	# Tight (loose) iso cut = 0.15 (0.25)

jet_pt_cut = 30
jet_eta_cut = 2.4

# B tagging discriminator WPs
# Loose:  0.605   Mistag rate: 10%
# Medium: 0.89    Mistag rate: 1%
# Tight:  0.97    Mistag rate: 0.1%
btag_disc = 0.89

####################################################################################################################
# Cut-based Electron ID Medium WP
# https://twiki.cern.ch/twiki/bin/view/CMS/CutBasedElectronIdentificationRun2#Spring15_selection_25ns
# 
# cut[barrel, endcap]
# barrel: |eta supercluster| <= 1.479
# endcap: 1.479 < |eta supercluster| < 2.5     
ele_full5x5_sigmaIetaIeta_cut = [0.0101, 0.0283];
ele_dEtaIn_cut = [0.0103, 0.00733];
ele_dPhiIn_cut = [0.0336, 0.114];
ele_HoverE_cut = [0.0876, 0.0678];
ele_relIso_cut = [0.0766, 0.0678];
ele_ooEmooP_cut = [0.0174, 0.0898];
ele_d0_cut = [0.0118, 0.0739];
ele_dz_cut = [0.373, 0.602];
ele_missingInnerHits_cut = [2, 1];
####################################################################################################################

# Region 0: barrel
# Region 1: endcap
def detector_region(SCEta):
    return 0 if abs(SCEta) <= 1.479 else 1

# Veto all electrons whose supercluster eta falls in the transition region
def transition_region_veto(SCEta):
    return False if abs(SCEta) > 1.4442 and abs(SCEta) < 1.5660 else True


# kEleGammaAndNeutralHadronIso03
# Spring15 25ns effective areas
# RecoEgamma/ElectronIdentification/data/Spring15/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_25ns.txt
def ele_effective_area(SCEta):
    eta = abs(SCEta)
    if eta < 1.0: return 0.1752
    elif eta < 1.479: return 0.1862
    elif eta < 2.0: return 0.1411
    elif eta < 2.2: return 0.1534
    elif eta < 2.3: return 0.1903
    elif eta < 2.4: return 0.2243
    else: return 0.2687


"""
Perform the analysis on a single file
"""
def runAnalysis(inFileURL, outFileURL, xsec=None, n_mc_events=None):

    print '...analysing %s' % inFileURL                                           
    jet_mult_bins = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    eta_bins = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4]
    pt_bins = [20,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    eta_signed_bins = [-3.0, -2.8, -2.6, -2.4, -2.2, -2.0, -1.8, -1.6, -1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0]
    lepton_ct_bins = [0, 1, 2, 3, 4]
    lepton_high_ct_bins = [2.5, 3.5, 4.5] 
    energy_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    invariant_mass_bins = [ 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    e_sum_bins = [20, 50, 80, 110, 140, 170, 200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500]
    pt_sum_bins = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    title = ';p_{T}(l^{+}) [GeV];Events'

    luminosity = 2689 # pb^-1    

    histos = {}
    
    # Selection cut plots:
    #
    # Step 1: After lepton selection (Pt > 20, |eta| <= 2.5)
    # Step 2: After jet selection (Pt > 30, |eta| <= 2.5)
    # Step 3: After bjet selection (at least 1 bjet)


    histos["mu_pt"] = ROOT.TH1F("mu_pt", "Mu Pt", len(pt_bins)-1, array('d', pt_bins))
    histos["mu_eta"] = ROOT.TH1F("mu_eta", "Mu eta", len(eta_bins)-1, array('d', eta_bins))
    histos["mu_eta_signed"] = ROOT.TH1F("mu_eta_signed", "Mu eta signed", len(eta_signed_bins)-1, array('d', eta_signed_bins))
    histos["ele_pt"] = ROOT.TH1F("ele_pt", "Ele pt", len(pt_bins)-1, array('d', pt_bins))
    histos["ele_eta"] = ROOT.TH1F("ele_eta", "Ele eta", len(eta_bins)-1, array('d', eta_bins))
    histos["ele_eta_signed"] = ROOT.TH1F("ele_eta_signed", "Ele eta signed", len(eta_signed_bins)-1, array('d', eta_signed_bins))
    histos["ele_sc_eta"] = ROOT.TH1F("ele_sc_eta", "Ele SC eta", len(eta_bins)-1, array('d', eta_bins))
    histos["ele_sc_eta_signed"] = ROOT.TH1F("ele_sc_eta_signed", "Ele SC eta signed", len(eta_signed_bins)-1, array('d', eta_signed_bins))
    histos["jet_pt"] = ROOT.TH1F("jet_pt", "Jet pt", len(pt_bins)-1, array('d', pt_bins))
    histos["jet_eta"] = ROOT.TH1F("jet_eta", "Jet eta", len(eta_bins)-1, array('d', eta_bins))
    histos["jet_mult"] = ROOT.TH1F("jet_mult", "Jet mult", len(jet_mult_bins)-1, array('d', jet_mult_bins)) 
    histos["bjet_pt"] = ROOT.TH1F("bjet_pt", "Jet pt", len(pt_bins)-1, array('d', pt_bins))
    histos["bjet_eta"] = ROOT.TH1F("bjet_eta", "Jet eta", len(eta_bins)-1, array('d', eta_bins))
    histos["bjet_mult"] = ROOT.TH1F("bjet_mult", "Jet mult", len(jet_mult_bins)-1, array('d', jet_mult_bins))
    histos["lepton_count"] = ROOT.TH1F("lepton_count", "Lepton count", len(lepton_ct_bins)-1, array('d', lepton_ct_bins))
    histos["lepton_high_count"] = ROOT.TH1F("lepton_high_count", "Lepton high count", len(lepton_high_ct_bins)-1, array('d', lepton_high_ct_bins))

    # Kinematic distributions
    histos["pt_pos"] = ROOT.TH1F("pt_pos", "pt(l+)", len(pt_bins)-1, array('d', pt_bins))
    histos["pt_ll"] = ROOT.TH1F("pt_ll", "pt(l-)", len(pt_bins)-1, array('d', pt_bins))
    histos["E_pos"] = ROOT.TH1F("E_pos", "E(l+)", len(energy_bins)-1, array('d', energy_bins))
    histos["M_ll"] = ROOT.TH1F("M_ll", "M(l+l-)", len(invariant_mass_bins)-1, array('d', invariant_mass_bins)) 
    histos["Ep_Em"] = ROOT.TH1F("Ep_Em", "Ep Em", len(e_sum_bins)-1, array('d', e_sum_bins))
    histos["ptp_ptm"] = ROOT.TH1F("ptp_ptm", "pt(l+) + pt(l-)", len(pt_sum_bins)-1, array('d', pt_sum_bins))


    for key in histos:
        histos[key].Sumw2()
        histos[key].SetDirectory(0)

    print "About to open file %s" % (inFileURL)
   
    fIn=ROOT.TFile.Open(inFileURL)
  
    tfile_dir = fIn.Get("ggNtuplizer")
    tree=tfile_dir.Get("EventTree")


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



    # If xsec == None then we are handling a data event
    # Otherwise it is MC
    isData = True if xsec == None else False

    totalEntries=tree.GetEntriesFast()
    print "Total entries: %s" % (totalEntries)
    totalIterations = min(debug_iter, totalEntries) if debug else totalEntries

    for i in xrange(0, totalIterations):
	if i%100==0 : 
	    sys.stdout.write('\r [ %d/100 ] done' %(int(float(100.*i)/float(totalEntries))) )
	    sys.stdout.flush()
	
	tree.GetEntry(i)
	
	
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
	ele = ROOT.TLorentzVector()
	mu = ROOT.TLorentzVector()
	jet = ROOT.TLorentzVector()

	e_ind = -1	# Index of leading electron
	mu_ind = -1	# Index of leading muon
	lepton_count = 0    # total of e that pass ele cuts and u that pass mu cuts  


	# Process electrons
	for ele_n in xrange(0, tree.nEle):
	    region = detector_region(tree.eleSCEta[ele_n])
	    ele_relIso = tree.elePFChIso[ele_n] + max(0., tree.elePFNeuIso[ele_n] \
		+ tree.elePFPhoIso[ele_n] - max(0., tree.rho) * ele_effective_area(tree.eleSCEta[ele_n])) / tree.elePt[ele_n] 
	    
	    # Impose selection cuts	
	    #print "About to impose ele cuts..."		
	    if (tree.elePt[ele_n] > ele_pt_cut
		and ROOT.TMath.Abs(tree.eleEta[ele_n]) < ele_eta_cut 
		and transition_region_veto(tree.eleSCEta[ele_n]) 
		and tree.eleSigmaIEtaIEtaFull5x5[ele_n] < ele_full5x5_sigmaIetaIeta_cut[region]
	        and abs(tree.eledEtaAtVtx[ele_n]) < ele_dEtaIn_cut[region]
	        and abs(tree.eledPhiAtVtx[ele_n]) < ele_dPhiIn_cut[region]
	        and tree.eleHoverE[ele_n] < ele_HoverE_cut[region]
	        and ele_relIso < ele_relIso_cut[region]
	        and abs(tree.eleD0[ele_n]) < ele_d0_cut[region]
	        and abs(tree.eleDz[ele_n]) < ele_dz_cut[region]
	        and tree.eleMissHits[ele_n] <= ele_missingInnerHits_cut[region]
	        and bool(tree.eleConvVeto[ele_n])):
		
		    nElectrons += 1
		    lepton_count += 1	
		    _eleDict.update( {ele_n:tree.elePt[ele_n]} ) 


	# For dict  { key:value }  itemgetter(0) for key, itemgetter(1) for value
	if len(_eleDict) > 0:
	    # Found a good electron
	    goodEleList = sorted(_eleDict.items(), key=operator.itemgetter(1))  # Returns a list of the dictionary items sorted by value (pt)
	    goodEleList.reverse()	# Sort in descending pt order
	    e_ind = (goodEleList[0])[0]	 # Index of leading pt electron

	#print "Processed electrons"


	# Process muons
	for mu_n in xrange(0, tree.nMu):
	    mu_relIso = ( tree.muPFChIso[mu_n] + max(0., tree.muPFNeuIso[mu_n] + tree.muPFPhoIso[mu_n] - 0.5 * tree.muPFPUIso[mu_n]) ) / tree.muPt[mu_n]

	    if (tree.muPt[mu_n] > mu_pt_cut
	        and ROOT.TMath.Abs(tree.muEta[mu_n]) < mu_eta_cut
	        and bool(tree.muIsTightID[mu_n])
	        and mu_relIso < mu_relIso_cut):
		
		    nMuons += 1
		    lepton_count += 1

		    _muDict.update( {mu_n:tree.muPt[mu_n]} )


	if len(_muDict) > 0:
	    goodMuList = sorted(_muDict.items(), key=operator.itemgetter(1))
	    goodMuList.reverse()
	    mu_ind = (goodMuList[0])[0]

 	
	# Process jets
	for jet_n in xrange(0, tree.nJet):
	    jet.SetPtEtaPhiM(tree.jetPt[jet_n], tree.jetEta[jet_n], tree.jetPhi[jet_n], 0.)
	    if jet.Pt > 30 and ROOT.TMath.Abs(jet.Eta()) < 2.4:
		nJets += 1

		_jetDict.update( {jet_n:tree.jetPt[jet_n]} )
	
		if tree.jetpfCombinedInclusiveSecondaryVertexV2BJetTags[jet_n] > btag_disc:
		    _bjetDict.update( {jet_n:tree.jetPt[jet_n]} )
 
		totalJets.append(jet)
	

	if len(_jetDict) > 0: 
	    # At least 1 jet
	    goodJetList = sorted(_jetDict.items(), key=operator.itemgetter(1))
	    goodJetList.reverse()
	    histos["jet_mult"].Fill(len(goodJetList), 1)

	if len(_bjetDict) > 0:
	    # At least 1 bjet	
	    goodBJetList = sorted(_bjetDict.items(), key=operator.itemgetter(1))
	    goodBJetList.reverse()
	    histos["bjet_mult"].Fill(len(goodBJetList), 1)

	
	#############################
	#### Begin selction cuts ####
	#############################
	if e_ind > -1 and mu_ind > -1:	# There is a good leading electron and muon  
	    # Set lepton TLorentz vectors 
	    ele.SetPtEtaPhiM(tree.elePt[e_ind], tree.eleEta[e_ind], tree.elePhi[e_ind], 0.)	
	    mu.SetPtEtaPhiM(tree.muPt[mu_ind], tree.muEta[mu_ind], tree.muPhi[mu_ind], 0.)

	    lp = ROOT.TLorentzVector()	# Positive lepton
	    lm = ROOT.TLorentzVector()  # Negative lepton
	    ll = ROOT.TLorentzVector()  # l+l- pair

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
	
	histos["lepton_count"].Fill(lepton_count, 1) 
	if lepton_count > 2:
	    #print "\nlepton_count = %s\n" % (lepton_count)
	    histos["lepton_high_count"].Fill(lepton_count, 1) 
    """
    for i in xrange(0,totalIterations):
	#if i%100==0 : sys.stdout.write('\r [ %d/100 ] done' %(int(float(100.*i)/float(totalEntries))) )
    	tree.GetEntry(i)
        # If the cross section xsec is 'None' then we are handling a data event.
    	# Otherwise, it is MC and xsec will be set to the value of the cross section specified in the json file 
    
    	# base weight = pileup * lepton selection * xsec weight
	
	# Event weight (1 if data)
	weight = 1 if isData else tree.LepSelEffWeights[0] * tree.PUWeights[0] * tree.GenWeights[0] 
	if xsec == None: 
	    jet_weight = 1
            lep_weight = 1
	else:
	    jet_weight = luminosity * xsec * tree.PUWeights[0] * tree.LepSelEffWeights[0]
	    if tree.nGenWeight > 0 : jet_weight *= tree.GenWeights[0]
	    lep_weight = tree.PUWeights[0] * tree.LepSelEffWeights[0] * luminosity * xsec / n_mc_events 	 

	###########################
	## Run Pt(l+l-) analysis ##
	###########################
	lp = ROOT.TLorentzVector()
	lm = ROOT.TLorentzVector()
	ll = ROOT.TLorentzVector()

	if tree.Lepton_id[0] > 0:
	    # First entry is the positive lepton (doesn't matter whether electron or muon)
	    lp.SetPtEtaPhiM(tree.Lepton_pt[0], tree.Lepton_eta[0], tree.Lepton_phi[0], 0.)
	    lm.SetPtEtaPhiM(tree.Lepton_pt[1], tree.Lepton_eta[1], tree.Lepton_phi[1], 0.)

	else:
	    # First entry is the negative lepton
	    lm.SetPtEtaPhiM(tree.Lepton_pt[0], tree.Lepton_eta[0], tree.Lepton_phi[0], 0.)
            lp.SetPtEtaPhiM(tree.Lepton_pt[1], tree.Lepton_eta[1], tree.Lepton_phi[1], 0.)

	# Lepton selection cut
	if lp.Pt() > 20 and lm.Pt() > 20 and ROOT.TMath.Abs(lp.Eta()) <= 2.5 and ROOT.TMath.Abs(lp.Eta()) <= 2.5:
	    # Stage 1 selection passed
	    ll = lp + lm
	    
	    # Fill stage 1 histograms
	    histos["pt_ll_1"].Fill(ll.Pt(), lep_weight)
	    histos["pt_lp_1"].Fill(lp.Pt(), lep_weight)
	    histos["pt_lm_1"].Fill(lm.Pt(), lep_weight)

	    # Check for jets
	    jets = []
	    bjets = []
	    for j in xrange(0, tree.nJet):
		j4 = ROOT.TLorentzVector()
		j4.SetPtEtaPhiM(tree.Jet_pt[j], tree.Jet_eta[j], tree.Jet_phi[j], tree.Jet_mass[j])
	    
		# Jet selection
		if j4.Pt() <= 30 or ROOT.TMath.Abs(j4.Eta()) > 2.5 : continue
		jets.append(j4)
		
		if isData:
		    # B jet selection
		    # Discriminator values for different operating points:
		    # Loose:  0.605   Mistag rate: 10%
		    # Medium: 0.89    Mistag rate: 1%
		    # Tight:  0.97    Mistag rate: 0.1%
		    if tree.Jet_CombIVF[j] > 0.89:
			bjets.append(j4)

		else:
		    # B Tagging Efficiency (for MC events only!)
		    # Compute scale factor SF
		    #SF = reader.eval(jet_flavor, jet_eta, jet_pt)
                    if tree.Jet_flavour[j] == 5:
			SF = reader.eval(0, tree.Jet_eta[j], tree.Jet_pt[j])
		    else:
			SF = reader.eval(1, tree.Jet_eta[j], tree.Jet_pt[j])		    

		    # Set b tagging efficiency to 65%
		    btag_eff = 0.65		    


		    isBTagged = True if tree.Jet_CombIVF[j] > 0.89 else False
	            rng = random.uniform(0,1)    # Choose a random number between 0 and 1	
		    if SF > 1:
			# TODO: Insert jet tag switching here
			if not isBTagged:
			    mistag_percent = (1.0 - SF) / (1.0 - (1.0/btag_eff) );
			    if debug: print "rng: %f ; SF: %f ; Mistag_pct: %f" % (rng, SF, mistag_percent)	
			    if rng < mistag_percent:
				# Upgrade the jet to a bjet
				isBTagged = True
				nUpgradedJets += 1
				if debug: print "Upgraded to bjet"

		    
		    elif SF < 1:
			if debug: print "rng: %f ; SF: %f" % (rng, SF)
			if isBTagged and rng > SF:
			    isBTagged = False
			    nDowngradedJets += 1
			    if debug: print "Downgraded from bjet"

		    if isBTagged:
			bjets.append(j4)			
					
					    

	    if len(jets) > 0:
		# At least 1 jet passed the selection cuts. Stage 2 criteria met
		histos["pt_ll_2"].Fill(ll.Pt(), lep_weight)
		histos["pt_lp_2"].Fill(lp.Pt(), lep_weight)
		histos["pt_lm_2"].Fill(lm.Pt(), lep_weight)

		# Check for stage 3 criteria (at least 1 bjet)
		if len(bjets) > 0:
		    histos["pt_ll_3"].Fill(ll.Pt(), lep_weight)
		    histos["pt_lp_3"].Fill(lp.Pt(), lep_weight)
		    histos["pt_lm_3"].Fill(lm.Pt(), lep_weight)
    """		   
	##############################	    
	## End of Pt(l+l-) analysis ##
	##############################
    """
        for j in xrange(0, tree.nJet):
            jp4 = ROOT.TLorentzVector()
            jp4.SetPtEtaPhiM(tree.Jet_pt[j], tree.Jet_eta[j], tree.Jet_phi[j], tree.Jet_mass[j])
            if jp4.Pt() < 30 or ROOT.TMath.Abs(jp4.Eta()) > 2.4 : continue

            nJets += 1
	    if xsec != None: weighted_jets += jet_weight

           # taggedJetsP4.append(jp4)
            histos['jet_mult'].Fill(1, jet_weight)
            histos['jet_pt'].Fill(jp4.Pt(), jet_weight)
            histos['jet_eta'].Fill(ROOT.TMath.Abs(jp4.Eta()), jet_weight)

            # Test for bjet using results of Combined Secondary Vertex algorithm
            if tree.Jet_CombIVF[j] > 0.605:
                nBtags += 1
		if xsec != None: weighted_bjets += jet_weight

                #taggedBJetsP4.append(jp4)
                histos['bjet_mult'].Fill(1, jet_weight)
                histos['bjet_pt'].Fill(jp4.Pt(), jet_weight)
                histos['bjet_eta'].Fill(ROOT.TMath.Abs(jp4.Eta()), jet_weight)

	histos['jet_mult'].Fill(nJets, jet_weight)
	histos['bjet_mult'].Fill(nBtags, jet_weight)

	nLeptons = 0
	#############
	# Lepton IDs:
	# e-  :  11
	# e+  : -11
	# mu- :  13
	# mu+ : -13
	#############
	for j in xrange(0, tree.nLepton):
	    lepP4 = ROOT.TLorentzVector()
	    lepP4.SetPtEtaPhiM(tree.Lepton_pt[j], tree.Lepton_eta[j], tree.Lepton_phi[j], 0.)
	    if lepP4.Pt() < 30 or ROOT.TMath.Abs(lepP4.Eta()) > 2.4: continue

	    if ROOT.TMath.Abs(tree.Lepton_id[j]) == 11:
		nElectrons += 1
		if xsec != None: weighted_electrons += lep_weight

		taggedElectrons.append(lepP4)
		histos["elec_pt"].Fill(lepP4.Pt(), lep_weight)
		histos["elec_eta"].Fill(lepP4.Eta(), lep_weight)
	    elif ROOT.TMath.Abs(tree.Lepton_id[j]) == 13:
		nMuons += 1
		if xsec != None: weighted_muons += lep_weight

		taggedMuons.append(lepP4)
		histos["muon_pt"].Fill(lepP4.Pt(), lep_weight)
                histos["muon_eta"].Fill(lepP4.Eta(), lep_weight)

	for j in xrange(0, tree.nLepton):
	    # Positive lepton
	    lp = ROOT.TLorentzVector()
	    lp.SetPtEtaPhiM(tree.Lepton_pt[j],tree.Lepton_eta[j],tree.Lepton_phi[j],0.)
	    if lp.Pt() < 30 or ROOT.TMath.Abs(lp.Eta()) > 2.4: continue # or tree.Lepton_id[j] > 0 : continue
	
	    nLeptons += 1
	    taggedLeptons.append(lp)
	    histos[rec].Fill(lp.Pt(),weight)
	    if xsec != None:
		histos[gen].Fill(lp.Pt(), weight)
    """
    # TODO: Gen lepton paramaters are not available in this data set

#    glp = ROOT.TLorentzVector()
#    glp.SetPtEtaPhiM(tree.GenLmPt,tree.GenLmEta,tree.GenLmPhi,0.)

    # Fill the histogram
   # for l in xrange(0, len(taggedLeptons)):
	#binWidth = histos[rec].GetXaxis().GetBinWidth(histos[rec].GetXaxis().FindBin(taggedLeptons[l].Pt() ))
	#histos[rec].Fill(taggedLeptons[j].Pt(),weight/binWidth)
#	histos[rec].Fill(taggedLeptons[l].Pt(),weight)

#    # If MC
#    if xsec != 1:
#	binWidthGen = histos[gen].GetXaxis().GetBinWidth(histos[gen].GetXaxis().FindBin(glp.Pt() ))
#	histos[gen].Fill(glp.Pt(),weight/binWidthGen)

    #for j in xrange(0, len(taggedElectrons)):
    #	histos["elec_pt"].Fill(taggedElectrons[j].Pt(), weight




    sys.stdout.write('\r [ 100/100 ] done\n' )
    sys.stdout.flush()
    #all done with this file
    fIn.Close()
 #   if nUpgradedJets == 1:
#	print "1 jet upgraded to b-tagged jet"
#    else:
#        print "{} jets upgraded to b-tagged jets".format(nUpgradedJets)
#    if nDowngradedJets == 1:
#	print "1 b-tagged jet downgraded to jet"
#    else:
#        print "{} b-tagged jets downgraded to jets".format(nDowngradedJets)


#    if xsec == None:
    #print outFileURL, " Jets: ", nJets, " B Jets: ", nBtags, " Electrons: ", nElectrons, " Muons: ", nMuons 
    
    print "Total good events ", totalGoodEntries
#    else:
#	print outFileURL, " Jets: ", nJets, " weighted_jets: ", weighted_jets, " B Jets: ", nBtags, " weighted_bjets: ", weighted_bjets, " Electrons: ", nElectrons, " weighted_electrons: ", weighted_electrons, " weighted_muons: ", weighted_muons

    #save histograms to file
    fOut=ROOT.TFile.Open(outFileURL,'RECREATE')
    for key in histos: histos[key].Write()
    fOut.Close()


"""
Wrapper to be used when run in parallel
"""
def runAnalysisPacked(args):
    
    try:
        return runAnalysis(inFileURL=args[0],
                                 outFileURL=args[1],
                                 xsec=args[2],
				 n_mc_events=args[3])
    except :
        print 50*'<'
        print "  Problem  (%s) with %s continuing without"%(sys.exc_info()[1],args[0])
        print 50*'<'
        return False


"""
steer the script
"""
def main():

    #configuration
    usage = 'usage: %prog [options]'
    parser = optparse.OptionParser(usage)
    parser.add_option('-j', '--json',        dest='json'  ,      help='json with list of files',      default=None,        type='string')
    parser.add_option('-i', '--inF',       dest='inF',       help='input file',   default=None,        type='string')
    parser.add_option('-o', '--outDir',      dest='outDir',      help='output directory',             default='analysis',  type='string')
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
    for sample, sampleInfo in samplesList: 
        inFileURL  = opt.inF 
        #if not os.path.isfile(inFileURL): continue
        xsec=sampleInfo[0] if sampleInfo[1]==0 else None
	n_mc_events=sampleInfo[5] if sampleInfo[1]==0 else None        
        outFileURL = "%s/plots.root" % (opt.outDir)
        taskList.append( (inFileURL,outFileURL,xsec,n_mc_events) )

    #run the analysis jobs
    if opt.njobs == 0:
        for inFileURL, outFileURL, xsec in taskList:
            runAnalysis(inFileURL=inFileURL, outFileURL=outFileURL, xsec=xsec, n_mc_events=n_mc_events)
    else:
        from multiprocessing import Pool
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
