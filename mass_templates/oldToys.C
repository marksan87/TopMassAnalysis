#include <TTree.h>
#include <TObject.h>
#include <TRandom3.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <unordered_set>
using std::vector;
using std::unordered_set;
using std::cout;
using std::flush;
using std::endl;

vector< vector< float > > createToys(TTree* t, char* obsName, float cut, int npoints, int ntoys)
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
    unordered_set<int> toyPoints;   
    
    long max = t->GetEntriesFast();
    int evt = 0, n = 0;
    cout<<"Creating "<<ntoys<<" toys of observable "<<obsName<<" with "<<npoints<<" points and ";
    if (cut < 0.f)
    {
        cut = 1000000.f;
        cout<<"no cut"<<endl<<endl;
        
    }
    else { cout<<"cut at "<<cut<<" GeV"<<endl<<endl; }

    for (int toy = 0; toy < ntoys; toy++)
    {
        cout<<"Creating toy "<<toy+1<<".. "<<flush;
        toyPoints.clear();
        TRandom3 r(0);
        m1 = m2 = w = 0.0f;
        n = 0;
        for (int p = 0; p < npoints; p++)
        {
            evt = r.Integer(max) + 1;
            //if (toyPoints.find(evt) != toyPoints.end() )
            if (!toyPoints.insert(evt).second)
            {
                p--;
                continue;
            }
            t->GetEntry(evt);
            if (obs > cut) { continue; }
            n++;
            w += weight;
            m1 += weight * obs;
            m2 += weight * obs * obs;
        }
        cout<<n<<" points"<<endl; 
        m1 /= w;
        m2 /= w;
        //weights.push_back(w);
        moment1.push_back(m1);
        moment2.push_back(m2);
    }

    vector< vector<float> > results;
    //results.push_back(w);
    results.push_back(moment1);
    results.push_back(moment2);
    return results;
}
