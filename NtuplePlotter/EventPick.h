#ifndef EVENTPICK_H
#define EVENTPICK_H

#include<vector>
#include<string>
#include<set>
#include<iostream>
#include<TH1F.h>
#include"EventTree.h"
#include"Selector.h"

class EventPick{
public:
	EventPick(std::string titleIn, bool liteMode);
	~EventPick();
	
	void process_event(const EventTree* inp_tree, const Selector* inp_selector, double weight=1.0);
	void print_cutflow();
	
	std::string title;
	bool isLiteMode;

	// selected object indices
	std::vector<int> Electrons;
	std::vector<int> Muons;
	std::vector<int> Jets;
	std::vector<int> bJets;
	
	// delta R cuts
	double veto_jet_dR;
	double veto_lep_jet_dR;
	
	// cuts as parameters, to modify easily
	double MET_cut;
	bool no_trigger;
	
	int Njet_ge;
	int NBjet_ge;
	int Jet_Pt_cut_1;
	int Jet_Pt_cut_2;
	int Jet_Pt_cut_3;	
	int Nele_eq;
	int Nmu_eq;
	int NEleVeto_le;
	int jet_pt_cut;

	//int NlooseMuVeto_le;
	//int NlooseEleVeto_le;
	//int NmediumEleVeto_le;
	
	// variables showing passing or failing selections
	bool passPreSel; // passed preselection
	bool passAll; // single flag: event passed all cuts: preselection + photon
	bool passFirstcut; // pass the sync cut	
	bool passVertexCut;
	bool passElectronCut;
	bool passMuonCut;
	bool passJetCut;
	bool passbJetCut;
	bool passTriggers;
	// histograms
	std::vector<TH1F*> histVector;
	TH1F* cutFlow;
	TH1F* cutFlowWeight;

private:
	const EventTree* tree;
	const Selector* selector;
	
	void clear_vectors();
	void set_cutflow_labels(TH1F* hist);
	double dR_jet_ele(int jetInd, int eleInd);
	double dR_jet_mu(int jetInd, int muInd);
};
#endif
