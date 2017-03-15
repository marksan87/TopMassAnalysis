from ROOT import TFile
#import optparse
import argparse
import sys

def main():
    usage = 'usage %prog [options]'
    #parser = optparse.OptionParser(usage)
    #parser.add_option('-i', '--inF', dest='inF', help='input file (.root)', default=None, type='string')
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="input file (.root)")
    args = parser.parse_args()
    #(opt, args) = parser.parse_args()
    #print "About to open %s" % (opt.inF) 
    #f = TFile.Open(opt.inF)
    f = TFile.Open(args.file)
    t = f.Get("ggNtuplizer/EventTree")
    print "Total entries in file %s: %d" % (args.file, t.GetEntries()) 
    #print "Total entries in file %s: %d" % (opt.inF, t.GetEntries())
    exit(0)

if __name__ == "__main__":
    sys.exit(main())
