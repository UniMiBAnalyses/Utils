# Example

## Reweight deltaeta VBS for Wjets sample
 python -i reweight_variable.py --inputfile plots_2017v6s5.root \
                        --output reweight_wjets_deltaetavbs_mu.root \
                        --var deltaeta_vbs --cat res_wjetcr_mjjincl_mu     
                        --samples DY top VV VVV VBF-V Fake --sample-to-reweight Wjets  
                        --fit-func pol3 --fit-range 2 6.4


## Reweight Lepton_pt for Wjets sample

python -i reweight_variable.py --inputfile plots_2017v6s5.root \
                    --output reweight_wjets_leptonpt_mu.root \
                    --var Lepton_pt --cat res_wjetcr_mjjincl_mu \
                    --samples DY top VV VBF-V VVV Fake --sample-to-reweight Wjets \
                    --fit-func expo --fit-range 30 300
