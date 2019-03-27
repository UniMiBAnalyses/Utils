import ROOT as rt
from ROOT import TLorentzVector
from math import cosh
from itertools import combinations
from operator import itemgetter

def get_quadrimomenta(pts, etas, phis, nvec, debug=False):
    vectors = []
    for i in range(nvec):
        pt, eta, phi = pts[i], etas[i], phis[i]
        if debug:
            print "pt:", pt ," eta:", eta, " phi:", phi
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

def get_hard_partons(event, debug=False):
    partons = []
    pids = []
    for i, (pt, eta, phi, pid, isHard) in enumerate(
            zip(event.std_vector_partonGen_pt, event.std_vector_partonGen_eta,
                event.std_vector_partonGen_phi, event.std_vector_partonGen_pid,
                event.std_vector_partonGen_isHardProcess)):
        if isHard==1 and abs(eta) < 10 :
            vec = get_quadrimomentum(pt, eta, phi)
            # check if different from the previous one
            if len(partons)==0 or vec != partons[-1]:
                if debug:
                    print "pid: ", pid, " pt:", pt ," eta:", eta, " phi:", phi
                partons.append(vec)
                pids.append(int(pid))
    return partons, pids


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
    return l[0][1]

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