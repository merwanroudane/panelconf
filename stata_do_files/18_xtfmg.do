*==============================================================*
*  18 - xtfmg                                                   *
*  ROLE: Second-generation heterogeneous panel ESTIMATORS with  *
*        individual and common shocks — including the Fourier   *
*        CCE Mean Group (F-CCEMG).                              *
*        (Guliyev 2026; Pesaran & Smith 1995; Pesaran 2006).    *
*==============================================================*
*
*  In plain words:
*    Estimates the AVERAGE slope when firms share common shocks
*    (cross-sectional dependence) AND may break at DIFFERENT dates.
*    The Fourier terms absorb the breaks; the cross-section
*    averages remove the common shock.
*
*  Sub-commands (choose one):
*    fe      = pooled fixed effects (the simple benchmark)
*    mg      = Mean Group (average of the unit slopes)
*    ccemg   = CCE Mean Group (removes common shocks)
*    surmg   = SUR Mean Group
*    fsurmg  = Fourier SUR Mean Group
*    fccemg  = Fourier CCE Mean Group  <- the main one
*    all     = run all six and compare in one table
*    map     = tells you WHICH estimator your data needs
*    breaks  = tests each unit for a structural break (sup-Wald)
*
*  Look for:  the mean slope, its standard error, and (for map)
*             the recommended estimator.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) START HERE: let the command diagnose your panel and recommend
*    an estimator (checks cross-sectional dependence)
xtfmg map invest mvalue kstock

* 3) does any firm have a structural break? (sup-Wald test per firm)
xtfmg breaks invest mvalue kstock, plot

* 4) the simplest estimator: Mean Group (no common shocks removed)
xtfmg mg invest mvalue kstock

* 5) CCE Mean Group: removes the common shock
xtfmg ccemg invest mvalue kstock

* 6) Fourier CCE Mean Group: common shock removed AND breaks absorbed
xtfmg fccemg invest mvalue kstock, heteroplot fourierplot

* 7) compare all six estimators in one journal-style table
xtfmg all invest mvalue kstock, coefplot
