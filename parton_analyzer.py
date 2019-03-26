import utils 
import ROOT as rt  
import sys  


file = rt.TFile(sys.argv[1])
tree = file.Get("latino")

nevents = 10
if len(sys.argv) > 2:
    nevents = int(sys.argv[2])




iev = 0

for event in tree:
    print "> event: ", iev
    ids = [int(pid) for pid in event.std_vector_partonGen_pid if pid!=-9999]
    print "partons PID: ",ids
    partons = utils.get_quadrimomenta(event.std_vector_partonGen_pt, 
                                      event.std_vector_partonGen_eta, 
                                      event.std_vector_partonGen_phi, debug=True)
    

    #invariant masses
    masses = mjj_pairs(partons)
    print masses

    iev+=1
    if iev> nevents:
        break