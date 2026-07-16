*==============================================================*
*  05 - xtpcointegboot                                          *
*  ROLE: Bootstrap panel COINTEGRATION test                     *
*        (Westerlund & Edgerton 2007).                          *
*==============================================================*
*
*  In plain words:
*    Tests cointegration and uses a BOOTSTRAP to get correct
*    critical values when firms share common shocks.
*    H0 = cointegration.  REJECT => no cointegration.
*
*  Look for:  the LM+ statistic, the BOOTSTRAP p-value, and the
*             bootstrap critical values (1%, 5%, 10%).
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: individual intercepts, 399 bootstrap draws
xtpcointegboot invest mvalue, model(constant) nboot(399)

* 3) add a linear trend, and draw the bootstrap distribution
xtpcointegboot invest mvalue, model(trend) nboot(399) graph
