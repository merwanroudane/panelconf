*==============================================================*
*  16 - xtpvarcoint                                             *
*  ROLE: Panel VAR with COINTEGRATION, structural breaks and    *
*        cross-section dependence.                              *
*==============================================================*
*
*  In plain words:
*    A full panel VAR toolbox: pick the lag length, test for
*    cointegration, estimate the model, and get impulse responses.
*
*  Subcommands (choose one):
*    speci  = choose the lag length
*    pcoint = panel cointegration test
*    pvar   = estimate the panel VAR
*    pvec   = estimate the panel VECM (with cointegration)
*    irf    = impulse-response functions (after estimation)
*    fevd   = variance decomposition (after estimation)
*
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) choose the lag length (try lags 1 to 4)
xtpvarcoint speci var invest mvalue kstock, lagset(1 2 3 4)

* 3) panel cointegration test (Johansen type), 2 lags
xtpvarcoint pcoint invest mvalue kstock, method(JO) lags(2) type(Case3)

* 4) estimate the panel VECM with 1 cointegrating relation
xtpvarcoint pvec invest mvalue kstock, lags(2) rank(1) type(Case3)

* 5) impulse responses over 20 periods (run after estimation)
xtpvarcoint irf, horizon(20)
