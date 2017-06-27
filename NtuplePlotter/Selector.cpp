#include"Selector.h"

const string roc_file = "Roc_muon_corrections/rcdata.2016.v3"; 

double dR(double eta1, double phi1, double eta2, double phi2){
	double dphi = phi2 - phi1;
	double deta = eta2 - eta1;
	static const double pi = TMath::Pi();
	dphi = TMath::Abs( TMath::Abs(dphi) - pi ) - pi;
	return TMath::Sqrt( dphi*dphi + deta*deta );
}

Selector::Selector(){
	rc = new RoccoR(roc_file);	// Rochester muon pt corrector
	rand = new TRandom3();
	// jets
	jet_pt_cut = 25;
	jet_eta_cut = 2.4;
	btag_cut = 0.8484;

	// Muons
	mu_pt_loose_cut = 10.0;
	mu_RelIsoLoose_cut = 0.25;
        mu_RelIso_range[0] = 0.0;
        mu_RelIso_range[1] = 0.15;
	mu_Iso_invert = false;
	mu_eta_loose_cut = 2.4;
	
	// Electron kinematic cuts
	ele_pt_loose_cut = 15.0;
	ele_eta_loose_cut = 2.4;
	
	ele_RelIso_range[0] = 0.0;
	ele_RelIso_range[1] = 0.1;

	// Electron isolation cut
	ele_RelIsoLoose_cut = 0.15;
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
		double SCeta = tree->eleSCEta_->at(eleInd);
		double pt = tree->elePt_->at(eleInd);
		double rho_zero = std::max(0.0, (double)tree->rho_);
		Ele03RelIso.push_back( 	
			(tree->elePFChIso_->at(eleInd) + 
			 std::max(0.0, tree->elePFNeuIso_->at(eleInd) + tree->elePFPhoIso_->at(eleInd) - rho_zero * eleEffArea03(SCeta))
			) / pt );
		
		if (tree->eleIDbit_->size() != tree->elePt_->size()){	
			std::cout << " vectors are of different length skip to next electron " << std::endl;
			continue;
		}
		
		
		bool looseSel = fabs(tree->eleEta_->at(eleInd)) < ele_eta_loose_cut &&
				pt > ele_pt_loose_cut && 
				tree->eleIDbit_->at(eleInd) >> 1 & 1 &&    // Loose cut ID
				!(fabs(SCeta) > 1.4442 && fabs(SCeta) < 1.5660); // Transition region veto

		if( looseSel ){
			Electrons.push_back(eleInd);
		}
	}
}


void Selector::filter_muons(){
	for(int muInd = 0; muInd < tree->nMu_; ++muInd){
		double eta = tree->muEta_->at(muInd);

		//  Apply rochestor correction
		if (tree->isData_) {
		    tree->muPt_->at(muInd) *= rc->kScaleDT(tree->muCharge_->at(muInd), tree->muPt_->at(muInd), tree->muEta_->at(muInd), tree->muPhi_->at(muInd)); 
		}
		else {
		    tree->muPt_->at(muInd) *= rc->kScaleAndSmearMC(tree->muCharge_->at(muInd), tree->muPt_->at(muInd), tree->muEta_->at(muInd), tree->muPhi_->at(muInd), tree->muTrkLayers_->at(muInd), rand->Rndm(), rand->Rndm());
		}

		double pt = tree->muPt_->at(muInd);
		double frelIsocorr = ( tree->muPFChIso_->at(muInd) + 
					fmax(0.0, tree->muPFNeuIso_->at(muInd) + 
						tree->muPFPhoIso_->at(muInd) -
						0.5*tree->muPFPUIso_->at(muInd)
					) 
				     ) / pt;
		

		bool passLoose = pt > mu_pt_loose_cut && abs(eta) < mu_eta_loose_cut && frelIsocorr < 0.25 && ( tree->muIDbit_->at(muInd) >> 1 & 1 ); 
		 
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
