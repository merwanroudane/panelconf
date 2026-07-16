*==============================================================*
*  12 - xtkpybreak                                              *
*  ROLE: CCE estimation that stays valid with I(1) common       *
*        factors, PLUS multiple breaks in slopes and loadings    *
*        (Kapetanios-Pesaran-Yamagata 2011; Baltagi-Feng-Wang    *
*         2025).                                                *
*==============================================================*
*
*  In plain words:
*    Two jobs:
*      cce   = estimate the average slope, robust to common shocks
*              even when those shocks are non-stationary (I(1)).
*      break = on top of that, find breaks in the slopes.
*    After it runs you can use test, lincom, etc. (it is a normal
*    estimation command).
*
*  Look for:  the mean-group slope (cce); the break dates and
*             regime slopes (break).
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) CCE estimation of the average slope
xtkpybreak cce invest mvalue kstock

* 3) same, with the two diagnostic plots
xtkpybreak cce invest mvalue kstock, coefplot factorplot

* 4) estimate ONE structural break in the slopes, with plots
xtkpybreak break invest mvalue kstock, nbreaks(1) breakplot coefevolution

* after a break run you can test if a slope changed across regimes:
* test [r1]mvalue = [r2]mvalue
