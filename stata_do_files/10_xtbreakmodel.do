*==============================================================*
*  10 - xtbreakmodel                                            *
*  ROLE: ESTIMATE structural breaks in the panel coefficients   *
*        (finds the break DATES and the coefficients in each     *
*         regime). Four methods in one command.                 *
*==============================================================*
*
*  In plain words:
*    Instead of just testing, this ESTIMATES where the slope of x
*    changes and its value before/after. Choose a method:
*      pls   = all firms share the same break dates (simple start)
*      bfk   = sequential least squares (fast)
*      sara  = nonparametric screen-and-rank (robust)
*      gagfl = firms split into groups with their own breaks
*
*  Look for:  the number of breaks, the break dates, and the
*             regime-by-regime coefficient table + graph.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest method: common breaks (pls)
xtbreakmodel invest mvalue, method(pls)

* 3) two regressors with common breaks
xtbreakmodel invest mvalue kstock, method(pls)

* 4) fast sequential method
xtbreakmodel invest mvalue, method(bfk)

* 5) groups with their own breaks (2 groups)
*    gagfl is the heaviest method. We keep nsim()/ngrid() small here so it
*    finishes fast for learning. For real work use the defaults (nsim(50)
*    ngrid(40)) or larger for more accurate group/break detection.
xtbreakmodel invest mvalue, method(gagfl) groups(2) nsim(10) ngrid(15)
