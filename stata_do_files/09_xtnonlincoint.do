*==============================================================*
*  09 - xtnonlincoint                                           *
*  ROLE: NONLINEAR panel COINTEGRATION tests                    *
*        (Omay, Emirmahmutoglu & Denaux 2017; Fourier version). *
*==============================================================*
*
*  In plain words:
*    Tests cointegration when the adjustment back to equilibrium
*    is ASYMMETRIC (faster on one side than the other), and a
*    Fourier version for smooth breaks.
*    H0 = no cointegration.  REJECT => cointegration.
*
*  Subcommands (choose one):
*    ecm    = nonlinear error-correction test
*    fffff  = Fourier (smooth break) cointegration test
*    all    = run both
*
*  Look for:  the (modified Wald / bootstrap) statistic and p-value.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) nonlinear ECM test  (breps = bootstrap draws)
xtnonlincoint ecm invest mvalue kstock, lags(1) breps(299)

* 3) Fourier (smooth break) test, with a graph
xtnonlincoint fffff invest mvalue kstock, graph

* 4) run both at once (fix the seed so results reproduce)
xtnonlincoint all invest mvalue kstock, breps(299) seed(123)
