#include"Selector.h"

double dR(double eta1, double phi1, double eta2, double phi2){
	double dphi = phi2 - phi1;
	double deta = eta2 - eta1;
	static const double pi = TMath::Pi();
	dphi = TMath::Abs( TMath::Abs(dphi) - pi ) - pi;
	return TMath::Sqrt( dphi*dphi + deta*deta );
}

Selector::Selector(){
	// jets
	jet_pt_cut = 30;
	jet_eta_cut = 2.4;
	btag_cut = 0.89;

	// Muons
	mu_pt_loose_cut = 10.0;
	mu_RelIsoLoose_cut = 0.25;
        mu_RelIso_range[0] = 0.0;
        mu_RelIso_range[1] = 0.15;
	mu_Iso_invert = false;
	mu_eta_loose_cut = 2.4;
	//mu_Pt_cut = 26;
	
	// Electron kinematic cuts
	ele_pt_cut = 30.0;
	ele_eta = 2.4;
	ele_pt_loose_cut = 15.0;
	ele_eta_loose_cut = 2.4;
	
	ele_ptmedium_cut = 20.0;
	ele_RelIso_range[0] = 0.0;
	ele_RelIso_range[1] = 0.1;

	// Electron isolation cut
	ele_RelIsoLoose_cut = 0.15;

	///////////////////////////////////////////////////////////////////////////////////////////////////////////
	// Cut-based Electron ID Loose Working Point
	// https://twiki.cern.ch/twiki/bin/viewauth/CMS/CutBasedElectronIdentificationRun2#Working_points_for_2016_data_for
	// barrel: |eta supercluster| <= 1.479
	ele_barrel_full5x5_sigmaIetaIeta_cut = 0.011;
	ele_barrel_dEtaIn_cut = 0.00477;
	ele_barrel_dPhiIn_cut = 0.222;
	ele_barrel_HoverE_cut = 0.298;
	ele_barrel_relIso_cut = 0.0994;
	ele_barrel_ooEmooP_cut = 0.241;
	ele_barrel_d0_cut = 0.05;
	ele_barrel_dz_cut = 0.10;
	ele_barrel_missingInnerHits_cut = 1;

	// endcap: 1.479 < |eta supercluster| < 2.5	
	ele_endcap_full5x5_sigmaIetaIeta_cut = 0.0314;
	ele_endcap_dEtaIn_cut = 0.00868;
	ele_endcap_dPhiIn_cut = 0.213;
	ele_endcap_HoverE_cut = 0.101;
	ele_endcap_relIso_cut = 0.107;
	ele_endcap_ooEmooP_cut = 0.14;
	ele_endcap_d0_cut = 0.10;
	ele_endcap_dz_cut = 0.20;
	ele_endcap_missingInnerHits_cut = 1;
	///////////////////////////////////////////////////////////////////////////////////////////////////////////
}

void Selector::process_objects(const EventTree* inp_tree){
	tree = inp_tree;
	clear_vectors();
        
	filter_muons();
 	filter_electrons();
	filter_jets();
}

void Selector::clear_vectors() {	
	Electrons.clear();
	Muons.clear();
	Jets.clear();
	bJets.clear();
	Ele03RelIso.clear();
}

void Selector::filter_electrons() {
	for(int eleInd = 0; eleInd < tree->nEle_; ++eleInd){
		//std::cout << "start to iterate over electron number " << eleInd << " out of " << tree->nEle_ << std::endl; 
		double eta = tree->eleSCEta_->at(eleInd);
		double pt = tree->elePt_->at(eleInd);
		double rho_zero = std::max(0.0, (double)tree->rho_);
		Ele03RelIso.push_back( 	
			(tree->elePFChIso_->at(eleInd) + 
			 std::max(0.0, tree->elePFNeuIso_->at(eleInd) + tree->elePFPhoIso_->at(eleInd) - rho_zero * eleEffArea03(eta))
			) / pt );
		
		if (tree->eleIDbit_->size() != tree->elePt_->size()){	
			std::cout << " vectors are of different length skip to next electron " << std::endl;
			continue;
		}
		
		
		bool looseSel = fabs(eta) < ele_eta_loose_cut &&
				pt > ele_pt_loose_cut;
		
		if (abs(eta) <= 1.479)  {   // Barrel
			looseSel &= tree->eleSigmaIEtaIEtaFull5x5_->at(eleInd) < ele_barrel_full5x5_sigmaIetaIeta_cut &&
				    abs(tree->eledEtaAtVtx_->at(eleInd)) < ele_barrel_dEtaIn_cut &&
				    abs(tree->eledPhiAtVtx_->at(eleInd)) < ele_barrel_dPhiIn_cut &&
				    tree->eleHoverE_->at(eleInd) < ele_barrel_HoverE_cut &&
				    Ele03RelIso[eleInd] < ele_barrel_relIso_cut &&
				    tree->eleEoverPInv_->at(eleInd) < ele_barrel_ooEmooP_cut &&
				    abs(tree->eleD0_->at(eleInd)) < ele_barrel_d0_cut &&
				    abs(tree->eleDz_->at(eleInd)) < ele_barrel_dz_cut &&
				    tree->eleMissHits_->at(eleInd) <= ele_barrel_missingInnerHits_cut &&
				    tree->eleConvVeto_->at(eleInd);
		}
		else if (abs(eta) > 1.479 && abs(eta) < 2.5) {  // Endcap	
			looseSel &= tree->eleSigmaIEtaIEtaFull5x5_->at(eleInd) < ele_endcap_full5x5_sigmaIetaIeta_cut &&
				    abs(tree->eledEtaAtVtx_->at(eleInd)) < ele_endcap_dEtaIn_cut &&
				    abs(tree->eledPhiAtVtx_->at(eleInd)) < ele_endcap_dPhiIn_cut &&
				    tree->eleHoverE_->at(eleInd) < ele_endcap_HoverE_cut &&
				    Ele03RelIso[eleInd] < ele_endcap_relIso_cut &&
				    tree->eleEoverPInv_->at(eleInd) < ele_endcap_ooEmooP_cut &&
				    abs(tree->eleD0_->at(eleInd)) < ele_endcap_d0_cut &&
				    abs(tree->eleDz_->at(eleInd)) < ele_endcap_dz_cut &&
				    tree->eleMissHits_->at(eleInd) <= ele_endcap_missingInnerHits_cut &&
				    tree->eleConvVeto_->at(eleInd);
		}


		if( looseSel ){
			Electrons.push_back(eleInd);
		}
	}
}


void Selector::filter_muons(){
	for(int muInd = 0; muInd < tree->nMu_; ++muInd){
		const unsigned int GlobalMuon     =  1<<1;
		const unsigned int TrackerMuon    =  1<<2;
		const unsigned int PFMuon =  1<<5;
		const unsigned int TightMuon = 1 ;
		bool isGlobalMuon  = tree->muType_->at(muInd) & GlobalMuon;
		bool isTrackerMuon = tree->muType_->at(muInd) & TrackerMuon;
		bool isPFMuon      = tree->muType_->at(muInd) & PFMuon;
		double eta = tree->muEta_->at(muInd);
		double pt = tree->muPt_->at(muInd);
		double frelIsocorr = ( tree->muPFChIso_->at(muInd) + 
					fmax(0.0, tree->muPFNeuIso_->at(muInd) + 
						tree->muPFPhoIso_->at(muInd) -
						0.5*tree->muPFPUIso_->at(muInd)
					) 
				     ) / pt;
		
		double rho_zero = std::max(0.0, (double)tree->rho_);

		bool IsoPass = frelIsocorr >= mu_RelIso_range[0] && frelIsocorr <= mu_RelIso_range[1];		

		if (mu_Iso_invert) IsoPass = !IsoPass;

		bool passLoose = pt > mu_pt_loose_cut && abs(eta) < mu_eta_loose_cut && frelIsocorr < 0.25 && ( tree->muIDbit_->at(muInd) >> 1 & 1 ); 
//		bool passLoose = pt > mu_pt_loose_cut && abs(eta) < mu_eta_loose_cut && frelIsocorr < 0.25 && isPFMuon && ( isGlobalMuon || isTrackerMuon );
		 if (passLoose) {
		 	Muons.push_back(muInd);
		 }

	}
}



// jet ID is not likely to be altered, so it is hardcoded
void Selector::filter_jets(){
	for(int jetInd = 0; jetInd < tree->nJet_; ++jetInd){
		bool jetID_pass = false;
		
		if ( tree->jetPt_->size() == tree->jetPFLooseID_->size() ) {
			 jetID_pass = ( tree->jetPFLooseID_->at(jetInd) == 1) ; 
		}

		bool jetPresel = TMath::Abs(tree->jetEta_->at(jetInd)) < jet_eta_cut &&
						 tree->jetPt_->at(jetInd) >= jet_pt_cut &&
						 jetID_pass ;
		
		if( jetPresel) {
			Jets.push_back(jetInd);
			if(tree->jetCSV2BJetTags_->at(jetInd) > btag_cut) bJets.push_back(jetInd);
		}
	}
}

bool Selector::fidEtaPass(double Eta){
	double fabsEta = TMath::Abs(Eta);
	if( fabsEta > 2.5) return false;
	if( 1.4442 < fabsEta && fabsEta < 1.566) return false;
	return true;
}

// kEleGammaAndNeutralHadronIso03
// Summer16 80X effective areas
// https://github.com/ikrav/cmssw/blob/egm_id_80X_v1/RecoEgamma/ElectronIdentification/data/Summer16/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_80X.txt
double Selector::eleEffArea03(double SCEta){
	double eta = TMath::Abs(SCEta);
	static const double area[7] = {0.1703, 0.1715, 0.1213, 0.1230, 0.1635, 0.1937, 0.2393};
	int region = 0;
	if( eta >= 1.0 )   region++;
	if( eta >= 1.479 ) region++;
	if( eta >= 2.0 )   region++;
	if( eta >= 2.2 )   region++;
	if( eta >= 2.3 )   region++;
	if( eta >= 2.4 )   region++;
	return area[region];
}

Selector::~Selector(){
}
