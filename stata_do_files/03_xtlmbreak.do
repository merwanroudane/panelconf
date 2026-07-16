*==============================================================*
*  03 - xtlmbreak                                               *
*  ROLE: Panel COINTEGRATION test (LM) that allows MULTIPLE     *
*        structural breaks in level and trend (Westerlund 2006).*
*==============================================================*
*
*  In plain words:
*    Tests whether y and x share a long-run relationship.
*    H0 = cointegration (there IS a long-run relation).
*    REJECT => no cointegration.
*    The relationship's level/trend is allowed to break.
*
*  Look for:  the Z statistic and its p-value.
*             Small p-value => reject cointegration.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: intercept only, no break
xtlmbreak invest mvalue, model(intercept)

* 3) allow a linear trend
xtlmbreak invest mvalue, model(trend)

* 4) allow LEVEL breaks (up to 2), and draw the graph
xtlmbreak invest mvalue, model(levelbreak) maxbreaks(2) graph

* 5) allow LEVEL and TREND breaks
xtlmbreak invest mvalue, model(trendbreak) maxbreaks(2)
