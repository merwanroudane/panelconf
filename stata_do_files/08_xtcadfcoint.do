*==============================================================*
*  08 - xtcadfcoint                                             *
*  ROLE: Panel COINTEGRATION test with structural INSTABILITIES *
*        (breaks in the intercept, the slope, and the factor    *
*         loadings)  (Banerjee & Carrion-i-Silvestre 2025).     *
*==============================================================*
*
*  In plain words:
*    The most general cointegration test here. It lets breaks hit
*    the intercept, the long-run slope, AND the common factors.
*    H0 = no cointegration.  REJECT => cointegration.
*
*  Options you will see:
*    model(1)=intercept, model(3)=intercept+trend
*    breaks(#)     = number of breaks (0 = none)
*    nfactors(#)   = number of common factors
*    brkslope      = allow the slope to break
*    brkloadings   = allow the factor loadings to break
*    simulate(#)   = draws for the critical values
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: intercept, no break, 1 factor
xtcadfcoint invest mvalue, model(1) breaks(0) nfactors(1)

* 3) allow ONE break, with a simulated p-value
*    NOTE: breaks() > 0 requires model(3) (intercept + trend)
xtcadfcoint invest mvalue, model(3) breaks(1) nfactors(1) simulate(500)

* 4) allow breaks in slope AND loadings (the full instability model)
xtcadfcoint invest mvalue, model(3) breaks(1) brkslope brkloadings nfactors(1) simulate(500)
