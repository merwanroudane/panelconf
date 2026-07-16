import streamlit as st
import common as C

A = C.TOPIC["software"]
C.hero(
    "Stata Software Map",
    "Every concept in this guide is implemented. Here are the 14 break-in-panels commands "
    "from the xt* suite — what each tests or estimates, and the exact syntax — plus the "
    "workflow that ties them together.",
    A, tag="From theory to Stata",
)
C.callout("Author",
          "The commands below were developed by <b>Dr Merwan Roudane</b> and are published on the "
          '<a href="https://ideas.repec.org/f/pro1421.html">IDEAS/RePEc</a> archive (100+ modules, '
          "Top-5% author).", A)

tab1, tab2, tab3 = st.tabs(["🧪 Tests & detection", "📐 Estimators", "🧭 Workflow & syntax"])

with tab1:
    C.section("Tests / detection — breaks in panel data", "7 commands", A)
    tests = [
        ("xtpqroot", "Panel quantile unit-root tests with common shocks & structural breaks (CIPS(τ) + Fourier/LST tFR)", "H₀: unit root", "Yang–Wei–Cai 2022; Corakci–Omay 2023"),
        ("xtpkpss", "Panel KPSS stationarity test with multiple structural breaks (level/trend), Z(hom)/Z(het)", "H₀: stationary", "Carrion-i-Silvestre et al. 2005"),
        ("xtlmbreak", "Panel LM cointegration test with multiple structural breaks in level & trend", "H₀: cointegration", "Westerlund 2006"),
        ("xtpcointegwe", "Panel cointegration with breaks & common factors (PD-τ / PD-φ)", "H₀: no cointegration", "Westerlund–Edgerton 2008"),
        ("xtpcointegboot", "Bootstrap panel cointegration (LM⁺ from FM-OLS, sieve bootstrap)", "H₀: cointegration", "Westerlund–Edgerton 2007"),
        ("xtbreakcoint / xtccecoint / xtcadfcoint", "Panel cointegration with structural breaks & CSD (2015 / 2017 CCE / 2025 instabilities)", "H₀: no cointegration", "Banerjee–Carrion 2015/2017/2025"),
        ("xtnonlincoint", "Nonlinear ECM-based panel cointegration test, asymmetric adjustment", "H₀: no cointegration", "Omay–Emirmahmutoglu–Denaux 2017"),
        ("xtgets", "Panel GETS indicator saturation for structural-break detection", "detection", "GETS / IIS"),
    ]
    for name, desc, null, ref in tests:
        C.card(name, f"{desc}<br><span style='color:#8A97A6'>{null} · {ref}</span>", A)

with tab2:
    C.section("Estimators — breaks in panel data", "7 commands", A)
    ests = [
        ("xtbreakmodel", "Heterogeneous structural breaks: GAGFL (groups), PLS (common), BFK (sequential), SaRa (nonparametric)", "Okui–Wang 2021; Qian–Su 2016; BFK 2016; Li–Xiao–Chen"),
        ("xtcbc", "Coefficient-by-coefficient breaks (CBCL); each coefficient breaks on its own schedule", "Kaddoura 2025"),
        ("xtkpybreak", "CCE under I(1) factors + multiple breaks in slopes AND factor loadings", "KPY 2011; Baltagi–Feng–Wang 2025"),
        ("xtbfkbreak", "Common breaks in heterogeneous panels with CCE and (optional) endogenous regressors", "Baltagi–Feng–Kao 2016/2019"),
        ("xtquantilebreak", "Shrinkage quantile regression with multiple structural breaks across quantiles", "Zhang–Zhu–Feng–He 2022"),
        ("xtpvarcoint", "Panel VAR with cointegration, structural breaks & cross-sectional dependence", "panel VAR + breaks"),
        ("xtdynestimb", "Dynamic linear panel estimators robust to breaks, long-T over-ID, and CSD", "dynamic panel + breaks"),
    ]
    for name, desc, ref in ests:
        C.card(name, f"{desc}<br><span style='color:#8A97A6'>{ref}</span>", A)

with tab3:
    C.section("The recommended workflow", "Order a referee expects", A)
    steps = [
        ("1 · Cross-section dependence", "Pesaran CD, Breusch–Pagan LM. If CD rejects, first-generation tools are invalid.", "xtcd2 / built-in"),
        ("2 · Test & date the breaks", "Bai–Perron on the deterministic part; if breaks exist, go 3ʳᵈ-generation.", "xtbreak / xtgets"),
        ("3 · Unit-root / stationarity, break- & CSD-robust", "PANIC-with-breaks or panel KPSS; report the null direction and break dates.", "xtpkpss · xtpqroot"),
        ("4 · Number of common factors", "Bai–Ng ICp2 — is non-stationarity common or idiosyncratic?", "inside the commands"),
        ("5 · Cointegration with breaks", "Match the break in the equilibrium to a real regime change.", "xtpcointegwe · xtbreakcoint · xtlmbreak"),
        ("6 · Estimate break-dated coefficients", "Recover where the slopes shift and to what.", "xtkpybreak · xtcbc · xtbreakmodel"),
        ("7 · Interpret the long-run relation", "Read adjustment speed and shifted long-run coefficients against the dated regime change.", "CUP-FM / PMG"),
    ]
    for title, body, cmd in steps:
        C.card(title, f"{body}<br><span class='chip' style='--chipbg:#EEF4FF;--chipfg:#1C7ED6;--chipfg33:#1C7ED644'>{cmd}</span>", A)

    C.section("Copy-paste demo", "pennxrate + Grunfeld", A)
    st.code(
        """webuse pennxrate, clear
xtset id year

* ---- testing half (all CSD-robust) ----
xtpkpss        y,   model(constbreak) maxbreaks(3) graph
xtpqroot       y,   quantile(0.1 0.5 0.9) cdtest individual
xtpqroot       y,   fourier model(trendshift) bootreps(2000)
xtpcointegwe   y x, model(regimeshift) maxfactors(3) graph
xtpcointegboot y x, model(constant) nboot(399)

* ---- estimation half ----
xtkpybreak break y x, nbreaks(1) breakplot coefevolution

webuse grunfeld, clear
xtset company year
xtbreakmodel invest mvalue kstock, method(pls)
xtbreakmodel invest mvalue,        method(gagfl) groups(2)
xtcbc        invest mvalue kstock, graph""",
        language="stata",
    )

C.dev_footer()
