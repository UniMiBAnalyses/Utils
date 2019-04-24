import ROOT as rt
from ROOT import TLorentzVector
from math import cosh, sqrt
from itertools import combinations
from operator import itemgetter

def get_quadrimomenta(pts, etas, phis, nvec, debug=False):
    vectors = []
    for i in range(nvec):
        pt, eta, phi = pts[i], etas[i], phis[i]
        if debug:
            print ("pt:", pt ," eta:", eta, " phi:", phi)
        if abs(eta)>10:
            continue
        else:
            p = pt * cosh(eta)
        #assume m =0, p = E
        v = TLorentzVector()
        v.SetPtEtaPhiE(pt, eta, phi, p)
        vectors.append(v)
    return vectors


def get_quadrimomentum(pt, eta, phi):
        p = pt * cosh(eta)
        v = TLorentzVector()
        v.SetPtEtaPhiE(pt, eta, phi, p)
        return v

def get_hard_partons(event, ptmin=20., debug=False):
    partons = []
    pids = []
    for i, (pt, eta, phi, pid, isHard) in enumerate(
            zip(event.std_vector_partonGen_pt, event.std_vector_partonGen_eta,
                event.std_vector_partonGen_phi, event.std_vector_partonGen_pid,
                event.std_vector_partonGen_isHardProcess)):
        if pt < ptmin or pt < 0:
            break
        if isHard==1 and abs(eta) < 10:
            vec = get_quadrimomentum(pt, eta, phi)
            # check if different from the previous one
            if len(partons)==0 or vec != partons[-1]:
                if debug:
                    print ("Parton > pid: ", pid, " pt:", pt ," eta:", eta, " phi:", phi)
                partons.append(vec)
                pids.append(int(pid))
    return partons, pids

def get_jets(event, ptmin=20., debug=False):
    jets = []
    for pt, eta, phi,mass in  zip(event.std_vector_jet_pt, 
                     event.std_vector_jet_eta, event.std_vector_jet_phi, 
                     event.std_vector_jet_mass):
        if pt < 0 or pt < ptmin:
            break
        if abs(eta) < 10 :
            p = pt * cosh(eta)
            vec = TLorentzVector()
            en = sqrt(p**2 + mass**2)
            vec.SetPtEtaPhiE(pt, eta, phi, en)
            # check if different from the previous one
            if debug:
                print "Jet > pt:", pt ," eta:", eta, " phi:", phi, " mass:", mass
            jets.append(vec)
    return jets
        

def associate_vectors(jets, partons, dist):
    ''' The params influences the flag of the event:
    0 = OK
    1 = Overlapping partons
    2 = At least one parton not associated 
    '''
    flag = 0
    ntotjets = len(jets)
    ntotpartons = len(partons)
    comb = []
    for nj, j in enumerate(jets):
        for njr, jr in enumerate(partons):
            comb.append( (nj, njr, j.DrEtaPhi(jr)))
    comb = sorted(comb, key=itemgetter(2))
    results = [[-1]*ntotpartons,[0.]*ntotpartons]
    assigned_part = 0
    for nj, njr, distance  in comb:        
        # the jet can be reused if the parton
        # is nearer than the max_distance
        if results[0][njr] == -1 and distance <= dist:
                if nj in results[0]:
                    # the jet is already associated with a parton
                    # This is an overlapping parton
                    flag = 1
                results[0][njr] = nj
                results[1][njr] = distance 
                assigned_part+=1
        if assigned_part == ntotpartons:
            break  #early exit when partons are all assigned
    # Check if at least one parton is not associated
    if -1 in results[0]:
        flag = 2
    return results, flag



def mjj_pairs(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], (vectors[i]+ vectors[k]).M() ))
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l

def deltaeta_pairs(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], abs(vectors[i].Eta()- vectors[k].Eta()) ) )
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l

def deltaR_pairs(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], vectors[i].DeltaR(vectors[k])) )
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l

def max_deltaeta_pair(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], abs(vectors[i].Eta() - vectors[k].Eta())))
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l[0][0]

def max_mjj_pair(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], (vectors[i]+ vectors[k]).M() ))
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l[0][0]

def max_pt_pair(vectors):
    ''' Returns the pair with highest Pt'''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(( [i,k], (vectors[i]+ vectors[k]).Pt() ))
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l[0][0]

def nearest_mass_pair(vectors, mass):
    ''' Returns the pair of vectors with invariant mass nearest to 
    the given mass '''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(([i,k], abs(mass - (vectors[i]+ vectors[k]).M() )))  
    l = sorted(l, key=itemgetter(1))
    return l[0][0]

def nearest_masses_pair(vectors, masses):
    ''' Returns the pair of vectors with invariant mass nearest to one of the 
    masses in the parameter'''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        distances= [abs(mass - (vectors[i]+ vectors[k]).M() ) for mass in masses]
        l.append(([i,k], min(distances)))  
    l = sorted(l, key=itemgetter(1))
    return l[0][0]

def mass_of_nearest_mass_pair(vectors, mass):
    ''' Returns mass of the pair of vectors with invariant mass nearest to 
    the given mass'''
    l = []
    pair_mass = 0
    for i ,k  in combinations(range(len(vectors)),2):
        pair_mass = (vectors[i]+ vectors[k]).M()
        l.append(([i,k], abs(mass - pair_mass ), pair_mass))  
    l = sorted(l, key=itemgetter(1))
    return l[0][2]

def nearest_R_pair(vectors):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(([i,k], vectors[i].DeltaR(vectors[k]) ))  
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l[0][0]
    
def get_nearest_vector(target, vectors):
    ''' Return the nearest vector from target in the vectors list'''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(([i,k], vectors[i].DeltaR(target) ))  
    l = sorted(l, key=itemgetter(1), reverse=True)
    return l[0][0][0]