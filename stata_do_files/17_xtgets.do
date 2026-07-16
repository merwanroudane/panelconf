*==============================================================*
*  17 - xtgets                                                  *
*  ROLE: DETECT structural breaks automatically with            *
*        Indicator Saturation (General-to-Specific).            *
*==============================================================*
*
*  In plain words:
*    It searches the data and discovers WHICH units broke and WHEN,
*    by testing a large set of possible break dummies and keeping
*    only the ones that matter.
*
*  Saturation methods (pick at least one):
*    fesis = fixed-effect structural breaks (per-unit shifts)  <- most common
*    iis   = impulse (outlier) indicators
*    csis  = common structural breaks
*    tis   = trend breaks
*
*  Look for:  the retained break indicators (unit + date) and the
*             cleaned coefficient estimates.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: detect per-unit structural breaks
xtgets invest mvalue kstock, fesis effect(twoways)

* 3) a slightly looser threshold finds more breaks (t_pval = 1%)
xtgets invest mvalue kstock, fesis effect(twoways) t_pval(0.01)

* 4) also look for outliers (impulse indicators)
xtgets invest mvalue kstock, fesis iis effect(twoways) t_pval(0.01)

* 5) picture of the detected breaks (run right after xtgets)
xtgets_plot, type(breaks)
