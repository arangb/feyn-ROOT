#!/usr/bin/env python
import sys
import re
import itertools
import os # to run shell commands
from ROOT import TCanvas, TArrow, TCurlyLine, TLine, TLatex, TMathText, TMarker, gStyle, gPad
r'''
Aran Garcia-Bellido (April 2019)

To run: 
python simpleFeynman.py s g W "#gamma" t "#bar{t}"
# To write a prime, the best is to just use the ' as here (don't use \\prime or #prime):
python simpleFeynman.py s q "#bar{q}" "Z'" "#chi" "#bar{#chi}"
python simpleFeynman.py t q "#bar{q}" "#Phi" "#chi" "#bar{#chi}"
python simpleFeynman.py t g g " " "t" "#bar{t}"
(also includes an option to have a H -> tt branch in the middle for 4-top) 
python simpleFeynman.py Hgg 
python simpleFeynman.py HVBF
python simpleFeynman.py VBF g g "#bar{t}" t t "#bar{t}" H 
Can include also simple decays:
python simpleFeynman.py tD "g" "g" " " "t" "#bar{t}" "W^{#plus}" "b" "W^{#minus}" "#bar{b}"
python simpleFeynman.py sD "g" "g" "g" "t" "#bar{t}" "W^{#plus}" "b" "W^{#minus}" "#bar{b}"
And can include radiation/assoc process in tD and sD modes by leaving d1 and d2 empty:
python simpleFeynman.py tD "q" "g" "#bar{q}" "#gamma" "q" "" "" "#gamma" "q"
Kaon oscilaltion: d bar{s} = K^0 ; bar{d} s = bar{K}^0 (strangeness changes from +1 to -1)
python simpleFeynman.py BOX d "#bar{s}" "bar{u}" #bar{d} s "W^{#minus}" "W^{#plus}" u

# It's better to use #minus and #plus instead of "e^{-}" and "e^{+}". Longer lines.

If you need to use the Latex \ell, that can be done with:
if ('\\ell' in particle_name): 
    tm = TMathText(); tm.SetTextSize(0.1); tm.DrawMathText(132,78,'\\ell^{+}')
# the problem is that this doesn't print in a pdf, you have to save as eps, and then convert: epstopdf <file.eps>
# It also looks better if you look for /STIXGeneral-Italic ... /afii61289 in the eps file and remove the -Italic
From a shell script:
sed -i 's/STIXGeneral-Italic findfont/STIXGeneral findfont/' sch-DoubleDecay.eps
epstopdf sch-DoubleDecay.eps TTbar_lnuJets.pdf
All this can be done in savefile()

2025: Had to add the r before the triple comma comments to not get a SyntaxWarning: invalid escape sequence '\ ' for the drawings
2026: Added the dictionary of functions in main() to run more efficiently than with if statements.
'''
bosons=['W','Z','#gamma',"Z'", "W/Z", "Z/#gamma", '#gamma','W^{#plus}','W^{#minus}','W^{0}','Z^{0}', 'V']
bosons = bosons + list(x + '*' for x in bosons) # This adds the imaginary case to each item ['W*', ...]
gluons=['g']
scalars=['H','H^{0}','h','h^{0}','A', 'A^{0}', 'X', 'X^{0}','#tilde{#chi}','#tilde{#chi}_{1}^{0}','H_{u}','#Phi','#bar{#Phi}', '#phi', '#bar{#phi}'] #'#chi','#bar{#chi}'
scalars = scalars + list('#tilde{'+x+'}' for x in ['e','#mu','#tau','f','q','t','b','u','d'])
scalars = scalars + list('#tilde{'+x+'}^{'+s+'}' for x,s in  itertools.product(['e','#mu','#tau','f','q','t','b','u','d'],['+','-']))
gStyle.SetLineStyleString(9,"89 20") # the default 9 has a leftover tick in the diagonal lines
gStyle.SetLineStyleString(11,"80 20") # old default 9, for horizontal (full ticks), and for arcs (makes it touch both bases)
wl=0.034
amp=0.017
def get_line(p='g',x1=10,y1=10,x2=60,y2=10,wl=0.034,amp=0.017,arrowsize=0.03):
    ''' Decide what line to draw based on the label of the particle '''
    line=TCurlyLine(x1, y1, x2, y2, wl, amp) # start as gluon 
    if (p in bosons or p[0] in bosons):
        line.SetWavy()
    elif (p in gluons):
        line.SetCurly()
    elif (p in scalars or p[0] in scalars): # should we draw an arrow for scalars?
        line = TLine(x1, y1, x2, y2)
        if (y1 == y2) or (x1==x2):
            line.SetLineStyle(11) # this doesn't end in half a tick for horiz or vert lines
        else:
            line.SetLineStyle(9) # this doesn't end in half a tick for diagonal lines
    else: # if any(i in a for i in ['#bar','+'])
        line = TArrow(x1, y1, x2, y2, arrowsize,"-<|-" if '#bar' in p or '#plus' in p or "+" in p or p == " " else "-|>-")
        # if the p is just an empty space, we assume this is a mediator anti-fermion, typically followed by "t" "#bar{t}"
        if (x1==x2): # a fermion exchanged in t-channel (vertical line) should not have any arrows.
            #line = TLine(x1, y1, x2, y2)
            # if you want an arrow, uncomment this (this is the default):
            line = TArrow(x1, y1, x2, y2, arrowsize,"-|>-" if '#bar' in p or '+' in p or p == " " else "-<|-")
            # if you uncomment the next line, you will be breaking other scripts, so put back the line above after you are finished.
            #line = TArrow(x1, y1, x2, y2, arrowsize,"-<|-" if '#bar' in p or '+' in p or p == " "  else "-|>-")
    return line

def savefile(canvas,args,fname):
    r'''Looks for \ell in any of the particles and does the trick to print \ell in eps and then convert to pdf'''
    name, ext = os.path.splitext(fname)
    # added str(p) to avoid Bool case when passing arguments directly python3 -c ...
    if any('\\ell' in str(p) for p in args.values()): #if any('\\ell' in p for p in [d,e]):
        canvas.SaveAs(name+".eps")
        os.system('sed -i "s/STIXGeneral-Italic findfont/STIXGeneral findfont/g" '+name+'.eps')
        print('You should run: epstopdf '+name+'.eps'+' '+fname)
        # for some reason os.system('/usr/bin/epstopdf sch-feyn.eps sch-feyn.pdf') doesn't work
    else:
        canvas.SaveAs(name+ext)

def simpleTCh(a="g", b="g", c="t", d="t", e="#bar{t}", YukawaCorr=False, ttH=False, FSR='', vtx=False, angle=False):
    arguments = locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 120, 60)
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(30) # horiz. centered 20, horiz. right-justified 30, horiz. left-justified 10 
    t.SetTextSize(0.1)
    # 
    dy = 5 if angle else 0 # in case we want to slant the lines
    #
    lt = get_line(a,10, 50, 60, 50-dy)
    lt.Draw()
    #t.DrawLatex(24,46,"g") #middle of line
    t.DrawLatex(7,48,a) #beginning of line
    #
    lb = get_line(b,10, 10, 60, 10+dy)
    lb.Draw()
    #t.DrawLatex(24,8,"g") # //middle of line
    t.DrawLatex(7,8,b) #beginning of line
    #
    middle = get_line(c,60, 50-dy, 60, 10+dy)
    #middle = get_line(c,60, 10+dy, 60, 50-dy)
    middle.Draw()
    t.SetTextAlign(10)
    if FSR == "":
        t.DrawLatex(67,28,c)
    else:
        t.DrawLatex(57,28,c)
    #
    rt = get_line(d,60, 50-dy, 110, 50)
    rt.Draw()
    #t.DrawLatex(113,46,d) # middle of line
    t.SetTextAlign(20)
    t.DrawLatex(115,48,d) # end of line
    #
    rb = get_line(e,60, 10+dy, 110, 10)
    rb.Draw()
    #t.DrawLatex(113,10,"#bar{q}") # middle of line
    t.DrawLatex(115,8,e) # end of line
    
    if YukawaCorr:# draw Yukawa coupling weak corrections between d and e
        #g = TCurlyLine(95, 10, 95, 50,wl,amp)
        #g.SetWavy()
        #g.Draw()
        #t.DrawLatex(102,28,"#Gamma") #end of line 
        g=get_line('h',95, 10, 95, 50)
        g.Draw()
        t.DrawLatex(102,28,"h") 
        # Do the markers:
        p1=TMarker(95,10,20); p1.SetMarkerColor(2); p1.Draw()
        t.SetTextColor(2); t.DrawLatex(99,10.5,"#kappa_{t}")
        p2=TMarker(95,50,20); p2.SetMarkerColor(2); p2.Draw()
        t.DrawLatex(99,43.5,"#kappa_{t}")

    if ttH: # draw ttH
        H = TLine(60,30,90,30)
        #H.SetLineColor(2)
        H.SetLineStyle(9) # dashed
        H.Draw()
        t.DrawLatex(75,32,"H")
        # Decay of the H:
        d1 = TArrow(90,30,110,40, 0.03, "-|>-")
        d1.Draw()
        t.DrawLatex(115,38,"t") # end of line
        d2 = TArrow(90,30,110,20, 0.03, "-<|-")
        d2.Draw()
        t.DrawLatex(115,18,"#bar{t}") # end of line
    
    if FSR != '': # radiation in the middle 
        rad = get_line(FSR,60,30,110,30)
        rad.Draw()
        t.DrawLatex(115,28,FSR)
    
    if vtx: # draw vertices as dots
        pp = TMarker(60,10+dy,20); pp.SetMarkerColor(1); pp.SetMarkerSize(1.3); pp.Draw()
        t.SetTextAlign(23); t.DrawLatex(60,8+dy,"#lambda") #"g"
        rr = TMarker(60,50-dy,20); rr.SetMarkerColor(1); rr.SetMarkerSize(1.3); rr.Draw()
        t.SetTextAlign(21); t.DrawLatex(60,53-dy,"#lambda") #"g"
    
    c1.Update()
    savefile(c1,arguments,"tch-feyn.pdf")
    return

def simpleSCh(a="g", b="g", c="g", d="t", e="#bar{t}", YukawaCorr=False, ISR=True, FSR=False, vtx=False):
    '''
    Problem: if d or e is more than one character, there is no proper room.
    Perhaps make box bigger, or middle line smaller?
    '''
    arguments = locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 120, 60)
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(20) # horizontally centered
    t.SetTextSize(0.1)
    wl=0.034
    amp=0.017
    #
    lt = get_line(a,10,50,40,30)
    lt.Draw()
    #t.DrawLatex(24,46,a) #middle of line
    t.DrawLatex(5,48,a) #beginning of line
    #
    lb = get_line(b,10, 10, 40, 30)
    lb.Draw()
    #t.DrawLatex(24,8,b) # //middle of line
    t.DrawLatex(5,6,b) #beginning of line
    #
    middle = get_line(c,40, 30, 80, 30)
    middle.Draw()
    t.DrawLatex(60,36,c) 
    #
    rt = get_line(d,80, 30, 110, 50)
    rt.Draw()
    #t.DrawLatex(113,10,"#bar{q}") # middle of line
    t.DrawLatex(115,48,d) # end of line
    #
    rb = get_line(e,80, 30, 110, 10)
    rb.Draw()
    #t.DrawLatex(113,46,"q") # middle of line
    t.DrawLatex(115,6,e) # end of line
    
    if YukawaCorr: # draw Yukawa weak corrections between d and e:
        #g = TCurlyLine(102, 15.5, 102, 44.5,wl,amp)
        #g.SetWavy()
        #g.Draw()
        #t.DrawLatex(109,28,"#Gamma") #end of line 
        g=get_line('h',102, 15.5, 102, 44.5)
        g.Draw()
        t.DrawLatex(109,28,"h") 
        # Do the markers:
        p1=TMarker(102,15.5,20); p1.SetMarkerColor(2); p1.Draw()
        t.SetTextColor(2); t.DrawLatex(102,8.5,"#kappa_{t}")
        p2=TMarker(102,44.5,20); p2.SetMarkerColor(2); p2.Draw()
        t.DrawLatex(102,46.5,"#kappa_{t}")
        
    if ISR: # change here what particle is radiated
        i=get_line("g",18, 15, 50, 15)
        i.Draw()
        t.SetTextAlign(12) # horiz-left just, vertically centered
        t.DrawLatex(52,15, "g")
    
    if FSR: # change here what particle is radiated
        f=get_line("q",87.5, 25, 110, 25)
        f.Draw()
        t.SetTextAlign(22) # horiz center just, vertically centered
        t.DrawLatex(115,25, "q")
        
    if vtx: # draw vertices as dots
        pp = TMarker(40,30,20); pp.SetMarkerColor(1); pp.SetMarkerSize(1.3); pp.Draw()
        t.SetTextAlign(23); t.DrawLatex(40,28,"g_{q}")
        rr = TMarker(80,30,20); rr.SetMarkerColor(1); rr.SetMarkerSize(1.3); rr.Draw()
        t.SetTextAlign(23); t.DrawLatex(80,28,"g_{#chi}")
        #rr = TMarker(80,30,20); rr.SetMarkerColor(1); rr.SetMarkerSize(1.3); rr.Draw()
        #t.SetTextAlign(23); t.DrawLatex(80,28,"#kappa")
        
    c1.Update()
    savefile(c1,arguments,"sch-feyn.pdf")

    return

def HiggsGluGluProd(d1='',d2=''):
    r'''
       gg fusion (top quark loop), with possible daughters d1 and d2 (none by default):
       g-----|\         /d1 if given
             | \_____H /
             | /       \
       g-----|/         \d2 if given
       
       Can also add decay of Higgs
    '''
    arguments = locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 190, 60)
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(20) # horizontally centered
    t.SetTextSize(0.1)
    wl=0.034
    amp=0.017
    # 
    lt = TCurlyLine(10, 50, 60, 50,wl,amp)
    lt.Draw()
    t.DrawLatex(5,48,'g') #beginning of line
    #
    lb = TCurlyLine(10, 10, 60, 10,wl,amp)
    lb.Draw()
    t.DrawLatex(5,8,'g') #beginning of line
    #
    lv = TArrow(60, 50, 60, 10, 0.03,"-<|-")
    lv.Draw()
    lu = TArrow(60, 50, 90, 30, 0.03,"-|>-")
    lu.Draw()
    ld = TArrow(60, 10, 90, 30, 0.03,"-<|-")
    ld.Draw()
    t.DrawLatex(80,40,'t') #middle of line
    # 
    #H = TCurlyLine(90,30,140,30,wl,amp)
    #H.SetWavy()
    H = TArrow(90, 30, 140, 30, 0.03,"-") # can draw arrow "-|>-"
    H.SetLineStyle(9) # dashed
    H.Draw()
    t.DrawLatex(115,34,"h") # Z, #chi
    # We can also add the decay products of Higgs: 
    if (d1 and d2):
        rt = get_line(d1,140, 30, 170, 50)
        rt.Draw()
        t.DrawLatex(175,48,d1) # end of line
        #
        rb = get_line(d1,140, 30, 170, 10)
        rb.Draw()
        t.DrawLatex(175,8,d2) #'#bar{t}') # end of line
    c1.Update()
    savefile(c1,arguments,"Higgs.pdf")
    return
    
def GenericVBFProd(a="q", b="q'", chi="W/Z", clo="W/Z", d="q", e="q'", h="h", h1="", h2=""):
    r'''
    This function can be used for Vector Boson Fusion:
    GenericVBFProd("q","q'","W/Z","W/Z","q","q'","H")
    or H associated with quarks:
    GenericVBFProd("g","g","#bar{t}","t","t","#bar{t}","H")
    
     a ------|------d
         chi |______h / h1 if given
         clo |        \ h2 if given
     b ------|------e
     
     If clo == "" the line will use chi to determine its type and not print anything. 
     If clo == " " the line will be a fermion and print nothing.
     The slant boolean can be used to raise/lower the d/e lines by 10 pixels
    '''
    slant = False # if False, a || d and b || e. If False, dy(d)=5 and dy(e)=-5
    inslant = True # if False clo || chi. If True, clo and chi have an angle and h is shorter
    arguments = locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    #c1 = TCanvas("c1", "A canvas", 10,10, 1200, 1200)
    c1.SetFillColor(0)
    c1.Range(0, 10, 120, 70)
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(20) # horizontally centered
    t.SetTextSize(0.1)
    wl=0.034
    amp=0.017
    #
    lt = get_line(a,10, 60, 60 if inslant == True else 60, 60)
    lt.Draw()
    #t.DrawLatex(24,46,"g") #middle of line
    t.DrawLatex(5,58,a) #beginning of line
    #
    lb = get_line(b,10, 20, 60 if inslant == True else 60, 20)
    lb.Draw()
    #t.DrawLatex(24,8,"g") # //middle of line
    t.DrawLatex(5,18,b) #beginning of line
    #
    umiddle = get_line(chi,60, 60, 65 if inslant == True else 60, 40)
    umiddle.Draw()
    t.SetTextAlign(32) # right justified, vertically centered
    t.DrawLatex(58 if inslant == True else 55,51,chi)
    #
    if clo == "": # clo should be the same as chi:
        bmiddle = get_line(chi, 65, 40, 60 if inslant == True else 65, 20,wl,amp)
        #print('AGB')
    else:
        bmiddle = get_line(clo, 60, 20, 65 if inslant == True else 60, 40,wl,amp)
    bmiddle.Draw()
    t.SetTextAlign(32) # right justified, vertically centered
    t.DrawLatex(58 if inslant == True else 55,30,clo)#clo if clo == "" else chi)
    #h Higgs in the middle
    #H = TArrow(60, 40, 110, 40, 0.03,"-|>-")
    if (h1 != "" and h2 != ""): # we can also add H decays and make H shorter:
        H = get_line(h,65 if inslant == True else 60, 40, 85, 40,wl,amp)
        hda1 = get_line(h1,85, 40, 110, 50,wl,amp)
        hda2 = get_line(h2,85, 40, 110, 30,wl,amp)
        H.Draw(); hda1.Draw(); hda2.Draw()
        t.DrawLatex(117,50,h1)
        t.DrawLatex(117,30,h2)
        t.SetTextAlign(20) # back to horizontally centered
        t.DrawLatex(75 if inslant == True else 72,42,h)
    else:
        H = get_line(h,65 if inslant == True else 60, 40, 110, 40,wl,amp)
        H.Draw()
        t.SetTextAlign(20) # back to horizontally centered
        t.DrawLatex(115,38,h) 
    #d slanted upwards
    rt = get_line(d,60, 60, 110, 68 if slant == True else 60) # was 70
    rt.Draw()
    t.DrawLatex(115,64 if slant == True else 58,d) # was 68
    #e slanted downwards
    rb = get_line(e,60, 20, 110, 12 if slant == True else 20) # was 10
    rb.Draw()
    #t.DrawLatex(113,10,"#bar{q}") # middle of line
    t.DrawLatex(115,11 if slant == True else 18,e) # was 8
    #
    c1.Update()
    savefile(c1,arguments,"GenericVBF.pdf")
    return
    
def TChWithDecay(a="g", b="g", c=" ", d="t", e="#bar{t}", d1="W^{#plus}", d2="b", e1="W^{#minus}", e2="#bar{b}"):
    r'''        d  / d1
    a ------|-----\ d2
            |c
            |     / e1
    b ------|-----\ e2
               e
    If you leave d1 and d2 as empty strings "", the d line will extend until the end
    '''
    arguments=locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 150, 110) # Force this plot to have the same dimensions as SChWithDecay
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(30) # horiz. centered 20, horiz. right-justified 30, horiz. left-justified 10 
    t.SetTextSize(0.1)
    # 
    lt = get_line(a,20, 80, 70, 80)
    lt.Draw()
    t.DrawLatex(17,75,a) #beginning of line
    #
    lb = get_line(b,20, 30, 70, 30)
    lb.Draw()
    t.DrawLatex(17,25,b) #beginning of line
    #
    middle = get_line(c,70, 80, 70, 30)
    middle.Draw()
    t.SetTextAlign(10)
    t.DrawLatex(74,52,c)
    #
    rt = get_line(d,70, 80, 100, 80)
    if (d1 == "" and d2 ==""): # this line does not decay, extend to the end
        rt = get_line(d,70,80,130,80)
        t.SetTextAlign(10) # left justified
        t.DrawLatex(132,78,d) # end of line
    else:
        t.SetTextAlign(20) # horizontally centered
        t.DrawLatex(85,86,d) # middle of line
    rt.Draw()
    #
    rb = get_line(e,70, 30, 100, 30)
    rb.Draw()
    t.DrawLatex(85,16,e) # middle of line
    # Daughters:
    if not (d1 == "" and d2 ==""):
        dt = get_line(d1,100,80,130,100)
        dt.Draw()
        t.SetTextAlign(10) # left justified
        t.DrawLatex(132,95,d1)
    
        db = get_line(d2,100,80,130,60)
        db.Draw()
        t.DrawLatex(132,58,d2)
    
    et = get_line(e1,100,30,130,50)
    et.Draw()
    t.DrawLatex(132,45,e1)
    
    eb = get_line(e2,100,30,130,10)
    eb.Draw()
    t.DrawLatex(132,8,e2)

    if False: # draw vertices as dots on the production
        pp = TMarker(70,30,20); pp.SetMarkerColor(1); pp.SetMarkerSize(1.3); pp.Draw()
        t.SetTextAlign(23); t.DrawLatex(70,25,"#alpha_{s}") #"g"
        rr = TMarker(70,80,20); rr.SetMarkerColor(1); rr.SetMarkerSize(1.3); rr.Draw()
        t.SetTextAlign(21); t.DrawLatex(70,87,"y_{d}") #"g"


    c1.Update()
    savefile(c1,arguments,"tch-decay.pdf")
    return
    
def SChWithDecay(a="g", b="g", c="g", d="t", e="#bar{t}", d1="W^{#plus}", d2="b", e1="W^{#minus}", e2="#bar{b}", vtx=False):
    r'''
    If you leave d1 and d2 as empty strings "", the d line will extend until the end
    a          / d1 
     \       d/\ d2
      \___c__/     
      /      \
     /       e\/ e1
    b          \ e2

    '''
    arguments=locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 150, 110) # We forced TChWithDecay to have the same dimensions as this one
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(30) # horiz. centered 20, horiz. right-justified 30, horiz. left-justified 10 
    t.SetTextSize(0.1)
    #
    lt = get_line(a,10, 80, 40, 55)
    lt.Draw()
    #t.DrawLatex(24,46,a) #middle of line
    t.DrawLatex(8,75,a) #beginning of line
    #
    lb = get_line(b,10, 30, 40, 55)
    lb.Draw()
    #t.DrawLatex(24,8,b) # //middle of line
    t.DrawLatex(8,25,b) #beginning of line
    #
    middle = get_line(c,40, 55, 70, 55)
    middle.Draw()
    t.DrawLatex(60,60,c) 
    #
    rt = get_line(d,70, 55, 100, 80)
    if (d1 == "" and d2 ==""): # this line does not decay, extend to the end
        rt = get_line(d,70,55,130,80)
        t.SetTextAlign(10) # left justified
        t.DrawLatex(132,78,d) # end of line
    else:
        t.SetTextAlign(20) # center justified
        t.DrawLatex(85,75,d) # middle of line 
    rt.Draw()
    #
    rb = get_line(e,70, 55, 100, 30)
    rb.Draw()
    t.DrawLatex(80,30,e) # middle of line
    # Daughters:
    if not (d1 == "" and d2 ==""): 
        dt = get_line(d1,100,80,130,100)
        dt.Draw()
        t.SetTextAlign(10) # left justified
        t.DrawLatex(132,95,d1)
    
        db = get_line(d2,100,80,130,60)
        db.Draw()
        t.DrawLatex(132,58,d2)
    
    et = get_line(e1,100,30,130,50)
    et.Draw()
    t.DrawLatex(132,45,e1)
    
    eb = get_line(e2,100,30,130,10)
    eb.Draw()
    t.DrawLatex(132,8,e2)

    if vtx: # draw vertices as dots 70, 55, 100, 30
        # marker at beginning of e:
        #be = TMarker(70,55,20); be.SetMarkerColor(1); be.SetMarkerSize(1.3); ee.Draw()
        #t.SetTextAlign(22); t.DrawLatex(70,48,"#lambda") #"g"
        # marker at end of e:
        ee = TMarker(100,30,20); ee.SetMarkerColor(1); ee.SetMarkerSize(1.3); ee.Draw()
        t.SetTextAlign(22); t.DrawLatex(100,23,"#lambda") #"g"
        # marker at end of d:
        ed = TMarker(100,80,20); ed.SetMarkerColor(1); ed.SetMarkerSize(1.3); ed.Draw()
        t.SetTextAlign(22); t.DrawLatex(100,88,"#lambda") #"g"

    c1.Update()
    savefile(c1,arguments,"sch-decay.pdf")
    return 
    
def SChWithDoubleDecay(a="g", b="g", c="g", d="t", e="#bar{t}", d1="b", d2="W^{#plus}", e1="#bar{b}", e2="W^{#minus}", d21="l^{#plus}",d22="#nu",e21="q",e22="#bar{q}"):
    r'''         d1
    a          /     /d21
     \       d/------\
      \___c__/   d2   \d22
      /      \   
     /       e\-----e1
    b          \   /e21  
                e2/ 
                  \e22
    
    If you leave d1 and d2 as empty strings "", the d line will extend until the end
    '''
    arguments=locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 150, 110) # We forced TChWithDecay to have the same dimensions as this one
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(30) # horiz. centered 20, horiz. right-justified 30, horiz. left-justified 10 
    t.SetTextSize(0.1)
    #
    lt = get_line(a,10, 80, 40, 55)
    lt.Draw()
    #t.DrawLatex(24,46,a) #middle of line
    t.DrawLatex(8,75,a) #beginning of line
    #
    lb = get_line(b,10, 30, 40, 55)
    lb.Draw()
    #t.DrawLatex(24,8,b) # //middle of line
    t.DrawLatex(8,25,b) #beginning of line
    #
    middle = get_line(c,40, 55, 70, 55)
    middle.Draw()
    t.DrawLatex(60,60,c) 
    #
    rt = get_line(d,70, 55, 100, 80)
    if (d1 == "" and d2 ==""): # this line does not decay, extend to the end
        rt = get_line(d,70,55,130,80)
        t.SetTextAlign(10) # left justified
        t.DrawLatex(132,78,d) # end of line
    else:
        t.SetTextAlign(20) # center justified
        t.DrawLatex(85,75,d) # middle of line 
    rt.Draw()
    #
    rb = get_line(e,70, 55, 100, 30)
    rb.Draw()
    t.DrawLatex(85,25,e) # middle of line
    # Daughters:
    if not (d1 == "" and d2 ==""): 
        dt = get_line(d1,100,80,130,100)
        dt.Draw()
        t.SetTextAlign(10) # left justified
        t.DrawLatex(132,95,d1)
    
        db = get_line(d2,100,80,115.1,69.95) # 115,70 leaves a white space 
        db.Draw()
        t.DrawLatex(100,60,d2)
        
        db1 = get_line(d21,115,70,130,80)
        db1.Draw()
        if r'\ell' in d21:
            tm = TMathText(); tm.SetTextSize(0.1); tm.DrawMathText(132,78,d21)
        else:
            t.DrawLatex(132,78,d21)
        
        db2 = get_line(d22,115,70,130,60)
        db2. Draw() 
        t.DrawLatex(132,58,d22)
        
    et = get_line(e1,100,30,130,50)
    et.Draw()
    t.DrawLatex(132,45,e1)
    
    eb = get_line(e2,100,30,115.1,20.05) # 115,20 leaves a white space
    eb.Draw()
    t.DrawLatex(100,8,e2)
    
    eb1 = get_line(e21,115,20,130,30)
    eb1.Draw()
    if r'\ell' in eb1:
        tm = TMathText(); tm.SetTextSize(0.1); tm.DrawMathText(132,28,e21)
    else:
        t.DrawLatex(132,28,e21)
    
    eb2 = get_line(e22,115,20,130,10)
    eb2.Draw()
    t.DrawLatex(132,8,e22)


    c1.Update()
    savefile(c1,arguments,"sch-DoubleDecay.pdf")
    return 

def BoxDiagram(a="g",b="g",c="f",d="#gamma",e="#gamma",f="",g="",h=""):
    '''       
    a ------|---|------d
            | f | 
          c | g | h
    b ------|---|------e
    
    '''
    arguments = locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 0, 150, 60)
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(30) # horiz. centered 20, horiz. right-justified 30, horiz. left-justified 10 
    t.SetTextSize(0.1)
    # 
    lt = get_line(a,10, 50, 55, 50) # 
    lt.Draw()
    t.DrawLatex(7,48,a) #beginning of line
    #
    lb = get_line(b,10, 10, 55, 10) #y 30 -->10
    lb.Draw()
    t.DrawLatex(7,8,b) #beginning of line
    # box:
    middleleft = get_line(c,55, 50, 55, 10) # from top to bottom to get default arrows right around loop if " "
    middleleft.Draw()
    t.SetTextAlign(10)
    t.DrawLatex(59,28,c)
    middletop = get_line(f,55, 50, 90, 50) 
    middletop.Draw()
    t.DrawLatex(70,42,f)
    middleright = get_line(h,90, 50, 90, 10) 
    middleright.Draw()
    t.DrawLatex(82,28,h)
    middlebot = get_line(g,90, 10, 55, 10) # from right to left to get default arrows right around loop if " "
    middlebot.Draw()
    t.DrawLatex(70,14,g)
    #
    rt = get_line(d,90, 50, 135, 50)
    rt.Draw()
    t.SetTextAlign(20)
    t.DrawLatex(140,48,d) # end of line
    #
    rb = get_line(e,90, 10, 135, 10)
    rb.Draw()
    t.DrawLatex(140,8,e) # end of line

    c1.Update()
    savefile(c1,arguments,"box.pdf")
    return

def TripleT(a="q", b="q'", chi="W/Z", cmi="W/Z", clo="W/Z", d="q", e="q'", h="h", f="h"):
    ''' 
    To draw this type of diagrams:
    
     a ------|------d
         chi |______h 
         cmi |______f        
         clo |
     b ------|------e
     
     If clo == "" the line will use chi to determine its type and not print anything. 
     If clo == " " the line will be a fermion and print nothing.
     Same for cmi.
     The slant boolean can be used to raise/lower the d/e lines by 10 pixels
    '''
    slant = False # if False, a || d and b || e. If False, dy(d)=10 and dy(e)=-10
    arguments = locals()
    c1 = TCanvas("c1", "A canvas", 10,10, 500, 300)
    c1.SetFillColor(0)
    c1.Range(0, 10, 120, 70)
    gStyle.SetLineWidth(3)
    t = TLatex()
    t.SetTextAlign(20) # horizontally centered
    t.SetTextSize(0.1)
    wl=0.034
    amp=0.017
    #
    lt = get_line(a,10, 60, 60, 60)
    lt.Draw()
    #t.DrawLatex(24,46,"g") #middle of line
    t.DrawLatex(5,58,a) #beginning of line
    #
    lb = get_line(b,10, 20, 60, 20)
    lb.Draw()
    #t.DrawLatex(24,8,"g") # //middle of line
    t.DrawLatex(5,18,b) #beginning of line
    #
    umiddle = get_line(chi,60, 60, 60, 46.7)
    umiddle.Draw()
    t.SetTextAlign(32) # right justified, vertically centered
    t.DrawLatex(55,53,chi) 
    #
    if cmi == "": # cmi should be the same as chi:
        cmiddle = get_line(chi,60, 46.7, 60, 33.33,wl,amp)
    else:
        cmiddle = get_line(cmi,60, 46.7, 60, 33.33,wl,amp)
    cmiddle.Draw()
    t.SetTextAlign(32) # right justified, vertically centered
    t.DrawLatex(55,40,cmi)#clo if clo == "" else chi)
    #
    if clo == "": # clo should be the same as chi:
        bmiddle = get_line(chi,60, 33.33, 60, 20,wl,amp)
    else:
        bmiddle = get_line(clo,60, 33.33, 60, 20,wl,amp)
    bmiddle.Draw()
    t.SetTextAlign(32) # right justified, vertically centered
    t.DrawLatex(55,28,clo)#clo if clo == "" else chi)
    #
    H = get_line(h,60, 46.7, 110, 46.7,wl,amp)
    H.Draw()
    t.SetTextAlign(20) # back to horizontally centered
    t.DrawLatex(115,44,h) 
    # 
    F = get_line(f,60, 33.33, 110, 33.33,wl,amp)
    F.Draw()
    t.SetTextAlign(20) # back to horizontally centered
    t.DrawLatex(115,31,f) 
    #d slanted upwards
    rt = get_line(d,60, 60, 110, 70 if slant == True else 60)
    rt.Draw()
    t.DrawLatex(115,68 if slant == True else 58,d) # end of line
    #e slanted downwards
    rb = get_line(e,60, 20, 110, 10 if slant == True else 20)
    rb.Draw()
    #t.DrawLatex(113,10,"#bar{q}") # middle of line
    t.DrawLatex(115, 8 if slant == True else 18,e) # end of line
    #
    c1.Update()
    savefile(c1,arguements,"TripleT.pdf")
    return


def main():
    # First check for any - or --:
    for argindex in range(len(sys.argv)):
        if sys.argv[argindex] == "-": # typically for a fermion with no tag
            sys.argv[argindex] = " "
        if sys.argv[argindex] == "--": # typically will continue the line
            sys.argv[argindex] = ""

    flag=sys.argv[1]  # the function we want to call (abbreviated name)
    args=sys.argv[2:] # the arguments we want to pass to that function

    functions = {# create dictionary of abbreviations to call each function defined above
        "s": simpleSCh,
        "t": simpleTCh,
        "Hgg": HiggsGluGluProd,
        "VBF": GenericVBFProd,
        "tD": TChWithDecay,
        "sD": SChWithDecay,
        "sDD": SChWithDoubleDecay,
        "BOX": BoxDiagram,
        "TripleT": TripleT
    }
    minargs = {# minimum number of arguments each function expects
        "s": 5,
        "t": 5,
        "Hgg": 0,
        "VBF": 7,
        "tD": 9,
        "sD": 9,
        "sDD": 13,
        "BOX": 5,
        "TripleT": 9
    }

    func_help = {# Provide help with the expected arguments
        "s": r'''simpleSCh(a="g", b="g", c="g", d="t", e="#bar{t}", YukawaCorr=False, ISR=True, FSR=False, vtx=False)
    a=left-top             a          d
    b=left-bottom           \        /
    c=middle                 \___c__/
    d=right-top              /      \
    e=right-bottom          /        \
                           b          e
''',
        "t": r'''simpleTCh(a="g", b="g", c="t", d="t", e="#bar{t}", YukawaCorr=False, ttH=False, FSR='', vtx=False, angle=False)
    a=left-top             a ----------- d
    b=left-bottom                 |
    c=middle                      | c
    d=right-top                   |
    e=right-bottom         b ----------- e
''',
        "Hgg": r'''HiggsGluGluProd(d1='',d2='')
       gg fusion (top quark loop), with possible daughters d1 and d2 (none by default):
       g-----|\         /d1 if given
             | \_____H /
             | /       \
       g-----|/         \d2 if given
''',
        "VBF": r'''GenericVBFProd(a="q", b="q'", chi="W/Z", clo="W/Z", d="q", e="q'", h="h", h1="", h2="")
     a ------|------d
         chi |______h / h1 if given    If clo == "" the line will use chi to determine its type and not print anything.
         clo |        \ h2 if given    If clo == " " the line will be a fermion and print nothing.
     b ------|------e
''',
        "tD": r'''TChWithDecay(a="g", b="g", c=" ", d="t", e="#bar{t}", d1="W^{#plus}", d2="b", e1="W^{#minus}", e2="#bar{b}")
               d  / d1
    a ------|-----\ d2   If you leave d1 and d2 as empty strings "", the d line will extend until the end
            |c
            |     / e1
    b ------|-----\ e2
               e
''',
        "sD": r'''SChWithDecay(a="g", b="g", c="g", d="t", e="#bar{t}", d1="W^{#plus}", d2="b", e1="W^{#minus}", e2="#bar{b}")
    a          / d1
     \       d/\ d2   If you leave d1 and d2 as empty strings "", the d line will extend until the end
      \___c__/
      /      \
     /       e\/ e1
    b          \ e2
''',
        "sDD": r'''SChWithDoubleDecay(a="g", b="g", c="g", d="t", e="#bar{t}", d1="b", d2="W^{#plus}", e1="#bar{b}", e2="W^{#minus}", d21="l^{#plus}",d22="#nu",e21="q",e22="#bar{q}")
               d1
    a          /     /d21
     \       d/------\
      \___c__/   d2   \d22     If you leave d1 and d2 as empty strings "", the d line will extend until the end
      /      \
     /       e\-----e1
    b          \   /e21
                e2/
                  \e22
''',
        "BOX": r'''BoxDiagram(a="g",b="g",c="f",d="#gamma",e="#gamma",f="",g="",h="")
    a ------|---|------d
            | f |
          c | g | h
    b ------|---|------e
''',
        "TripleT": r'''TripleT(a="q", b="q'", chi="W/Z", cmi="W/Z", clo="W/Z", d="q", e="q'", h="h", f="h")
     a ------|------d
         chi |______h          If clo == "" the line will use chi to determine its type and not print anything.
         cmi |______f          If clo == " " the line will be a fermion and print nothing.
         clo |                 Same for cmi.
     b ------|------e
'''
    }

    if flag in functions.keys():
        if len(args) >= minargs[flag]:
            functions[flag](*args) # calls function based on input name
        else:
            print("ERROR: need to pass at least ", minargs[flag],  " arguments to this function ")
            print(func_help[flag])
            #print('In new laptop 2025 we cannot pass \"\" nor \" \" as arguments, sys.argv doesnt get them.')
            #print('You should use - for \" \" and -- for \"\" ')


if __name__ == "__main__":
    main()
