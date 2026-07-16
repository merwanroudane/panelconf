import streamlit as st
import common as C

A = C.TOPIC["references"]
C.hero(
    "References",
    "The foundational papers behind every pre-concept in this guide, grouped by theme.",
    A, tag="Bibliography",
)

C.section("Static panel models", "Foundations", A)
st.markdown(
    "- **Mundlak, Y. (1978).** On the pooling of time series and cross section data. *Econometrica* 46(1).\n"
    "- **Hausman, J.A. (1978).** Specification tests in econometrics. *Econometrica* 46(6).\n"
    "- **Nickell, S. (1981).** Biases in dynamic models with fixed effects. *Econometrica* 49(6).\n"
    "- **Pesaran, M.H. & Smith, R. (1995).** Estimating long-run relationships from dynamic "
    "heterogeneous panels. *Journal of Econometrics* 68(1). *(Mean Group)*\n"
    "- **Pesaran, M.H., Shin, Y. & Smith, R. (1999).** Pooled mean group estimation of dynamic "
    "heterogeneous panels. *JASA* 94(446). *(PMG → `xtpmg`)*\n"
    "- **Baltagi, B.H.** *Econometric Analysis of Panel Data.* Wiley. *(the standard textbook)*"
)

C.section("Integration, unit roots, cointegration", "Time-series backbone", A)
st.markdown(
    "- **Granger, C.W.J. & Newbold, P. (1974).** Spurious regressions in econometrics. "
    "*Journal of Econometrics* 2(2).\n"
    "- **Engle, R.F. & Granger, C.W.J. (1987).** Co-integration and error correction. "
    "*Econometrica* 55(2).\n"
    "- **Kwiatkowski, D., Phillips, P.C.B., Schmidt, P. & Shin, Y. (1992).** Testing the null of "
    "stationarity. *Journal of Econometrics* 54(1–3). *(KPSS)*\n"
    "- **Levin, A., Lin, C.-F. & Chu, C.-S.J. (2002).** Unit root tests in panel data. "
    "*Journal of Econometrics* 108(1). *(LLC)*\n"
    "- **Im, K.S., Pesaran, M.H. & Shin, Y. (2003).** Testing for unit roots in heterogeneous "
    "panels. *Journal of Econometrics* 115(1). *(IPS)*\n"
    "- **Hadri, K. (2000).** Testing for stationarity in heterogeneous panel data. "
    "*Econometrics Journal* 3(2).\n"
    "- **Pedroni, P. (2004); Kao, C. (1999).** Panel cointegration tests."
)

C.section("Cross-sectional dependence: the CSA / CCE family", "Averages route", A)
st.markdown(
    "- **Pesaran, M.H. (2006).** Estimation and inference in large heterogeneous panels with a "
    "multifactor error structure. *Econometrica* 74(4). *(CCE, CCEMG, CCEP)*\n"
    "- **Pesaran, M.H. (2007).** A simple panel unit root test in the presence of cross-section "
    "dependence. *Journal of Applied Econometrics* 22(2). *(CADF / CIPS)*\n"
    "- **Kapetanios, G., Pesaran, M.H. & Yamagata, T. (2011).** Panels with non-stationary "
    "multifactor error structures. *Journal of Econometrics* 160(2). *(CCE valid with I(1) factors)*\n"
    "- **Chudik, A. & Pesaran, M.H. (2015).** Common correlated effects estimation of "
    "heterogeneous dynamic panels. *Journal of Econometrics* 188(2). *(dynamic CCE, CS-ARDL)*\n"
    "- **Chudik, A., Mohaddes, K., Pesaran, M.H. & Raissi, M. (2016).** Long-run effects in large "
    "heterogeneous panels. *(CS-DL)*\n"
    "- **Guliyev, H. (2026).** Second-generation heterogeneous panel with individual and common "
    "shocks. *(F-CCEMG, F-SURMG)*"
)

C.section("Cross-sectional dependence: the factor / PC family", "Principal-components route", A)
st.markdown(
    "- **Bai, J. & Ng, S. (2002).** Determining the number of factors in approximate factor models. "
    "*Econometrica* 70(1). *(IC criteria)*\n"
    "- **Bai, J. & Ng, S. (2004).** A PANIC attack on unit roots and cointegration. "
    "*Econometrica* 72(4). *(PANIC)*\n"
    "- **Bai, J. (2009).** Panel data models with interactive fixed effects. *Econometrica* 77(4).\n"
    "- **Bai, J., Kao, C. & Ng, S. (2009).** Panel cointegration with global stochastic trends. "
    "*Journal of Econometrics* 149(1). *(CUP-FM, CUP-BC)*\n"
    "- **Moon, H.R. & Perron, B. (2004).** Testing for a unit root in panels with dynamic factors. "
    "*Journal of Econometrics* 122(1)."
)

C.section("CSD tests", "Diagnostics", A)
st.markdown(
    "- **Breusch, T.S. & Pagan, A.R. (1980).** The Lagrange multiplier test. *RES* 47(1). *(LM)*\n"
    "- **Pesaran, M.H. (2004, 2021).** General diagnostic tests for cross-sectional dependence in "
    "panels. *(CD test)* *Empirical Economics* 60.\n"
    "- **Pesaran, M.H. (2015).** Testing weak cross-sectional dependence in large panels. "
    "*Econometric Reviews* 34(6–10).\n"
    "- **Pesaran, M.H., Ullah, A. & Yamagata, T. (2008).** A bias-adjusted LM test of error "
    "cross-section independence. *Econometrics Journal* 11(1).\n"
    "- **Baltagi, B.H., Feng, Q. & Kao, C. (2012).** A Lagrange multiplier test for cross-sectional "
    "dependence in a fixed effects panel. *Journal of Econometrics* 170(1).\n"
    "- **Frees, E.W. (1995).** Assessing cross-sectional correlation in panel data. "
    "*Journal of Econometrics* 69(2).\n"
    "- **Bailey, N., Kapetanios, G. & Pesaran, M.H. (2016).** Exponent of cross-sectional "
    "dependence: estimation and inference. *Journal of Applied Econometrics* 31(6). *(the α exponent)*"
)

C.section("Breaks: dummy, Fourier, regularization", "Modelling toolkits", A)
st.markdown(
    "- **Perron, P. (1989).** The great crash, the oil price shock, and the unit root hypothesis. "
    "*Econometrica* 57(6). *(the Perron critique)*\n"
    "- **Bai, J. & Perron, P. (1998, 2003).** Estimating and testing linear models with multiple "
    "structural changes. *Econometrica* 66(1); *JAE* 18(1).\n"
    "- **Gallant, A.R. (1981).** On the bias in flexible functional forms. "
    "*Journal of Econometrics* 15(2). *(the Fourier basis)*\n"
    "- **Enders, W. & Lee, J. (2012).** The flexible Fourier form and Dickey–Fuller-type unit root "
    "tests. *Economics Letters* 117(1).\n"
    "- **Olayeni, R.O., Tiwari, A.K. & Wohar, M.E. (2021).** Fractional frequency flexible Fourier "
    "form (FFFFF) for panel cointegration. *Applied Economics Letters* 28(6).\n"
    "- **Tibshirani, R. (1996).** Regression shrinkage and selection via the lasso. *JRSS-B* 58(1).\n"
    "- **Tibshirani, R. et al. (2005).** Sparsity and smoothness via the fused lasso. *JRSS-B* 67(1).\n"
    "- **Zou, H. (2006).** The adaptive lasso and its oracle properties. *JASA* 101(476).\n"
    "- **Qian, J. & Su, L. (2016).** Shrinkage estimation of common breaks via adaptive group fused "
    "lasso. *Journal of Econometrics* 191(1).\n"
    "- **Okui, R. & Wang, W. (2021).** Heterogeneous structural breaks in panel data models. "
    "*Journal of Econometrics* 220(2). *(GAGFL)*\n"
    "- **Bonhomme, S. & Manresa, E. (2015).** Grouped patterns of heterogeneity in panel data. "
    "*Econometrica* 83(3). *(grouped fixed effects)*\n"
    "- **Kaddoura, Y. (2025).** Estimating coefficient-by-coefficient breaks in panel data models. "
    "*Journal of Econometrics* 249. *(CBC)*\n"
    "- **Zhang, L., Zhu, Z., Feng, X. & He, Y. (2022).** Shrinkage quantile regression for panel "
    "data with multiple structural breaks. *Canadian Journal of Statistics* 50(3)."
)

C.callout(
    "Developer & citation",
    "This guide was developed by <b>Dr Merwan Roudane</b>, author of the <b>xt*</b> panel "
    "structural-break Stata suite (100+ modules). Please cite the original methodological papers "
    "above when using the commands. "
    '<a href="https://ideas.repec.org/f/pro1421.html">ideas.repec.org/f/pro1421</a> · '
    '<a href="https://github.com/merwanroudane">github.com/merwanroudane</a>',
    A,
)

C.dev_footer()
