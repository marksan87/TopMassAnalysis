#!/usr/bin/env python
from array import array
import optparse
import operator
import os,sys
import json
import pickle
import random
import ROOT
from ROOT import TH1F, TH2F, TFile, TLorentzVector
from subprocess import Popen, PIPE

# Load histogram interpolation class
ROOT.gROOT.ProcessLine('.L ../src/th1fmorph_cc+') 

def findMassFromFilename(fName):
    """
    Returns a string with the mass value for labeling
    """
    if fName.find('165') > -1: return 165.5
    if fName.find('169') > -1: return 169.5
    if fName.find('171') > -1: return 171.5
    if fName.find('173') > -1: return 173.5
    if fName.find('175') > -1: return 175.5
    if fName.find('178') > -1: return 178.5

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

STYPE = enum('DOWN', 'NORM', 'UP')
OP = enum('LOOSE', 'MEDIUM', 'TIGHT')
JER_var_type = STYPE.NORM



def make_hist(name, title, bins, xlabel="", ylabel=""):
    h = TH1F(name, title, len(bins)-1, array('d', bins))
    h.GetXaxis().SetTitle(xlabel)
    h.GetYaxis().SetTitle(ylabel)
    h.SetTitle(title)
    return h

TT_FILELIST = ['mc_TT_mt1665.root', 'mc_TT_mt1695.root', 'mc_TT_mt1715.root', 'mc_TT_mt1735.root', 'mc_TT_mt1755.root', 'mc_TT_mt1785.root']

def mass_templates():
    pt_bins = [20,30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    energy_bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    invariant_mass_bins = [ 0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400]
    e_sum_bins = [20, 50, 80, 110, 140, 170, 200, 230, 260, 290, 320, 350, 380, 410, 440, 470, 500]
    pt_sum_bins = [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250]
    
    histos = {}

    histos["pt_ll"] = make_hist("pt_ll", "p_{T}(l^{+}l^{-}) t#bar{t} templates", pt_bins, "p_{T} [GeV]", "ratio")
    histos["pt_pos"] = make_hist("pt_pos", "p_{T}(l^{+}) t#bar{t} templates", pt_bins, "p_{T}(l^{+}) [GeV]", "Events/bin")
    histos["E_pos"] = make_hist("E_pos", "E(l^{+}) t#bar{t} templates", energy_bins, "E(l^{+}) [GeV]", "Events/bin") 
    histos["M_ll"] = make_hist("M_ll", "M(l^{+}l^{-}) t#bar{t} templates", invariant_mass_bins, "M(l^{+}l^{-}) [GeV]", "Events/bin")
    histos["Ep_Em"] = make_hist("Ep_Em", "E(l^{+}) + E(l^{-}) t#bar{t} templates", e_sum_bins,"E(l^{+}) + E(l^{-}) [GeV]", "Events/bin")
    histos["ptp_ptm"] = make_hist("ptp_ptm", "p_{T}(l^{+}) + p_{T}(l^{-}) t#bar{t} templates", pt_sum_bins, "p_{T}(l^{+}) + p_{T}(l^{-}) [GeV]", "Events/bin")


    ttFiles = []
    for f in TT_FILELIST:
	ttFiles.append(TFile.Open(f, 'READ'))


    for key in histos:
	histos[key].Sumw2()
	
	for i, f in enumerate(ttFiles):
	    histos[key].Add(ttFiles.Get(key))
	
	histos[key].Scale(1.0 / histos[key].Integral())

    outF = TFile.Open("mc_TT_hypotheses.root", "RECREATE")
    for key in histos():
	histos[key].Write()





def runAnalysis(inFileDir, inFileName, file_index, outFileURL, pileupFile, xsec=None, n_mc_events=None):
    """
    Perform the analysis on a single file
    """
    print '...analysing %s' % inFileName                                           

    histos = {}
   
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
    
    inFileURL = "%s/%s/%s_%d.root" % (inFileDir, inFileName, inFileName, file_index)
				    
    print "About to open file %s" % (inFileURL)
   
    fIn = TFile.Open(inFileURL)

    print "%s opened successfully!" % (inFileURL)

    mass

    tfile_dir = fIn.Get("ggNtuplizer")
    tree=tfile_dir.Get("EventTree")


    pileupWeighter = PyleupRW(mc_file_list=inFileURL, pileupFile=pileupFile)
    
    
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
   
    
    for i in xrange(0, totalIterations):   
	if i%100==0 : 
	    sys.stdout.write('\r [ %d/100 ] done' %(int(float(100.*i)/float(totalEntries))) )
	    sys.stdout.flush()
	
	tree.GetEntry(i)
	
	# Apply Jet Resoution corrections (mc only)
	doJER(tree, JER_var_type)
	
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

	weight = 1.0

	pileup_weight = pileupWeighter.getWeight(tree.nPUInfo, tree.puBX, tree.puTrue)
	if pileup_weight != 1.0:
	    puWeightSum += pileup_weight
	    puEvents += 1

	weight = pileup_weight
	
	

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
		and bool(tree.eleIDbit[ele_n] >> 2 & 1)  # Medium ele cut
	        and ele_relIso < ele_relIso_cut[region]
		and tree.eleD0[ele_n] < ele_D0_cut[region]
		and tree.eleDz[ele_n] < ele_Dz_cut[region]):
		
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
	    # Rochester muon corrections
	    if tree.isData:
		tree.muPt[mu_n] *= rc.kScaleDT(tree.muCharge[mu_n], tree.muPt[mu_n], tree.muEta[mu_n], tree.muPhi[mu_n])
	    else:
		tree.muPt[mu_n] *= rc.kScaleAndSmearMC(tree.muCharge[mu_n], tree.muPt[mu_n], tree.muEta[mu_n], tree.muPhi[mu_n], tree.muTrkLayers[mu_n], random.random(), random.random()) 

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

			eleSCEta = tree.eleSCEta[e_ind]
			elePt = tree.elePt[e_ind]
			eleSF  = eleID_SF.GetBinContent(eleID_SF.FindBin(eleSCEta, min(150.0, elePt)))
			eleSF *= eleReco_SF.GetBinContent(eleReco_SF.FindBin(eleSCEta, min(150.0, elePt)))
			
			if eleSF == 0.0: print "eleSF = 0, SCEta = ", eleSCEta, "  Pt = ", elePt
			weight *= eleSF
			
			muEta = tree.muEta[mu_ind]
			muAEta = abs(muEta)
			muPt = tree.muPt[mu_ind]
			# Mu SFs stored in 2D histogram: (x,y) = (abs(eta), pt)
			muBF_SF  = muID_SF_BF.GetBinContent(muID_SF_BF.FindBin(muAEta, min(119.9, muPt)))
			muBF_SF *= muIso_SF_BF.GetBinContent(muIso_SF_BF.FindBin(muAEta, min(119.9, muPt)))
			muGH_SF  = muID_SF_GH.GetBinContent(muID_SF_GH.FindBin(muAEta, min(119.9, muPt)))
			muGH_SF *= muIso_SF_GH.GetBinContent(muIso_SF_GH.FindBin(muAEta, min(119.9, muPt)))
			if muBF_SF == 0.0: print "muBF_SF = 0!"
			if muGH_SF == 0.0: print "muGH_SF = 0!"

			muTrkSF = muTrack_SF.Eval(muAEta)
			if muTrkSF == 0.0: print "muTrkSF = 0, muAEta = ", muAEta
			

			mu8ele23_SF = 0.0
			mu23ele8_SF = 0.0
			if (tree.HLTEleMuX >> 23 & 1) | (tree.HLTEleMuX >> 24 & 1):
			    mu8ele23_SF = mu8_SF.GetBinContent(mu8_SF.FindBin(muEta, min(199.9, muPt))) * \
				      ele23_SF.GetBinContent(ele23_SF.FindBin(eleSCEta, min(99.9, elePt)))

			if (tree.HLTEleMuX >> 25 & 1) | (tree.HLTEleMuX >> 26 & 1):
			    mu23ele8_SF = mu23_SF.GetBinContent(mu23_SF.FindBin(muEta, min(199.9, muPt))) * \
				      ele8_SF.GetBinContent(ele8_SF.FindBin(eleSCEta, min(99.9, elePt)))
		       
			trigSF = max(mu8ele23_SF, mu23ele8_SF)
			#print "trigSF = ", trigSF
			weight *= (lumiBF * muBF_SF + lumiGH * muGH_SF) * muTrkSF * trigSF

			    
			    
			histos["pt_pos"].Fill(lp.Pt(), weight)
			histos["pt_ll"].Fill(ll.Pt(), weight)
			histos["E_pos"].Fill(lp.E(), weight)
			histos["M_ll"].Fill(ll.M(), weight)
			histos["Ep_Em"].Fill(lp.E() + lm.E(), weight)
			histos["ptp_ptm"].Fill(lp.Pt() + lm.Pt(), weight)
			    
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
    for key in histos: 
	histos[key].Scale(1.0 / histos[key].Integral())
	histos[key].Write()
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
				 pileupFile=args[4],
                                 xsec=args[5],
				 n_mc_events=args[6])
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
    num_files_in_sample = []

    # Determine number of files each sample is split into 
    for sample, sampleInfo in samplesList:
	p1 = Popen(["ls", "-alh", "%s/%s/" % (opt.inDir, sample)], stdout=PIPE)
	p2 = Popen(["grep", "root"], stdin=p1.stdout, stdout=PIPE)
	p3 = Popen(["wc", "-l"], stdin=p2.stdout, stdout=PIPE)
	num_files = int(p3.communicate()[0])
	num_files_in_sample.append(num_files)

	

    for index, (sample, sampleInfo) in enumerate(samplesList):
        #inFileURL  = "%s/%s.root" % (opt.inDir,sample)
        #if not os.path.isfile(inFileURL): continue
        xsec=sampleInfo[0] if sampleInfo[1]==0 else None
	n_mc_events=sampleInfo[5] if sampleInfo[1]==0 else None 
	
	for n in xrange(0, num_files_in_sample[index]):
	    outFileURL = "%s/%s_%d.root" % (opt.outDir, sample, n)
	    taskList.append( (opt.inDir, sample, n, outFileURL, opt.puF, xsec, n_mc_events) )
    
    # Run the analysis jobs
    if opt.njobs == 0:
        for inFileDir, inFileName, outFileURL, mc_file_list, xsec, n_mc_events in taskList:
            runAnalysis(inFileDir=inFileDir, inFileName=inFileName, numFiles=1, outFileURL=outFileURL, pileupFile=opt.puF, xsec=xsec, n_mc_events=n_mc_events)
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
