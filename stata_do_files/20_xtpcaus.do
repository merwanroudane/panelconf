*==============================================================*
*  20 - xtpcaus                                                 *
*  ROLE: Panel Granger CAUSALITY tests —                        *
*        PFTY  = Panel Fourier Toda-Yamamoto                    *
*        PQC   = Panel Quantile Causality                       *
*        (Yilanci & Gorus 2020; Emirmahmutoglu & Kose 2011;     *
*         Toda & Yamamoto 1995; Dumitrescu & Hurlin 2012).      *
*==============================================================*
*
*  In plain words:
*    "Does x help predict y?"  That is Granger causality.
*    - PFTY: adds Fourier terms (so smooth breaks do not fool the
*            test) and uses the Toda-Yamamoto trick, so you do NOT
*            need to worry about unit roots first.
*    - PQC:  tests causality at different QUANTILES — x may cause y
*            only in bad times, or only in good times.
*
*  IMPORTANT: causality has a DIRECTION. Always run it BOTH ways.
*
*  Look for:  the panel statistic and its BOOTSTRAP p-value.
*             Small p-value => x Granger-causes y.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

*    NOTE: nboot() = bootstrap draws. We use 199 here so the file runs
*    fast while you learn. For results you will publish, use 999 or more.

* 2) direction 1: does mvalue cause invest?
*    (first variable = the one being explained)
xtpcaus invest mvalue, test(pfty) pmax(2) kmax(3) dmax(1) nboot(199) seed(12345)

* 3) direction 2: does invest cause mvalue?  (reverse the order)
xtpcaus mvalue invest, test(pfty) pmax(2) kmax(3) dmax(1) nboot(199) seed(12345)

* 4) quantile causality: is the effect different in low / middle /
*    high quantiles?
xtpcaus invest mvalue, test(pqc) pmax(2) nboot(199) quantiles(0.25 0.5 0.75) seed(54321)

* 5) (optional) use the Schwarz criterion instead of AIC for lag selection:
* xtpcaus invest mvalue, test(pfty) pmax(2) kmax(3) dmax(1) nboot(199) ic(sbc) seed(12345)
