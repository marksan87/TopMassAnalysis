#include <TTree.h>
#include <TObject.h>
#include <TRandom3.h>
#include <TMath.h>
#include <TH1F.h>
#include <TFile.h>
#include <iostream>
#include <vector>
using std::vector;
using std::cout;
using std::flush;
using std::endl;

vector< vector< float > > createToys(TTree* t, char* obsName, float cut, int ntoys)
{
    Float_t weight;
    Float_t obs;
    t->SetBranchAddress("weight", &weight);
    t->SetBranchAddress(obsName, &obs);
    //set<int> toyPoints;
    vector<float> moment1;
    vector<float> moment2;
    vector<float> weights;
    float m1, m2, w;
    float toyWeight;    // Variation on actual event weight
    TH1F* wh = new TH1F("weights","Event Weights", 100, -1.0, 2.0); 
    TH1F* whtoys = new TH1F("toyweights","Toy Weights", 100, -1.0, 2.0); 

    long numEvts = t->GetEntriesFast();
    cout<<"Creating "<<ntoys<<" toys of observable "<<obsName<<" with all points and ";
    if (cut < 0.f)
    {
        cut = 1000000.f;
        cout<<"no cut"<<endl<<endl;
        
    }
    else { cout<<"cut at "<<cut<<" GeV"<<endl<<endl; }

    for (int toy = 0; toy < ntoys; toy++)
    {
        if (toy % 10 == 0) { cout<<"On toy "<<toy<<endl; }
        //cout<<"On toy "<<toy<<".."<<flush;
        TRandom3 r(0);
        m1 = m2 = w = 0.0f;
        for (int evt = 0; evt < numEvts; evt++)
        {
            t->GetEntry(evt);
            if (obs > cut) { continue; }
            //toyWeight = TMath::Max((Float_t)r.Gaus(weight,weight), (Float_t)0.0);    // Fluctuate weight with a gaussian of mean = std = event weight       
            toyWeight = r.Gaus(weight,weight);    // Fluctuate weight with a gaussian of mean = std = event weight       
            wh->Fill(weight);
            whtoys->Fill(toyWeight); 
            /*
            if (toy == 0) 
            { 
                wh->Fill(weight);
                whtoys->Fill(toyWeight); 
            } 
            */
            w += toyWeight;
            m1 += toyWeight * obs;
            m2 += toyWeight * obs * obs;
        }
        m1 /= w;
        m2 /= w;
        weights.push_back(w);
        moment1.push_back(m1);
        moment2.push_back(m2);
       // cout<<"done."<<endl;
    }
    TFile* f = new TFile("weights.root", "recreate");
    wh->Write();
    whtoys->Write();
    f->Close();
    delete f;
    delete wh;
    vector< vector<float> > results;
    results.push_back(weights);
    results.push_back(moment1);
    results.push_back(moment2);
    return results;
}
