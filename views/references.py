import streamlit as st
import common as C

A = C.TOPIC["references"]
C.hero(
    "References & Source Papers",
    "The papers this guide is built on, grouped by theme, each mapped to the Stata command "
    "that implements it. Every method above traces to a source here.",
    A, tag="Bibliography",
)

C.section("Panel unit-root & stationarity with breaks", "→ xtpkpss · xtpqroot", A)
st.markdown(
    "- **Carrion-i-Silvestre, J.L., del Barrio-Castro, T. & López-Bazo, E. (2005).** Breaking the "
    "panels: an application to the GDP per capita. *Econometrics Journal* 8(2), 159–175.  → `xtpkpss`\n"
    "- **Hadri, K. (2000).** Testing for stationarity in heterogeneous panel data. *Econometrics "
    "Journal* 3(2), 148–161.\n"
    "- **Kwiatkowski, D., Phillips, P.C.B., Schmidt, P. & Shin, Y. (1992).** Testing the null of "
    "stationarity. *Journal of Econometrics* 54(1–3), 159–178.\n"
    "- **Pesaran, M.H. (2007).** A simple panel unit root test in the presence of cross-section "
    "dependence. *Journal of Applied Econometrics* 22(2), 265–312.\n"
    "- **Yang, Z., Wei, Z. & Cai, Y. (2022).** Quantile unit root inference for panel data with "
    "common shocks. *Economics Letters* 219, 110809.  → `xtpqroot`\n"
    "- **Corakci, A. & Omay, T. (2023).** Is there convergence in renewable energy deployment? "
    "*Renewable Energy* 205, 648–662.  → `xtpqroot fourier`\n"
    "- **Nazlioglu, S. & Karul, C. (2017).** A panel stationarity test with gradual structural "
    "shifts. *Economic Modelling*.\n"
    "- **Karavias, Y., Tzavalis, E. & Zhang, H. (2022).** Missing values in panel data unit root "
    "tests. *Econometrics* 10(1), 12.  → `xtmunitroot`"
)

C.section("Panel cointegration with breaks", "→ xtlmbreak · xtpcointegwe/boot · xtbreakcoint · xtccecoint · xtcadfcoint · xtnonlincoint", A)
st.markdown(
    "- **Westerlund, J. (2006).** Testing for panel cointegration with multiple structural breaks. "
    "*Oxford Bulletin of Economics and Statistics* 68(1), 101–132.  → `xtlmbreak`\n"
    "- **Westerlund, J. & Edgerton, D.L. (2007).** A panel bootstrap cointegration test. "
    "*Economics Letters* 97(3), 185–190.  → `xtpcointegboot`\n"
    "- **Westerlund, J. & Edgerton, D.L. (2008).** A simple test for cointegration in dependent "
    "panels with structural breaks. *Oxford Bulletin of Economics and Statistics* 70(5), 665–704.  → `xtpcointegwe`\n"
    "- **Banerjee, A. & Carrion-i-Silvestre, J.L. (2015).** Cointegration in panel data with "
    "structural breaks and cross-section dependence. *Journal of Applied Econometrics*.  → `xtbreakcoint`\n"
    "- **Banerjee, A. & Carrion-i-Silvestre, J.L. (2017).** Testing for panel cointegration using "
    "common correlated effects estimators. *Journal of Time Series Analysis* 38(4), 610–636. "
    "doi:10.1111/jtsa.12234  → `xtccecoint`\n"
    "- **Banerjee, A. & Carrion-i-Silvestre, J.L. (2025).** Panel data cointegration testing with "
    "structural instabilities. *Journal of Business & Economic Statistics* 43(1), 122–133. "
    "doi:10.1080/07350015.2024.2327844  → `xtcadfcoint`\n"
    "- **Omay, T., Emirmahmutoglu, F. & Denaux, Z.S. (2017).** Nonlinear error correction based "
    "cointegration test in panel data. *Economics Letters* 157, 1–4.  → `xtnonlincoint`\n"
    "- **McCoskey, S.K. & Kao, C. (1998).** A residual-based test of the null of cointegration in "
    "panel data. *Econometric Reviews* 17(1), 57–84.\n"
    "- **Gregory, A.W. & Hansen, B.E. (1996).** Residual-based tests for cointegration in models "
    "with regime shifts. *Journal of Econometrics* 70(1), 99–126."
)

C.section("Cross-section dependence, CCE & factors", "→ xtkpybreak · xtccecoint", A)
st.markdown(
    "- **Pesaran, M.H. (2006).** Estimation and inference in large heterogeneous panels with a "
    "multifactor error structure. *Econometrica* 74(4), 967–1012.\n"
    "- **Kapetanios, G., Pesaran, M.H. & Yamagata, T. (2011).** Panels with non-stationary "
    "multifactor error structures. *Journal of Econometrics* 160(2), 326–348. "
    "doi:10.1016/j.jeconom.2010.10.001  → `xtkpybreak cce`\n"
    "- **Bai, J. & Ng, S. (2002).** Determining the number of factors in approximate factor "
    "models. *Econometrica* 70(1), 191–221.\n"
    "- **Bai, J. & Ng, S. (2004).** A PANIC attack on unit roots and cointegration. *Econometrica* "
    "72(4), 1127–1177.\n"
    "- **Bai, J. (2009).** Panel data models with interactive fixed effects. *Econometrica* 77(4), "
    "1229–1279.\n"
    "- **Chang, Y. (2004).** Bootstrap unit-root tests in panels with cross-sectional dependency. "
    "*Journal of Econometrics* 120, 263–293."
)

C.section("Break estimators for panel coefficients", "→ xtbreakmodel · xtcbc · xtbfkbreak · xtquantilebreak", A)
st.markdown(
    "- **Bai, J. & Perron, P. (1998).** Estimating and testing linear models with multiple "
    "structural changes. *Econometrica* 66(1), 47–78.\n"
    "- **Bai, J. & Perron, P. (2003).** Computation and analysis of multiple structural change "
    "models. *Journal of Applied Econometrics* 18(1), 1–22.\n"
    "- **Qian, J. & Su, L. (2016).** Shrinkage estimation of common breaks in panel data models "
    "via adaptive group fused lasso. *Journal of Econometrics* 191(1), 86–109.  → `xtbreakmodel(pls)`\n"
    "- **Baltagi, B.H., Feng, Q. & Kao, C. (2016).** Estimation of heterogeneous panels with "
    "structural breaks. *Journal of Econometrics* 191(1), 176–195.  → `xtbreakmodel(bfk)`\n"
    "- **Baltagi, B.H., Feng, Q. & Kao, C. (2019/2021).** Structural changes in heterogeneous "
    "panels with endogenous regressors.  → `xtbfkbreak`\n"
    "- **Baltagi, B.H., Feng, Q. & Wang, W. (2025).** Nonstationary heterogeneous panels with "
    "multiple structural changes. *Econometric Reviews.* doi:10.1080/07474938.2025.2480626  → `xtkpybreak`\n"
    "- **Okui, R. & Wang, W. (2021).** Heterogeneous structural breaks in panel data models. "
    "*Journal of Econometrics* 220(2), 447–473.  → `xtbreakmodel(gagfl)`\n"
    "- **Li, F., Xiao, Y. & Chen, Z.** Estimation of common breaks in linear panel data models via "
    "screening and ranking algorithm.  → `xtbreakmodel(sara)`\n"
    "- **Kaddoura, Y. (2025).** Estimating coefficient-by-coefficient breaks in panel data models. "
    "*Journal of Econometrics* 249, 106005.  → `xtcbc`\n"
    "- **Kaddoura, Y. & Westerlund, J. (2023).** Estimation of panel data models with random "
    "interactive effects and multiple structural breaks when T is fixed. *JBES* 41(3), 778–790.\n"
    "- **Zhang, L., Zhu, Z., Feng, X. & He, Y. (2022).** Shrinkage quantile regression for panel "
    "data with multiple structural breaks. *Canadian Journal of Statistics* 50(3), 820–851.  → `xtquantilebreak`\n"
    "- **Bonhomme, S. & Manresa, E. (2015).** Grouped patterns of heterogeneity in panel data. "
    "*Econometrica* 83(3), 1147–1184."
)

C.section("Fourier & smooth breaks", "→ xtpfardl · xtpqroot fourier", A)
st.markdown(
    "- **Olayeni, R.O., Tiwari, A.K. & Wohar, M.E. (2021).** Fractional frequency flexible Fourier "
    "form (FFFFF) for panel cointegration test. *Applied Economics Letters* 28(6), 482–486. "
    "doi:10.1080/13504851.2020.1761526\n"
    "- **Guliyev, H. (2026).** Second-generation heterogeneous panel data model with individual "
    "and common shocks (F-SURMG, F-CCEMG). *Working paper.*\n"
    "- **Enders, W. & Lee, J. (2012).** The flexible Fourier form and Dickey–Fuller-type unit root "
    "tests. *Economics Letters* 117(1), 196–199."
)

C.callout("Developer & citation",
          "This guide and the accompanying <b>xt*</b> Stata suite were developed by "
          "<b>Dr Merwan Roudane</b>. Please cite the original methodological papers above when "
          "using the commands. Suite: "
          '<a href="https://ideas.repec.org/f/pro1421.html">ideas.repec.org/f/pro1421</a> · '
          '<a href="https://github.com/merwanroudane">github.com/merwanroudane</a>.', A)

C.dev_footer()
