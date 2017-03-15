#include"PUReweight.h"
#include<iostream>
#include<TCanvas.h> 
/*#include <TH1D.h>

PUReweight::PUReweight(TH1D* wgtHist) {
	if (wgtHist == NULL) { return; }
	PUweightHist = (TH1D*)wgtHist->Clone();
	PUweightHist->SetDirectory(0);
}


TH1D* PUReweight::getPUweightHist() {
	return PUweightHist;
}
*/
PUReweight::PUReweight(int nFiles, char** fileNames, std::string PUfilename){
	PUweightSum = 0.0;
	events = 0;
	TFile* pileupFile = new TFile(PUfilename.c_str(),"READ");
	PUweightHist = (TH1D*)pileupFile->Get("pileup");
	PUweightHist->SetDirectory(0);
	pileupFile->Close();
	TH1D* PUbackup;
	if(PUweightHist->GetNbinsX() != 1000){
		std::cout << "Wrong number of bins in the pileup histogram" << std::endl;
		PUbackup = new TH1D("pileup_new","pileup_new",1000,0,200);
		for(int ibin=1; ibin <= PUweightHist->GetNbinsX(); ibin++){
			PUbackup->SetBinContent(ibin, PUweightHist->GetBinContent(ibin));
			// assuming the same scale
		}
		PUweightHist = (TH1D*)PUbackup->Clone();
	}
	double PUweightInt = PUweightHist->Integral();
	TH1F* mcPU = NULL;
	for(int nmcfile = 0; nmcfile<nFiles; nmcfile++){
		std::cout << "reading file " << std::string(fileNames[nmcfile]) << std::endl;
		TFile* mcFile = TFile::Open(fileNames[nmcfile],"READ");
		if(!(mcFile->Get("ggNtuplizer/hPUTrue"))) {
			std::cout << "no hPU histogram here!" << std::endl;
			delete PUweightHist;
			PUweightHist = NULL;
			return;
		}
		if( mcPU==NULL) mcPU = (TH1F*)mcFile->Get("ggNtuplizer/hPUTrue");
		else mcPU->Add((TH1F*)mcFile->Get("ggNtuplizer/hPUTrue"));
		mcPU->SetDirectory(0);
		mcFile->Close();
	}
	//TCanvas *c1 = new TCanvas("c1","A Simple Graph Example",1000,500);
        //c1->SetFillColor(0);
        //c1->SetGrid();
        
	TH1D* mcPUbackup;
	if(mcPU->GetNbinsX() != 100){
/*		std::cout << "Wrong number of bins in the mc pileup histogram" << std::endl;
		mcPUbackup = new TH1D("mc_pileup_new","mc_pileup_new",100,0,100);
		for(int ibin=1; ibin <= mcPU->GetNbinsX(); ibin++){
			mcPUbackup->SetBinContent(ibin, mcPU->GetBinContent(ibin));
			// assuming the same scale
		}
		mcPU = (TH1F*)mcPUbackup->Clone();
*/
	}
	mcPU->Scale(1.0/mcPU->Integral());
	PUweightHist->Divide(mcPU);
	PUweightHist->Scale(1.0/PUweightInt);
	//PUweightHist->Scale(1.0/PUweightHist->Integral());
	//PUweightHist->Draw();
//	c1->SaveAs("PUReweight.png");	
	delete mcPU;
}

PUReweight::~PUReweight(){
	delete PUweightHist;
}

double PUReweight::getWeight(int nPUInfo, std::vector<int> *puBX, std::vector<float> *puTrue){
	double PUweight=0.0;
	if(!PUweightHist) {
	  std::cout << "you are calling getWeight by mistake" << std::endl; 
	  return 1.0;
	}
	
	for(int puInd=0; puInd<nPUInfo; ++puInd){
		if( puBX->at(puInd) == 0 ){
			PUweight = PUweightHist->GetBinContent(PUweightHist->GetXaxis()->FindBin(puTrue->at(puInd)));
			break;
		}
	}
	events++;
	PUweightSum+=PUweight;
	return PUweight;
}

double PUReweight::getAvgWeight(){
	if(events!=0) return PUweightSum/events;
	else return -1.0;
}
