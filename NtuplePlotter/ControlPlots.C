void MakePlots(string filename) {

    TChain Data("clusters");
    File.Add("data_c.root");
    File.Add("data_d.root");
    File.Add("ttgamma.root"); 
    File.Add("st_t.root");
    File.Add("st_t_bar.root");
    File.Add("st_tW_bar.root");
    File.Add("st_tW.root");
    File.Add("st_s.root");
    File.Add("Wjets.root");
    File.Add("Zjets.root");
    File.Add("DYJets.root");
    File.Add("ttjets.root");
    
    TChain Data("EventTree");
    
    Double_t jetPt, muPt, nJet, nMu ;

    Data.SetBranchAddress("nMu", &nMu);
    Data.SetBranchAddress("nJet", &nJet);
    Data.SetBranchAddress("jetPt", &jetPt);
    Data.SetBranchAddress("muPt", &muPt);

    int NumEvents = Data.GetEntries();

    for(int event = 0; event < NumEvents; event++) {
        if(event % 1000 == 0) cout << "Processing Event " << event << endl;
        Data.GetEvent(event);
	
    }
}
