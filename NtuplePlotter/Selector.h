#ifndef SELECTOR_H
#define SELECTOR_H

#include<vector>
#include<iostream>
#include<algorithm>
#include<TFile.h>
//#include<TH1F.h>
#include<TMath.h>
#include<TLorentzVector.h>
#include"EventTree.h"
#include"Roc_muon_corrections/RoccoR.h"
#include<string>
#include<TRandom3.h>

double dR(double eta1, double phi1, double eta2, double phi2);

class Selector{
public:
	Selector();
	~Selector();
	
	void process_objects(const EventTree* inp_tree);

	RoccoR* rc;  // Rochester muon pt corrector
	TRandom3* rand;
    

	// selected object indices
	std::vector<int> Electrons;
	std::vector<int> Muons;
	std::vector<int> Jets;
	std::vector<int> bJets;
	
	// calculated rho corrected PF isolations
	std::vector<double> Ele03RelIso;
	
	// jets
	double jet_pt_cut;
	double jet_eta_cut;
	double btag_cut;

	// electrons
	double ele_pt_cut;
	double ele_pt_loose_cut;
	double ele_eta;
	double ele_eta_loose_cut;
	double mu_eta_loose;
	double mu_eta_tight;
	double mu_pt_cut;
	double ele_ptmedium_cut;
	double ele_RelIso_range[2];
	double ele_RelIsoLoose_cut;
	double ele_MVA_range[2];
	double ele_cutbased_range[2];
	double ele_MVALoose_cut;
	double ele_Dxy_cut;
	int    ele_MissInnHit_cut;
	bool   ele_Iso_MVA_invert;
	
	// Cut-based Electron ID vars
	double ele_barrel_full5x5_sigmaIetaIeta_cut;
	double ele_barrel_dEtaIn_cut;
	double ele_barrel_dPhiIn_cut;
	double ele_barrel_HoverE_cut;
	double ele_barrel_relIso_cut;
	double ele_barrel_ooEmooP_cut;
	double ele_barrel_d0_cut;
	double ele_barrel_dz_cut;
	double ele_barrel_missingInnerHits_cut;

	double ele_endcap_full5x5_sigmaIetaIeta_cut;
	double ele_endcap_dEtaIn_cut;
	double ele_endcap_dPhiIn_cut;
	double ele_endcap_HoverE_cut;
	double ele_endcap_relIso_cut;
	double ele_endcap_ooEmooP_cut;
	double ele_endcap_d0_cut;
	double ele_endcap_dz_cut;
	double ele_endcap_missingInnerHits_cut;

	// muons
	double mu_pt_loose_cut;
	double mu_eta_loose_cut;
	double mu_RelIsoLoose_cut;
	double mu_RelIso_range[2];
 	double mu_MVA_range[2];
	bool   mu_Iso_invert;

private:
	const EventTree* tree;
	void clear_vectors();
	void filter_electrons();
	void filter_muons();
	void filter_jets();
	
	bool fidEtaPass(double Eta);
	
	// Electron effective area
	double eleEffArea03(double SCEta);
};

#endif
