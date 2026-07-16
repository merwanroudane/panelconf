*==============================================================*
*  15 - xtdynestimb                                             *
*  ROLE: DYNAMIC panel estimators that are robust to structural *
*        breaks and cross-section dependence.                   *
*==============================================================*
*
*  In plain words:
*    For dynamic models (y depends on its own past). It can find
*    breaks and estimate the coefficients while staying robust to
*    common shocks.
*
*  Subcommands (choose one):
*    breaks  = detect the break dates
*    dd      = difference-based dynamic estimator
*    csdgmm  = GMM robust to cross-section dependence
*    ablasso = lasso-based dynamic estimator
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) first, DETECT the breaks in the series
xtdynestimb breaks invest, minlength(3)

* 3) dynamic estimator with 1 lag, and a graph
xtdynestimb dd invest, lags(1) graph graphname(g_dd)

* 4) add a regressor
xtdynestimb dd invest mvalue, lags(1) variant(full)

* 5) GMM version robust to cross-section dependence
xtdynestimb csdgmm invest mvalue, variant(system) graph graphname(g_csd)
