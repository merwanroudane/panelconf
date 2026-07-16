*==============================================================*
*  13 - xtbfkbreak                                              *
*  ROLE: ESTIMATE a common break in heterogeneous panels with   *
*        common correlated effects, allowing ENDOGENOUS         *
*        regressors  (Baltagi, Feng & Kao 2016/2019).           *
*==============================================================*
*
*  In plain words:
*    Finds a common break in the slopes while removing common
*    shocks (CCE). It can also handle a regressor that is
*    endogenous by using an instrument.
*
*  Look for:  the estimated break date and the before/after slopes.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: find ONE break, with a graph
xtbfkbreak invest mvalue, breaks(1) graph

* 3) allow up to TWO breaks, with trimming 15% off each end
xtbfkbreak invest mvalue, breaks(2) trim(0.15) graph

* 4) endogenous regressor example:
*    "invest depends on mvalue, and mvalue is instrumented by kstock"
*    syntax:  y (endogenous = instrument)
xtbfkbreak invest (mvalue = kstock), breaks(1)
