#include<iostream>
#include<string>
#include"JECvariation.h"
#include<TFile.h>
#include<TTree.h>
#include<TDirectory.h>
#include<TObject.h>
#include"EventTree.h"
#include"Selector.h"
#include"EventPick.h"
using std::cout;
using std::endl;
using std::flush;
using std::string;

const string XRD_FERMI("root://cmsxrootd.fnal.gov/");
const string XRD_GLOBAL("root://cms-xrd-global.cern.ch/");
const string XRD_CERN("root://cms-xrd-global.cern.ch/");
//const string NTUPLE_PATH("root://eoscms.cern.ch//store/group/phys_smp/ggNtuples/13TeV/Data/V08_00_11_01");

const bool LIKELY_FLAG = false;  // true for likely mode (only keep eu events) or false for full mode (keep all events with >= 2 leptons)
const bool DEBUG = false;
const bool DEBUG_PRINT = false;
const Long64_t DEBUG_ITER = 10000 ;

int main(int ac, char** av){
	if(ac < 3){
		cout << "usage: ./makeSkim outputFileName inputFile[s]" << endl;
		return -1;
	}
	// input: dealing with TTree first
	//bool isMC = false;
	EventTree* tree = new EventTree(ac-2, av+2);
	char **inputs = av+2;
	cout<<inputs[0]<<" successfully loaded!"<<endl;
	Selector* selector = new Selector();
	selector->jet_pt_cut = 30;
	EventPick* evtPick = new EventPick("nominal", LIKELY_FLAG);
        evtPick->MET_cut = -1.0;
	bool isMC = !(tree->isData_);
	
	// DEPRICATED
	/*
	JECvariation *JEC = NULL;	
	if (isMC) {
		JEC = new JECvariation("./Spring16_25nsV6_MC/Spring16_25nsV6", isMC);
		cout <<"JECvariation created successfully!"<<endl;
	}
	else {
		//JEC = new JECvariation("./Summer15_25nsV6_DATA/Summer15_25nsV6", isMC);

	}
	*/

	//string outDirName(av[1]);
	//outDirName = PATH + outDirName;

	evtPick->NBjet_ge = 1;
	

	int totalPassedPreSel = 0;
	//evtPick->no_trigger = true;
		
	
	TFile* outFile = TFile::Open( av[1], "RECREATE" );
	
	TDirectory* ggDir = outFile->mkdir("ggNtuplizer","ggNtuplizer");
	ggDir->cd();
	TTree* newTree = tree->chain->CloneTree(0);

	Long64_t nEntr = tree->GetEntries();
	if (DEBUG && (DEBUG_ITER < nEntr)) { nEntr = DEBUG_ITER; }
	//cout<<tree->GetEntries()<<" total entries\n"<<endl<<flush;
	cout<<endl<<flush;
	for(Long64_t entry= 0; entry < nEntr; entry++){
		
		if(((int)entry % 1000) == 0) {
			float pct = 100.0f * (float)entry / (float)nEntr;  
			cout << "\rprocessing entry " << entry << " out of " << nEntr << "  [" ;
			
		//	if (pct <= 50) {
		//		int p = (int)((float)pct / 2.5f);
		//		if (p > 0)  { cout << string(p, '-'); }
		//		if (p < 20) { cout << string(20-p, ' '); }
		//	}
		//	else {
		//		int p = (int)((float)(pct-50) / 2.5f);	
		//		if (p > 0)  { cout << string(p, '='); }
		//		if (p < 20) { cout << string(20-p, '-'); }
		//		//cout << string(((pct-50) % 5), '=') << string(10-((pct-50) % 5), '-');
		//	}
		
			float x = pct / 5.0f;
			cout << string((int)x, '=');
			if (pct - (int)x * 5.0f >= 2.5f) { cout << '-' << string(19-(int)x, ' '); }
			else { cout << string(20-(int)x, ' '); }
			cout << "]  " << (int)pct << "\% complete" << flush;
		}
		tree->GetEntry(entry);
		selector->process_objects(tree);
	
		///////////////////////////////////////////////////
		// Depricated: Jet Energy Corrections performed  //
		//	       at Ntuplization level		 //
		// if (isMC)					 //
		//    JEC->applyJEC(tree,1);			 //
		///////////////////////////////////////////////////

		evtPick->process_event(tree,selector);
		
		// make selection here
		if (DEBUG_PRINT) cout<<"evtPick processed event "<<entry<<endl;
		if( evtPick->passPreSel ) {
			totalPassedPreSel++;
			if (DEBUG_PRINT) cout<<"Pre-selection passed"<<endl;
			newTree->Fill();
		}
		else if (DEBUG_PRINT) cout<<"Pre-selection failed"<<endl;
		
	        //cout << "finished with entry " <<  entry << endl;	
	}
	cout << "\rprocessing entry " << nEntr << " out of " << nEntr << "  [====================]  100\% complete" << endl << endl;
	
	newTree->Write();
	evtPick->print_cutflow();	
	cout<<"Total events that passed pre-selection: "<<totalPassedPreSel<<"/"<<nEntr<<endl<<endl;
	std::map<std::string, TH1F*> histMap;

	// copy histograms
	for(int fileInd = 2; fileInd < ac; ++fileInd){
		TFile* tempFile = TFile::Open(av[fileInd], "READ");
		TIter next(((TDirectory*)tempFile->Get("ggNtuplizer"))->GetListOfKeys());
		TObject* obj;
		while ((obj = next())){
			std::string objName(obj->GetName());
			if( objName != "EventTree"){
				TH1F* hist = (TH1F*)tempFile->Get(("ggNtuplizer/"+objName).c_str());

				if( histMap.find(objName) != histMap.end() ){
					histMap[objName]->Add(hist);
				}
				else {
					hist->SetDirectory(0);
					histMap[objName] = hist;
				}
			}
		}
		tempFile->Close();
	}
	cout<<"Exiting copy histograms"<<endl;	
	ggDir->cd();
	for(std::map<std::string, TH1F*>::iterator it = histMap.begin(); it!= histMap.end(); ++it){
		it->second->SetDirectory(ggDir);
		it->second->Write();
	}
	
	outFile->Close(); 
	return 0;
}
