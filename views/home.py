import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["home"]
C.hero(
    "Structural Breaks in Panel Data",
    "A deep, self-contained guide to the pre-concepts, tests, estimators and methods "
    "for structural change in panel data — for every researcher who needs to get it right.",
    A,
    tag="A Researcher's Guide",
)

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(
        "This guide walks from **first principles** to the **research frontier**. "
        "It starts by explaining every pre-concept the founding papers assume — "
        "integration, spurious regression, cointegration, cross-sectional dependence, "
        "common factors, deterministic components, and what a *break* actually is — "
        "and then explains, in depth and with the mathematics, each **test**, "
        "**estimator** and **method** that copes with structural change in panels."
    )
    st.markdown(
        "Everything is organised around one modern principle: a credible panel study "
        "must survive **three** complications at once — **non-stationarity**, "
        "**cross-sectional dependence**, and **structural breaks**. The tools below "
        "are exactly those that do."
    )
with col2:
    C.callout(
        "Developed by",
        "<b>Dr Merwan Roudane</b><br>Author of the <b>xt*</b> panel structural-break "
        "Stata suite (100+ modules).<br>"
        '<a href="https://ideas.repec.org/f/pro1421.html">IDEAS / RePEc</a> · '
        '<a href="https://github.com/merwanroudane">GitHub</a>',
        A,
    )

# ----------------------------------------------------------------------
C.section("The three complications, in one picture", "Why this field exists", A)
st.markdown(
    "Below: five units of a panel. Toggle each complication to see what it does to the data — "
    "and why first-generation tools break down when all three are present at once."
)

c1, c2, c3 = st.columns(3)
csd = c1.toggle("Cross-sectional dependence", value=True, help="A shared common factor")
brk = c2.toggle("Structural break", value=True, help="A regime shift at T_B")
ns = c3.toggle("Non-stationarity", value=True, help="Unit-root (random-walk) dynamics")

rng = C.rng(11)
N, T = 5, 120
TB = 60
t = np.arange(T)
F = np.cumsum(rng.normal(0, 1, T)) if ns else rng.normal(0, 1, T)
fig = go.Figure()
cols = [C.PALETTE[k] for k in ["indigo", "teal", "pink", "orange", "grape"]]
for i in range(N):
    lam = 0.6 + rng.random() * 0.9
    idio = np.cumsum(rng.normal(0, 0.6, T)) if ns else rng.normal(0, 0.7, T)
    shift = (1.8 + rng.random() * 1.2) * (1 if rng.random() < .5 else -1)
    y = (0.0 + (lam * F if csd else 0) + idio
         + (np.where(t >= TB, shift, 0.0) if brk else 0.0))
    fig.add_trace(go.Scatter(x=t, y=y, mode="lines", name=f"unit {i+1}",
                             line=dict(color=cols[i], width=2)))
if brk:
    fig.add_vline(x=TB, line=dict(color=C.PALETTE["red"], dash="dash", width=2),
                  annotation_text="break T_B", annotation_position="top")
C.show(fig, height=380)

st.markdown(
    "- **CSD on** → the series move *together* (they share the factor). Pooling as if "
    "independent gives wrong standard errors and over-rejection.\n"
    "- **Break on** → every series jumps at `T_B`. A stationary series around a shifted "
    "mean *looks* like a unit root (the **Perron critique**).\n"
    "- **Non-stationarity on** → the series wander (integrated). Levels can't be used "
    "in naïve regressions without risking **spurious** results."
)

# ----------------------------------------------------------------------
C.section("The map of this guide", "How to read it", A)
roadmap = [
    ("📚 Preliminary Concepts", "Integration, spurious regression, cointegration, CSD, factors, deterministics — the language of every paper here.", C.TOPIC["preliminaries"]),
    ("🧱 Anatomy of a Break", "Level vs trend vs regime shifts; single/multiple; known/unknown dates; common/heterogeneous; slope vs loading breaks.", C.TOPIC["anatomy"]),
    ("📉 Unit-Root & Stationarity Tests", "Carrion et al. panel KPSS, PANIC with breaks, quantile CIPS(τ) — testing I(1) when the panel breaks.", C.TOPIC["unitroot"]),
    ("🔗 Cointegration Tests", "Westerlund LM, Westerlund–Edgerton, Banerjee–Carrion (2015/2017/2025), nonlinear ECM — long-run relations that shift.", C.TOPIC["coint"]),
    ("🌊 Fourier & Smooth Breaks", "Flexible Fourier form, fractional frequencies, gradual vs sharp change, logistic smooth transition.", C.TOPIC["fourier"]),
    ("📐 Break Estimators", "Bai–Perron, Qian–Su, Baltagi–Feng–Kao, Okui–Wang GAGFL, SaRa, CBCL, shrinkage quantile breaks.", C.TOPIC["estimators"]),
    ("🌐 CSD & Factors", "CCE, PANIC, interactive effects, I(1) factors (KPY) — how dependence is removed.", C.TOPIC["csd"]),
    ("🎯 Break-Date Estimation", "SSR grid search, dynamic programming, sup-Wald, information criteria, super-consistency.", C.TOPIC["breakdate"]),
    ("🧰 Stata Software Map", "The 14 break-in-panels commands, syntax, and which method each implements.", C.TOPIC["software"]),
]
cc = st.columns(3)
for i, (t_, b_, col) in enumerate(roadmap):
    with cc[i % 3]:
        C.card(t_, b_, col)

# ----------------------------------------------------------------------
C.section("The founding papers", "What this guide is built on", A)
st.markdown(
    "Each concept and command is traced to its source. The core references:"
)
C.chips(
    ["Carrion-i-Silvestre, del Barrio-Castro & López-Bazo (2005)",
     "Westerlund (2006)", "Westerlund & Edgerton (2007, 2008)",
     "Kapetanios, Pesaran & Yamagata (2011)",
     "Baltagi, Feng & Kao (2016, 2019)", "Baltagi, Feng & Wang (2025)",
     "Banerjee & Carrion-i-Silvestre (2015, 2017, 2025)",
     "Okui & Wang (2021)", "Li, Xiao & Chen (SaRa)",
     "Zhang, Zhu, Feng & He (2022)", "Corakci & Omay (2023)",
     "Nazlioglu & Karul (2017)", "Olayeni, Tiwari & Wohar (2021)",
     "Omay, Emirmahmutoglu & Denaux (2017)"],
    A,
)

C.dev_footer()
