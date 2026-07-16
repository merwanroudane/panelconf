*==============================================================*
*  19 - xtpfardl                                                *
*  ROLE: Fourier-Augmented Panel ARDL / CS-ARDL estimator.      *
*        Gives the LONG-RUN and SHORT-RUN coefficients when the *
*        long-run relation shifts SMOOTHLY (Fourier) and firms  *
*        share common shocks (cross-section averages).          *
*        (Ersin 2026; Sardarli & Suleymanli 2026;               *
*         Chudik et al. 2016; Pesaran, Shin & Smith 1999).      *
*==============================================================*
*
*  In plain words:
*    ARDL handles variables that are I(0) or I(1) mixed together
*    and separates the LONG-RUN effect from the SHORT-RUN effect.
*    This version adds:
*      - Fourier terms  -> the long-run relation can bend smoothly
*      - cross-section averages -> removes the common shock
*
*  Models (choose one with model()):
*    csardl = Cross-Sectionally augmented ARDL   (default)
*    mg     = Mean Group
*    pmg    = Pooled Mean Group (long run pooled, short run free)
*    dfe    = Dynamic Fixed Effects
*
*  Look for:  the LONG-RUN table, the error-correction (adjustment)
*             speed (should be negative), and the chosen Fourier
*             frequency k.
*
*  NOTE: this command needs "xtdcce2" installed (already OK here).
*        If missing:  ssc install xtdcce2
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: CS-ARDL with Fourier
*    crlags() = lags of the cross-section averages; keep it small
*    because this panel is short (T = 20)
xtpfardl invest mvalue kstock, model(csardl) crlags(1)

* 3) Pooled Mean Group: the LONG-RUN effect is the same for all
*    firms, the short-run dynamics are free
xtpfardl invest mvalue kstock, model(pmg) crlags(1)

* 4) fix the Fourier frequency at k = 1 instead of searching
xtpfardl invest mvalue kstock, model(mg) k(1) crlags(1)

* 5) turn the Fourier terms OFF -> a standard panel ARDL
*    (useful to see what the Fourier terms actually add)
xtpfardl invest mvalue kstock, model(mg) nofourier crlags(1)

* 6) test whether pooling the long run is acceptable (PMG vs MG)
xtpfardl invest mvalue kstock, model(pmg) crlags(1) hausman
