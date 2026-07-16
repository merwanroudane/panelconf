*==============================================================*
*  06 - xtbreakcoint                                            *
*  ROLE: Panel COINTEGRATION test with structural breaks and    *
*        cross-section dependence                               *
*        (Banerjee & Carrion-i-Silvestre 2015).                *
*==============================================================*
*
*  In plain words:
*    Tests for a long-run relation while ALLOWING a break and
*    controlling for common shocks with common factors.
*    H0 = no cointegration.  REJECT => cointegration.
*
*  Look for:  the test statistic and its p-value / critical values,
*             plus the estimated break date(s).
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) simplest run: constant only (no break)
*    keep maxlag small because the panel is short (T = 20)
xtbreakcoint invest mvalue kstock, model(constant) maxlag(1)

* 3) allow a single LEVEL shift
xtbreakcoint invest mvalue kstock, model(levelshift) maxlag(1)

* 4) allow a REGIME shift (level and slope), and draw the graph
xtbreakcoint invest mvalue kstock, model(regimeshift) maxlag(1) graph
