*==============================================================*
*  04 - xtpcointegwe                                            *
*  ROLE: Panel COINTEGRATION test with breaks AND common        *
*        factors (Westerlund & Edgerton 2008).                  *
*==============================================================*
*
*  In plain words:
*    Like test 03, but it also cleans out common shocks shared by
*    all firms (cross-sectional dependence) using common factors.
*    H0 = NO cointegration.  REJECT => there IS a long-run relation.
*
*  Look for:  PD-Tau and PD-Phi statistics and their p-values.
*             Small p-value => cointegration found.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: no break, let it pick up to 2 common factors
xtpcointegwe invest mvalue, model(nobreak) maxfactors(2)

* 3) allow a single LEVEL shift in the relationship
xtpcointegwe invest mvalue, model(levelshift) maxfactors(2) graph

* 4) allow a REGIME shift (level AND slope change)
xtpcointegwe invest mvalue, model(regimeshift) maxfactors(2)
