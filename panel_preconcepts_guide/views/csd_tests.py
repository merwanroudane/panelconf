import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["csdtests"]
C.hero(
    "CSD tests — all the types",
    "Before you choose an estimator you must test for cross-sectional dependence. There are more "
    "tests than most researchers realise, and each is valid in a different (N, T) regime.",
    A, tag="Diagnostics",
)

C.callout("Why this page matters",
          "Reporting 'we tested for CSD' is not enough. The <b>Breusch–Pagan LM</b> test needs "
          "N fixed and T → ∞; on a large-N panel it is badly oversized. The <b>CD</b> test works "
          "for large N. Picking the wrong one gives the wrong answer at step one of the workflow.", A)

# ================================================================
C.section("1 · The common building block", "Pairwise correlations", A)
st.markdown(
    "Every test starts from the **pairwise correlation** of the residuals of unit $i$ and unit $j$:"
)
st.latex(r"\hat\rho_{ij}=\frac{\sum_{t=1}^{T}\hat u_{it}\hat u_{jt}}{\Big(\sum_{t=1}^{T}\hat u_{it}^{2}\Big)^{1/2}\Big(\sum_{t=1}^{T}\hat u_{jt}^{2}\Big)^{1/2}}")
st.markdown(
    "The tests differ in **how they aggregate** these $N(N-1)/2$ correlations, and in what "
    "asymptotics they assume."
)
st.latex(r"H_0:\ \mathrm{Cov}(u_{it},u_{jt})=0 \ \ \forall i\neq j \qquad(\text{no cross-sectional dependence})")

# ================================================================
C.section("2 · Breusch–Pagan LM (1980)", "The original — N fixed, T → ∞", A)
st.latex(r"LM = T\sum_{i=1}^{N-1}\sum_{j=i+1}^{N}\hat\rho_{ij}^{2}\ \xrightarrow{d}\ \chi^2_{N(N-1)/2}")
c1, c2 = st.columns(2)
with c1:
    C.card("✅ Use when", "N is <b>small</b> and T is large (few countries, long series).", A)
with c2:
    C.card("❌ Fails when", "N is large: the degrees of freedom N(N−1)/2 explode and the test "
           "becomes <b>severely oversized</b> (rejects almost always).", C.PALETTE["red"])

# ================================================================
C.section("3 · Pesaran scaled LM (CD_LM)", "Standardising the LM", A)
st.latex(r"CD_{LM}=\sqrt{\frac{1}{N(N-1)}}\sum_{i=1}^{N-1}\sum_{j=i+1}^{N}\big(T\hat\rho_{ij}^{2}-1\big)\ \xrightarrow{d}\ N(0,1)")
st.markdown(
    "Rescales the LM so the limit is standard normal. Better than raw LM, but it still suffers "
    "**size distortion when N is large relative to T**, because $T\\hat\\rho_{ij}^2$ is a biased "
    "estimate of its expectation in finite $T$."
)

# ================================================================
C.section("4 · Bias-corrected scaled LM", "Fixing the finite-T bias", A)
st.latex(r"LM_{BC}=CD_{LM}-\frac{N}{2(T-1)}")
C.eqcap("Baltagi, Feng & Kao (2012): subtract the finite-T bias term. Valid for large N and T in a "
        "fixed-effects panel.")

# ================================================================
C.section("5 · Pesaran CD test — the workhorse", "Large N, any T", A)
st.latex(r"CD=\sqrt{\frac{2T}{N(N-1)}}\sum_{i=1}^{N-1}\sum_{j=i+1}^{N}\hat\rho_{ij}\ \xrightarrow{d}\ N(0,1)")
c1, c2 = st.columns(2)
with c1:
    C.card("✅ Strengths", "Valid for <b>large N</b>, even small T. Robust to structural breaks and "
           "to unit roots. The default choice in applied work. (Pesaran 2004, 2015, 2021)", A)
with c2:
    C.card("⚠️ The known weakness", "It averages <b>signed</b> correlations. If positive and "
           "negative dependence cancel out, CD can have <b>no power</b> — it may miss real "
           "dependence.", C.PALETTE["yellow"])
C.callout("What CD actually tests (2015 refinement)",
          "Pesaran (2015) reinterprets the null as <b>weak</b> cross-sectional dependence, not "
          "zero dependence. So rejecting CD means dependence is <b>strong</b> enough to matter — "
          "which is exactly the practical question.", A)

st.markdown("**The cancellation problem, visualised:**")
mode = st.radio("Dependence pattern", ["All positive", "Mixed (+ and −)"], horizontal=True)
rng = C.rng(9)
if mode == "All positive":
    rhos = rng.normal(0.45, 0.12, 400)
else:
    rhos = np.concatenate([rng.normal(0.45, 0.12, 200), rng.normal(-0.45, 0.12, 200)])
cd_val = np.mean(rhos) * np.sqrt(len(rhos))
fig = go.Figure()
fig.add_trace(go.Histogram(x=rhos, nbinsx=40, marker_color=C.PALETTE["indigo"], opacity=.8,
                           name="pairwise ρ̂ᵢⱼ"))
fig.add_vline(x=np.mean(rhos), line=dict(color=C.PALETTE["red"], width=3),
              annotation_text=f"mean ρ̂ = {np.mean(rhos):.2f}")
fig.update_layout(xaxis_title="pairwise correlation ρ̂ᵢⱼ", yaxis_title="count")
C.show(fig, height=320, title="Why signed averaging can fail")
if mode == "Mixed (+ and −)":
    C.callout("Cancellation!", "Dependence is clearly present (correlations are far from 0), but "
              "the <b>mean is ≈ 0</b>, so CD does not reject. Use the LM-family or CD* here.",
              C.PALETTE["red"])
else:
    C.callout("CD works well", "All correlations share a sign, so the average is large and CD "
              "rejects strongly.", C.PALETTE["teal"])

# ================================================================
C.section("6 · CD* — the power-corrected CD", "Pesaran & Xie", A)
st.markdown(
    "**CD\\*** applies the CD test to residuals that have been **de-factored first** (using "
    "estimated common factors). It fixes both problems: it removes the strong factor (so the null "
    "of *weak* dependence is tested properly) and restores power. In Stata: `xtcd2, pca(#)`."
)
st.latex(r"CD^{*}=CD\big(\text{residuals after removing } \hat r \text{ estimated factors}\big)")

# ================================================================
C.section("7 · Non-parametric alternatives", "Frees and Friedman", A)
c1, c2 = st.columns(2)
with c1:
    C.card("Frees (1995)", "Aggregates <b>squared rank</b> correlations — so it is immune to the "
           "sign-cancellation problem that hurts CD. Uses a Q-distribution.", A)
with c2:
    C.card("Friedman (1937)", "Based on Spearman <b>rank</b> correlations; a non-parametric "
           "alternative for small N.", A)
st.latex(r"\text{Frees: } R_{AVE}^{2}=\frac{2}{N(N-1)}\sum_{i<j}\hat r_{ij}^{2},\qquad \hat r_{ij}=\text{rank correlation}")

# ================================================================
C.section("8 · Measuring the degree: the alpha exponent", "Beyond yes/no", A)
st.markdown(
    "Bailey, Kapetanios & Pesaran estimate the **exponent $\\alpha$** itself, turning the binary "
    "question into a measurement:"
)
st.latex(r"\sum_{i=1}^{N}|\gamma_i|=O(N^{\alpha}),\qquad \hat\alpha \text{ estimated from the cross-section variance of the averages}")
st.markdown(
    "- $\\hat\\alpha \\approx 1$ → **strong** dependence (a genuine factor) → use CCE/PANIC.\n"
    "- $\\hat\\alpha \\approx 0.5$ → **weak** dependence → robust standard errors may suffice.\n"
    "This is the modern, *quantitative* answer to 'how dependent is my panel?'"
)

# ================================================================
C.section("9 · The decision table", "Which test to use", A)
st.markdown(
    "| Test | Statistic aggregates | Valid when | Weakness | Stata |\n"
    "|---|---|---|---|---|\n"
    "| Breusch–Pagan LM | $T\\sum\\hat\\rho^2$ | **small N**, large T | explodes for large N | `xttest2` |\n"
    "| Scaled LM ($CD_{LM}$) | standardised $\\sum(T\\hat\\rho^2-1)$ | N, T large | size distortion, N≫T | `xtcsd` |\n"
    "| Bias-corrected LM | scaled LM − bias | large N and T (FE) | needs FE structure | — |\n"
    "| **Pesaran CD** | $\\sum\\hat\\rho$ (signed) | **large N**, any T | sign cancellation | `xtcd2`, `xtcsd, pesaran` |\n"
    "| CD\\* | CD on de-factored residuals | large N | needs r̂ | `xtcd2, pca(#)` |\n"
    "| Frees | squared **rank** correlations | small–moderate N | non-parametric | `xtcsd, frees` |\n"
    "| Friedman | rank correlations | small N | low power | `xtcsd, friedman` |\n"
    "| α exponent | measures strength | large N | not a test, an estimate | — |"
)

C.callout("Practical recipe",
          "Run <b>Pesaran CD</b> first (it is the default and robust). If it does <b>not</b> reject "
          "but you suspect dependence, check <b>Frees</b> (immune to cancellation) and <b>CD*</b>. "
          "If N is small, use the <b>LM</b> family. Report the test, the statistic, and the "
          "p-value — then choose CCE/factor methods accordingly.", A)

C.dev_footer()
