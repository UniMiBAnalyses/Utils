import ROOT as rt
from ROOT import TLorentzVector
from math import cosh

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