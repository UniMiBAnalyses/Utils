import ROOT as rt
from ROOT import TLorentzVector
from math import cosh
from itertools import combinations
from operator import itemgetter

def get_quadrimomenta(pts, etas, phis, debug=False):
    vectors = []
    for pt,eta,phi in zip(pts, etas, phis):
        if debug:
            print "pt:", pt ," eta:", eta, " phi:", phi
        if pt <= 0.:
            #reached end of event
            return vectors
        p = pt * cosh(eta)
        #assume m =0, p = E
        v = TLorentzVector()
        v.SetPtEtaPhiE(pt, eta, phi, p)
        vectors.append(v)
    return vectors


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