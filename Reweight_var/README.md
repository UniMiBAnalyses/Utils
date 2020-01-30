## Reproduce these weights

```
## configuration-dependent parameters
## samples = ggWW Vg top WW VVV DY VgS VZ
export NVTX_ROOTFILE_SOURCE=/afs/cern.ch/user/d/dmapelli/latino/CMSSW_10_2_0/src/PlotsConfigurations/Configurations/VBSjjlnu/ControlRegions/check_jets_horns/DY2018v5/rootFile/plots_DY2018v5.root
export NVTX_DATADIR=./reweight_data/

# Zmm weights
python reweight_ratiodatamc.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_Zmm.txt \
  --var nvtx --cat Zmm --samples ggWW Vg top WW VVV DY VgS VZ

python reweight_ratiofit.py \
  --input ${NVTX_DATADIR}reweight_ratiodatamc_Zmm.txt \
  --output ${NVTX_DATADIR}reweight_wrongnorm_Zmm.txt

python reweight_closure.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --input_weight ${NVTX_DATADIR}reweight_wrongnorm_Zmm.txt \
  --output_norm ${NVTX_DATADIR}reweight_constscale_Zmm.txt \
  --var nvtx --cat Zmm --samples ggWW Vg top WW VVV DY VgS VZ

python reweight_ratiofit.py \
  --input ${NVTX_DATADIR}reweight_ratiodatamc_Zmm.txt --constscale ${NVTX_DATADIR}reweight_constscale_Zmm.txt \
  --output ${NVTX_DATADIR}reweight_wrongnorm_Zmm.txt --output_scaled ${NVTX_DATADIR}reweight_goodnorm_Zmm.txt

python reweight_closure.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --input_weight ${NVTX_DATADIR}reweight_wrongnorm_Zmm.txt --input_weight_scaled ${NVTX_DATADIR}reweight_goodnorm_Zmm.txt \
  --var nvtx --cat Zmm --samples ggWW Vg top WW VVV DY VgS VZ

# Zee
python reweight_ratiodatamc.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_Zee.txt \
  --var nvtx --cat Zee --samples ggWW Vg top WW VVV DY VgS VZ

python reweight_ratiofit.py \
  --input ${NVTX_DATADIR}reweight_ratiodatamc_Zee.txt \
  --output ${NVTX_DATADIR}reweight_wrongnorm_Zee.txt

python reweight_closure.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --input_weight ${NVTX_DATADIR}reweight_wrongnorm_Zee.txt \
  --output_norm ${NVTX_DATADIR}reweight_constscale_Zee.txt \
  --var nvtx --cat Zee --samples ggWW Vg top WW VVV DY VgS VZ

# Zee closure Zmm
python reweight_closure.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --input_weight ${NVTX_DATADIR}reweight_wrongnorm_Zmm.txt \
  --output_norm ${NVTX_DATADIR}reweight_constscale_Zmm.txt \
  --var nvtx --cat Zee --samples ggWW Vg top WW VVV DY VgS VZ

# some checks
python -i reweight_checkcats.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --var nvtx --samples ggWW Vg top WW VVV DY VgS VZ

python -i reweight_checkfit.py \
  --input_ele ${NVTX_DATADIR}reweight_ratiodatamc_Zee.txt --input_mu ${NVTX_DATADIR}reweight_ratiodatamc_Zmm.txt
```


------------------------------
# Reweight only one sample against the data - others MC

samples = DY top Wjets VVV VV VBF-V Fake 
export NVTX_ROOTFILE_SOURCE=/eos/user/d/dvalsecc/www/VBSPlots/FullRun2/full2017_dnnoutput_200129_v1/configuration/rootFile/plots_2017v6s5.root
export NVTX_DATADIR=./reweight_data/

# Zmm weights
python reweight_ratiodatamc_onesample.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_mu.txt \
  --var deltaeta_vbs --cat lowen_CR_looseVBS_mu --samples DY top VVV VV VBF-V Fake --sample-to-reweight Wjets

  python reweight_ratiodatamc_onesample.py \
  --file ${NVTX_ROOTFILE_SOURCE} \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_ele.txt \
  --var deltaeta_vbs --cat lowen_CR_looseVBS_ele --samples DY top VVV VV VBF-V Fake --sample-to-reweight Wjets


python reweight_ratiofit.py \
  --input ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_ele.txt \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_ele_fit.txt

python -i reweight_closure_onesample.py  --file ${NVTX_ROOTFILE_SOURCE} \
  --input-weight reweight_data/reweight_ratiodatamc_wjets_deltaetavbs_ele_fit.txt \
  --output-norm reweight_data/corr_factor_deltavbs_ele.txt \
  --var deltaeta_vbs --samples DY top VVV VV VBF-V Fake \
  --sample-to-reweight Wjets --cat lowen_CR_wjets_ele

python reweight_ratiofit.py \
--input ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_ele.txt \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_ele_fit.txt \
  --constscale ${NVTX_DATADIR}corr_factor_deltavbs_ele.txt \
> --output_scaled ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_ele_fit_scaled.txt


python -i reweight_closure_onesample.py  --file ${NVTX_ROOTFILE_SOURCE} \
  --input-weight reweight_data/reweight_ratiodatamc_wjets_deltaetavbs_ele_fit.txt \
  --output-norm reweight_data/corr_factor_deltavbs_ele.txt\
  --var deltaeta_vbs --samples DY top VVV VV VBF-V Fake \
  --sample-to-reweight Wjets --cat lowen_CR_wjets_ele\
  --input-weight-scaled reweight_data/reweight_ratiodatamc_wjets_deltaetavbs_ele_fit_scaled.txt

#### muon 

python reweight_ratiofit.py \
  --input ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_mu.txt \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_mu_fit.txt

python -i reweight_closure_onesample.py  --file ${NVTX_ROOTFILE_SOURCE} --input-weight reweight_data/reweight_ratiodatamc_wjets_deltaetavbs_mu_fit.txt --output-norm reweight_data/corr_factor_deltavbs_mu.txt --var deltaeta_vbs --samples DY top VVV VV VBF-V Fake --sample-to-reweight Wjets

python reweight_ratiofit.py \
--input ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_mu.txt \
  --output ${NVTX_DATADIR}reweight_ratiodatamc_wjets_deltaetavbs_mu_fit.txt
  --constscale ${NVTX_DATADIR}corr_factor_deltavbs_mu.txt

