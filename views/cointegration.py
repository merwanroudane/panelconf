import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["coint"]
C.hero(
    "Panel Cointegration Tests with Structural Breaks",
    "The long-run equilibrium itself can shift. These tests decide whether a genuine "
    "long-run relation survives — allowing its level, slope, and factor loadings to break — "
    "while remaining valid under cross-sectional dependence.",
    A, tag="Testing · Long-run relations",
)

C.callout("Read the null before the p-value",
          "Half of these test <b>H₀: cointegration</b> (residual/LM based) and half test "
          "<b>H₀: no cointegration</b> (ECM / factor based). 'Reject' means opposite things. "
          "This is the single most common misreading in applied panels.", A)

# regime-shift cointegration illustration
rng = C.rng(7); T = 200; TB = 110
x = np.cumsum(rng.normal(0, 1, T))
e = np.zeros(T)
for k in range(1, T):
    e[k] = 0.55*e[k-1] + rng.normal(0, 0.6)
beta = np.where(np.arange(T) >= TB, 1.3, 0.7)
alpha = np.where(np.arange(T) >= TB, 2.5, 0.5)
y = alpha + beta*x + e
fig = go.Figure()
fig.add_trace(go.Scatter(y=y, name="y", line=dict(color=C.PALETTE["violet"], width=2)))
fig.add_trace(go.Scatter(y=alpha+beta*x, name="shifting long-run α+β·x", line=dict(color=C.PALETTE["teal"], width=2)))
fig.add_vline(x=TB, line=dict(color=C.PALETTE["red"], dash="dash"), annotation_text="regime shift T_B")
C.show(fig, height=330, title="Regime-shift cointegration: the equilibrium moves at T_B")

# ======================================================================
C.section("1 · Westerlund (2006) — LM test with multiple breaks", "OBES 68 · xtlmbreak", A)
st.markdown(
    "An **LM test for the null of cointegration** that extends McCoskey–Kao (1998) to allow "
    "an **unknown number of breaks in both the level and the trend**, possibly at "
    "**different dates for different units**, and endogenous regressors. The cointegrating "
    "regression with $m_i$ breaks:"
)
st.latex(r"y_{it}=\alpha_i+\sum_{k}\theta_{ik}DU_{ikt}+\beta_i t+\sum_k\delta_{ik}DT_{ikt}+\gamma_i'x_{it}+z_{it},\quad z_{it}=\sum_{s\le t}u_{is}")
st.latex(r"LM_i=\frac{1}{T^2}\sum_{t}\frac{S_{it}^2}{\hat\omega_i^2},\qquad Z(M)=\frac{\sqrt N(\overline{LM}-\bar\mu)}{\bar\sigma}\xrightarrow{d}N(0,1)")
C.eqcap("Sᵢₜ = partial sums of the regression residuals. Right-tail rejection ⇒ no cointegration. Breaks/dates estimated by SSR minimisation; CSD via bootstrap.")
st.code("xtlmbreak y x, ...        // panel LM cointegration, multiple breaks (level & trend)", language="stata")

# ======================================================================
C.section("2 · Westerlund–Edgerton — factor & bootstrap versions", "2007, 2008 · xtpcointegwe / xtpcointegboot", A)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Westerlund–Edgerton (2008)** — `xtpcointegwe`")
    st.markdown(
        "Individual ADF regressions on the cointegrating residuals, augmented with break "
        "dummies; **CSD via a common-factor structure** estimated by principal components "
        "(number of factors by Bai–Ng ICp1). Two standardised statistics:"
    )
    st.latex(r"PD_\tau,\;PD_\phi\;\xrightarrow{d}\;N(0,1)")
    C.eqcap("PD-τ (t-ratio based), PD-φ (coefficient based). H₀: no cointegration; left-tail rejection. Models: nobreak / levelshift / regimeshift.")
with c2:
    st.markdown("**Westerlund–Edgerton (2007)** — `xtpcointegboot`")
    st.markdown(
        "The McCoskey–Kao **LM⁺** statistic from **FM-OLS** residuals (adjusting for endogeneity "
        "and serial correlation). Because asymptotic CVs are poorly sized under CSD, a "
        "**sieve bootstrap** (VAR on differences, resample innovations) supplies critical values:"
    )
    st.latex(r"LM^{+}=\frac{1}{N}\sum_i\frac{1}{T^2}\sum_t\frac{S_{it}^2}{\hat\omega_i^2}")
    C.eqcap("H₀: cointegration; right-tail rejection. Both asymptotic and bootstrap p-values reported.")
st.code("xtpcointegwe y x, model(regimeshift) maxfactors(3) graph   // factors + break\n"
        "xtpcointegboot y x, model(constant) nboot(399)             // sieve bootstrap", language="stata")

# ======================================================================
C.section("3 · Banerjee & Carrion-i-Silvestre — the trilogy", "2015 · 2017 · 2025", A)
st.markdown(
    "Three papers that progressively unify **structural breaks + cross-sectional dependence** "
    "for the null of **no cointegration**, using cross-section averages / factors to control "
    "dependence."
)
c1, c2, c3 = st.columns(3)
with c1:
    C.card("2015 (JAE) → xtbreakcoint",
           "Cointegration in panel data with structural breaks and cross-section dependence. "
           "Test statistics valid when one or both features are present; breaks in the "
           "deterministic component; factors control CSD.", A)
with c2:
    C.card("2017 (JTSA) → xtccecoint",
           "Testing panel cointegration using <b>CCE</b> estimators. Consistent estimation of the "
           "long-run average parameter via cross-section averages under strong/semi-weak/weak "
           "dependence; a CCE-based cointegration statistic.", A)
with c3:
    C.card("2025 (JBES) → xtcadfcoint",
           "Cointegration testing with <b>structural instabilities</b>: (possibly unknown) "
           "multiple breaks affecting the <b>deterministic component, the cointegrating vector, "
           "AND the factor loadings</b> simultaneously. Individual & panel CADF statistics.", A)
st.markdown("The common structure (2025, most general):")
st.latex(r"y_{it}=D_{it}(\text{breaks})+\theta_i'x_{it}(\text{breaks})+\gamma_i(\text{breaks})'F_t+e_{it}")
st.latex(r"\text{test } H_0:\; e_{it}\sim I(1)\ (\text{no coint.})\quad\text{vs}\quad H_1:\; e_{it}\sim I(0)")
C.eqcap("Defactored CADF-type statistic on the residuals; cross-section averages remove F_t; break dates estimated by SSR. Left-tail rejection ⇒ cointegration.")
st.code("xtbreakcoint y x, ...     // Banerjee-Carrion (2015)\n"
        "xtccecoint  y x, ...      // Banerjee-Carrion (2017), CCE\n"
        "xtcadfcoint y x, ...      // Banerjee-Carrion (2025), instabilities + CSD", language="stata")

# ======================================================================
C.section("4 · Nonlinear ECM-based cointegration", "Omay, Emirmahmutoglu & Denaux (2017) · xtnonlincoint", A)
st.markdown(
    "The first **nonlinear error-correction** panel cointegration test. Adjustment toward "
    "equilibrium is **asymmetric** — modelled with a logistic transition so that the speed of "
    "correction differs above vs below the equilibrium. A modified Wald statistic tests the ECM "
    "term; CSD is handled by a **sieve bootstrap**:"
)
st.latex(r"\Delta y_{it}=\phi_i\,\big[1+\exp(-\gamma_i (e_{i,t-1}-c_i))\big]^{-1} e_{i,t-1}+\text{(short-run)}+\varepsilon_{it}")
C.eqcap("H₀: no cointegration (φᵢ = 0 ∀i). The logistic term makes correction regime-dependent — fast for large disequilibria, slow for small ones.")

# ======================================================================
C.section("5 · Single-equation ancestors", "Gregory–Hansen (1996); Westerlund (2007) ECM", A)
c1, c2 = st.columns(2)
with c1:
    C.card("Gregory–Hansen (1996)",
           "The time-series root: ADF / Zₜ / Zₐ on residuals allowing a <b>regime shift</b>, break "
           "date = argmin of the statistic. Models: level shift (C), level+trend (C/T), regime "
           "shift (C/S). The template for regime-shift cointegration.", A)
with c2:
    C.card("Westerlund (2007) ECM",
           "Error-correction panel tests Gₜ, Gₐ (group-mean) and Pₜ, Pₐ (pooled): test "
           "cointegration through the significance of the adjustment speed φᵢ. Second-generation "
           "(bootstrap CSD); the natural base to bolt a break onto.", A)
st.latex(r"\text{ECM: } \Delta y_{it}=\delta_i+\phi_i(y_{i,t-1}-\beta_i'x_{i,t-1})+\dots\;;\quad H_0:\phi_i=0\;(\text{no coint.})")

# ======================================================================
C.section("6 · The null-direction cheat-sheet", "Keep this on screen", A)
st.markdown(
    "| Test | Command | H₀ | Reject ⇒ | CSD via |\n"
    "|---|---|---|---|---|\n"
    "| Westerlund (2006) LM | `xtlmbreak` | cointegration | no cointegration | bootstrap |\n"
    "| Westerlund–Edgerton 2008 | `xtpcointegwe` | no cointegration | cointegration | common factors |\n"
    "| Westerlund–Edgerton 2007 | `xtpcointegboot` | cointegration | no cointegration | sieve bootstrap |\n"
    "| Banerjee–Carrion 2015 | `xtbreakcoint` | no cointegration | cointegration | factors |\n"
    "| Banerjee–Carrion 2017 | `xtccecoint` | no cointegration | cointegration | CCE |\n"
    "| Banerjee–Carrion 2025 | `xtcadfcoint` | no cointegration | cointegration | CCE + factors |\n"
    "| Nonlinear ECM | `xtnonlincoint` | no cointegration | cointegration | sieve bootstrap |"
)

C.dev_footer()
