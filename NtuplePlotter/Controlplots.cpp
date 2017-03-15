#include<iostream>
#include<string>
#include<TChain>
#include<TFile.h>
#include<TTree.h>
#include<TDirectory.h>
#include<TObject.h>
#include<TH1F.h>
#include<TCanvas.h>
#ifndef Control_plots

void Control_plots() {
			//read the Tree
			TChain *mychain = new TChain("ggNtuplizer/EventTree");

			
