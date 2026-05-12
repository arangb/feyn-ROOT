# LHC Higgs prod:
python3 ../simpleFeynman.py Hgg
mv -f Higgs.pdf Higgsprod_gg_fusion.pdf
python3 ../simpleFeynman.py s q "#bar{q}'" "V*" "V" "h"
mv -f sch-feyn.pdf Higgsprod_qq_Higgsstrahlung.pdf
python3 ../simpleFeynman.py VBF "q" "q'" "W/Z" "W/Z" "q" "q'" "h"
mv -f GenericVBF.pdf Higgsprod_VBF.pdf 
python3 ../simpleFeynman.py VBF g g "#bar{q}" "q" "q" "#bar{q}" "h"
mv -f GenericVBF.pdf Higgsprod_QQH.pdf
python3 ../simpleFeynman.py VBF g g "#bar{t}" "t" "t" "#bar{t}" "h"
mv -f GenericVBF.pdf Higgsprod_gg_ttH.pdf
python3 ../simpleFeynman.py VBF q "#bar{b}" "W" "W" "q'" "#bar{t}" "h"
mv -f GenericVBF.pdf Higgsprod_qb_tHq_VBF.pdf
#python3 ../simpleFeynman.py tD "q" "#bar{b}" "W" "q'" "#bar{t}" "" "" "h" "#bar{t}"
#mv -f tch-decay.pdf Higgsprod_qb_tHq_tchannel.pdf
python3 ../simpleFeynman.py BOX g g " " "h" "Z" " " " " "t"
mv -f box.pdf Higgsprod_HZ_box.pdf
# LHC ZZ/gaga background:
python3 ../simpleFeynman.py t q "#bar{q}" " " "#gamma" "#gamma"
mv -f tch-feyn.pdf LHC_qq_gaga.pdf
python3 ../simpleFeynman.py t q "#bar{q}" " " "Z" "Z"
mv -f tch-feyn.pdf LHC_qq_ZZ.pdf
python3 ../simpleFeynman.py t "#bar{q}" "q" "q'" "W^{#plus}" "W^{#minus}"
mv -f tch-feyn.pdf LHC_qq_WW.pdf
python3 ../simpleFeynman.py sD "q" "#bar{q}" "Z" "f" "#bar{f}" "" "" "Z" "#bar{f}"
mv -f sch-decay.pdf LHC_ZZ_resonant.pdf
# LHC gamma gamma + jet background (Bremstr)
python3 ../simpleFeynman.py tD "q" "g" "#bar{q}" "#gamma" "q" "" "" "#gamma" "q"
mv -f tch-decay.pdf LHC_qg_gagaj.pdf
# LHC gamma gamma Box background:
python3 ../simpleFeynman.py BOX g g " " "#gamma" "#gamma" " " " " "q"
mv -f box.pdf LHC_gaga_box.pdf
# LEP Higgs:
python3 ../simpleFeynman.py s "e^{#minus}" "e^{#plus}" "Z*" "Z" "h"
mv -f sch-feyn.pdf Higgsprod_LEP_Higgsstrahlung.pdf
python3 ../simpleFeynman.py VBF "e^{#minus}" "e^{#plus}" "W" "W" "e^{#minus}" "e^{#plus}" "h"
mv -f GenericVBF.pdf Higgsprod_LEP_VBF.pdf 
# LEP WW:
python3 ../simpleFeynman.py s "e^{#minus}" "e^{#plus}" "Z/#gamma*" "W^{#minus}" "W^{#plus}"
mv -f sch-feyn.pdf LEP_WWprod_schannel.pdf
# Here below you don't want an arrow on the t-channel neutrino, so uncomment line 78 in simpleFeynman:
python3 ../simpleFeynman.py t "e^{#plus}" "e^{#minus}" "#nu_{e}" "W^{#plus}" "W^{#minus}"
mv -f tch-feyn.pdf LEP_WWprod_tchannel.pdf
# LHC Z width # uncomment daughter decay in Hgg
python3 ../simpleFeynman.py Hgg Z Z
mv -f Higgs.pdf  Higgsprod_gg_fusion_ZZ.pdf
python3 ../simpleFeynman.py BOX g g " " "Z" "Z" " " " " "q"
mv -f box.pdf LHC_ZZ_box.pdf
python3 ../simpleFeynman.py s g g g t "#bar{t}" #need to activate the True statement to add the Higgs line in between
mv -f sch-feyn.pdf Feynman_tt_with_H_correction.pdf
# DiHiggs production:
python3 ../simpleFeynman.py BOX g g " " "h" "h" " " " " "t"
mv -f box.pdf LHC_DiHiggs_box.pdf
python3 ../simpleFeynman.py Hgg h h
mv -f Higgs.pdf LHC_DiHiggs_ggFusion.pdf
python3 ../simpleFeynman.py VBF q "q" "V" "V" "q'" "q'" "h" "h" "h"
mv -f GenericVBF.pdf LHC_DiHiggs_VBF.pdf
python3 ../simpleFeynman.py s "g" "g" "h" "h" "h"
mv -f sch-feyn.pdf LHC_DiHiggs_gg_BSMschannel.pdf
python3 ../simpleFeynman.py VBF "e^{#minus}" "e^{#plus}" "W" "W" "#nu" "#bar{#nu}" "h" "h" "h"
mv -f GenericVBF.pdf LC_DiHiggs_VBF.pdf
python3 ../simpleFeynman.py sD "e^{#minus}" "e^{#plus}" "Z*" "Z" "h" "" "" "h" "h"
mv -f sch-decay.pdf LC_DiHiggs_Hstrahlung.pdf
# Wbbar
python3 ../simpleFeynman.py tD  "q" "#bar{q}" " " "W" "g" "" "" "b" "#bar{b}"
mv -f tch-decay.pdf TEV_Wbb.pdf
python3 ../simpleFeynman.py s d "#bar{s}" "A^{0}" "s" "#bar{d}"
mv -f sch-feyn.pdf KKmixing_2HDM.pdf
# Weak decay of charged pions: 
python3 ../simpleFeynman.py s u "#bar{d}" "W^{#plus}" "#mu^{#plus}" "#nu_{#mu}"
mv -f sch-feyn.pdf Chargedpion_decay.pdf
# neutral current (angle=True):
python3 ../simpleFeynman.py t "#nu_{#mu}" "e^{#minus}" "Z^{0}" "#nu_{#mu}" "e^{#minus}"
mv -f tch-feyn.pdf NeutralCurrent_Gargamelle.pdf
