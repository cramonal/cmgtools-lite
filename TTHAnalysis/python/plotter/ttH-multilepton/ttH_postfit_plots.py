#!/usr/bin/env python
import sys
import re
import os

ODIR=sys.argv[1]
YEAR=sys.argv[2]
lumis = {
    '2016': '36.33',
    '2017': '41.5',
    '2018': '59.8',
    'all' : '36.33,41.5,59.8',
}


submit = '{command}' 
dowhat = "plots" 
YEARDIR=YEAR if YEAR != 'all' else ''
P0     = "/pool/ciencias/HeppyTrees/EdgeZ/TTH/"
nCores = 4
TREESALL ="--xf THQ_LHE,THW_LHE,TTTW,TTWH --FMCs {P}/0_jmeUnc_v1 --Fs {P}/1_recl_allvars --FMCs {P}/2_btag_SFs --FMCs {P}/2_scalefactors_lep_fixed --Fs {P}/3_tauCount --Fs {P}/4_evtVars --Fs {P}/5_BDThtt_reco_new_blah --Fs {P}/6_mva2lss --Fs {P}/6_mva3l --Fs {P}/6_mva_2lss1tau_new --FMCs {P}/6_mva_tauSFs --Fs {P}/6_mva4l --Fs {P}/7_mvaCP_2lss --Fs {P}/7_mvaCP_2lss1tau --Fs {P}/7_mvaCP_3l"
TREESONLYSKIM     = "-P "+P0+"/NanoTrees_TTH_090120_091019_v6_skim2lss_forCP/%s "%(YEARDIR,)

def base(selection):
    THETREES = TREESALL
    CORE=' '.join([THETREES,TREESONLYSKIM])
    CORE+=" -f -j %d -l %s -L ttH-multilepton/functionsTTH.cc --tree NanoAOD --mcc ttH-multilepton/lepchoice-ttH-FO.txt --split-factor=-1 --WA prescaleFromSkim --year %s  --mcc ttH-multilepton/mcc-METFixEE2017.txt"%(nCores, lumis[YEAR],YEAR if YEAR!='all' else '2016,2017,2018')# --neg" --s2v 
    RATIO= " --maxRatioRange 0.0  1.99 --ratioYNDiv 505 "
    RATIO2=" --showRatio --attachRatioPanel --fixRatioRange "
    LEGEND=" --legendColumns 3 --legendWidth 0.65 "
    LEGEND2=" --legendFontSize 0.027 "
    SPAM=" --noCms --topSpamSize 1.1 --lspam '#scale[1.1]{#bf{CMS}} #scale[0.9]{#it{Preliminary}}' "
    if dowhat == "plots": CORE+=RATIO+RATIO2+LEGEND+LEGEND2+SPAM+"  --showMCError --rebin 4 "

    if selection=='2lss':
        GO="%s ttH-multilepton/mca-2lss-mcdata-frdata-combineplot.txt ttH-multilepton/2lss_tight_legacy.txt"%CORE
        GO="%s -W 'L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_2lss*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 2, year)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt "
        GO += " --binname 2lss "
        GO += "--printBF '#bf{Best Fit:  #kappa_{t} = 0.9, #tilde #kappa_{t}= 1.0}' --noStatTotLegendOnRatio "
        GO += "--unc ttH-multilepton/systsUnc.txt  --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU "
        GO += "--plotgroup data_fakes+=.*_promptsub--neglist .*_promptsub.* "
    elif selection=='2lss1tau':
        GO="%s ttH-multilepton/mca-2lss-mcdata-frdata-combineplot.txt ttH-multilepton/2lss_tight_legacy.txt"%CORE
        GO="%s -W 'L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_3l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|4)lep_.*' --xP '^lep4_.*' --xP 'kinMVA_2lss_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.65 ")
        GO += " --binname 2lss1tau "
        GO += "--printBF '#bf{Best Fit:  #kappa_{t} = 0.9, #tilde #kappa_{t}= 1.0}' --noStatTotLegendOnRatio "
        GO += "--unc ttH-multilepton/systsUnc.txt  --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU "
        GO += "--plotgroup data_fakes+=.*_promptsub--neglist .*_promptsub.* "
    elif selection=='3l':
        GO="%s ttH-multilepton/mca-3l-mcdata-frdata-combineplot.txt ttH-multilepton/3l_tight_legacy.txt "%CORE
        GO="%s -W 'L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_3l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|4)lep_.*' --xP '^lep4_.*' --xP 'kinMVA_2lss_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.65 ")
        GO += " --binname 3l "
        GO += "--printBF '#bf{Best Fit:  #kappa_{t} = 0.9, #tilde #kappa_{t}= 1.0}' --noStatTotLegendOnRatio "
        GO += "--unc ttH-multilepton/systsUnc.txt  --xu CMS_ttHl_TTZ_lnU,CMS_ttHl_TTW_lnU "
        GO += "--plotgroup data_fakes+=.*_promptsub--neglist .*_promptsub.* "

    elif selection=='4l':
        GO="%s ttH-multilepton/mca-4l-mcdata-frdata-CP_new.txt ttH-multilepton/4l_tight.txt "%CORE
        GO="%s -W 'L1PreFiringWeight_Nom*puWeight*btagSF_shape*leptonSF_4l*triggerSF_ttH(LepGood1_pdgId, LepGood1_conePt, LepGood2_pdgId, LepGood2_conePt, 3, year)'"%GO
        if dowhat in ["plots","ntuple"]: GO+=" ttH-multilepton/2lss_3l_plots.txt --xP '^(2|3)lep_.*' --xP '^lep(1|2|3|4)_.*' --xP 'kinMVA_.*' "
        if dowhat == "plots": GO=GO.replace(LEGEND, " --legendColumns 3 --legendWidth 0.65 ")
        GO += " --binname 4l "
    else:
        raise RuntimeError, 'Unknown selection'

    if '_prescale' in torun:
        GO = doprescale3l(GO,torun)

    return GO
def add(GO,opt):
    return '%s %s'%(GO,opt)

def runIt(GO,name,plots=[],noplots=[]):
    if dowhat == "plots":  
        submit = 'sbatch -c %d -p batch --wrap "{command}"'%nCores
        print(submit.format(command=' '.join(['python mcPlots.py',"--pdir %s/%s/%s"%(ODIR,YEAR,name),GO,' '.join(['--sP %r'%p for p in plots]),' '.join(['--xP %r'%p for p in noplots]),' '.join(sys.argv[4:])])))
        

if __name__ == '__main__':

    torun = sys.argv[3]
    print(torun)
    if '2lss_0tau' in torun:
        x = base('2lss')
        if 'ttH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_ttHnewnode --vertLines  ttH-multilepton/lines_2lss_ttH.py  --externalPostfitPlot cards/7ene_filtering/prefit_plots2lss_0tau_ee_em_mm_ttH_fixedbin.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_ttHnewnode --vertLines  ttH-multilepton/lines_2lss_ttH.py  --externalPostfitPlot cards/7ene_filtering/postfit_plots2lss_0tau_ee_em_mm_ttH_fixedbin.root")
        elif 'ttW' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_ttWnode --vertLines ttH-multilepton/lines_2lss_ttW.py   --externalPostfitPlot cards/7ene_filtering/prefit_2lss0tau_ttW.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_ttWnode --vertLines ttH-multilepton/lines_2lss_ttW.py   --externalPostfitPlot cards/7ene_filtering/postfit_2lss0tau_ttW.root")

        elif 'rest' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_Restnode --vertLines ttH-multilepton/lines_2lss_rest.py  --externalPostfitPlot cards/7ene_filtering/prefit_2lss0tau_Rest.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_Restnode --vertLines ttH-multilepton/lines_2lss_rest.py  --externalPostfitPlot cards/7ene_filtering/postfit_2lss0tau_Rest.root")
        elif 'tH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_tHnode --vertLines ttH-multilepton/lines_2lss_tH.py  --externalPostfitPlot cards/7ene_filtering/prefit_2lss0tau_tH.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_MVA_CP_tHnode --vertLines ttH-multilepton/lines_2lss_tH.py  --externalPostfitPlot cards/7ene_filtering/postfit_2lss0tau_tH.root")
        elif 'CPMVA' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  CP_2lss_0tau  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots2lss_0tau_CPMVA.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP  CP_2lss_0tau  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots2lss_0tau_CPMVA.root") 

        else:
           raise RuntimeError, 'Unknown node'
        runIt(x,'%s'%torun)
    if '2lss_1tau' in torun:
        x = base('2lss1tau')
        if 'ttH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss1tau_MVA_CP_nodettH --vertLines  ttH-multilepton/lines_2lss1tau_ttH.py  --externalPostfitPlot cards/7ene_filtering/prefit_plots2lss_1tau_ttH_fixedbin.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss1tau_MVA_CP_nodettH --vertLines  ttH-multilepton/lines_2lss1tau_ttH.py --externalPostfitPlot cards/7ene_filtering/postfit_plots2lss_1tau_ttH_fixedbin.root")
        elif 'rest' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss1tau_MVA_CP_nodeRest   --externalPostfitPlot cards/7ene_filtering/prefit_plots2lss1tau_rest_fixedbin.root ")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss1tau_MVA_CP_nodeRest   --externalPostfitPlot cards/7ene_filtering/postfit_plots2lss1tau_rest_fixedbin.root ")
        elif 'tH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_2lss1tau_MVA_CP_nodetH --vertLines ttH-multilepton/lines_2lss_tH.py  --externalPostfitPlot cards/7ene_filtering/prefit_plots2lss1tau_tH_fixedbin.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss1tau_MVA_CP_nodetH --vertLines ttH-multilepton/lines_2lss_tH.py  --externalPostfitPlot cards/7ene_filtering/postfit_plots2lss1tau_tH_fixedbin.root")
        elif 'CPMVA' in  torun:
            print('hy')
            if "prefit" in ODIR:
                x = add(x,"--sP  CP_2lss_1tau  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots2lss_1tau_CPMVA.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP  CP_2lss_1tau  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots2lss_1tau_CPMVA.root") 
        else:
           raise RuntimeError, 'Unknown node'
        runIt(x,'%s'%torun)
    if '3j' in torun:
        x = base('2lss')
        if 'dEtaBB' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_2lss_input_dEtaBB_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots3jCR_dEtaBB.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_input_dEtaBB_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots3jCR_dEtaBB.root")
        elif 'dRlep12' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_2lss_dRlep12  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots3jCR_drlep12.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_dRlep12  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots3jCR_drlep12.root")
        elif 'mTTH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_2lss_input_mTTH_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots3jCR_mTTH.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_input_mTTH_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots3jCR_mTTH.root")
        elif 'mindr_lep2jet' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_2lss_input_mindr_lep2_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots3jCR_mindr_lep2_jet.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_input_mindr_lep2_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots3jCR_mindr_lep2_jet.root")
        elif 'mindr_lep1jet' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_2lss_input_mindr_lep1_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots3jCR_mindr_lep1_jet.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_2lss_input_mindr_lep1_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots3jCR_mindr_lep1_jet.root")
        else:
           raise RuntimeError, 'Unknown node'
        runIt(x,'%s'%torun)
    if 'cr_3l' in torun:
        x = base('3l')
        if "prefit" in ODIR:
            x = add(x,"--sP cr_3l --vertLines  ttH-multilepton/lines_cr_3l.py --externalPostfitPlot cards/7ene_filtering/prefit_plotscr_3l_fixedbin.root")
        elif "postfit" in ODIR:
            x = add(x,"--sP cr_3l --vertLines  ttH-multilepton/lines_cr_3l.py --externalPostfitPlot cards/7ene_filtering/postfit_plotscr_3l_fixedbin.root")
        runIt(x,'%s'%torun)
    if 'cr_4l' in torun:
        x = base('4l')
        if "prefit" in ODIR:
           x = add(x,"--sP cr_4l  --externalPostfitPlot  cards/7ene_filtering/postfit_plotscr_4l_fixedbin.root")
        if "postfit" in ODIR:
           x = add(x,"--sP cr_4l  --externalPostfitPlot  cards/7ene_filtering/postfit_plotscr_4l_fixedbin.root")
        runIt(x,'%s'%torun)
    if '3l' in torun and not "cr" in torun:
        x = base('3l')
        if 'ttH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_3l_catBinIndex_MVA_CP_nodettH --vertLines  ttH-multilepton/lines_3l_ttH.py  --externalPostfitPlot cards/7ene_filtering/prefit_3l0tau_3l_ttH.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_catBinIndex_MVA_CP_nodettH --vertLines  ttH-multilepton/lines_3l_ttH.py --externalPostfitPlot cards/7ene_filtering/postfit_3l0tau_3l_ttH.root")
        elif 'rest' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_3l_catBinIndex_MVA_CP_nodeRest --vertLines ttH-multilepton/lines_3l_rest.py  --externalPostfitPlot cards/7ene_filtering/prefit_3l0tau_3l_Rest.root ")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_catBinIndex_MVA_CP_nodeRest  --vertLines ttH-multilepton/lines_3l_rest.py --externalPostfitPlot cards/7ene_filtering/postfit_3l0tau_3l_Rest.root ")
        elif 'tH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP kinMVA_3l_catBinIndex_MVA_CP_nodetH --vertLines ttH-multilepton/lines_3l_tH.py  --externalPostfitPlot cards/7ene_filtering/prefit_3l0tau_3l_tH.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_catBinIndex_MVA_CP_nodetH --vertLines ttH-multilepton/lines_3l_tH.py  --externalPostfitPlot cards/7ene_filtering/postfit_3l0tau_3l_tH.root")
        elif 'CPMVA' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  CP_3l  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plots3l_0tau_CPMVA.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP  CP_3l  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plots3l_0tau_CPMVA.root") 
        else:
           raise RuntimeError, 'Unknown node'
        runIt(x,'%s'%torun)
    if 'wz' in torun:
        x = base('3l')
        if 'dEtaBB' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_dEtaBB_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotswzcr_dEtaBB_2lss.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_dEtaBB_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotswzcr_dEtaBB_2lss.root")
        elif 'dRlep12' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_dRlep12  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotswzcr_dRlep12.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_dRlep12  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotswzcr_dRlep12.root")
        elif 'mTTH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_mTTH_3l  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotswzcr_mTTH_3l.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_mTTH_3l  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotswzcr_mTTH_3l.root")
        elif 'mindr_lep1jet' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_mindr_lep1_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotswzcr_mindr_lep1_jet.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_mindr_lep1_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotswzcr_mindr_lep1_jet.root")
        elif 'mindr_lep2jet' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_mindr_lep2_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotswzcr_mindr_lep2_jet.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_mindr_lep2_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotswzcr_mindr_lep2_jet.root") 
         
        else:
           raise RuntimeError, 'Unknown node'
        runIt(x,'%s'%torun) 
    if 'ttz' in torun:
        x = base('3l')
        if 'dEtaBB' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_dEtaBB_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotsttzcr_dEtaBB.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_dEtaBB_2lss  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotsttzcr_dEtaBB.root")
        elif 'dRlep12' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_dRlep12  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotsttzcr_dRlep12.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_dRlep12  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotsttzcr_dRlep12.root")
        elif 'mTTH' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_mTTH_3l  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotsttzcr_mTTH_3l.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_mTTH_3l  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotsttzcr_mTTH_3l.root")
        elif 'mindr_lep1jet' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_mindr_lep1_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotsttzcr_mindr_lep1_jet.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_mindr_lep1_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotsttzcr_mindr_lep1_jet.root")
        elif 'mindr_lep2jet' in  torun:
            if "prefit" in ODIR:
                x = add(x,"--sP  kinMVA_3l_input_mindr_lep2_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/prefit_plotsttzcr_mindr_lep2_jet.root")
            elif "postfit" in ODIR:
                x = add(x,"--sP kinMVA_3l_input_mindr_lep2_jet  --externalPostfitPlot cards/7ene_filtering/extended_plots/postfit_plotsttzcr_mindr_lep2_jet.root")

        else:
           raise RuntimeError, 'Unknown node'
        runIt(x,'%s'%torun)
