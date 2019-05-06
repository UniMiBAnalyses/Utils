module_name =    ''' 
       _        _    _____              _         _     __      __ ____    _____ 
      | |      | |  |  __ \            (_)       (_)    \ \    / /|  _ \  / ____|
      | |  ___ | |_ | |__) |__ _  _ __  _   __ _  _  _ __\ \  / / | |_) || (___  
  _   | | / _ \| __||  ___// _` || '__|| | / _` || || '_ \\ \/ /  |  _ <  \___ \ 
 | |__| ||  __/| |_ | |   | (_| || |   | || (_| || || | | |\  /   | |_) | ____) |
  \____/  \___| \__||_|    \__,_||_|   |_| \__, ||_||_| |_| \/    |____/ |_____/ 
                                            __/ |                                
                                           |___/                                  
'''

#
# This module extracts the pairs of b-jets and W-jets looking at parton
# level and geometrically matching with reco jets. 
# 

import optparse
import numpy
import ROOT
import os.path
from LatinoAnalysis.Gardener.gardening import TreeCloner
import LatinoAnalysis.Gardener.variables.PairingUtils as utils 


#Functions to put in PairingUtils
def get_bjets(event, ptmin, debug):
    jets = []
    l = []
    
    maxbtag1 = max(event.std_vector_jet_DeepCSVB)
    maxbtag2 = -9999.
    b_jet1 = 0
    b_jet2 = 0

    index = 0
    for pt, eta, phi,mass, bvalue in  zip(event.std_vector_jet_pt, 
                     event.std_vector_jet_eta, event.std_vector_jet_phi, 
                     event.std_vector_jet_mass, event.std_vector_jet_DeepCSVB):

       if pt < 0 or pt < ptmin:
            break
        if abs(eta) < 10 :
            p = pt * cosh(eta)
            vec = TLorentzVector()
            en = sqrt(p**2 + mass**2)

            vec.SetPtEtaPhiE(pt, eta, phi, en)
            
            if bvalue == maxbtag1:
                b_jet1 = index
            elif bvalue > maxbtag2:
                maxbtag2 = bvalue
                b_jet2 = index

            jets.append(vec)

        index+=1


    l = [b_jet1, b_jet2]
    l.sort()
    return jets, l


def nearest_mass_pair_notH(vectors, mass, hpair):
    ''' Returns the pair of vectors with invariant mass nearest to 
    the given mass, checking if it isn't the bb pair '''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(([i,k], abs(mass - (vectors[i]+ vectors[k]).M() )))  
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]

def max_pt_pair_notH(vectors, hpair):
    ''' Returns the pair with highest Pt, , checking that it isn't the bb pair'''
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append(( [i,k], (vectors[i]+ vectors[k]).Pt() ))
    l = sorted(l, key=itemgetter(1), reverse=True)
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]

def min_deltaeta_pairs_notH(vectors, hpair):
    l = []
    for i ,k  in combinations(range(len(vectors)),2):
        l.append( ([i,k], abs(vectors[i].Eta()- vectors[k].Eta()) ) )
    l = sorted(l, key=itemgetter(1))
    for i in range(len(l)):
        if (l[i][0][0] != hpair[0] and l[i][0][0] != hpair[1]):
            if (l[i][0][1] != hpair[0] and l[i][0][1] != hpair[1]):
                return l[i][0]



class JetPairingHH(TreeCloner):

    def __init__(self):
        pass

    def __del__(self):
        pass

    def help(self):
        return '''Identify pairs of jets for semileptonic analyses'''

    def addOptions(self,parser):
        description = self.help()
        group.add_option('-d', '--debug',  dest='debug',  help='Debug flag',  default="0")
        group.add_option('--ptminjet',  dest='ptmin_jet',  help='Min Pt for jets',  default=20.)
        group.add_option('-m', '--mode',  dest='mode',  help='Pairing mode, 0=nearest W mas, 1=max_pt, 2=mindeltaeta',  default="0")
        group.add_option('-b', '--bWP1',  dest='bWP',  help='btagging WP: L,M,T',  default="L")
        group.add_option('-b', '--bWP2',  dest='bWP',  help='btagging WP: L,M,T',  default="L")
        parser.add_option_group(group)
        return group


    def checkOptions(self,opts):
        self.debug = (opts.debug == "1")

    def process(self,**kwargs):
        print module_name

        tree  = kwargs['tree']
        input = kwargs['input']
        output = kwargs['output']

        self.connect(tree,input)

        newbranches = ["H_jets", "W_jets"]

        self.clone(output,newbranches)
        H_jets    =   numpy.zeros(2, dtype=numpy.int32)
        W_jets  =   numpy.zeros(2, dtype=numpy.int32)
        self.otree.Branch('H_jets',         H_jets,         'H_jets[2]/I')
        self.otree.Branch('W_jets',         W_jets,         'W_jets[2]/I')

        nentries = self.itree.GetEntries()
        print 'Total number of entries: ',nentries 

        # avoid dots to go faster
        itree     = self.itree
        otree     = self.otree

        print '- Starting eventloop'
        step = 5000
        for i in xrange(nentries):
            itree.GetEntry(i)
            if i > 0 and i%step == 0.:
                print i,'events processed :: ', nentries

            hpair = [-1,-1]
            wpair = [-1,-1]
            jets, b_scores = utils.get_jets_and_bscore(itree, self.ptmin_jet, self.debug)

            bjets = [(i, bscore) for i, bscore in enumerate(b_scores)
                    if bscore >= bTaggingWPs['deepCSV'][self.bWP]]

            print bjets

            if len(bjets) >= 2:
                # Take the indexes of the two jets with bigger bscore
                hpair = [j[0] for j in list(sorted(bjets, key=itemgetter(1), reverse=True))[:2]]
                
                if len(jets) >=4:
                    if self.mode == 0:
                        wpair = utils.nearest_mass_pair_notH(jets, 80.385, hpair)
                    elif self.mode == 1:
                        wpair = utils.max_pt_pair_notH(jets, hpair)   
                    elif self.mode == 2:
                        wpair = utils.min_deltaeta_pairs_notH(jets, hpair)

            H_jets[0], H_jets[1] = hpair 
            W_jets[0], W_jets[1] = wpair
                
            otree.Fill()
  
        self.disconnect()
        print '- Eventloop completed'
