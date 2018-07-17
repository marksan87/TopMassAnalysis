import ROOT
from ROOT import TFile, TH1F, TH1D, TCanvas

class PyleupRW(object):
    def __init__(self, mc_file_list=None, pileupFile=None, PUweightHist=None):
	"""Initializes the pileup reweighter
	   Inputting mc_file_list and pileupFile calculates a new pileup weight histogram 
	   Inputting just PUweightHist creates a copy of the object 

	"""
	
	self.PUweightSum = {"nom":0, "up":0, "down":0}  # sum of all of the pu corrections 
	self.events = {"nom":0, "up":0, "down":0}  # sum of all the events which require pu corrections
	self.PUweightHist = {}  # Dictionary of pileup histograms with systematics: nominal, up, down 
	self.mcPUHist = None
	ROOT.gROOT.cd()
	if mc_file_list is not None and pileupFile is not None and PUweightHist is not None:
	    print "Too many args. Either input mc_file_list and pileupFile OR PUweightHist"
	    return

	if mc_file_list is not None and pileupFile is not None:
	    # Create new pileup histogram
	    self._createPUweightHist(mc_file_list, pileupFile)

	elif PUweightHist is not None:
	    # Copy pileup histogram
	    self.PUweightHist = PUweightHist.Clone()
	    self.PUweightHist.SetDirectory(0)

    def _createPUweightHist(self, mc_file_list, pileupFile):
	# Internal method
	ROOT.gROOT.cd()
	puF = TFile.Open(pileupFile)
	self.PUweightHist["nom"] = puF.Get("pileup")
	self.PUweightHist["nom"].SetDirectory(0)
	
        self.PUweightHist["up"] = puF.Get("pileupUp")
	self.PUweightHist["up"].SetDirectory(0)
	
	self.PUweightHist["down"] = puF.Get("pileupDown")
	self.PUweightHist["down"].SetDirectory(0)
        puF.Close()

	mcPU = None 
	for mc_file in mc_file_list:
	    #print "reading file ", mc_file
	    mcFile = TFile.Open(mc_file)
	    if not mcFile.Get("ggNtuplizer/hPUTrue"):
		print "no hPU histogram here!"
		PUweightHist = None
		return

	    if mcPU == None: 
		mcPU = mcFile.Get("ggNtuplizer/hPUTrue")
	    else: 
		mcPU.Add(mcFile.Get("ggNtuplizer/hPUTrue"))
	    
	    mcPU.SetDirectory(0)
	    mcFile.Close()

	self.mcPUHist = mcPU.Clone()
	self.mcPUHist.SetDirectory(0)

	mcPU.Scale(1.0/mcPU.Integral())
	
        for sys in ["nom", "down", "up"]:
            PUweightInt = self.PUweightHist[sys].Integral()
            self.PUweightHist[sys].Divide(mcPU)
            self.PUweightHist[sys].Scale(1.0/PUweightInt)


    def getWeight(self, nPUInfo, puBX, puTrue,sys="nom"):
	PUweight = 0.0
	if self.PUweightHist is None:
	    print "PUweightHist invalid"
	    return 1.0

	for puInd in xrange(0, nPUInfo):
	    if puBX[puInd] == 0:
		PUweight = self.PUweightHist[sys].GetBinContent(self.PUweightHist[sys].GetXaxis().FindBin(puTrue[puInd]))
		break

	self.events[sys] += 1
	self.PUweightSum[sys] += PUweight
	return PUweight

    def getAvgWeight(self, sys="nom"):
	return -1.0 if self.events[sys] == 0 else self.PUweightSum[sys]/self.events[sys]

