*==============================================================*
*  07 - xtccecoint                                              *
*  ROLE: Panel COINTEGRATION test using Common Correlated       *
*        Effects (CCE)  (Banerjee & Carrion-i-Silvestre 2017).  *
*==============================================================*
*
*  In plain words:
*    A CADF-type cointegration test. It removes common shocks by
*    adding cross-section averages (the CCE idea), then tests the
*    residuals. H0 = no cointegration. REJECT => cointegration.
*
*  Look for:  the CADF_P panel statistic and its p-value.
*
*  Options you will see:
*    model(1) = intercept, model(2) = intercept + trend
*    nfactors(#) = number of common factors to remove
*    plags(#)    = lags in the ADF part
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: intercept, 1 common factor, 1 lag
xtccecoint invest mvalue, model(1) nfactors(1) plags(1)

* 3) intercept + trend, more factors
xtccecoint invest mvalue kstock, model(2) nfactors(2) plags(1)

* 4) draw the plot and save it
xtccecoint invest mvalue, model(1) nfactors(1) plags(1) plot
