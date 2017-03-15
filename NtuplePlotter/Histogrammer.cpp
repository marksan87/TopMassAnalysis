#include"Histogrammer.h"

double secondMinDr(int myInd, const EventTree* tree);

Histogrammer::Histogrammer(std::string titleIn){
	title = titleIn;
	
	// 2d histograms
/*	make_hist2d("photon1_Sigma_ChIso","photon1 SigmaIetaIeta vs ChIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_Sigma_ChSCRIso","photon1 SigmaIetaIeta vs ChSCRIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_Sigma_PhoIso","photon1 SigmaIetaIeta vs PhoIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_Sigma_PhoSCRIso","photon1 SigmaIetaIeta vs PhoSCRIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_25_35_Sigma_ChSCRIso","photon1 Et 25 to 35 SigmaIetaIeta vs ChSCRIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_35_45_Sigma_ChSCRIso","photon1 Et 35 to 45 SigmaIetaIeta vs ChSCRIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_45_60_Sigma_ChSCRIso","photon1 Et 45 to 60 SigmaIetaIeta vs ChSCRIso",160,0,0.04,300,-10,20);
	make_hist2d("photon1_60_up_Sigma_ChSCRIso","photon1 Et 60 up SigmaIetaIeta vs ChSCRIso",160,0,0.04,300,-10,20);

	make_hist2d("MTW_M3","W trans mass v.s. M3",60,0,300,60,0,600);
	make_hist2d("photon1_Sigma_Et","photon1 SigmaIetaIeta vs Et",160,0,0.04,40,0,200);
	make_hist2d("photon1_ChSCRIso_Et","photon1 ChSCRIso_Et vs Et", 300,-10,20,40,0,200);
	hists2d["photon1_ChSCRIso_Et"]->GetXaxis()->SetTitle("ChSCRIso");
	hists2d["photon1_ChSCRIso_Et"]->GetYaxis()->SetTitle("Photon p_{T} (GeV)");

	hists2d["photon1_Sigma_Et"]->GetXaxis()->SetTitle("Sigmaietaieta");
	hists2d["photon1_Sigma_Et"]->GetYaxis()->SetTitle("Photon p_{T} (GeV)");
*/
	// creating histograms
	// muons
	make_hist("mu1Pt","muon 1 Pt",20,0,300,"Muon p_{T} (GeV)","Events / 15 GeV");
	make_hist("mu1Eta","muon 1 Eta",12,0,3,"Muon #eta","Events / 0.25");
	make_hist("mu1RelIso","muon 1 relative isolation",120,0,1.2,"Muon RelIso","Events / 0.01");
	make_hist("mu2Pt","muon 2 Pt",30,0,300,"p_{T} (GeV)","Events / 10 GeV");
        make_hist("mu2RelIso","muon 2 relative isolation",10,0,0.5,"RelIso","Events / 0.05");

	
	// electrons
	make_hist("ele1Pt","electron 1 Pt",30,0,300,"Electron p_{T} (GeV)","Events / 10 GeV");
	make_hist("ele1Eta","electron 1 Eta",26,-2.6,2.6,"Electron #eta","Events / 0.2");
	make_hist("ele1RelIso","electron 1 relative isolation",120,0,1.2,"Electron RelIso","Events / 0.01");
	//make_hist("ele1RelIso","electron 1 relative isolation",12,0,0.12,"Electron RelIso","Events / 0.01");
	make_hist("ele1MVA","electron 1 MVA",220,-1.1,1.1,"Electron MVA Trig","Events / 0.01");
	//make_hist("ele1MVA","electron 1 MVA",80,0.5,1.3,"Electron MVA Trig","Events / 0.01");
	make_hist("ele1D0","electron 1 Dxy_PV",80,-0.2,0.2,"Electron Dxy_PV (cm)","Events / 0.005 cm");
	make_hist("ele1Dz","electron 1 Dz",75,-0.15,0.15,"Electron D_{Z} (cm)","Events / 0.004 cm");
	make_hist("ele1EoverP","electron 1 EoverP",25,0,5,"Electron E/P","Events / 0.2");
	make_hist("ele1sigmaIetaIeta","electron 1 sigmaIetaIeta",80,0,0.04,"Electron #sigma_{i#etai#eta}","Events / 0.0005");
	make_hist("ele1MissHits","electron 1 missing hits",10,-0.5,9.5,"Electron missing hits","Events");
	make_hist("ele1DrJet","dR electron 1 to closest jet",60,0,6,"Electron #DeltaR(e,jet)","Events / 0.1");
	make_hist("ele1MotherID","electron 1 mother PDG ID",35,-0.5,34.5,"Electron mother PID","Events");
	make_hist("ele1GMotherID","electron 1 Gmother PDG ID",35,-0.5,34.5,"Electron Gmother PID","Events");
		
	make_hist("ele2Pt","electron 2 Pt",30,0,300,"p_{T} (GeV)","Events / 10 GeV");
	make_hist("ele2RelIso","electron 2 relative isolation",10,0,0.5,"RelIso","Events / 0.05");
	
	// photons
/*	make_hist("photon1Et","photon 1 Et",20,0,200,"Photon E_{T} (GeV)","Events / 10 GeV");
	make_hist("photon1Eta","photon 1 Eta",26,-2.6,2.6,"Photon #eta","Events / 0.2");
	make_hist("photon1IsConv","photon 1 IsConv",2,-0.5,1.5,"","");
	make_hist("photon1HoverE","photon 1 HoverE",100,0,0.1,"Photon H/E","Events / 0.001");
	make_hist("photon1SigmaIEtaIEta","photon 1 sigmaIetaIeta",80,0,0.04,"Photon #sigma_{i#etai#eta}","Events / 0.0005");
	make_hist("photon1ChHadIso","photon 1 Charged Had Isolation",60,-2.0,10,"Photon ChHadIso","Events / 0.2 GeV");
	make_hist("photon1ChHadSCRIso","photon 1 Charged Had SCR Isolation",60,-2.0,10,"Photon ChHadSCRIso","Events / 0.2 GeV");
	make_hist("photon1ChHadRandIso","photon 1 Charged Had Rand Isolation",110,-2.0,20,"Photon ChHadRandIso","Events / 0.2 GeV");

	make_hist("photon1_25_35_ChHadRandIso","photon 1 Et 25 to 35 Charged Had Rand Isolation",110,-2.0,20,"Photon ChHadRandIso","Events / 0.2 GeV");
	make_hist("photon1_35_45_ChHadRandIso","photon 1 Et 35 to 45 Charged Had Rand Isolation",110,-2.0,20,"Photon ChHadRandIso","Events / 0.2 GeV");
	make_hist("photon1_45_60_ChHadRandIso","photon 1 Et 45 to 60 Charged Had Rand Isolation",110,-2.0,20,"Photon ChHadRandIso","Events / 0.2 GeV");
	make_hist("photon1_60_up_ChHadRandIso","photon 1 Et 60 up Charged Had Rand Isolation",110,-2.0,20,"Photon ChHadRandIso","Events / 0.2 GeV");

	make_hist("photon1NeuHadIso","photon 1 Neutral Had Isolation",75,-5,10,"Photon NeuHadIso","Events / 0.2 GeV");
	make_hist("photon1PhoIso","photon 1 Photon Isolation",75,-5,10,"Photon PhoIso","Events / 0.2 GeV");
	make_hist("photon1PhoSCRIso","photon 1 Photon SCR Isolation",75,-5,10,"Photon PhoSCRIso","Events / 0.2 GeV");
	make_hist("photon1PhoRandIso","photon 1 Photon Rand Isolation",125,-5,20,"Photon PhoRandIso","Events / 0.2 GeV");
	make_hist("photon1DrElectron","dR photon 1 to closest electron",60,0,6,"#DeltaR(#gamma,e)","Events / 0.1");
	make_hist("photon1DrJet","dR photon 1 to closest jet",60,0,6,"#DeltaR(#gamma,jet)","Events / 0.1");
	make_hist("photon1MotherID","photon 1 mother PDG ID",35,-0.5,34.5,"Photon mother PID","Events");
	make_hist("photon1GMotherID","photon 1 Gmother PDG ID",35,-0.5,34.5,"Photon Gmother PID","Events");
	make_hist("photon1DrMCbquark","dR photon 1 to gen level b",40,0,2,"#DeltaR(#gamma,b_{MC})","Events / 0.05");
	make_hist("GenPhotonEt","Et of matched Gen Photon",20,0,200,"Gen Photon E_{T} (GeV)","Events / 10 GeV");
	make_hist("GenPhotonMinDR","MinDR of matched Gen Photon",100,0,1,"Gen Photon Min #DeltaR","Events");
	make_hist("nPhotons","number of photons",15,-0.5,14.5,"N_{#gamma}","Events");
*/
	// jets
	make_hist("jet1Pt","jet 1 pt",50,0,500,"p_{T} (GeV)","Events / 10 GeV");
	make_hist("jet1Eta","jet 1 Eta",26,-2.6,2.6,"#eta","Events / 0.2");
	make_hist("jet2Pt","jet 2 pt",30,0,300,"p_{T} (GeV)","Events / 10 GeV");
	make_hist("jet2Eta","jet 2 Eta",26,-2.6,2.6,"#eta","Events / 0.2");
	make_hist("jet3Pt","jet 3 pt",30,0,300,"p_{T} (GeV)","Events / 10 GeV");
	make_hist("jet3Eta","jet 3 Eta",26,-2.6,2.6,"#eta","Events / 0.2");
	make_hist("jet4Pt","jet 4 pt",15,0,150,"p_{T} (GeV)","Events / 10 GeV");
	make_hist("jet4Eta","jet 4 Eta",26,-2.6,2.6,"#eta","Events / 0.2");
	
	// event
/*	make_hist("looseEleDrGenPho","dR loose electron to Gen Photon",60,0,6,"#DeltaR(e_{loose},#gamma_{MC})","Events / 0.1");
	make_hist("WtransMass","W transverse mass",20,0,200,"M(W_{T})(GeV)","Events / 10 GeV");
	make_hist("ele1pho1Mass","electron + photon mass",20,0,200,"M(e,#gamma)(GeV)","Events / 10 GeV");
	make_hist("ele1ele2Mass","Di-electron mass",40,0,200,"M(e,e)(GeV)","Events / 5 GeV");
	make_hist("mu1mu2Mass","Di-muon mass",40,0,200,"M(mu,mu)(GeV)","Events / 5 GeV");
	make_hist("Ht","Ht",30,0,1500,"H_{T} (GeV)","Events / 50 GeV");
	make_hist("MET","Missing Transverse Momentum",10,0,200,"MET (GeV)","Events / 10 GeV");
	make_hist("MET_low","Missing Transverse Momentum",20,0,20,"MET (GeV)","Events / 10 GeV");
*/	make_hist("nVtx","Number of Primary Vertices",50,0.5,50.5,"N_{PV}","Events");
	make_hist("nJets","number of jets",15,-0.5,14.5,"N_{jets}","Events");
	make_hist("PUweight","Event weight",30,0,3,"EventWeight","Events / 10");
	
/*	make_hist("M3first","Mass of 3 highest Pt jets",100,0,1000,"highest pt M3 (GeV)","Events / 10 GeV");
	make_hist("minM3","Minimal Mass of 3 jets",60,0,600,"min M3 (GeV)","Events / 10 GeV");
	make_hist("M3minPt","Mass of 3 jets with smallest total Pt",60,0,600,"M3 min Pt (Gev)","Events / 10 GeV");
	make_hist("M3","Mass of 3 jets with highest total Pt",80,0,800,"M3 (GeV)","Events / 10 GeV");
	make_hist("M3pho","Mass of 3 jets + photon with highest total Pt",40,0,400,"M(3jets+#gamma) (Gev)","Events / 10 GeV");
	make_hist("M3phoMulti","Mass of all combinations 3 jets + photon",40,0,400,"M(all 3jets+#gamma) (Gev)","Events / 10 GeV");
	make_hist("ele1D0","electron 1 Dxy_PV",80,-0.2,0.2,"Electron Dxy_PV (cm)","Events / 0.005 cm");
	make_hist("dRpho3j","dR photon to 3 jets",65,0.0,6.5,"#DeltaR(#gamma,3jets)","Events / 0.1");
*/
	make_hist("M3_0_30","Mass of 3 jets with highest total Pt",100,0,1000,"M3 (GeV)","Events / 10 GeV");
	make_hist("M3_30_100","Mass of 3 jets with highest total Pt",100,0,1000,"M3 (GeV)","Events / 10 GeV");
	make_hist("M3_100_200","Mass of 3 jets with highest total Pt",100,0,1000,"M3 (GeV)","Events / 10 GeV");
	make_hist("M3_200_300","Mass of 3 jets with highest total Pt",100,0,1000,"M3 (GeV)","Events / 10 GeV");
	make_hist("M3_300_up","Mass of 3 jets with highest total Pt",100,0,1000,"M3 (GeV)","Events / 10 GeV");
	
	make_hist("MCcategory","MC category",11,0.5,11.5,"category","Events");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(1,"Total");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(2,"AllHad");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(3,"1 lepton");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(4,"2 leptons");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(5,"");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(6,"1 e");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(7,"2 e");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(8,"1 #mu");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(9,"2 #mu");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(10,"1 #tau");
	hists["MCcategory"]->GetXaxis()->SetBinLabel(11,"2 #tau");

	make_hist("MCcategoryfid","MC category fiducial region",19,0.5,19.5,"category","Events");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(1,"Total");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(2,"AllHad");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(3,"1 lepton");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(4,"2 leptons");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(5,"");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(6,"1 e");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(7,"2 e");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(8,"1 #mu");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(9,"2 #mu");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(10,"1 e 1 #mu");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(11,"1 e, 3 jets");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(12,"1 e, 3 jets 1 b");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(13,"1 e, 3 jets 1 b, MET");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(14,"1 e, 3 jets 1 b, MET, 1 pho");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(16,"1 #mu, 3 jets");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(17,"1 #mu, 3 jets 1 b");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(18,"1 #mu, 3 jets 1 b, MET");
	hists["MCcategoryfid"]->GetXaxis()->SetBinLabel(19,"1 #mu, 3 jets 1 b, MET, 1 pho");
	

}

void Histogrammer::fill(Selector* selector, EventPick* selEvent, EventTree* tree, double weight){
	// sanity check: PU weight
	hists["PUweight"]->Fill(weight);
	// 2d photon candidate histograms
	//std::cout << "here0" << std::endl;
/*	if(selEvent->PhotonsPresel.size()>0){
		int candArrInd = -1;
		int candInd = -1;
		for(int phoItmp = 0; phoItmp < selEvent->PhotonsPresel.size(); phoItmp++){
			if((int)selEvent->PhoPassChHadIso[phoItmp] + 
			   (int)selEvent->PhoPassPhoIso[phoItmp]+
			   (int)selEvent->PhoPassSih[phoItmp] >= 1){
				// at least 1 cut passed.
				candArrInd = selEvent->PhotonsPresel[phoItmp];
				candInd = phoItmp;
				break;
			}
		}
		//std::cout << "here01" << std::endl;
		if(candInd >= 0 && selEvent->PhoPassPhoIso[candInd]){
			hists2d["photon1_Sigma_ChIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03ChHadIso[candArrInd], weight);
			hists2d["photon1_Sigma_ChSCRIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03ChHadSCRIso[candArrInd], weight);
			hists2d["photon1_Sigma_Et"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd), tree->phoEt_->at(candArrInd), weight);
		        hists2d["photon1_ChSCRIso_Et"]->Fill(selector->Pho03ChHadSCRIso[candArrInd], tree->phoEt_->at(candArrInd), weight);
			hists2d["photon1_ChSCRIso_Et"]->SetOption("box");
			hists2d["photon1_Sigma_Et"]->SetOption("box");
	                
			double phoEt = tree->phoEt_->at(candArrInd);
			if(phoEt>=25 && phoEt<35){
				hists2d["photon1_25_35_Sigma_ChSCRIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03ChHadSCRIso[candArrInd], weight);
			}
			if(phoEt>=35 && phoEt<45){
				hists2d["photon1_35_45_Sigma_ChSCRIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03ChHadSCRIso[candArrInd], weight);
			}
			if(phoEt>=45 && phoEt<60){
				hists2d["photon1_45_60_Sigma_ChSCRIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03ChHadSCRIso[candArrInd], weight);
			}
			if(phoEt>=60){
				hists2d["photon1_60_up_Sigma_ChSCRIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03ChHadSCRIso[candArrInd], weight);
			}
		}
		if(candInd >= 0 && selEvent->PhoPassChHadIso[candInd]){
			hists2d["photon1_Sigma_PhoIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03PhoIso[candArrInd], weight);
			hists2d["photon1_Sigma_PhoSCRIso"]->Fill(tree->phoSigmaIEtaIEta_->at(candArrInd),selector->Pho03PhoSCRIso[candArrInd], weight);
		}
		
	}
*/	//std::cout << "here1" << std::endl;
	// full event selection histograms
	if(!selEvent->passAll) return;

	// mc category
	if( tree->isData_ == 0 ){
		int EleP = 0;
		int EleM = 0;
		int MuP = 0;
		int MuM = 0;
		int TauP = 0;
		int TauM = 0;
		for( int mcI = 0; mcI < tree->nMC_; ++mcI){
	//	  std::cout << "starting to loop over nMC " << std::endl;
		  
		  if(abs(tree->mcMomPID->at(mcI))==24 && tree->mcParentage->at(mcI)==10){
		    if( tree->mcPID->at(mcI) == 11 )  EleP = 1;
		    if( tree->mcPID->at(mcI) == -11 ) EleM = 1;
		    if( tree->mcPID->at(mcI) == 13 )  MuP = 1;
		    if( tree->mcPID->at(mcI) == -13 ) MuM = 1;
		    if( tree->mcPID->at(mcI) == 15)   TauP = 1;
		    if( tree->mcPID->at(mcI) == -15)  TauM = 1;		    
		  }
		}
	//	std::cout << " Starting to fill the MC histograms " << std::endl;
		hists["MCcategory"]->Fill(1.0, weight); // Total
		int nEle = EleP + EleM;
		int nMu = MuP + MuM;
		int nTau = TauP + TauM;
		if( nEle + nMu + nTau == 0) hists["MCcategory"]->Fill(2.0, weight); // All Had
		if( nEle + nMu + nTau == 1) hists["MCcategory"]->Fill(3.0, weight); // Single Lepton
		if( nEle + nMu + nTau == 2) hists["MCcategory"]->Fill(4.0, weight); // Di Lepton
		
		if(nEle==1 && nMu==0 && nTau==0) hists["MCcategory"]->Fill(6.0, weight); // 1 e
		if(nEle==2 && nMu==0 && nTau==0) hists["MCcategory"]->Fill(7.0, weight); // 2 e
		if(nEle==0 && nMu==1 && nTau==0) hists["MCcategory"]->Fill(8.0, weight); // 1 mu
		if(nEle==0 && nMu==2 && nTau==0) hists["MCcategory"]->Fill(9.0, weight); // 2 mu
		if(nEle==0 && nMu==0 && nTau==1) hists["MCcategory"]->Fill(10.0, weight); // 1 tau
		if(nEle==0 && nMu==0 && nTau==2) hists["MCcategory"]->Fill(11.0, weight); // 2 tau

		//std::cout << " done filling the MCcategory histograms " << std::endl;
		//Count the number of electrons and muons for the fiducial cross section measurement
		int ElePfid = 0;
		int EleMfid = 0;
		int MuPfid = 0;
		int MuMfid = 0;
		int nNufid = 0;
		int nPhofid = 0;

		TVector2 MET = TVector2(0,0);
		TVector2 tempNu = TVector2(0,0);

		for( int mcI = 0; mcI < tree->nMC_; ++mcI){
		 // std::cout << "starting to loop over MC again " << std::endl;
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
		      tempNu.SetMagPhi(tree->mcPt->at(mcI),tree->mcPhi->at(mcI));
		      MET += tempNu;
		  }

		  if(tree->mcPID->at(mcI) == 22 && 
		     (tree->mcParentage->at(mcI)==2 || tree->mcParentage->at(mcI)==10 || tree->mcParentage->at(mcI)==26) && 
		     tree->mcPt->at(mcI) > 25 && 
		     fabs(tree->mcEta->at(mcI)) < 1.4442){
		    nPhofid += 1;
		  }
		  
		}
		if (ElePfid > 1 || EleMfid > 1 || MuPfid > 1 || MuMfid > 1 ){ cout << "SAME SIGN DILEPTON" << endl;}

		int nElefid = ElePfid + EleMfid;
		int nMufid = MuPfid + MuMfid;

		int nJetsfid = 0;
		int nBJetsfid = 0;

		if ((nElefid + nMufid)==1){
		  for ( int jetI = 0; jetI < tree->nJet_; jetI++){
		    if (tree->jetGenJetPt_->at(jetI) >= 30 && fabs(tree->jetGenEta_->at(jetI)) < 2.4){
		      nJetsfid += 1;
		      if (abs(tree->jetGenPartonID_->at(jetI))==5) nBJetsfid += 1;
		    }
		  }
		}
		
		//std::cout << "starting to fill the MC category fiduciary region " << std::endl;

		hists["MCcategoryfid"]->Fill(1.0, weight); // Total
		if( nElefid + nMufid == 0) hists["MCcategoryfid"]->Fill(2.0, weight); // All Had
		if( nElefid + nMufid == 1) hists["MCcategoryfid"]->Fill(3.0, weight); // Single Lepton
		if( nElefid + nMufid == 2) hists["MCcategoryfid"]->Fill(4.0, weight); // Di Lepton
		
		if(nElefid==1 && nMufid==0) hists["MCcategoryfid"]->Fill(6.0, weight); // 1 e
		if(nElefid==2 && nMufid==0) hists["MCcategoryfid"]->Fill(7.0, weight); // 2 e
		if(nElefid==0 && nMufid==1) hists["MCcategoryfid"]->Fill(8.0, weight); // 1 mu
		if(nElefid==0 && nMufid==2) hists["MCcategoryfid"]->Fill(9.0, weight); // 2 mu
		if(nElefid==1 && nMufid==1) hists["MCcategoryfid"]->Fill(9.0, weight); // 1 e 1 mu



		if(nElefid==1 && nMufid==0 && nJetsfid >=3){
		  hists["MCcategoryfid"]->Fill(11.0, weight);
		  if (nBJetsfid >= 1){
		    hists["MCcategoryfid"]->Fill(12.0, weight);
		    //if (tree->genMET_ > 20){
		    if (MET.Mod() > 20){
		      hists["MCcategoryfid"]->Fill(13.0, weight);
		      if (nPhofid > 0) hists["MCcategoryfid"]->Fill(14.0, weight);
		    }
		  }
		}
		
		if(nElefid==0 && nMufid==1 && nJetsfid >=3){
		  hists["MCcategoryfid"]->Fill(16.0, weight);
		  if (nBJetsfid >= 1){
		    hists["MCcategoryfid"]->Fill(17.0, weight);
		    //if (tree->genMET_ > 20){
		    if (MET.Mod() > 20){
		      //	    if (nNufid == 1){
		      hists["MCcategoryfid"]->Fill(18.0, weight);
		      if (nPhofid > 0) hists["MCcategoryfid"]->Fill(19.0, weight);
		    }
		  }
		}
	//	std::cout << " done filling histograms in MCcategoryfid " << std::endl;

	}
	//std::cout << " Done with MC " << std::endl;
	double MTW = 0.0;
	// muons
	if( selEvent->Muons.size() > 0 ){
		int ind = selEvent->Muons[0];
		hists["mu1Pt"]->Fill( tree->muPt_->at(ind), weight );
		hists["mu1Eta"]->Fill( tree->muEta_->at(ind), weight );
		hists["mu1RelIso"]->Fill( selector->Mu04RelIso[ind], weight );
		MTW = TMath::Sqrt(2*(tree->muPt_->at(ind))*(tree->pfMET_)*( 1.0 - TMath::Cos(dR(0.0,tree->muPhi_->at(ind),0.0,tree->pfMETPhi_)) ));

		hists["WtransMass"]->Fill( MTW, weight );
		if (selEvent->Muons.size() > 1) {
			int ind2 = selEvent->Muons[1];
			hists["mu2Pt"]->Fill( tree->muPt_->at(ind2), weight );
                        hists["mu2RelIso"]->Fill( selector->Mu04RelIso[ind2], weight );
                        TLorentzVector mu1;
                        TLorentzVector mu2;
                        mu1.SetPtEtaPhiM(tree->muPt_->at(ind), tree->muEta_->at(ind), tree->muPhi_->at(ind), 0.0);
                        mu2.SetPtEtaPhiM(tree->muPt_->at(ind2), tree->muEta_->at(ind2), tree->muPhi_->at(ind2), 0.0);
                        hists["mu1mu2Mass"]->Fill( (mu1+mu2).M(), weight);
                }

	//std::cout << " Done filling Muons " << std::endl;	
	}

	// electrons
	if( selEvent->Electrons.size() > 0 ){
		int ind = selEvent->Electrons[0];
		hists["ele1Pt"]->Fill( tree->elePt_->at(ind), weight );
		hists["ele1Eta"]->Fill( tree->eleSCEta_->at(ind), weight );
		hists["ele1RelIso"]->Fill( selector->Ele03RelIso[ind], weight );
		hists["ele1MVA"]->Fill( tree->eleIDMVATrg_->at(ind), weight );
		hists["ele1D0"]->Fill( tree->eleD0_->at(ind), weight );
		hists["ele1Dz"]->Fill( tree->eleDz_->at(ind), weight );
		hists["ele1EoverP"]->Fill( tree->eleEoverP_->at(ind), weight );
		hists["ele1sigmaIetaIeta"]->Fill( tree->eleSigmaIEtaIEta_->at(ind), weight );
		hists["ele1MissHits"]->Fill( tree->eleMissHits_->at(ind), weight );
		hists["ele1DrJet"]->Fill( minDr(tree->eleSCEta_->at(ind), tree->elePhi_->at(ind), selEvent->Jets, tree->jetEta_, tree->jetPhi_), weight );
		if( tree->isData_ == 0 ){
/*			if( tree->eleGenIndex_->at(ind) >= 0 ){
				hists["ele1MotherID"]->Fill( fabs(tree->eleGenMomPID_->at(ind)), weight );
				//if( TMath::Abs(tree->eleGenMomPID_->at(ind)) == 11 )
				hists["ele1GMotherID"]->Fill( fabs(tree->eleGenGMomPID_->at(ind)), weight );
			}
			else hists["ele1MotherID"]->Fill( 0.0, weight );
*/		}
		if( selEvent->Electrons.size() > 1 ){
			int ind2 = selEvent->Electrons[1];
			hists["ele2Pt"]->Fill( tree->elePt_->at(ind2), weight );
			hists["ele2RelIso"]->Fill( selector->Ele03RelIso[ind2], weight );
			TLorentzVector ele1;
			TLorentzVector ele2;
			ele1.SetPtEtaPhiM(tree->elePt_->at(ind), tree->eleSCEta_->at(ind), tree->elePhi_->at(ind), 0.0);
			ele2.SetPtEtaPhiM(tree->elePt_->at(ind2), tree->eleSCEta_->at(ind2), tree->elePhi_->at(ind2), 0.0);
			hists["ele1ele2Mass"]->Fill( (ele1+ele2).M(), weight);
		}
		
	/*	if(selEvent->Photons.size() > 0){
			TLorentzVector ele;
			TLorentzVector pho;
			int phoi = selEvent->Photons[0];
			ele.SetPtEtaPhiM(tree->elePt_->at(ind), tree->eleSCEta_->at(ind), tree->elePhi_->at(ind), 0.0);
			pho.SetPtEtaPhiM(tree->phoEt_->at(phoi), tree->phoEta_->at(phoi), tree->phoPhi_->at(phoi), 0.0);
			hists["ele1pho1Mass"]->Fill( (ele+pho).M(), weight);
		} 
	*/
	}
	//std::cout << "here2" << std::endl;
	// Loose Electrons (if any)
	if(selEvent->ElectronsLoose.size() > 0 && tree->isData_ == 0){
		int eleInd = selEvent->ElectronsLoose[0];
		double mindr = 999;
		for( int mcI = 0; mcI < tree->nMC_; ++mcI){
			if( tree->mcPID->at(mcI) == 22 ){
				double thisdr = dR(tree->mcEta->at(mcI), tree->mcPhi->at(mcI), tree->eleSCEta_->at(eleInd), tree->elePhi_->at(eleInd));
				if( mindr > thisdr ) mindr = thisdr;
			}
		}
		hists["looseEleDrGenPho"]->Fill(mindr, weight);
	}
	//std::cout << "Done filling electrons" << std::endl;
	// photons
/*	hists["nPhotons"]->Fill(selEvent->Photons.size(), weight);
	if( selEvent->Photons.size() > 0 ){
		int ind = selEvent->Photons[0];
		hists["photon1Et"]->Fill( tree->phoEt_->at(ind), weight );
		hists["photon1Eta"]->Fill( tree->phoEta_->at(ind), weight );
		hists["photon1IsConv"]->Fill( tree->phohasPixelSeed_->at(ind), weight );
		
		hists["photon1ChHadIso"]->Fill( selector->Pho03ChHadIso[ind], weight );
		hists["photon1ChHadSCRIso"]->Fill( selector->Pho03ChHadSCRIso[ind], weight );
		hists["photon1ChHadRandIso"]->Fill( selector->Pho03RandChHadIso[ind], weight );
		double phoEt = tree->phoEt_->at(ind);
		if(phoEt>=25 && phoEt<35){
			hists["photon1_25_35_ChHadRandIso"]->Fill( selector->Pho03RandChHadIso[ind], weight );
		}
		if(phoEt>=35 && phoEt<45){
			hists["photon1_35_45_ChHadRandIso"]->Fill( selector->Pho03RandChHadIso[ind], weight );
		}
		if(phoEt>=45 && phoEt<60){
			hists["photon1_45_60_ChHadRandIso"]->Fill( selector->Pho03RandChHadIso[ind], weight );
		}
		if(phoEt>=60){
			hists["photon1_60_up_ChHadRandIso"]->Fill( selector->Pho03RandChHadIso[ind], weight );
		}

		hists["photon1NeuHadIso"]->Fill( selector->Pho03NeuHadIso[ind], weight );
		
		hists["photon1PhoIso"]->Fill( selector->Pho03PhoIso[ind], weight );
		hists["photon1PhoSCRIso"]->Fill( selector->Pho03PhoSCRIso[ind], weight );
		hists["photon1PhoRandIso"]->Fill( selector->Pho03RandPhoIso[ind], weight );
		
		hists["photon1HoverE"]->Fill( tree->phoHoverE_->at(ind), weight );
		hists["photon1SigmaIEtaIEta"]->Fill( tree->phoSigmaIEtaIEta_->at(ind), weight );
		hists["photon1DrElectron"]->Fill( minDr(tree->phoEta_->at(ind), tree->phoPhi_->at(ind), selEvent->Electrons, tree->eleSCEta_, tree->elePhi_), weight );
		hists["photon1DrJet"]->Fill( minDr(tree->phoEta_->at(ind), tree->phoPhi_->at(ind), selector->Jets, tree->jetEta_, tree->jetPhi_), weight );
               // std::cout << "Most of photons done" << std::endl;
	//	if( tree->isData_ == 0 ){
			//if( tree->phoGenIndex_->at(ind) >= 0 ){
			//	hists["photon1MotherID"]->Fill( fabs(tree->phoGenMomPID_->at(ind)), weight );
				//if( TMath::Abs(tree->phoGenMomPID_->at(ind)) == 22 )
			//	hists["photon1GMotherID"]->Fill( fabs(tree->phoGenGMomPID_->at(ind)), weight );
		//	}
		//	else {
		//		hists["photon1MotherID"]->Fill( 0.0, weight );
		//	}
			
			// find the closest b-jet
	//		double mindr = minDrPhoB(ind, tree);
	//		int phoGen=-1;
			//for( int mcI = 0; mcI < tree->nMC_; ++mcI){
			//	if( tree->mcIndex->at(mcI) == tree->phoGenIndex_->at(ind) ) 
			//		phoGen=mcI;
		//	}
	//		if( phoGen > 0){
	//			hists["GenPhotonEt"]->Fill(tree->mcPt->at(phoGen), weight);
			//	hists["GenPhotonMinDR"]->Fill(secondMinDr(phoGen, tree), weight);
	//		}
	//		if(mindr<999) {
	//			hists["photon1DrMCbquark"]->Fill( mindr, weight );
	//		}
		
	//	}
	} */
	//std::cout << "almost done " << std::endl;
	hists["Ht"]->Fill( calc_ht(selEvent, tree), weight );
	hists["MET"]->Fill( tree->pfMET_, weight );
        hists["MET_low"]->Fill(tree->pfMET_,weight);
	hists["nVtx"]->Fill( tree->nVtx_, weight );
	hists["nJets"]->Fill( selEvent->Jets.size(), weight );
	//std::cout << "here5" << std::endl;

	// jets
	if(selEvent->Jets.size()>=3){
		TLorentzVector j1,j2,j3;
		int jetI;
		
		double minM3 = 99999.9;
		double M3maxPt = 99999.9;
		double M3minPt = 99999.9;
		double minPt = 99999.9;
		double M4maxPt = 99999.9;
		double max4Pt = 0.0;
		double maxPt = 0.0;
		double M3first = 0.0;
		TLorentzVector maxPtsystem;
		TLorentzVector phovec;
		phovec.SetPtEtaPhiM(0.00001,0.0,0.0,0.0);
		/*if( selEvent->Photons.size() > 0 ){
                	int phoi = selEvent->Photons[0];
			phovec.SetPtEtaPhiM(tree->phoEt_->at(phoi), tree->phoEta_->at(phoi), tree->phoPhi_->at(phoi), 0.0);
		}*/
		for(int jet1I=0; jet1I < selEvent->Jets.size()-2; jet1I++){	
			jetI = selEvent->Jets[jet1I];
			j1.SetPtEtaPhiM(tree->jetPt_->at(jetI), tree->jetEta_->at(jetI), tree->jetPhi_->at(jetI), 0.0);
			for(int jet2I=jet1I+1; jet2I < selEvent->Jets.size()-1; jet2I++){
				jetI = selEvent->Jets[jet2I];
				j2.SetPtEtaPhiM(tree->jetPt_->at(jetI), tree->jetEta_->at(jetI), tree->jetPhi_->at(jetI), 0.0);
				for(int jet3I=jet2I+1; jet3I < selEvent->Jets.size(); jet3I++){
					jetI = selEvent->Jets[jet3I];
					j3.SetPtEtaPhiM(tree->jetPt_->at(jetI), tree->jetEta_->at(jetI), tree->jetPhi_->at(jetI), 0.0);
		
					double m3 = (j1+j2+j3).M();
					double totalPt = (j1+j2+j3).Pt();

					if(jet1I==0 && jet2I==1 && jet3I==2) M3first = m3;
					if(m3 < minM3) minM3 = m3;
					
					if(minPt > totalPt){
						minPt = totalPt;
						M3minPt = m3;
					}
					if(maxPt < totalPt){
						maxPt = totalPt; 
						M3maxPt = m3; 
						maxPtsystem = (j1+j2+j3);
					}

					if( phovec.DrEtaPhi(j1) < 0.3 )
						j1 = j1 - phovec;
					if( phovec.DrEtaPhi(j2) < 0.3 )
						j2 = j2 - phovec;
					if( phovec.DrEtaPhi(j3) < 0.3)
						j3 = j3 - phovec;
					double m4 = (phovec+j1+j2+j3).M();
					double total4Pt = (phovec+j1+j2+j3).Pt();
					hists["M3phoMulti"]->Fill(m4, weight);
					if(max4Pt < total4Pt ){ 
						max4Pt=total4Pt;
						M4maxPt=m4;
					}
				}
			}
		}
		
		double toppt=0.0;
		double antitoppt=0.0;
		for(int mcInd=0; mcInd<tree->nMC_; ++mcInd){
			if(tree->mcPID->at(mcInd)==6) toppt = tree->mcPt->at(mcInd);
			if(tree->mcPID->at(mcInd)==-6) antitoppt = tree->mcPt->at(mcInd);
		}
		double maxtoppt = std::max(toppt,antitoppt);
		if( maxtoppt < 30 ) hists["M3_0_30"]->Fill(M3maxPt, weight);
		else if( maxtoppt < 100) hists["M3_30_100"]->Fill(M3maxPt, weight);
		else if( maxtoppt < 200) hists["M3_100_200"]->Fill(M3maxPt, weight);
		else if( maxtoppt < 300) hists["M3_200_300"]->Fill(M3maxPt, weight);
		else hists["M3_300_up"]->Fill(M3maxPt, weight);

		hists["M3first"]->Fill(M3first, weight);
		hists["M3"]->Fill(M3maxPt, weight);
		hists["M3minPt"]->Fill(M3minPt, weight);
	/*	if( selEvent->Photons.size() > 0 ) {
			hists["M3pho"]->Fill(M4maxPt, weight);
			hists["dRpho3j"]->Fill(phovec.DrEtaPhi(maxPtsystem), weight);
		}
	*/	hists["minM3"]->Fill(minM3, weight);
		hists2d["MTW_M3"]->Fill( MTW, M3maxPt, weight);
		
	}

	if( selEvent->Jets.size() > 0 ){
		int ind = selEvent->Jets[0];
		hists["jet1Pt"]->Fill( tree->jetPt_->at(ind), weight );
		hists["jet1Eta"]->Fill( tree->jetEta_->at(ind), weight );
	}
	if( selEvent->Jets.size() > 1 ){
		int ind = selEvent->Jets[1];
		hists["jet2Pt"]->Fill( tree->jetPt_->at(ind), weight );
		hists["jet2Eta"]->Fill( tree->jetEta_->at(ind), weight );
	}
	if( selEvent->Jets.size() > 2 ){
		int ind = selEvent->Jets[2];
		hists["jet3Pt"]->Fill( tree->jetPt_->at(ind), weight );
		hists["jet3Eta"]->Fill( tree->jetEta_->at(ind), weight );
	}
	if( selEvent->Jets.size() > 3 ){
		int ind = selEvent->Jets[3];
		hists["jet4Pt"]->Fill( tree->jetPt_->at(ind), weight );
		hists["jet4Eta"]->Fill( tree->jetEta_->at(ind), weight );
	}
//	std::cout << " Done filling everything " << std::endl;	
}

int Histogrammer::minDrIndex(double myEta, double myPhi, std::vector<int> Inds, std::vector<float> *etas, std::vector<float> *phis){
	double mindr = 999.0;
	double dr;
	int bestInd = -1;
	for( std::vector<int>::iterator it = Inds.begin(); it != Inds.end(); ++it){
		dr = dR(myEta, myPhi, etas->at(*it), phis->at(*it));
		if( mindr > dr ) {
			mindr = dr;
			bestInd = *it;
		}
	}
	return bestInd;
}

double Histogrammer::minDr(double myEta, double myPhi, std::vector<int> Inds, std::vector<float> *etas, std::vector<float> *phis){
	int ind = minDrIndex(myEta, myPhi, Inds, etas, phis);
	if(ind>=0) return dR(myEta, myPhi, etas->at(ind), phis->at(ind));
	else return 999.0;
}


/*double Histogrammer::minDrPhoB(int PhoInd, EventTree* tree){
	// find the closest b-jet
	TLorentzVector b;
	TLorentzVector bBar;
	int phoGen=-1;
	double mindr = 999.0;
	for( int mcI = 0; mcI < tree->nMC_; ++mcI){
		if( tree->mcIndex->at(mcI) == tree->phoGenIndex_->at(PhoInd) ) 
			phoGen=mcI;
		if( tree->mcPID->at(mcI) == 5) 
			b.SetPtEtaPhiM(tree->mcPt->at(mcI), tree->mcEta->at(mcI), tree->mcPhi->at(mcI), tree->mcMass->at(mcI));
		if( tree->mcPID->at(mcI) == -5) 
			bBar.SetPtEtaPhiM(tree->mcPt->at(mcI), tree->mcEta->at(mcI), tree->mcPhi->at(mcI), tree->mcMass->at(mcI));
	}
	if( phoGen > 0 && b.Pt() > 0.0001 && bBar.Pt() > 0.0001 ) {
		mindr = std::min(dR(tree->mcEta->at(phoGen), tree->mcPhi->at(phoGen), b.Eta(), b.Phi()),
						 dR(tree->mcEta->at(phoGen), tree->mcPhi->at(phoGen), bBar.Eta(), bBar.Phi()));
	}
	return mindr;
}
*/
double Histogrammer::calc_ht(EventPick* evtPick, EventTree* tree){
	double ht = 0.0;
	ht += tree->pfMET_;
	for( std::vector<int>::iterator it = evtPick->Jets.begin(); it != evtPick->Jets.end(); ++it)
		ht += tree->jetPt_->at(*it);
	for( std::vector<int>::iterator it = evtPick->Electrons.begin(); it != evtPick->Electrons.end(); ++it)
		ht += tree->elePt_->at(*it);
        for( std::vector<int>::iterator it = evtPick->ElectronsLoose.begin(); it != evtPick->ElectronsLoose.end(); ++it)
                ht += tree->elePt_->at(*it);
	//for( std::vector<int>::iterator it = evtPick->Muons.begin(); it != evtPick->Muons.end(); ++it)
	//	ht += tree->muPt_->at(*it);	
	for( std::vector<int>::iterator it = evtPick->MuonsLoose.begin(); it != evtPick->MuonsLoose.end(); ++it)
		ht += tree->muPt_->at(*it);			
	// photons are now also in jet collection
	//for( std::vector<int>::iterator it = evtPick->Photons.begin(); it != evtPick->Photons.end(); ++it)
	//	ht += tree->phoEt_->at(*it);
	return ht;
}

void Histogrammer::make_hist(const char* hname, const char* htitle, int nbins, double xlow, double xhigh, const char* xlabel, const char* ylabel){
	TH1F* h = new TH1F(hname, htitle, nbins, xlow, xhigh);
	h->GetXaxis()->SetTitle(xlabel);
	h->GetYaxis()->SetTitle(ylabel);
	h->SetDirectory(0);
	//h->Sumw2();u	hists[hname] = h;
	hists[hname] = h;
}

void Histogrammer::make_hist2d(const char* hname, const char* htitle, int nxbins, double xlow, double xhigh, int nybins, double ylow, double yhigh){
	TH2F* h2 = new TH2F(hname, htitle, nxbins, xlow, xhigh, nybins, ylow, yhigh);
	h2->SetDirectory(0);
	hists2d[hname] = h2;
}

void Histogrammer::write_histograms(std::string folderS, std::vector<TH1F*> histVector){

	TFile* outFile = new TFile((folderS+"/hist_"+title+".root").c_str(), "RECREATE");

	for( std::map< std::string, TH1F* >::iterator it = hists.begin(); it != hists.end(); ++it){
	  
		it->second->SetDirectory(outFile->GetDirectory(""));
		it->second->Write();
		it->second->SetDirectory(0);
	}

	for( std::vector<TH1F*>::iterator it = histVector.begin(); it != histVector.end(); ++it){
		(*it)->SetDirectory(outFile->GetDirectory(""));
		(*it)->Write();
		(*it)->SetDirectory(0);
	}

	for( std::map< std::string, TH2F* >::iterator it = hists2d.begin(); it != hists2d.end(); ++it){
		it->second->SetDirectory(outFile->GetDirectory(""));
		it->second->Write();
		it->second->SetDirectory(0);
	}

	outFile->Close();
}


Histogrammer::~Histogrammer(){
	// do not delete histograms
}
