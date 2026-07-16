*==============================================================*
*  01 - xtpkpss                                                 *
*  ROLE: Panel STATIONARITY test that allows structural breaks  *
*        (Carrion-i-Silvestre, del Barrio-Castro & Lopez-Bazo,  *
*         2005).                                                *
*==============================================================*
*
*  In plain words:
*    It asks "is the series stationary?"  (that is the H0).
*    If the test REJECTS, there is evidence of a UNIT ROOT.
*    It lets each firm have its own break(s) in the mean/trend.
*
*  Look for:  Z(hom) and Z(het) statistics and their p-values.
*             A big positive value / small p-value => reject
*             stationarity (so the series looks non-stationary).
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: stationarity around a constant (no break)
xtpkpss invest, model(constant)

* 3) allow LEVEL breaks (the mean can shift at unknown dates)
*    maxbreaks(2) = search for up to 2 breaks per firm
xtpkpss invest, model(constbreak) maxbreaks(2) graph

* 4) allow LEVEL and TREND breaks
xtpkpss invest, model(trendbreak) maxbreaks(2)

* Try another variable:
xtpkpss mvalue, model(constbreak) maxbreaks(2)
