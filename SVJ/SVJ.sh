# Basic diagrams for Semi-Visible Jets at the LHC
python3 ../simpleFeynman.py s q "#bar{q}" "Z'" "#chi" "#bar{#chi}"
mv -f sch-feyn.pdf SVJ_qq_Zp_schannel.pdf
python3 ../simpleFeynman.py tD q "#bar{q}" "-" "g" "Z'" "--" "--" "#chi" "#bar{#chi}"
mv -f tch-decay.pdf SVJ_qq_Zpg_tchannel.pdf
#python3 ../simpleFeynman.py s g g "#Phi" "#chi" "#chi"
#mv -f sch-feyn.pdf SVJ_gg_PhiPhi_schannel.pdf # Direct prod sch (can this happen with a Phi decaying to two Chis?)
python3 ../simpleFeynman.py t g g "#Phi" "#chi" "#chi"
mv -f tch-feyn.pdf SVJ_gg_ChiChi_tchannel.pdf  # Direct prod gg tch
python3 ../simpleFeynman.py t q "#bar{q}" "#Phi" "#chi" "#bar{#chi}"
mv -f tch-feyn.pdf SVJ_qq_ChiChi_tchannel.pdf # Direct prod qq tch
python3 ../simpleFeynman.py t "#bar{q}" "q" "#chi" "#Phi" "#Phi"
mv -f tch-feyn.pdf SVJ_qq_PhiPhi_tchannel.pdf # Pair production tch qq
# Here below you don't want an arrow on the t-channel #chi, so uncomment line 78 in simpleFeynman:
python3 ../simpleFeynman.py tD g g "#chi" "#Phi" "#Phi" "q" "#bar{#chi}" "#bar{q}" "#chi"
mv -f tch-decay.pdf SVJ_gg_PhiPhi_tchannel_Decay.pdf # Pair production tch decay
python3 ../simpleFeynman.py sD g g g "#Phi" "#Phi" q "#bar{#chi}" "#bar{q}" "#chi"
mv -f sch-decay.pdf SVJ_gg_PhiPhi_schannel_Decay.pdf # Pair production sch gg
python3 ../simpleFeynman.py tD q g "#Phi" "#chi" "#Phi" "--" "--" "q" "#bar{#chi}"
mv -f tch-decay.pdf SVJ_qg_PhiChi_tchannel_Decay.pdf # Associated production tch decay
python3 ../simpleFeynman.py s q g "q" "#Phi" "#chi"
mv -f sch-feyn.pdf SVJ_qg_PhiChi_schannel.pdf # Associated production sch
python3 ../simpleFeynman.py sD q g "q" "#chi" "#Phi" "--" "--" q "#bar{#chi}"
mv -f sch-decay.pdf SVJ_qg_PhiChi_schannel_Decay.pdf # Associated production sch decay
python3 ../simpleFeynman.py VBF "#bar{q}" q "#Phi" "#Phi" "#bar{#chi}" "#chi" g
mv -f GenericVBF.pdf SVJ_qq_ChigChi_tchannel.pdf # Direct production + 1 jet
python3 ../simpleFeynman.py VBF "#bar{q}" q "#Phi" "#Phi" "#bar{#chi}" "#chi" g q "#bar{q}"
mv -f GenericVBF.pdf SVJ_qq_ChiChiqq_VBF_Decay.pdf # Direct production + 2 jets
python3 ../simpleFeynman.py VBF q g "#Phi" g "#chi" g "#Phi" "#bar{q}" "#chi"
mv -f GenericVBF.pdf SVJ_qg_ChiChiqg_VBF_Decay.pdf # Direct production + 2 jets
python3 ../simpleFeynman.py TripleT g g "#bar{q}" "#Phi" "#bar{q}" q q "#chi" "#chi"
mv -f TripleT.pdf SVJ_gg_ChiChiqq_TripleT.pdf # Direct production + 2 jets
#

# If you want to bypass the reading of the command line, to pass the ISR option:
python3 -c "from simpleFeynman import *; simpleSCh('q','#bar{q}','Z\'','#chi','#bar{#chi}',ISR='g')"
# Note the escape on the prime in Z'


