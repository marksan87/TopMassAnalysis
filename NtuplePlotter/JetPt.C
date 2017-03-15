#include <math.h>
#include "TFile.h"
#include "TTree.h"
{
  gROOT->Reset();

  TFile  myFile("sync.root"); // Open the file
  TTree* myTree = (TTree*) myFile.Get("EventTree"); // Get the Muon tree from the file
  int              nJet_; // Number of muons in an entry
  vector<float>*  jetPt_;        // An array of the pT values for each of the muons
  myTree->SetBranchAddress("nJet_", &nJet_);
  myTree->SetBranchAddress("jetPt_",&jetPt_);
  
  
  gROOT->cd(0); // This tells ROOT to create next object in memory and not in file
  TH1D h("Leading jet", "Jet P_{T} histogram",30,0, 200);
  gStyle->SetOptStat(111111); // Tells ROOT to list histogram overflow/underflow
  int nEntries = myTree->GetEntries(); // Get the number of entries in this tree
  for (int iEnt = 0; iEnt < nEntries; iEnt++) {
  	myTree->GetEntry(iEnt); // Gets the next entry (filling the linked variables)
  	cout<<"Entry #"<< iEnt << endl;
        h.Fill(jetPt_->at(0))
  	for (int iPar = 0; iPar < nJet; iPar++) {
      		//cout<<"    Jet_pt["<< iPar <<"] = " << jetPt_->at(iPar) << endl;
      		h.Fill(jetPt_->at(iPar) );
    		}
  }
h.Draw(); // Draw histogram
  
myFile.Close(); // Close file
}
