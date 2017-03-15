#include "CondFormats/BTauObjects/interface/BTagCalibration.h"
#include "CondFormats/BTauObjects/interface/BTagCalibrationReader.h"
int main(int argc, char **argv)
{
// setup calibration readers
	BTagCalibration calib("csvv2", "CSVV2.csv");
	BTagCalibrationReader reader(BTagEntry::OP_LOOSE,  // operating point
                              	"central");           // systematics type
	BTagCalibrationReader reader_up(BTagEntry::OP_LOOSE, "up");  // sys up
	BTagCalibrationReader reader_do(BTagEntry::OP_LOOSE, "down");  // sys down
	reader.load(&calib,               // calibration instance
             	BTagEntry::FLAV_B,    // btag flavour
            	"comb")               // measurement type
}

