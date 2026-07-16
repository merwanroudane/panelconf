*==============================================================*
*  14 - xtquantilebreak                                         *
*  ROLE: ESTIMATE breaks in a panel QUANTILE regression         *
*        (breaks can differ across quantiles)                   *
*        (Zhang, Zhu, Feng & He 2022).                          *
*==============================================================*
*
*  In plain words:
*    Like test 10, but at chosen quantiles of y. It finds breaks
*    that may look different in the low, middle and high parts of
*    the distribution - useful when effects differ in good vs bad
*    outcomes.
*
*  Look for:  the break dates per quantile and the regime estimates.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: just the median quantile (fast)
xtquantilebreak invest mvalue kstock, quantiles(0.5)

* 3) three quantiles (low, middle, high) with the break-intensity heatmap
*    (more quantiles = a bit slower; each takes a few seconds)
xtquantilebreak invest mvalue kstock, quantiles(0.25 0.5 0.75) heatmap
