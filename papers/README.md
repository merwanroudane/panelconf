# Source papers — reference index

Every method implemented in this repository traces to a published paper. This is the index:
**author, journal, and a clickable DOI** for each, plus the `xt*` command that implements it.

> **Why are the PDFs not here?**
> Almost all of these papers are published by Elsevier, Wiley, Taylor & Francis, Oxford
> University Press or distributed via JSTOR, and are **protected by copyright**. Redistributing
> them in a public repository is not permitted — JSTOR's terms, for example, prohibit it
> explicitly. Use the DOI links below: they always resolve to the publisher's official version,
> and most authors also post accepted manuscripts on their own pages or on RePEc.
>
> The one paper included here (`Karavias_Tzavalis_Zhang_2022_Econometrics.pdf`) is
> **open access under a CC BY licence**, so it can be redistributed freely.

DOIs marked ✅ were read directly from the papers themselves. Entries without a DOI give the full
citation so the paper is findable.

---

## Cross-sectional dependence & CCE

| Paper | Journal | DOI | Command |
|---|---|---|---|
| **Pesaran, M.H. (2006).** Estimation and inference in large heterogeneous panels with a multifactor error structure | *Econometrica* 74(4), 967–1012 | ✅ [10.1111/j.1468-0262.2006.00692.x](https://doi.org/10.1111/j.1468-0262.2006.00692.x) | CCE base |
| **Pesaran, M.H. (2007).** A simple panel unit root test in the presence of cross-section dependence | *J. Applied Econometrics* 22(2), 265–312 | — | CIPS base |
| **Kapetanios, G., Pesaran, M.H. & Yamagata, T. (2011).** Panels with non-stationary multifactor error structures | *J. Econometrics* 160(2), 326–348 | ✅ [10.1016/j.jeconom.2010.10.001](https://doi.org/10.1016/j.jeconom.2010.10.001) | `xtkpybreak cce` |
| **Bai, J. & Ng, S. (2004).** A PANIC attack on unit roots and cointegration | *Econometrica* 72(4), 1127–1177 | — | PANIC base |
| **Chudik, A. & Pesaran, M.H. (2015).** Common correlated effects estimation of heterogeneous dynamic panels | *J. Econometrics* 188(2) | — | CS-ARDL base |
| **Guliyev, H. (2026).** Second-generation heterogeneous panel data model with individual and common shocks (F-CCEMG, F-SURMG) | arXiv working paper | [arXiv:2606.29063](https://arxiv.org/abs/2606.29063) | `xtfmg fccemg` |

## Panel unit root / stationarity with breaks

| Paper | Journal | DOI | Command |
|---|---|---|---|
| **Carrion-i-Silvestre, J.L., del Barrio-Castro, T. & López-Bazo, E. (2005).** Breaking the panels: an application to the GDP per capita | *Econometrics Journal* 8(2), 159–175 | ✅ [JSTOR 23113636](https://www.jstor.org/stable/23113636) | `xtpkpss` |
| **Corakci, A. & Omay, T. (2023).** Is there convergence in renewable energy deployment? A new panel unit root test with smooth and sharp structural breaks | *Renewable Energy* 205, 648–662 | — | `xtpqroot, fourier` |
| **Nazlioglu, S. & Karul, C. (2017).** A panel stationarity test with gradual structural shifts | *Economic Modelling* | — | Fourier KPSS |
| **Karavias, Y., Tzavalis, E. & Zhang, H. (2022).** Missing values in panel data unit root tests | *Econometrics* 10(1), 12 | ✅ [10.3390/econometrics10010012](https://doi.org/10.3390/econometrics10010012) — **CC BY, PDF included** | `xtmunitroot` |

## Panel cointegration with breaks

| Paper | Journal | DOI | Command |
|---|---|---|---|
| **Westerlund, J. (2006).** Testing for panel cointegration with multiple structural breaks | *Oxford Bulletin of Economics and Statistics* 68(1), 101–132 | — | `xtlmbreak` |
| **Banerjee, A. & Carrion-i-Silvestre, J.L. (2015).** Cointegration in panel data with structural breaks and cross-section dependence | *J. Applied Econometrics* | — | `xtbreakcoint` |
| **Banerjee, A. & Carrion-i-Silvestre, J.L. (2017).** Testing for panel cointegration using common correlated effects estimators | *J. Time Series Analysis* 38(4), 610–636 | ✅ [10.1111/jtsa.12234](https://doi.org/10.1111/jtsa.12234) | `xtccecoint` |
| **Banerjee, A. & Carrion-i-Silvestre, J.L. (2025).** Panel data cointegration testing with structural instabilities | *J. Business & Economic Statistics* 43(1), 122–133 | ✅ [10.1080/07350015.2024.2327844](https://doi.org/10.1080/07350015.2024.2327844) | `xtcadfcoint` |
| **Omay, T., Emirmahmutoglu, F. & Denaux, Z.S. (2017).** Nonlinear error correction based cointegration test in panel data | *Economics Letters* 157, 1–4 | — | `xtnonlincoint` |
| **Olayeni, R.O., Tiwari, A.K. & Wohar, M.E. (2021).** Fractional frequency flexible Fourier form (FFFFF) for panel cointegration test | *Applied Economics Letters* 28(6), 482–486 | ✅ [10.1080/13504851.2020.1761526](https://doi.org/10.1080/13504851.2020.1761526) | FFFFF / `xtpfardl` |

## Structural-break estimators

| Paper | Journal | DOI | Command |
|---|---|---|---|
| **Bai, J. & Perron, P. (1998).** Estimating and testing linear models with multiple structural changes | *Econometrica* 66(1), 47–78 | ✅ [10.2307/2998540](https://doi.org/10.2307/2998540) | break-date engine |
| **Bai, J. & Perron, P. (2003).** Computation and analysis of multiple structural change models | *J. Applied Econometrics* 18(1), 1–22 | ✅ [10.1002/jae.659](https://doi.org/10.1002/jae.659) | dynamic programming |
| **Qian, J. & Su, L. (2016).** Shrinkage estimation of common breaks in panel data models via adaptive group fused lasso | *J. Econometrics* 191(1), 86–109 | — | `xtbreakmodel, pls` |
| **Baltagi, B.H., Feng, Q. & Kao, C. (2016).** Estimation of heterogeneous panels with structural breaks | *J. Econometrics* 191(1), 176–195 | — | `xtbreakmodel, bfk` |
| **Baltagi, B.H., Feng, Q. & Kao, C. (2019).** Structural changes in heterogeneous panels with endogenous regressors | Working paper No. 214, Syracuse CPR | — | `xtbfkbreak` |
| **Baltagi, B.H., Feng, Q. & Wang, W. (2025).** Nonstationary heterogeneous panels with multiple structural changes | *Econometric Reviews* | ✅ [10.1080/07474938.2025.2480626](https://doi.org/10.1080/07474938.2025.2480626) | `xtkpybreak break` |
| **Okui, R. & Wang, W. (2021).** Heterogeneous structural breaks in panel data models | *J. Econometrics* 220(2), 447–473 | — | `xtbreakmodel, gagfl` |
| **Li, F., Xiao, Y. & Chen, Z.** Estimation of common breaks in linear panel data models via screening and ranking algorithm | working paper | — | `xtbreakmodel, sara` |
| **Kaddoura, Y. (2025).** Estimating coefficient-by-coefficient breaks in panel data models | *J. Econometrics* 249, 106005 | — | `xtcbc` |
| **Zhang, L., Zhu, Z., Feng, X. & He, Y. (2022).** Shrinkage quantile regression for panel data with multiple structural breaks | *Canadian J. Statistics* 50(3), 820–851 | — | `xtquantilebreak` |
| **Bonhomme, S. & Manresa, E. (2015).** Grouped patterns of heterogeneity in panel data | *Econometrica* 83(3), 1147–1184 | — | GFE step of GAGFL |

## Foundations

| Paper | Journal |
|---|---|
| **Pesaran, M.H. & Smith, R. (1995).** Estimating long-run relationships from dynamic heterogeneous panels | *J. Econometrics* 68(1) — *(MG)* |
| **Pesaran, M.H., Shin, Y. & Smith, R. (1999).** Pooled mean group estimation of dynamic heterogeneous panels | *JASA* 94(446) — *(PMG)* |
| **Perron, P. (1989).** The great crash, the oil price shock, and the unit root hypothesis | *Econometrica* 57(6) — *(the Perron critique)* |
| **Nickell, S. (1981).** Biases in dynamic models with fixed effects | *Econometrica* 49(6) |
| **Gallant, A.R. (1981).** On the bias in flexible functional forms | *J. Econometrics* 15(2) — *(the Fourier basis)* |
| **Tibshirani, R. (1996, 2005).** The lasso; sparsity and smoothness via the fused lasso | *JRSS-B* 58(1); 67(1) |
| **Zou, H. (2006).** The adaptive lasso and its oracle properties | *JASA* 101(476) |

---

**Please cite the original methodological papers above when using the `xt*` commands.**

Index compiled by **Dr Merwan Roudane** — [IDEAS/RePEc](https://ideas.repec.org/f/pro1421.html) ·
[GitHub](https://github.com/merwanroudane)
