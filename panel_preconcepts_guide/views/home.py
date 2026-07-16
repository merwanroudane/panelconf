import streamlit as st
import common as C

A = C.TOPIC["home"]
C.hero(
    "Panel Data Pre-Concepts",
    "Everything you must understand BEFORE third-generation methods — the two dimensions "
    "N and T, the basic static models, integration, the generations, cross-sectional "
    "dependence, the CSA/CCE family vs common factors, CSD tests, dummy vs Fourier, and "
    "regularization. Built as a guide for researchers.",
    A, tag="A Researcher's Guide",
)

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(
        "Third-generation panel econometrics (cross-sectional dependence **plus** structural "
        "breaks) is only learnable if the ground under it is solid. This guide is that ground. "
        "It answers, from zero:"
    )
    st.markdown(
        "- What do **N** and **T** actually change? Which estimator is valid when?\n"
        "- What are the **basic static models** (pooled, fixed effects, random effects, "
        "between, mean group) and what does each assume?\n"
        "- What are **I(0)/I(1)**, spurious regression and cointegration?\n"
        "- What defines each **generation** of panel tests?\n"
        "- What exactly is **cross-sectional dependence**, and how strong is it?\n"
        "- **CSA (cross-sectional averages) vs common factors** — what is the difference?\n"
        "- Which **CSD test** do I use — CD, LM, scaled LM, CD\\*, alpha exponent?\n"
        "- **Dummy or Fourier** for a break? And what is **regularization**?"
    )
with c2:
    C.callout(
        "Developed by",
        "<b>Dr Merwan Roudane</b><br>Author of the <b>xt*</b> panel structural-break "
        "Stata suite (100+ modules).<br>"
        '<a href="https://ideas.repec.org/f/pro1421.html">IDEAS / RePEc</a> · '
        '<a href="https://github.com/merwanroudane">GitHub</a>',
        A,
    )

C.section("The map of this guide", "How to read it", A)
roadmap = [
    ("📐 N and T", "Balanced vs unbalanced; micro vs macro panels; fixed-T vs large-T "
     "asymptotics; incidental parameters and Nickell bias.", C.TOPIC["nt"]),
    ("🧮 Basic static models", "Pooled OLS, Fixed Effects (within/LSDV), Random Effects, "
     "Between, Hausman; homogeneous vs heterogeneous slopes (MG/PMG/DFE).", C.TOPIC["static"]),
    ("📈 Integration & cointegration", "I(0) vs I(1), unit roots, spurious regression, "
     "cointegration and error correction, long-run variance.", C.TOPIC["integration"]),
    ("🧬 The three generations", "What each generation assumes and relaxes — the "
     "characteristics table.", C.TOPIC["generations"]),
    ("🌐 Cross-sectional dependence", "The common-factor error, why 1st-gen fails, and the "
     "degree of dependence (weak / semi-weak / strong, the alpha exponent).", C.TOPIC["csd"]),
    ("⚖️ CSA vs common factors", "The cross-sectional average (CCE) family — CCEMG, CCEP, "
     "CS-ARDL, CS-DL — versus the factor/PC family — PANIC, IFE, CUP-FM.", C.TOPIC["csa"]),
    ("🧪 CSD tests", "BP-LM, scaled LM, bias-corrected LM, Pesaran CD, CD*, CDw, Frees, "
     "Friedman, and the alpha-exponent estimator.", C.TOPIC["csdtests"]),
    ("🌊 Dummy vs Fourier", "Sharp vs smooth breaks — the two ways to write a break into a "
     "model, and when each wins.", C.TOPIC["dummyfourier"]),
    ("🎛️ Regularization", "Overfitting, bias–variance, ridge/lasso/fused lasso, adaptive "
     "weights — and how a penalty becomes a break detector.", C.TOPIC["regular"]),
]
cc = st.columns(3)
for i, (t_, b_, col) in enumerate(roadmap):
    with cc[i % 3]:
        C.card(t_, b_, col)

C.section("The one thing to carry forward", "Orientation", A)
C.callout(
    "Where this guide is heading",
    "Every page here is a prerequisite for one third-generation idea. <b>N and T</b> decide which "
    "asymptotics apply; <b>static models</b> give the regression that breaks; <b>integration</b> "
    "explains why levels are dangerous; <b>CSD</b> is the dependence that must be removed "
    "(by <b>CSA</b> or by <b>factors</b>); <b>dummy/Fourier/regularization</b> are the three ways "
    "to let the model break. Put together, they are third-generation panel econometrics.",
    A,
)

C.dev_footer()
