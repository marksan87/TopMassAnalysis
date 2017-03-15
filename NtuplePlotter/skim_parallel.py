from subprocess import Popen
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("outDir", help="output directory")
parser.add_argument("inDir", help="input directory")
parser.add_argument("numFiles", help="number files", type=int)
parser.add_argument("isMC", help="mc flag", type=int)
args = parser.parse_args()

def runPacked(a):
    return run_skim(a)

def run_skim(a):
    #print ("/uscms_data/d3/msaunder/topMassAnalysis/CMSSW_8_0_24_patch1/src/ttgamma_13TeV/NtuplePlotter/file_skim.csh {0} {1}").format(a[0], a[1]) 
    Popen(("/uscms_data/d3/msaunder/topMassAnalysis/CMSSW_8_0_26_patch1/src/ttgamma_13TeV/NtuplePlotter/file_skim.csh {0} {1}").format(a[0], a[1]), shell=True)


from multiprocessing import Pool
pool = Pool(10)

if args.isMC == 1: 
    fname = "ggtree_mc_"
else:
    fname = "ggtree_data_"

taskList = []
outDir = args.outDir
if outDir[-1] != '/':
    outDir += '/'

inDir = args.inDir
if inDir[-1] != '/':
    inDir += '/'

for i in xrange(1, args.numFiles+1):
    taskList.append((outDir + fname + str(i) + ".root", inDir + fname + str(i) + ".root")) 

#print taskList[0])

pool.map(runPacked,taskList)

#print args.outDir, args.inDir, args.numFiles, args.isMC

