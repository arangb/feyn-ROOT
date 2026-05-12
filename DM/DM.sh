# s-chan: qq -> V -> DMDM + ISR gluon
cd ../
python3 -c "from simpleFeynman import *; simpleSCh('q','#bar{q}','V','#chi','#bar{#chi}',ISR='g')"
mv -f sch-feyn.pdf DM/DM_sch_vector_ISR.pdf
cd -

# VBF:  gg -> qq#phi (#phi -> DMDM)
python3 ../simpleFeynman.py VBF "g" "g" "-" "--" "q" "#bar{q}" "#phi" "#chi" "#bar{#chi}"
mv -f GenericVBF.pdf DM_VBF_PhiChiChi.pdf

# s-chan Z' --> hA (A->DMDM)
python3 ../simpleFeynman.py sD "q" "#bar{q}" "Z'" "h" "A" "--" "--" "#chi" "#bar{#chi}"
mv -f sch-decay.pdf DM_sch_Zp_hA_ChiChi.pdf
