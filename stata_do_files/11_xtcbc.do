*==============================================================*
*  11 - xtcbc                                                   *
*  ROLE: ESTIMATE breaks COEFFICIENT-BY-COEFFICIENT             *
*        (each x can break at its own dates)  (Kaddoura 2025).  *
*==============================================================*
*
*  In plain words:
*    Test 10 breaks all coefficients together. This one lets EACH
*    coefficient break on its OWN schedule, and leaves the ones
*    that never change unbroken. Great when only some effects shift.
*
*  Look for:  a per-coefficient list of breaks (some may say "none")
*             and the regime-by-regime estimates.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run, with the diagnostic graphs
xtcbc invest mvalue kstock, graph

* 3) same, but also remove common shocks (cross-section demeaning)
xtcbc invest mvalue kstock, csdemean graph
