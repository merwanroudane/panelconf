*==============================================================*
*  02 - xtpqroot                                                *
*  ROLE: Panel UNIT-ROOT test across QUANTILES, and a version   *
*        with smooth + sharp breaks (Fourier).                  *
*        (Yang-Wei-Cai 2022; Corakci-Omay 2023).               *
*==============================================================*
*
*  In plain words:
*    Two tests in one command.
*    - CIPS(tau): tests a unit root at different quantiles, so you
*      can see if a series is persistent only in good or bad times.
*    - Fourier (tFR): allows the mean to bend smoothly and to jump.
*    H0 = unit root.  REJECT => the series is stationary.
*
*  Look for:  CIPS(tau) values and p-values at each quantile;
*             for Fourier, the tFR statistic vs the bootstrap CVs.
*==============================================================*

* 1) load the real data and set the panel
webuse grunfeld, clear
xtset company year

* 2) quantile unit-root test at three quantiles (low, middle, high)
*    reps() = simulations for the p-value; 200 is fine for learning
xtpqroot invest, quantile(0.25 0.5 0.75) reps(200)

* 3) also report the cross-sectional dependence (CD) test
xtpqroot invest, quantile(0.25 0.5 0.75) reps(200) cdtest

* 4) Fourier version: allows smooth AND sharp breaks
*    bootreps() = bootstrap replications; 299 is fine for learning
xtpqroot invest, fourier model(intercept) bootreps(299)
