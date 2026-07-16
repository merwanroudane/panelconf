import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["csd"]
C.hero(
    "Cross-Section Dependence & Common Factors",
    "The engine that makes every method here 'second/third generation'. If units share "
    "unobserved common shocks and you ignore them, your tests over-reject and your estimates "
    "are inconsistent. Here is how the shocks are modelled and removed.",
    A, tag="The dependence machinery",
)

# ======================================================================
C.section("1 · Detecting dependence — the CD test", "Pesaran (2004, 2021)", A)
st.markdown(
    "Before choosing a method, test whether CSD is present. The **CD test** averages pairwise "
    "residual correlations:"
)
st.latex(r"CD=\sqrt{\frac{2T}{N(N-1)}}\sum_{i=1}^{N-1}\sum_{j=i+1}^{N}\hat\rho_{ij}\;\xrightarrow{d}\;N(0,1)")
st.markdown(
    "Reject ⇒ dependence is present ⇒ first-generation tests are off the table. Complementary "
    "tests: Breusch–Pagan LM, Pesaran scaled LM, bias-corrected LM."
)

# ======================================================================
C.section("2 · The common-factor error structure", "How dependence is generated", A)
st.markdown("The modern model attributes dependence to a few unobserved common factors:")
st.latex(r"y_{it}=\beta_i'x_{it}+u_{it},\qquad u_{it}=\gamma_i'f_t+\varepsilon_{it}")
st.markdown(
    "- $f_t$ ($r\\times1$) — **common factors** (global shocks), possibly **I(1)**.\n"
    "- $\\gamma_i$ — **loadings** (each unit's exposure).\n"
    "- $\\varepsilon_{it}$ — idiosyncratic error.\n\n"
    "The regressors themselves usually load on the same factors, $x_{it}=\\Gamma_i'f_t+v_{it}$ — "
    "which is exactly what makes the CCE proxy work."
)
# factor extraction illustration
rng = C.rng(6); T = 120; N = 8
f = np.cumsum(rng.normal(0, 1, T))
fig = go.Figure()
for i in range(N):
    lam = 0.5 + rng.random()
    y = lam*f + rng.normal(0, 0.7, T)
    fig.add_trace(go.Scatter(y=y, line=dict(color="#B7C6D6", width=1), opacity=.7, showlegend=False))
fig.add_trace(go.Scatter(y=f, name="common factor fₜ (drives them all)", line=dict(color=C.PALETTE["cyan"], width=3.4)))
C.show(fig, height=330, title="One common factor visible behind many co-moving units")

# ======================================================================
C.section("3 · Strength of dependence", "Strong, semi-weak, weak", A)
c1, c2, c3 = st.columns(3)
with c1:
    C.card("Strong", "Loadings bounded away from zero for a non-negligible fraction of units "
           "(∑|γᵢ| grows at rate N). A genuine common factor. CCE/PANIC designed for this.", A)
with c2:
    C.card("Semi-weak", "Intermediate — loadings shrink but slowly. Banerjee–Carrion (2017) "
           "study CCE performance precisely across this range.", A)
with c3:
    C.card("Weak / spatial", "Local dependence (neighbours), ∑|γᵢ| bounded. Often handled by "
           "spatial models or robust standard errors rather than factors.", A)

# ======================================================================
C.section("4 · Removing it #1 — Common Correlated Effects (CCE)", "Pesaran (2006)", A)
st.markdown(
    "The dominant remedy. **Proxy the unobserved factors by the cross-section averages** of the "
    "observables and add them as regressors. Then estimate unit-by-unit and average:"
)
st.latex(r"\hat\beta_i=(X_i'\bar M X_i)^{-1}X_i'\bar M y_i,\qquad \bar M=I-\bar Z(\bar Z'\bar Z)^{-1}\bar Z',\;\; \bar Z=[\bar y,\bar X]")
st.latex(r"\hat\beta_{CCEMG}=\frac1N\sum_i\hat\beta_i\qquad(\text{Mean Group});\qquad \hat\beta_{CCEP}\;(\text{Pooled})")
C.eqcap("M̄ projects out the factor proxy. CCEMG averages unit slopes; CCEP pools. Both need no knowledge of the number of factors.")
# CCE filtering illustration
rng = C.rng(8); T = 120
f = np.cumsum(rng.normal(0, 1, T))
zbar = f + rng.normal(0, 0.15, T)     # cross-section average ~ factor
raw = 0.8*f + rng.normal(0, 0.6, T)
resid = raw - (np.polyfit(zbar, raw, 1)[0]*zbar + np.polyfit(zbar, raw, 1)[1])
fig = go.Figure()
fig.add_trace(go.Scatter(y=raw, name="one unit's series (factor-contaminated)", line=dict(color=C.PALETTE["orange"], width=2)))
fig.add_trace(go.Scatter(y=resid, name="after CCE de-factoring (factor removed)", line=dict(color=C.PALETTE["teal"], width=2)))
C.show(fig, height=300, title="CCE proxy filters out the common factor")

# ======================================================================
C.section("5 · The remarkable KPY result — CCE with I(1) factors", "Kapetanios, Pesaran & Yamagata (2011)", A)
st.markdown(
    "KPY prove the CCE approach **remains valid even when the common factors follow unit-root "
    "(I(1)) processes** — a striking result, because the individual components diverge yet the "
    "mean-group / pooled estimators keep the **same limiting form and the same variance "
    "estimators** as in the stationary case:"
)
st.latex(r"f_t=f_{t-1}+\phi_t\;\;(\text{I}(1)),\qquad \sqrt N(\hat\beta_{CCEMG}-\beta)\xrightarrow{d}N(0,\Sigma)\;\text{ as before}")
C.callout("Why it is the linchpin",
          "This is what lets Baltagi–Feng–Wang (2025, <code>xtkpybreak</code>) treat the "
          "unobserved I(1) factors as extra regressors and then apply Bai–Perron — turning "
          "break estimation in a nonstationary factor model into ordinary linear-regression "
          "break estimation.", A)

# ======================================================================
C.section("6 · Removing it #2 — PANIC & interactive fixed effects", "Bai–Ng (2004); Bai (2009)", A)
c1, c2 = st.columns(2)
with c1:
    C.card("PANIC (Bai–Ng 2004)",
           "Extract factors by principal components on <b>differenced</b> data, re-cumulate, and "
           "test the common and idiosyncratic parts <i>separately</i> for unit roots. Answers "
           "whether non-stationarity is shared or idiosyncratic.", A)
with c2:
    C.card("Interactive FE (Bai 2009)",
           "Estimate slopes and the factor structure <i>jointly</i> by iterated principal "
           "components — the alternative to CCE used by Banerjee–Carrion factor-based tests and "
           "the CupBC/CupFM estimators.", A)
st.latex(r"\text{PANIC: } \Delta y_{it}=\lambda_i'\Delta f_t+\Delta e_{it}\;\Rightarrow\;\hat f_t,\hat e_{it}=\textstyle\sum_{s\le t}(\cdot)")

# ======================================================================
C.section("7 · When factors aren't enough — the bootstrap", "Chang (2004); sieve bootstrap", A)
st.markdown(
    "If residual dependence remains (or the number of factors is uncertain), a **bootstrap** "
    "supplies valid critical values by **preserving the contemporaneous cross-section "
    "covariance**. Two schemes recur:"
)
st.markdown(
    "- **Row (block) bootstrap** — resample entire cross-section vectors (time rows) of centred "
    "residuals, keeping the $N\\times N$ dependence intact (Carrion et al.; Westerlund 2006).\n"
    "- **Sieve bootstrap** — fit a VAR to the differenced data, resample innovations, regenerate "
    "pseudo-data (Chang 2004; Westerlund–Edgerton 2007; tFR)."
)
C.callout("Rule of thumb",
          "Use <b>factors/CCE</b> when dependence is strong and low-dimensional; add a "
          "<b>bootstrap</b> when N is not huge, T is short, or you cannot pin down the number of "
          "factors. Many of the commands here do both.", A)

C.dev_footer()
