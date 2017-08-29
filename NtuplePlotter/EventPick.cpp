#include"EventPick.h"

const bool include_singleLep_triggers = true;
const bool use_data_triggers = true; 
const bool use_mc_triggers = false;
const bool runH = false;    // Disable non-DZ triggers for Run H


double secondMinDr(int myInd, const EventTree* tree);

// Full mode keeps all events with >=2 leptons
// Lite mode only keeps events with at least one e and one u (to surpress DY background)
EventPick::EventPick(std::string titleIn, bool liteMode){
	title = titleIn;
	isLiteMode = liteMode;

	cutFlow = new TH1F("cut_flow","cut flow",10,-0.5,9.5);
	cutFlow->SetDirectory(0);
	set_cutflow_labels(cutFlow); // keep the labels close to the cuts definitions (below)
	histVector.push_back(cutFlow);
	
	cutFlowWeight = new TH1F("cut_flow_weight","cut flow with PU weight",10,-0.5,9.5);
	cutFlowWeight->SetDirectory(0);
	set_cutflow_labels(cutFlowWeight);
	histVector.push_back(cutFlowWeight);

	// assign cut values
	//veto_jet_dR = 0.1;
	veto_lep_jet_dR = 0.4;

	jet_pt_cut = 30;
	Njet_ge = 1;
	NBjet_ge = 1;
	Nele_eq = 1;
	Nmu_eq = 1;
}

EventPick::~EventPick(){
}

void EventPick::process_event(const EventTree* inp_tree, const Selector* inp_selector, double weight) {
	tree = inp_tree;
	selector = inp_selector;
	clear_vectors();

	passPreSel = false;
	passAll = false;
	
	//loose electrons
	for(std::vector<int>::const_iterator eleInd = selector->Electrons.begin(); eleInd != selector->Electrons.end(); eleInd++){
		bool goodEle = true;
//		for(int jetInd = 0; jetInd < tree->nJet_; jetInd++){
//			double drje = dR_jet_ele(jetInd, *eleInd);
//			if(tree->jetPt_->at(jetInd) > jet_pt_cut && veto_jet_dR <= drje && drje < veto_lep_jet_dR) goodEle = false;
//		}
		if(goodEle) Electrons.push_back(*eleInd);
	}
	
	for(std::vector<int>::const_iterator muInd = selector->Muons.begin(); muInd != selector->Muons.end(); muInd++) {
		bool goodMu = true;
//		for(int jetInd = 0; jetInd < tree->nJet_; jetInd++){
//			double drjmu = dR_jet_mu(jetInd, *muInd);
//			if(tree->jetPt_->at(jetInd) > jet_pt_cut && veto_jet_dR <= drjmu && drjmu < veto_lep_jet_dR) goodMu = false;
//		}
		if(goodMu) Muons.push_back(*muInd);
	}


	// pre-selection: top ref selection
	// copy jet and electron collections, consiering overlap of jets with electrons, loose electrons:
	// keep jets not close to leptons (veto_lep_jet_dR)
	for(std::vector<int>::const_iterator jetInd = selector->Jets.begin(); jetInd != selector->Jets.end(); jetInd++){
		bool goodJet = true;
		
		//  Save jet cleaning for analysis-level cuts
//		for(std::vector<int>::const_iterator eleInd = selector->Electrons.begin(); eleInd != selector->Electrons.end(); eleInd++)
//			if(dR_jet_ele(*jetInd, *eleInd) < veto_lep_jet_dR) goodJet = false;
//		for(std::vector<int>::const_iterator muInd = selector->Muons.begin(); muInd != selector->Muons.end(); muInd++)
//		                      if(dR_jet_mu(*jetInd, *muInd) < veto_lep_jet_dR) goodJet = false;
		if(goodJet) Jets.push_back(*jetInd);
		
		// take care of bJet collection
		for(std::vector<int>::const_iterator bjetInd = selector->bJets.begin(); bjetInd != selector->bJets.end(); bjetInd++)
			if(*bjetInd == *jetInd && goodJet) bJets.push_back(*bjetInd);
	}
	
	cutFlow->Fill(0.0); // Input events
	cutFlowWeight->Fill(0.0,weight);
	passPreSel = true;
	passVertexCut = true;
	passElectronCut = true;
	passMuonCut = true;
	passJetCut = true;
	passbJetCut = true;

	passTriggers = false;

	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
	// HLT triggers (boolean flags) are contained within the HLTEleMuX_ variable, descriptions of which are located     //
	// in ggNtuplizer_globalEvent.cc. Each trigger flag is represented by a bitshift of this variable.		    //
	//														    //
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopTrigger#Run2016B_C_and_D_25_ns_data_with			    //
	// Dilepton eu triggers for Run2016 B-H 23Sep2016ReReco data with RunIISummer16 Moriond17_80X MC		    //
	//														    //
	// HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v  23								    //
	// HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_v  25								    //
	//														    //
	// HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v  24							    //
	// HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ_v  26							    //
	//														    //
	// HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v     51							    //
	// HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v  52							    //
	// HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v     53							    //
	// HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v  54							    //
	//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

/*
	if (use_data_triggers) {
	    passTriggers |= (tree->HLTEleMuX_ >> 24 & 1) | 
			    (tree->HLTEleMuX_ >> 26 & 1);

	    if (!runH) {
		passTriggers |= (tree->HLTEleMuX_ >> 23 & 1) |
				(tree->HLTEleMuX_ >> 25 & 1); 
	    }
	}
*/

	if (use_data_triggers) {
	    passTriggers |= (tree->HLTEleMuX_ >> 52 & 1) | 
			    (tree->HLTEleMuX_ >> 54 & 1) |
			    (tree->HLTEleMuX_ >> 24 & 1);

	    if (!runH) {
		passTriggers |= (tree->HLTEleMuX_ >> 51 & 1) |
				(tree->HLTEleMuX_ >> 53 & 1) | 
				(tree->HLTEleMuX_ >> 23 & 1);
	    }
	}
	
	if (use_mc_triggers) {
	    passTriggers |= (tree->HLTEleMuX_ >> 51 & 1) | 
			    (tree->HLTEleMuX_ >> 52 & 1) |
			    (tree->HLTEleMuX_ >> 23 & 1) |
			    (tree->HLTEleMuX_ >> 53 & 1) |
			    (tree->HLTEleMuX_ >> 54 & 1);
	}

	// DEPRICATED
	// Combining dilepton triggers with single lepton triggers increases statistics by ~10%
	// Single electron: HLT_Ele23_WPLoose_Gsf  (6)
	// Single muon: HLT_IsoMu20_v  (31)   and   HLT_IsoTkMu20_v  (32)
	
	//if (!use_dilepton_trigger) { passTriggers |= (tree->HLTEleMuX_ >> 6 & 1) | (tree->HLTEleMuX_ >> 31 & 1) | (tree->HLTEleMuX_ >> 32 & 1); }


	if (passPreSel && tree->nGoodVtx_ >= 0 && passTriggers) {  
		cutFlow->Fill(1.0); cutFlowWeight->Fill(1.0,weight);
	} 
	else { 
		passPreSel = false; 
		passVertexCut = false;
	}

	
	// Lite mode: Keep only events with at least 1 e and 1 u
	// Full mode: Keep all events that have >= 2 passing leptons (ignore flavor at this stage)
	if (isLiteMode) {
		if (passPreSel && Electrons.size() > 0 && Muons.size() > 0) {
			cutFlow->Fill(2.0); cutFlowWeight->Fill(2.0, weight);
		}
		else {	
			passPreSel = false;
			passElectronCut = (Electrons.size() == 0) ? false : true;
			passMuonCut = (Muons.size() == 0) ? false : true;
		}
	}

	else { // Full mode
		if (passPreSel && (Electrons.size() + Muons.size() >= 2))  {
			cutFlow->Fill(2.0); cutFlowWeight->Fill(2.0, weight);
		}
		else {
			passPreSel = false;
			passElectronCut = (Electrons.size() == 0) ? false : true;
			passMuonCut = (Muons.size() == 0) ? false : true;
		}
	}


	if ( passPreSel && Jets.size() > 0) {
		cutFlow->Fill(3.0); cutFlowWeight->Fill(3.0, weight);
	}
	else {
		passPreSel = false; 
		passJetCut = false; 
	}

	// Save events which aren't tagged as bjets (medium tagging used here). This allows for the use of different offline descriminators 
	if ( passPreSel &&  bJets.size() > 0) {
		cutFlow->Fill(4.0); cutFlowWeight->Fill(4.0,weight);
	}

	if ( !(tree->isData_) ) { 
	    int EleP = 0;
	    int EleM = 0;
	    int MuP = 0;
	    int MuM = 0;
	    int TauP = 0;
	    int TauM = 0;

	    for( int mcI = 0; mcI < tree->nMC_; ++mcI){
	      if(abs(tree->mcMomPID->at(mcI))==24 && tree->mcParentage->at(mcI)==10){
		if( tree->mcPID->at(mcI) == 11 ) EleP = 1;
		if( tree->mcPID->at(mcI) == -11 ) EleM = 1;
		if( tree->mcPID->at(mcI) == 13 ) MuP = 1;
		if( tree->mcPID->at(mcI) == -13 ) MuM = 1;
		if( tree->mcPID->at(mcI) == 15) TauP = 1;
		if( tree->mcPID->at(mcI) == -15) TauM = 1;
	      }
	    }
	    int nEle = EleP + EleM;
	    int nMu = MuP + MuM;
	    int nTau = TauP + TauM;
	    int nLep = nEle + nMu + nTau;
	    
	    int ElePfid = 0;
	    int EleMfid = 0;
	    int MuPfid = 0;
	    int MuMfid = 0;
	    int nNufid = 0;
	    for( int mcI = 0; mcI < tree->nMC_; ++mcI){
	      if((abs(tree->mcMomPID->at(mcI))==24 && tree->mcParentage->at(mcI)==10) || (abs(tree->mcMomPID->at(mcI))==15 && tree->mcParentage->at(mcI)==26)){		  
		if( tree->mcPID->at(mcI) == 11 ) {
		  if (tree->mcPt->at(mcI) > 35 && (fabs(tree->mcEta->at(mcI)) < 2.5 && !(fabs(tree->mcEta->at(mcI)) > 1.4442 && fabs(tree->mcEta->at(mcI))<1.566))) ElePfid += 1;
		}
		if( tree->mcPID->at(mcI) == -11 ) {
		  if (tree->mcPt->at(mcI) > 35 && (fabs(tree->mcEta->at(mcI)) < 2.5 && !(fabs(tree->mcEta->at(mcI)) > 1.4442 && fabs(tree->mcEta->at(mcI))<1.566))) EleMfid += 1;
		}
		if( tree->mcPID->at(mcI) == 13 ) {
		  if (tree->mcPt->at(mcI) > 26 && fabs(tree->mcEta->at(mcI)) < 2.1) MuPfid += 1;
		}
		if( tree->mcPID->at(mcI) == -13 ) {
		  if (tree->mcPt->at(mcI) > 26 && fabs(tree->mcEta->at(mcI)) < 2.1) MuMfid += 1;
		}
	      }
	      if( fabs(tree->mcPID->at(mcI)) == 12 || fabs(tree->mcPID->at(mcI)) == 14 || fabs(tree->mcPID->at(mcI)) == 16 ) {
		if (tree->mcPt->at(mcI) > 20) nNufid += 1;
	      }
	    }
	    int nElefid = ElePfid + EleMfid;
	    int nMufid = MuPfid + MuMfid;
	    int nJetsfid = 0;
	    if ((nElefid + nMufid)==1 && nNufid == 1){
	      for ( int jetI = 0; jetI < tree->nJet_; jetI++){
		if (tree->jetGenPt_->at(jetI) >= 30) {
		  if ( fabs(tree->jetGenEta_->at(jetI)) < 2.4) nJetsfid += 1;
		}
	      }
	    }
	}

	if(passPreSel && !(tree->isData_)){
	  double minDR = 999.;
	  for(int mcInd=0; mcInd<tree->nMC_; ++mcInd){
	    if(tree->mcPID->at(mcInd) == 22 &&
	       (tree->mcParentage->at(mcInd)==2 || tree->mcParentage->at(mcInd)==10 || tree->mcParentage->at(mcInd)==26)){
	      double dr = secondMinDr(mcInd, tree);
	      if (dr < minDR) minDR = dr;
	    }
	  }
	}

}

void EventPick::print_cutflow(){
//	std::cout << "Cut-Flow for the event selector: " << title << std::endl;
	std::cout << "Input Events                 " << cutFlow->GetBinContent(cutFlow->FindBin(0.0))  << std::endl;
	std::cout << "Passing PV and triggers      " << cutFlow->GetBinContent(cutFlow->FindBin(1.0)) << std::endl;
	std::cout << "Events with at least 2 leptons  "<<cutFlow->GetBinContent(cutFlow->FindBin(2.0)) << std::endl;
	std::cout << "Events with at least 1 jet  "<< cutFlow->GetBinContent(cutFlow->FindBin(3.0)) <<std::endl;
	std::cout << "Events with at least 1 bjet  "<< cutFlow->GetBinContent(cutFlow->FindBin(4.0)) <<std::endl;
}

void EventPick::set_cutflow_labels(TH1F* hist){
	hist->GetXaxis()->SetBinLabel(1,"Input");
	hist->GetXaxis()->SetBinLabel(2,"Trigger");
	hist->GetXaxis()->SetBinLabel(3,"Loose Ele");
	hist->GetXaxis()->SetBinLabel(4,"Loose Mu");
	hist->GetXaxis()->SetBinLabel(5,"N jets");
	hist->GetXaxis()->SetBinLabel(6,"N b-tags");
}

void EventPick::clear_vectors(){
	Electrons.clear();
	Muons.clear();
	Jets.clear();
	bJets.clear();
}

double EventPick::dR_jet_ele(int jetInd, int eleInd){
	return dR(tree->jetEta_->at(jetInd), tree->jetPhi_->at(jetInd), tree->eleSCEta_->at(eleInd), tree->elePhi_->at(eleInd));
}
double EventPick::dR_jet_mu(int jetInd, int muInd){
	return dR(tree->jetEta_->at(jetInd), tree->jetPhi_->at(jetInd), tree->muEta_->at(muInd), tree->muPhi_->at(muInd));
}
