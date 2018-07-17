#include <TROOT.h>
#include <TTree.h>
#include <TLatex.h>
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

vector< vector< float > > createToys(TTree* t, char* obsName, float cut, int ntoys, int nbins, float min, float max)
{
    float weight;
    float obs;
    t->SetBranchAddress("weight", &weight);
    t->SetBranchAddress(obsName, &obs);
    //set<int> toyPoints;
    vector<float> moment1;
    vector<float> moment2;
    vector<float> weights;
    float m1, m2, w;
    int evt;
    
    //nbins = 5;
    //float x[] = {0.0, 1.0, 2.0, 3.0, 4.0, 5.0};
    
    TRandom3* r = new TRandom3(0);
    long numEvts = t->GetEntriesFast();
    cout<<"Creating "<<ntoys<<" toys of observable "<<obsName<<" with "<<nbins<<" bins from "<<min<<" to "<<max<<" GeV and ";
    if (cut < 0.0)
    {
        cut = 1000000.0;
        cout<<"no cut"<<endl<<endl;
        
    }
    else { cout<<"cut at "<<cut<<" GeV"<<endl<<endl; }

    /*
    float* bins = new float[nbins+1];
    for (int i = 0; i < nbins+1; i++)
    {
        bins[i] = min + (max - min) / (float)nbins * (float)i;
    }
    */
    TH1F* h = new TH1F("nominal", "Nominal", nbins, min, max);
    //TH1F* h = new TH1F("nominal", "Nominal", nbins, min, cut);
    //TH1F* h = new TH1F("nominal", "Nominal", nbins, bins);
    //TH1F* h = new TH1F("nominal", "Nominal", nbins, x);
    char drawStr[200], cutStr[200];
    sprintf(drawStr, "%s>>nominal", obsName);
    sprintf(cutStr, "%s > %f && %s < %f", obsName, min, obsName, max);
    cout<<"drawStr = "<<drawStr<<endl;
    cout<<"cutStr = "<<cutStr<<endl;
    gROOT->SetBatch(true);
    t->Draw(drawStr, cutStr);
    h->SetTitle("p_{T}(ll)");
    h->GetXaxis()->SetTitle("p_{T}(ll) [GeV]");
    char ytitle[200];
    sprintf(ytitle, "Events / %.1f GeV", (max - min)/(float)nbins);
    h->GetYaxis()->SetTitle(ytitle);
    h->GetYaxis()->SetTitleOffset(1.2);

    TFile* f = new TFile("ptll.root", "recreate");
    //h->Write();
    h->Draw("HIST");
    TLatex txt;
    txt.SetNDC(true);
    txt.SetTextFont(43);
    txt.SetTextSize(20);
    txt.SetTextAlign(12);
    char label[200];
    sprintf(label, "#bf{CMS} #it{Work in Progress}  %3.1f fb^{-1} (13 TeV)", 35.9);
    txt.DrawLatex(0.1, 0.92, label);
    h->Write();
    f->Close();
    delete f;

    for (int toy = 0; toy < ntoys; toy++)
    {
        //if (toy % 10 == 0) { cout<<"On toy "<<toy<<endl; }
        //cout<<"On toy "<<toy<<".."<<flush;
       
        TH1F* htoy = (TH1F*)h->Clone();
        htoy->SetDirectory(0);

        for (int bin = 1; bin < nbins+1; bin++)
        {
            double binVal = htoy->GetBinContent(bin);
            double var = r->PoissonD(binVal);
            /*
            if (toy == 0) 
            {
                //cout<<"Toy "<<toy<<(bin < 10 ? " Bin " : " Bin  ")<<bin<<"  orig: "<<binVal;
                cout<<"Toy "<<toy<<(bin < 10 ? " Bin " : " Bin  ")<<bin<<"  orig: "<<binVal<<"\tvar: "<<var<<endl;
                if (binVal >= 1000)     
                {
                    cout<<"\tvar: "<<var<<endl; 
                }
                else
                {
                    cout<<"\t\tvar: "<<var<<endl; 
                }
            }
            */
            htoy->SetBinContent(bin, var);
        }


        //char name[100], title[100];
        //sprintf(name, "h%d", toy);
        //sprintf(title, "Toy %d", toy);
        //TH1D* h = new TH1D("nominal", , nbins, min, max);
        if (toy == 0)
        {
            cout<<"Nominal distribution:"<<endl;
            cout<<"m1 = "<<h->GetMean()<<" +- "<<h->GetMeanError()<<endl;
            cout<<"m2 = "<<h->GetStdDev()<<" +- "<<h->GetStdDevError()<<endl;
        }
        m1 = htoy->GetMean();
        m2 = htoy->GetStdDev();
        moment1.push_back(m1);
        moment2.push_back(m2);
        
        delete htoy;

       // cout<<"done."<<endl;
    }
    
    delete r;
    delete h;

    vector< vector<float> > results;
    results.push_back(moment1);
    results.push_back(moment2);
    return results;
}
