# Single top t-channel with t -> W b 
# It looks better with slant=True, inslant=True in GenericVBFProduction 
python3 ../simpleFeynman.py VBF "q" "g" "W" "b" "q'" "#bar{b}" "t" "W" "b"
mv -f GenericVBF.pdf st-tchan.pdf
# Single top s-channel with t-> W b
python3 ../simpleFeynman.py sD "q" "#bar{q}'" "W^{#plus}" "#bar{b}" "t" "--" "--" "W^{#plus}" "b"
mv -f sch-decay.pdf st-schan.pdf

# Single top tW prod:
python3 ../simpleFeynman.py t "b" "g" "-" "W" "t"
mv -f tch-feyn.pdf st-tWchan.pdf
# Single top tW prod with decay t -> Wb
python3 ../simpleFeynman.py tD "b" "g" "-" "W^{#minus}" "t" "--" "--" "W^{#plus}" "b"
mv -f tch-decay.pdf st-tWchan_decayWb.pdf

# ttbar s-channel gluon with l+jets decay
python3 ../simpleFeynman.py sDD 'g' 'g' 'g' 't' '#bar{t}' 'b' 'W^{#plus}' '#bar{b}' 'W^{#minus}' '\ell^{+}' '#nu' 'q' '#bar{q}'
# Bypassing command line: 
#python3 -c "from simpleFeynman import *; SChWithDoubleDecay('g','g','g','t','#bar{t}','b','W^{#plus}','#bar{b}','W^{#minus}','\\ell^{+}','#nu','q','#bar{q}')"
#sed -i 's/STIXGeneral-Italic findfont/STIXGeneral findfont/' sch-DoubleDecay.eps # to beautify the \ell script
epstopdf sch-DoubleDecay.eps TTbar_lnuJets.pdf
#ttbar s-channel gluon with decay to dilepton
python3 ../simpleFeynman.py sDD 'g' 'g' 'g' 't' '#bar{t}' 'b' 'W^{#plus}' '#bar{b}' 'W^{#minus}' '\ell^{+}' '#nu' '\ell^{-}' '#bar{#nu}'
epstopdf sch-DoubleDecay.eps TTbar_lnulnu.pdf
# W+jets with lepton decay
python3 ../simpleFeynman.py tD 'q' 'g' '-' 'W' 'q'  '\ell' '#bar{#nu}' 'q' 'g'
#python3 -c "from simpleFeynman import *; TChWithDecay('g','q','#bar{q}','q','W','q','g','\\ell','#bar{#nu}')"
#sed -i 's/STIXGeneral-Italic findfont/STIXGeneral findfont/' tch-decay.eps # to beautify the \ell script
epstopdf tch-decay.eps WJets.pdf
# QCD dijet:
python3 ../simpleFeynman.py s g g "g" "g" "g"
mv -f sch-feyn.pdf QCD_dijet.pdf 
# Z+jets to nu nu:
python3 ../simpleFeynman.py tD q "#bar{q}" "-" "Z" "g" "#nu" "#bar{#nu}" "q" "#bar{q}"
mv -f tch-decay.pdf ZplusJets_nunuJJ_decay.pdf

#Z Drell-Yan:
# qq Z ll
python3 ../simpleFeynman.py s 'q' '#bar{q}' 'Z' '\ell^{+}' '\ell^{-}'
#python3 -c "from simpleFeynman import *; simpleSCh('q','#bar{q}','Z','\\ell^{+}','\\ell^{-}')"
#sed -i 's/STIXGeneral-Italic findfont/STIXGeneral findfont/' sch-feyn.eps
epstopdf sch-feyn.eps DrellYan_qqZtoLL.pdf
# qq Z mumu with ISR of a gluon
python3 ../simpleFeynman.py s "q" "#bar{q}" "Z" "#mu^{#plus}" "#mu^{#minus}"
mv -f sch-feyn.pdf DrellYan_qqZtoLLISR.pdf
# gg -> box -> Zg
python3 ../simpleFeynman.py BOX "g" "g" "-" "Z" "g" "-" "-" "q"
mv -f box.pdf Zjets_gg-BOX-Zg.pdf
# qg -> Zq
python3 ../simpleFeynman.py t "q" "g" "-" "Z" "q"
# May need to change the get_line() if (x1==x2)...
mv -f tch-feyn.pdf Zjets_qg-Zq.pdf
python3 ../simpleFeynman.py t "b" "g" "-" "Z" "b"
mv -f tch-feyn.pdf Zjets_bg-Zb.pdf
# VBFlike: gg -> qZq
python3 ../simpleFeynman.py VBF "g" "g" "q" "#bar{q}" "#bar{q}" "q" "Z"
mv -f GenericVBF.pdf Zjets_gg-ZqqVBF.pdf
# qq tchannel Zg with g -> bb
python3 ../simpleFeynman.py tD q "#bar{q}" "-" "Z" "g" "--" "--" "b" "#bar{b}"
mv -f tch-decay.pdf ZJets_qq-Zbb_decay.pdf


