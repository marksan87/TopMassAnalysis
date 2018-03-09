all: skim 


signalAcceptance: Selector.o EventPick.o EventTree.o signalAcceptance.cpp OverlapRemove.cpp
	g++ -o signalAcceptance `root-config --libs` -I`root-config --incdir` -std=c++11 EventTree.o EventPick.o Selector.o OverlapRemove.cpp signalAcceptance.cpp

skim: Selector.o EventPick.o EventTree.o RoccoR.o OverlapRemove.cpp makeSkim.cpp
	g++ -o skim `root-config --libs` -I`root-config --incdir` -std=c++11 EventTree.o EventPick.o Selector.o OverlapRemove.cpp Roc_muon_corrections/RoccoR.o makeSkim.cpp

EventTree.o: EventTree.cpp EventTree.h
	g++ -c -I`root-config --incdir` -std=c++11 EventTree.cpp

Selector.o: EventTree.o Selector.cpp Selector.h
	g++ -c -I`root-config --incdir` -std=c++11 Selector.cpp

RoccoR.o: Roc_muon_corrections/RoccoR.cc Roc_muon_corrections/RoccoR.h
	g++ -c -I`root-config --incdir` -std=c++11 Roc_muon_corrections/RoccoR.cc -o Roc_muon_corrections/RoccoR.o

BTagCalibrationStandalone.o: BTagCalibrationStandalone.cpp BTagCalibrationStandalone.h
	g++ -c -I`root-config --incdir` -std=c++11 BTagCalibrationStandalone.cpp

EventPick.o: EventPick.cpp EventPick.h
	g++ -c -I`root-config --incdir` -std=c++11 EventPick.cpp 

Histogrammer.o: Histogrammer.cpp Histogrammer.h
	g++ -c -I`root-config --incdir` -std=c++11 Histogrammer.cpp

HistCollect.o: HistCollect.cpp HistCollect.h
	g++ -c -I`root-config --incdir` -std=c++11 HistCollect.cpp

clean:
	rm EventTree.o Selector.o EventPick.o RoccoR.o JECvariation.o BTagCalibrationStandalone.o  
