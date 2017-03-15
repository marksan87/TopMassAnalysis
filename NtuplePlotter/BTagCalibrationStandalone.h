#ifndef BTagEntry_H
#define BTagEntry_H

#include <TH1.h>


class BTagEntry
{
public:
  enum OperatingPoint {
    OP_LOOSE=0,
    OP_MEDIUM=1,
    OP_TIGHT=2,
    OP_RESHAPING=3,
  };
  enum JetFlavor {
    FLAV_B=0,
    FLAV_C=1,
    FLAV_UDSG=2,
  };
  struct Parameters {
    OperatingPoint operatingPoint;
    std::string measurementType;
    std::string sysType;
    JetFlavor jetFlavor;
    float etaMin;
    float etaMax;
    float ptMin;
    float ptMax;
    float discrMin;
    float discrMax;
Parameters(
      OperatingPoint op=OP_TIGHT,
      std::string measurement_type="comb",
      std::string sys_type="central",
      JetFlavor jf=FLAV_B,
      float eta_min=-99999.,
      float eta_max=99999.,
      float pt_min=0.,
      float pt_max=99999.,
      float discr_min=0.,
      float discr_max=99999.
    );

  };

  BTagEntry() {}
  BTagEntry(const std::string &csvLine);
  BTagEntry(const std::string &func, Parameters p);
  BTagEntry(const TF1* func, Parameters p);
  BTagEntry(const TH1* histo, Parameters p);
  ~BTagEntry() {}
  static std::string makeCSVHeader();
  std::string makeCSVLine() const;
  static std::string trimStr(std::string str);
  std::string formula;
  Parameters params;

};

#endif  // BTagEntry_H


#ifndef BTagCalibration_H
#define BTagCalibration_H

#include <map>
#include <vector>
#include <string>
#include <istream>
#include <ostream>


class BTagCalibration
{
public:
  BTagCalibration() {}
  BTagCalibration(const std::string &tagger);
  BTagCalibration(const std::string &tagger, const std::string &filename);
  ~BTagCalibration() {}

  std::string tagger() const {return tagger_;}

  void addEntry(const BTagEntry &entry);
  const std::vector<BTagEntry>& getEntries(const BTagEntry::Parameters &par) const;

  void readCSV(std::istream &s);
  void readCSV(const std::string &s);
  void makeCSV(std::ostream &s) const;
  std::string makeCSV() const;

protected:
  static std::string token(const BTagEntry::Parameters &par);

  std::string tagger_;
  std::map<std::string, std::vector<BTagEntry> > data_;

};

#endif  // BTagCalibration_H
#ifndef BTagCalibrationReader_H
#define BTagCalibrationReader_H

#include <memory>
#include <string>



class BTagCalibrationReader
{
public:
  BTagCalibrationReader() {}
  BTagCalibrationReader(BTagEntry::OperatingPoint op,
                        std::string sysType="central");

  void load(const BTagCalibration & c,
            BTagEntry::JetFlavor jf,
            std::string measurementType="comb");

  double eval(BTagEntry::JetFlavor jf,
              float eta,
              float pt,
              float discr=0.) const;

  std::pair<float, float> min_max_pt(BTagEntry::JetFlavor jf, 
                                     float eta, 
                                     float discr=0.) const;

protected:
  class BTagCalibrationReaderImpl;
  std::auto_ptr<BTagCalibrationReaderImpl> pimpl;
};


#endif  // BTagCalibrationReader_H














