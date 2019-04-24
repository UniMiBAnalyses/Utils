import ROOT as rt  
import sys  
import utils
import argparse
from TreeWriter import TreeWriter

parser = argparse.ArgumentParser(description='Parton Analyzer, jet pairing')
parser.add_argument('data_path', type=str, help='All the files in this directory will be analyzed')
parser.add_argument('--nevents', type=int, default=1, help='How many events per file should be analysed. Set to a negative value to include all events')
parser.add_argument('--debug', type=bool, default=False, help='Set debug mode')
parser.add_argument('--radius', type=float, default=0.8, help="Radius from jet")

args = parser.parse_args()

file = rt.TFile(args.data_path)
tree = file.Get("latino")

nevents = args.nevents
debug = args.debug

output = rt.TFile("output.root", "RECREATE")
output_tree = TreeWriter("tree", debug=args.debug)
output_tree.define_branches({
    1 : { 
        float: ["mjj_vbs", "W_mass",  "deltaeta_vbs", "W_pt", "W_eta",
                "lep_pt", "lep_eta"],
        int: ["hasTop"]
    },
    2: {
        float: ["vbs_pts", "vbs_etas", "w_pts", "w_etas"]
    }
})

iev = 0

for event in tree:

    if iev % 1000 ==0:
        print ("> event: ", iev)
    iev+=1
    partons, pids = utils.get_hard_partons(event, debug)
    #jets = utils.get_jets(event, debug)

    #print ("partons PID: ", pids)
    
    if 6 in pids or -6 in pids:
        output_tree.hasTop = True
    else: 
        output_tree.hasTop = False

    #remove tops
    partons = [  partons[i]  for i, p in enumerate(pids) if abs(p) !=6 ]

    vpair = utils.nearest_masses_pair(partons, [80.385, 91.1876])
    vbspair = [i for i in range(4) if not i in vpair]
    
    wpart = [partons[i] for i in vpair]
    vbspart = [partons[j] for j in vbspair]

    W = wpart[0] + wpart[1]
    
    output_tree.vbs_pts = [p.Pt() for p in vbspart]
    output_tree.vbs_etas = [p.Eta() for p in vbspart]
    output_tree.w_pts = [p.Pt() for p in wpart]
    output_tree.w_etas = [p.Eta() for p in wpart]
    output_tree.lep_pt = event.std_vector_leptonGen_pt[0]
    output_tree.lep_eta = event.std_vector_leptonGen_eta[0]
    output_tree.W_mass = W.M()
    output_tree.W_eta = W.Eta()
    output_tree.W_pt = W.Pt()
    output_tree.mjj_vbs = (vbspart[0] + vbspart[1]).M()
    output_tree.deltaeta_vbs = abs(vbspart[0].Eta() - vbspart[1].Eta())

    output_tree.fill()

    if nevents > 0 and iev>= nevents:
        break


output_tree.write()
output.Close()