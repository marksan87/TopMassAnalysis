#include"EventTree.h"

/*
EventTree::EventTree(EventTree *evtTree) {
	// Shallow copy
	chain = evtTree->chain;
}
*/
EventTree::EventTree(int nFiles, char** fileNames){
	chain = new TChain("ggNtuplizer/EventTree");


	for(int fileI=0; fileI<nFiles; fileI++){
		chain->Add(fileNames[fileI]);
	}
	chain->SetBranchStatus("*",0);
	
	// keep some important branches
//	chain->SetBranchStatus("nHLT",1);
//	chain->SetBranchAddress("nHLT", &nHLT_);
//	chain->SetBranchStatus("HLT",1);
//	chain->SetBranchAddress("HLT", HLT_);
//	chain->SetBranchStatus("HLTIndex",1);
//	chain->SetBranchAddress("HLTIndex", HLTIndex_);
//	chain->SetBranchStatus("bspotPos",1);
//	chain->SetBranchAddress("bspotPos", bspotPos_);
//	chain->SetBranchStatus("hasGoodVtx",1);
//	chain->SetBranchAddress("hasGoodVtx", &hasGoodVtx_);
	
	chain->SetBranchStatus("HLTEleMuX",1);
	chain->SetBranchAddress("HLTEleMuX", &HLTEleMuX_);

	chain->SetBranchStatus("HLTEleMuXIsPrescaled",1);
	chain->SetBranchStatus("HLTEleMuXIsPrescaled", &HLTEleMuXIsPrescaled_);

	if (chain->GetListOfBranches()->FindObject("nPUInfo")) {
	    chain->SetBranchStatus("nPUInfo",1);
	    chain->SetBranchAddress("nPUInfo", &nPUInfo_);
	}

	if (chain->GetListOfBranches()->FindObject("nPU")) {
	    nPU_ = new vector<int>;
	    chain->SetBranchStatus("nPU",1);
	    chain->SetBranchAddress("nPU", &nPU_);
	}

	if (chain->GetListOfBranches()->FindObject("puBX")) {
	    puBX_ = new vector<int>;
	    chain->SetBranchStatus("puBX",1);
	    chain->SetBranchAddress("puBX", &puBX_);
	}

	if (chain->GetListOfBranches()->FindObject("puTrue")) {
	    puTrue_ = new vector<float>;
	    chain->SetBranchStatus("puTrue",1);
	    chain->SetBranchAddress("puTrue", &puTrue_);
	}

	if (chain->GetListOfBranches()->FindObject("pdf")) {
	    chain->SetBranchStatus("pdf",1);
	    chain->SetBranchAddress("pdf", &pdf_);
	}

	// event
	
	chain->SetBranchStatus("run",1);
	chain->SetBranchAddress("run", &run_);

	chain->SetBranchStatus("event",1);
	chain->SetBranchAddress("event", &event_);
	
	chain->SetBranchStatus("lumis",1);
	chain->SetBranchAddress("lumis", &lumis_);

	chain->SetBranchStatus("isData",1);
	chain->SetBranchAddress("isData", &isData_);

	chain->SetBranchStatus("nVtx",1);
	chain->SetBranchAddress("nVtx", &nVtx_);

	chain->SetBranchStatus("pfMET",1);    
	chain->SetBranchAddress("pfMET", &pfMET_); 

	chain->SetBranchStatus("pfMETPhi",1);
	chain->SetBranchAddress("pfMETPhi", &pfMETPhi_);  

	if (chain->GetBranch("genMET")) {
	    chain->SetBranchStatus("genMET",1);    
	    chain->SetBranchAddress("genMET", &genMET_); 
	}
	// electrons	
	
	chain->SetBranchStatus("nEle",1);
	chain->SetBranchAddress("nEle", &nEle_);

	
	elePt_ = new vector<float>;
	chain->SetBranchStatus("elePt",1);
	chain->SetBranchAddress("elePt", &elePt_);

	eleEta_ = new vector<float>;
	chain->SetBranchStatus("eleEta",1);
	chain->SetBranchAddress("eleEta", &eleEta_);

	eleSCEta_ = new vector<float>;
	chain->SetBranchStatus("eleSCEta",1);
	chain->SetBranchAddress("eleSCEta", &eleSCEta_);

	elePhi_ = new vector<float>;
	chain->SetBranchStatus("elePhi",1);
	chain->SetBranchAddress("elePhi", &elePhi_);

	elePFChIso_ = new vector<float>;
	chain->SetBranchStatus("elePFChIso",1);
	chain->SetBranchAddress("elePFChIso", &elePFChIso_);

	elePFNeuIso_ = new vector<float>;
	chain->SetBranchStatus("elePFNeuIso",1);
	chain->SetBranchAddress("elePFNeuIso", &elePFNeuIso_);

	elePFPhoIso_ = new vector<float>;
	chain->SetBranchStatus("elePFPhoIso",1);
	chain->SetBranchAddress("elePFPhoIso", &elePFPhoIso_);

	chain->SetBranchStatus("rho",1);
	chain->SetBranchAddress("rho", &rho_);

//	eleIDMVATrg_ = new vector<float>;
//	chain->SetBranchStatus("eleIDMVATrg",1);
//	chain->SetBranchAddress("eleIDMVATrg", &eleIDMVATrg_);
        
//	eleIDMVANonTrg_ = new vector<float>;
//        chain->SetBranchStatus("eleIDMVANonTrg",1);
//        chain->SetBranchAddress("eleIDMVANonTrg", &eleIDMVANonTrg_); 
        
	eleIDbit_ = new vector<unsigned short>;
        chain->SetBranchStatus("eleIDbit",1);
        chain->SetBranchAddress("eleIDbit", &eleIDbit_);

	eleIDMVA_ = new vector<float>;
	chain->SetBranchStatus("eleIDMVA",1);
	chain->SetBranchAddress("eleIDMVA", &eleIDMVA_);

	eleIDMVAHZZ_ = new vector<float>;
	chain->SetBranchStatus("eleIDMVAHZZ",1);
	chain->SetBranchAddress("eleIDMVAHZZ", &eleIDMVAHZZ_);


	eleD0_ = new vector<float>;
	chain->SetBranchStatus("eleD0",1);
	chain->SetBranchAddress("eleD0", &eleD0_);

	eleMissHits_ = new vector<int>;
	chain->SetBranchStatus("eleMissHits",1);
	chain->SetBranchAddress("eleMissHits", &eleMissHits_);

	eleConvVeto_ = new vector<int>;
	chain->SetBranchStatus("eleConvVeto",1);
	chain->SetBranchAddress("eleConvVeto", &eleConvVeto_);
	
	eledEtaseedAtVtx_ = new vector<int>;
	chain->SetBranchStatus("eledEtaseedAtVtx",1);
	chain->SetBranchAddress("eledEtaseedAtVtx", &eledEtaseedAtVtx_);

	eleDz_ = new vector<float>;
	chain->SetBranchStatus("eleDz",1);
	chain->SetBranchAddress("eleDz", &eleDz_);

	eleHoverE_ = new vector<float>;
	chain->SetBranchStatus("eleHoverE",1);
	chain->SetBranchAddress("eleHoverE", &eleHoverE_);

	eleEoverP_ = new vector<float>;
	chain->SetBranchStatus("eleEoverP",1);
	chain->SetBranchAddress("eleEoverP", &eleEoverP_);

	eleEoverPInv_ = new vector<float>;
	chain->SetBranchStatus("eleEoverPInv",1);
	chain->SetBranchAddress("eleEoverPInv", &eleEoverPInv_);

	// keep this branch in the skim
//	chain->SetBranchStatus("elePin",1);

	//eleSigmaIEtaIEta_ = new vector<float>;
	//chain->SetBranchStatus("eleSigmaIEtaIEta",1);
	//chain->SetBranchAddress("eleSigmaIEtaIEta", &eleSigmaIEtaIEta_);

	eleSigmaIEtaIEtaFull5x5_ = new vector<float>;
	chain->SetBranchStatus("eleSigmaIEtaIEtaFull5x5", 1);
	chain->SetBranchAddress("eleSigmaIEtaIEtaFull5x5", &eleSigmaIEtaIEtaFull5x5_);

	eledEtaAtVtx_ = new vector<float>;
	chain->SetBranchStatus("eledEtaAtVtx",1);
	chain->SetBranchAddress("eledEtaAtVtx", &eledEtaAtVtx_);

	eledPhiAtVtx_ = new vector<float>;
	chain->SetBranchStatus("eledPhiAtVtx",1);
	chain->SetBranchAddress("eledPhiAtVtx", &eledPhiAtVtx_);

	
	eleCharge_ = new vector<int>;
	chain->SetBranchStatus("eleCharge");
	chain->SetBranchAddress("eleCharge", &eleCharge_);

//eleGenIndex_ = new vector<int>;
//	chain->SetBranchStatus("eleGenIndex",1);
//	chain->SetBranchAddress("eleGenIndex", &eleGenIndex_);

//	eleGenGMomPID_ = new vector<int>;
//	chain->SetBranchStatus("eleGenGMomPID",1);
//	chain->SetBranchAddress("eleGenGMomPID", &eleGenGMomPID_);

//	eleGenMomPID_ = new vector<int>;
//	chain->SetBranchStatus("eleGenMomPID",1);
//	chain->SetBranchAddress("eleGenMomPID", &eleGenMomPID_);

	// muons
	// keep some branches in the skim
	
	
	muChi2NDF_ = new vector<float>;
	chain->SetBranchStatus("muChi2NDF", 1);
	chain->SetBranchAddress("muChi2NDF",&muChi2NDF_);

	muTrkLayers_ = new vector<int>;
	chain->SetBranchStatus("muTrkLayers",1);
	chain->SetBranchAddress("muTrkLayers",&muTrkLayers_);
		
	muMuonHits_ = new vector<int>;
	chain->SetBranchStatus("muMuonHits",1);
	chain->SetBranchAddress("muMuonHits", &muMuonHits_);

	muPixelHits_ = new vector<int>;
	chain->SetBranchStatus("muPixelHits",1);
	chain->SetBranchAddress("muPixelHits",&muPixelHits_);
	
	muDz_ = new vector<float>;
	chain->SetBranchStatus("muDz",1);
	chain->SetBranchAddress("muDz",&muDz_);
	
	muD0_ = new vector<float>;
	chain->SetBranchStatus("muD0",1);
	chain->SetBranchAddress("muD0",&muD0_);

	muStations_ = new vector<int>;
	chain->SetBranchStatus("muStations",1);
	chain->SetBranchAddress("muStations",&muStations_);

	chain->SetBranchStatus("nMu",1);
	chain->SetBranchAddress("nMu", &nMu_);

	muPt_ = new vector<float>;
	chain->SetBranchStatus("muPt",1);
	chain->SetBranchAddress("muPt", &muPt_);

	muEta_ = new vector<float>;
	chain->SetBranchStatus("muEta",1);
	chain->SetBranchAddress("muEta", &muEta_);

	muPhi_ = new vector<float>;
	chain->SetBranchStatus("muPhi",1);
	chain->SetBranchAddress("muPhi", &muPhi_);
	
	muPFChIso_ = new vector<float>;
	chain->SetBranchStatus("muPFChIso",1);
	chain->SetBranchAddress("muPFChIso", &muPFChIso_);
	
	muPFNeuIso_ = new vector<float>;
	chain->SetBranchStatus("muPFNeuIso",1);
	chain->SetBranchAddress("muPFNeuIso", &muPFNeuIso_);
	
	muPFPhoIso_ = new vector<float>;
	chain->SetBranchStatus("muPFPhoIso",1);
	chain->SetBranchAddress("muPFPhoIso", &muPFPhoIso_);

	muPFPUIso_ = new vector<float>;
	chain->SetBranchStatus("muPFPUIso",1);
	chain->SetBranchAddress("muPFPUIso", &muPFPUIso_);

	muType_ = new vector<int>;
	chain->SetBranchStatus("muType",1);
	chain->SetBranchAddress("muType",&muType_);


	muCharge_ = new vector<int>;
	chain->SetBranchStatus("muCharge",1);
	chain->SetBranchAddress("muCharge", &muCharge_);

	muIDbit_ = new vector<unsigned short>;
	chain->SetBranchStatus("muIDbit",1);
	chain->SetBranchAddress("muIDbit", &muIDbit_);

	// jets
	
	chain->SetBranchStatus("nJet",1);
	chain->SetBranchAddress("nJet", &nJet_);

	jetPt_ = new vector<float>;
	chain->SetBranchStatus("jetPt",1);
	chain->SetBranchAddress("jetPt", &jetPt_);

	jetRawPt_ = new vector<float>;
	chain->SetBranchStatus("jetRawPt",1);
        chain->SetBranchAddress("jetRawPt", &jetRawPt_);
	
	jetEta_ = new vector<float>;
	chain->SetBranchStatus("jetEta",1);
	chain->SetBranchAddress("jetEta", &jetEta_);
	
	jetPhi_ = new vector<float>;
	chain->SetBranchStatus("jetPhi",1);
	chain->SetBranchAddress("jetPhi", &jetPhi_);

	jetEn_ = new vector<float>;
	chain->SetBranchStatus("jetEn",1);
	chain->SetBranchAddress("jetEn", &jetEn_);

	jetID_ = new vector<int>;
	chain->SetBranchStatus("jetID",1);
	chain->SetBranchAddress("jetID", &jetID_);

	jetPFLooseID_ = new vector<bool>;
	chain->SetBranchStatus("jetPFLooseId",1);
        chain->SetBranchAddress("jetPFLooseId", &jetPFLooseID_);

	jetArea_ = new vector<float>;
	chain->SetBranchStatus("jetArea",1);
	chain->SetBranchAddress("jetArea", &jetArea_);

	jetCHF_ = new vector<float>;
	chain->SetBranchStatus("jetCHF",1);
	chain->SetBranchAddress("jetCHF", &jetCHF_);

	jetNHF_ = new vector<float>;
	chain->SetBranchStatus("jetNHF",1);
	chain->SetBranchAddress("jetNHF", &jetNHF_);

	jetCEF_ = new vector<float>;
	chain->SetBranchStatus("jetCEF",1);
	chain->SetBranchAddress("jetCEF", &jetCEF_);
	
	jetNEF_ = new vector<float>;
	chain->SetBranchStatus("jetNEF",1);
	chain->SetBranchAddress("jetNEF", &jetNEF_);

/*	jetNNeutrals_ = new vector<float>;
	chain->SetBranchStatus("jetNNeutrals",1);
	chain->SetBranchAddress("jetNNeutrals", &jetNNeutrals_);

	jetNCharged_ = new vector<float>;
	chain->SetBranchStatus("jetNCharged",1);
	chain->SetBranchAddress("jetNCharged", &jetNCharged_);

	jetNConstituents_ = new vector<int>;
	chain->SetBranchStatus("jetNConstituents",1);
	chain->SetBranchAddress("jetNConstituents", &jetNConstituents_);
*/
	AK8Jetnconstituents_ = new vector<int>;
	chain->SetBranchStatus("AK8Jetnconstituents",1);
	chain->SetBranchAddress("AK8Jetnconstituents", &AK8Jetnconstituents_);
	
//	jetNCharged_ = new vector<float>;
//	chain->SetBranchStatus("jetNCharged",1);
//	chain->SetBranchAddress("jetNCharged", &jetNCharged_);

	AK8JetCEF_ = new vector<float>;	
	chain->SetBranchStatus("AK8JetCEF",1);
	chain->SetBranchAddress("AK8JetCEF", &AK8JetCEF_);

	AK8JetNHF_ = new vector<float>;
	chain->SetBranchStatus("AK8JetNHF",1);
	chain->SetBranchAddress("AK8JetNHF", &AK8JetNHF_);
	
	AK8JetNEF_ = new vector<float>;
	chain->SetBranchStatus("AK8JetNEF",1);
	chain->SetBranchAddress("AK8JetNEF", &AK8JetNEF_);
	
	AK8JetCHF_ = new vector<float>;
	chain->SetBranchStatus("AK8JetCHF",1);
	chain->SetBranchAddress("AK8JetCHF", &AK8JetCHF_);

	jetCSV2BJetTags_ = new vector<float>;
	chain->SetBranchStatus("jetCSV2BJetTags",1);
	chain->SetBranchAddress("jetCSV2BJetTags", &jetCSV2BJetTags_);
	
	if (chain->GetBranch("jetPartonID")) {
	    jetPartonID_ = new vector<int>;
	    chain->SetBranchStatus("jetPartonID",1);
	    chain->SetBranchAddress("jetPartonID", &jetPartonID_);
	}

	if (chain->GetBranch("jetGenPartonID")) {
	    jetGenPartonID_ = new vector<int>;
	    chain->SetBranchStatus("jetGenPartonID",1);
	    chain->SetBranchAddress("jetGenPartonID", &jetGenPartonID_);
	}

	if (chain->GetBranch("jetGenJetIndex")) {
	    jetGenJetIndex_ = new vector<int>;
	    chain->SetBranchStatus("jetGenJetIndex",1);
	    chain->SetBranchAddress("jetGenJetIndex", &jetGenJetIndex_);
	}

	if (chain->GetBranch("jetGenJetPt")) {
	    jetGenJetPt_ = new vector<float>;
	    chain->SetBranchStatus("jetGenJetPt",1);
	    chain->SetBranchAddress("jetGenJetPt", &jetGenJetPt_);
	}
    
	if (chain->GetBranch("jetGenPt")) {
	    jetGenPt_ = new vector<float>;
	    chain->SetBranchStatus("jetGenPt",1);
	    chain->SetBranchAddress("jetGenPt", &jetGenPt_);
	}

	if (chain->GetBranch("jetGenEta")) {
	    jetGenEta_ = new vector<float>;
	    chain->SetBranchStatus("jetGenEta",1);
	    chain->SetBranchAddress("jetGenEta", &jetGenEta_);
	}

	if (chain->GetBranch("jetGenPhi")) {
	    jetGenPhi_ = new vector<float>;
	    chain->SetBranchStatus("jetGenPhi",1);
	    chain->SetBranchAddress("jetGenPhi", &jetGenPhi_);
	}

/********************************************************************
// Photons
//  
	chain->SetBranchStatus("nPho",1);
	chain->SetBranchAddress("nPho", &nPho_);

	phoEt_ = new vector<float>;	
	chain->SetBranchStatus("phoEt",1);
	chain->SetBranchAddress("phoEt", &phoEt_);
	
	phoEta_ = new vector<float>;
	chain->SetBranchStatus("phoEta",1);
	chain->SetBranchAddress("phoEta", &phoEta_);

	phoPhi_ = new vector<float>;
	chain->SetBranchStatus("phoPhi",1);
	chain->SetBranchAddress("phoPhi", &phoPhi_);
	
	phoSeedBCE_ = new vector<int>;
	chain->SetBranchStatus("phoSeedBCE",1);
	chain->SetBranchAddress("phoSeedBCE", &phoSeedBCE_);
	
	phohasPixelSeed_ = new vector<int>;
	chain->SetBranchStatus("phohasPixelSeed",1);
	chain->SetBranchAddress("phohasPixelSeed", &phohasPixelSeed_);

	phoEleVeto_ = new vector<int>;
	chain->SetBranchStatus("phoEleVeto",1);
	chain->SetBranchAddress("phoEleVeto", &phoEleVeto_);
	
	phoHoverE_ = new vector<float>;
	chain->SetBranchStatus("phoHoverE",1);
	chain->SetBranchAddress("phoHoverE", &phoHoverE_);

	phoSigmaIEtaIEta_ = new vector<float>;
	chain->SetBranchStatus("phoSigmaIEtaIEta",1);
	chain->SetBranchAddress("phoSigmaIEtaIEta", &phoSigmaIEtaIEta_);
	
	phoPFChIso_ = new vector<float>;
	chain->SetBranchStatus("phoPFChIso",1);
	chain->SetBranchAddress("phoPFChIso", &phoPFChIso_);
	
	phoPFNeuIso_ = new vector<float>;
	chain->SetBranchStatus("phoPFNeuIso",1);
	chain->SetBranchAddress("phoPFNeuIso", &phoPFNeuIso_);

	phoPFPhoIso_ = new vector<float>;
	chain->SetBranchStatus("phoPFPhoIso",1);
	chain->SetBranchAddress("phoPFPhoIso", &phoPFPhoIso_);

	phoPFPhoIsoFrix7_ = new vector<float>;
	chain->SetBranchStatus("phoPFPhoIsoFrix7",1);
	chain->SetBranchAddress("phoPFPhoIsoFrix7", &phoPFPhoIsoFrix7_);

	phoPFChIsoFrix7_ = new vector<float>;
	chain->SetBranchStatus("phoPFChIsoFrix7",1);
	chain->SetBranchAddress("phoPFChIsoFrix7", &phoPFChIsoFrix7_);
	
	phoPFPhoIsoFrix6_ = new vector<float>;
	chain->SetBranchStatus("phoPFPhoIsoFrix6",1);
	chain->SetBranchAddress("phoPFPhoIsoFrix6", &phoPFPhoIsoFrix6_);
	
	phoPFChIsoFrix6_ = new vector<float>;
	chain->SetBranchStatus("phoPFChIsoFrix6",1);
	chain->SetBranchAddress("phoPFChIsoFrix6", &phoPFChIsoFrix6_);

//	phoGenIndex_ = new vector<int>;
//	chain->SetBranchStatus("phoGenIndex",1);
//	chain->SetBranchAddress("phoGenIndex", &phoGenIndex_);
	
//	phoGenGMomPID_ = new vector<int>;
//	chain->SetBranchStatus("phoGenGMomPID",1);
//	chain->SetBranchAddress("phoGenGMomPID", &phoGenGMomPID_);
	
//	phoGenMomPID_ = new vector<int>;
//	chain->SetBranchStatus("phoGenMomPID",1);
//	chain->SetBranchAddress("phoGenMomPID", &phoGenMomPID_);
*************************************************************************************/	

	// MC gen particles
	if (chain->GetBranch("nMC")) {	
	    chain->SetBranchStatus("nMC",1);
	    chain->SetBranchAddress("nMC", &nMC_);
	}
	
	if (chain->GetBranch("mcPt")) {
	    mcPt = new vector<float>;
	    chain->SetBranchStatus("mcPt",1);
	    chain->SetBranchAddress("mcPt", &mcPt);
	}

	if (chain->GetBranch("mcEta")) {
	    mcEta = new vector<float>;
	    chain->SetBranchStatus("mcEta",1);
	    chain->SetBranchAddress("mcEta", &mcEta);
	}
	
	if (chain->GetBranch("mcPhi")) {
	    mcPhi = new vector<float>;
	    chain->SetBranchStatus("mcPhi",1);
	    chain->SetBranchAddress("mcPhi", &mcPhi);
	}
	
	if (chain->GetBranch("mcMass")) {
	    mcMass = new vector<float>;
	    chain->SetBranchStatus("mcMass",1);
	    chain->SetBranchAddress("mcMass", &mcMass);
	}
	
	if (chain->GetBranch("mcPID")) {
	    mcPID = new vector<int>;
	    chain->SetBranchStatus("mcPID",1);
	    chain->SetBranchAddress("mcPID", &mcPID);
	}

	if (chain->GetBranch("mcMomPID")) {
	    mcMomPID = new vector<int>;
	    chain->SetBranchStatus("mcMomPID",1);
	    chain->SetBranchAddress("mcMomPID", &mcMomPID);
	}

	if (chain->GetBranch("mcGMomPID")) {
	    mcGMomPID = new vector<int>;
	    chain->SetBranchStatus("mcGMomPID",1);
	    chain->SetBranchAddress("mcGMomPID", &mcGMomPID);
	}

	if (chain->GetBranch("mcMomPt")) {
	    mcMomPt = new vector<float>;
	    chain->SetBranchStatus("mcMomPt",1);
	    chain->SetBranchAddress("mcMomPt", &mcMomPt);
	}
//	mcDecayType = new vector<int>;
//	chain->SetBranchStatus("mcDecayType",1);
//	chain->SetBranchAddress("mcDecayType", &mcDecayType);
	
	if (chain->GetBranch("mcIndex")) {
	    mcIndex = new vector<int>;
	    chain->SetBranchStatus("mcIndex",1);
	    chain->SetBranchAddress("mcIndex", &mcIndex);
	}

	if (chain->GetBranch("mcStatus")) {
	    mcStatus = new vector<int>;
	    chain->SetBranchStatus("mcStatus",1);
	    chain->SetBranchAddress("mcStatus", &mcStatus);
	}

	if (chain->GetBranch("mcMomEta")) {	
	    mcMomEta = new vector<float>;
	    chain->SetBranchStatus("mcMomEta",1);
	    chain->SetBranchAddress("mcMomEta", &mcMomEta);
	}

	if (chain->GetBranch("mcMomPhi")) {
	    mcMomPhi = new vector<float>;
	    chain->SetBranchStatus("mcMomPhi",1);
	    chain->SetBranchAddress("mcMomPhi", &mcMomPhi);
	}

	if (chain->GetBranch("mcMomMass")) {
	    mcMomMass = new vector<float>;
	    chain->SetBranchStatus("mcMomMass",1);
	    chain->SetBranchAddress("mcMomMass", &mcMomMass);
	}

	if (chain->GetBranch("mcParentage")) {
	    mcParentage = new vector<int>;
	    chain->SetBranchStatus("mcParentage",1);
	    chain->SetBranchAddress("mcParentage", &mcParentage);
	}	
}

EventTree::~EventTree(){
	delete chain;
	// will be some memory leak due to created vectors
}

Long64_t EventTree::GetEntries(){
	return chain->GetEntries();
}

Int_t EventTree::GetEntry(long long entry){
	chain->GetEntry(entry);
	return 0;
}
