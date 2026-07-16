import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import common as C

A = C.TOPIC["anatomy"]
C.hero(
    "Anatomy of a Structural Break",
    "Before choosing a test you must classify the break: where it sits, how many there are, "
    "whether the date is known, and whether it is shared across units and coefficients. "
    "Every method in this guide is defined by the answers.",
    A, tag="Taxonomy",
)

# ======================================================================
C.section("1 · Where the break lives — the deterministic component", "Location", A)
st.markdown(
    "Write any series as **deterministic part + stochastic part**. Breaks almost always "
    "enter through the *deterministic* part $D_{it}$:"
)
st.latex(r"y_{it} = \underbrace{D_{it}}_{\text{deterministics (breaks here)}} + \underbrace{\gamma_i' f_t}_{\text{common factor}} + \underbrace{e_{it}}_{\text{idiosyncratic}}")
st.markdown("The three classic deterministic break models (Perron's taxonomy, carried to panels):")

t = np.arange(120)
TB = 60
base = 0.03 * t
lvl = base + np.where(t >= TB, 1.6, 0.0)
trd = base + np.where(t >= TB, 0.05 * (t - TB), 0.0)
reg = base + np.where(t >= TB, 1.2 + 0.05 * (t - TB), 0.0)
fig = make_subplots(rows=1, cols=3, subplot_titles=(
    "Model A — level shift", "Model B — trend (slope) break", "Model C — regime shift (both)"))
for col, (s, c) in enumerate([(lvl, "yellow"), (trd, "orange"), (reg, "red")], start=1):
    fig.add_trace(go.Scatter(y=s, line=dict(color=C.PALETTE[c], width=2.6), showlegend=False), row=1, col=col)
    fig.add_vline(x=TB, line=dict(color="#888", dash="dash"), row=1, col=col)
C.show(fig, height=300)
c1, c2, c3 = st.columns(3)
with c1:
    st.latex(r"\text{A: } D_{it}=\mu_i+\theta_i\,\mathbf{1}\{t>T_B\}")
    C.card("Level / intercept shift", "The mean jumps; the trend slope is unchanged. "
           "<code>xtpkpss model(constbreak)</code>, <code>xtpcointegwe model(levelshift)</code>.", C.PALETTE["yellow"])
with c2:
    st.latex(r"\text{B: } D_{it}=\mu_i+\beta_i t+\delta_i (t-T_B)^{+}")
    C.card("Trend (slope) break", "The growth rate changes at T_B; the level is continuous. "
           "Common in convergence and growth studies.", C.PALETTE["orange"])
with c3:
    st.latex(r"\text{C: } D_{it}=\mu_i+\theta_i\mathbf{1}\{t>T_B\}+\beta_i t+\delta_i(t-T_B)^{+}")
    C.card("Regime shift (both)", "Level and slope both change — the most general. "
           "<code>xtpkpss model(trendbreak)</code>, <code>xtpcointegwe model(regimeshift)</code>.", C.PALETTE["red"])

# ======================================================================
C.section("2 · Breaks beyond the intercept", "Slopes, cointegrating vectors, loadings", A)
c1, c2, c3 = st.columns(3)
with c1:
    C.card("Break in the slope β(t)",
           "The marginal effect of x changes. In a regression this is a change in the "
           "structural coefficient — the object of xtbreakmodel, xtcbc, xtquantilebreak.", A)
with c2:
    C.card("Break in the cointegrating vector",
           "The long-run equilibrium relationship itself shifts (regime-shift cointegration). "
           "Banerjee–Carrion 2015/2025; Gregory–Hansen ancestry.", A)
with c3:
    C.card("Break in the factor loadings γ(t)",
           "How strongly a unit responds to the common shock changes — 'structural instability "
           "in the factor model'. Estimated jointly in Baltagi–Feng–Wang (2025) → xtkpybreak.", A)
st.latex(r"\text{BFW (2025): }\; y_{it}=x_{it}'\beta_i(K_0)+\gamma_i(K_1)'f_t+\varepsilon_{it}")
C.eqcap("Two independent break sets: K₀ in the slopes and K₁ in the factor loadings, both estimated by least squares.")

# ======================================================================
C.section("3 · How many, and do we know when?", "Count and timing", A)
c1, c2 = st.columns(2)
with c1:
    C.card("Single vs multiple breaks",
           "A single break (Gregory–Hansen, Westerlund–Edgerton) is simplest. Multiple breaks "
           "(Bai–Perron, Carrion et al., Westerlund 2006) need a partition of the sample and a "
           "rule for the number of breaks.", A)
with c2:
    C.card("Known vs unknown (endogenous) dates",
           "If T_B is known a priori, inference is standard. Usually it is <b>unknown</b> and "
           "must be <b>estimated</b> — which changes the null distribution and demands trimming "
           "and grid/dynamic-programming search.", A)
C.callout("The invariance trick",
          "LM / score tests (Im–Lee–Tieslau, Carrion et al., Westerlund) place the break "
          "<b>under the null too</b>, making the statistic <b>invariant to the break magnitude</b> "
          "and (asymptotically) to its estimated location. This is why they remain correctly "
          "sized when the date is estimated.", A)

# ======================================================================
C.section("4 · Who breaks — homogeneity of the break across units", "The heterogeneity axis", A)
st.markdown(
    "This is the axis that most sharply separates the modern **estimators**. Read left to right "
    "as progressively more heterogeneity allowed:"
)
t = np.arange(100)
fig = make_subplots(rows=1, cols=3, subplot_titles=(
    "Common break (all units, same date)",
    "Grouped breaks (latent groups)",
    "Heterogeneous breaks (each its own date)"))
# common
for k in range(4):
    y = np.where(t >= 50, 1.5, 0.5) + 0.05*k
    fig.add_trace(go.Scatter(y=y, line=dict(color=C.PALETTE["indigo"], width=1.6), opacity=.8, showlegend=False), row=1, col=1)
fig.add_vline(x=50, line=dict(color="#888", dash="dash"), row=1, col=1)
# grouped
for k in range(4):
    d = 35 if k < 2 else 65
    y = np.where(t >= d, 1.5, 0.5) + 0.05*k
    col = C.PALETTE["teal"] if k < 2 else C.PALETTE["pink"]
    fig.add_trace(go.Scatter(y=y, line=dict(color=col, width=1.6), opacity=.85, showlegend=False), row=1, col=2)
fig.add_vline(x=35, line=dict(color=C.PALETTE["teal"], dash="dash"), row=1, col=2)
fig.add_vline(x=65, line=dict(color=C.PALETTE["pink"], dash="dash"), row=1, col=2)
# heterogeneous
rng = C.rng(2)
for k in range(4):
    d = int(rng.integers(30, 75))
    y = np.where(t >= d, 1.5, 0.5) + 0.05*k
    fig.add_trace(go.Scatter(y=y, line=dict(color=C.PALETTE["orange"], width=1.6), opacity=.8, showlegend=False), row=1, col=3)
C.show(fig, height=300)
c1, c2, c3 = st.columns(3)
with c1:
    C.card("Common break", "Every unit breaks at the same date. Fewest parameters, most power. "
           "Qian–Su, Baltagi–Feng–Kao, xtbreakmodel(pls/bfk/sara).", C.PALETTE["indigo"])
with c2:
    C.card("Grouped breaks", "Units cluster into latent groups; each group has its own dates. "
           "Okui–Wang GAGFL → xtbreakmodel(gagfl).", C.PALETTE["teal"])
with c3:
    C.card("Heterogeneous breaks", "Each unit breaks on its own schedule. Hardest, but sometimes "
           "reality (Guliyev 2026 F-CCEMG absorbs these via Fourier).", C.PALETTE["orange"])

# ======================================================================
C.section("5 · Which coefficients break — vector vs coefficient-by-coefficient", "The coefficient axis", A)
c1, c2 = st.columns(2)
with c1:
    st.latex(r"\textbf{Vector break: } \beta_t \text{ changes in }\textit{all}\text{ K components at each }T_B")
    C.card("Vector break", "All slopes jump together at each break date. Standard assumption "
           "(Bai–Perron, Qian–Su, BFK). Splits every coefficient even if only one moved. "
           "→ xtbreakmodel.", A)
with c2:
    st.latex(r"\textbf{CBC break: } \beta_{k,t}\text{ has its }\textit{own}\; m_k\text{ breaks and dates}")
    C.card("Coefficient-by-coefficient", "Each coefficient breaks independently; stable ones are "
           "left unbroken. Avoids spurious regime-splitting (Kaddoura 2025 CBCL). → xtcbc.", A)
C.callout("Why it matters empirically",
          "In Kaddoura's US crime application the vector-break estimator finds 2 breaks in "
          "<b>all 16</b> coefficients, while the coefficient-by-coefficient estimator finds breaks "
          "in <b>only 3</b> — leaving the key deterrence coefficients correctly unbroken.", A)

# ======================================================================
C.section("6 · Sharp vs smooth (gradual) breaks", "The shape axis", A)
st.markdown(
    "A break need not be instantaneous. **Sharp** breaks are step functions; **smooth** breaks "
    "are gradual transitions. Two ways to model gradual change:"
)
t = np.arange(120)
sharp = np.where(t >= 60, 1.5, 0.0)
gamma = 0.3
lstr = 1.5 / (1 + np.exp(-gamma * (t - 60)))               # logistic smooth transition
fourier = 0.75 + 0.75*np.sin(2*np.pi*1*t/120) + 0.3*np.cos(2*np.pi*1*t/120)  # Fourier
fig = go.Figure()
fig.add_trace(go.Scatter(y=sharp, name="sharp (step / LST γ→∞)", line=dict(color=C.PALETTE["red"], width=2.6, shape="hv")))
fig.add_trace(go.Scatter(y=lstr, name="smooth: logistic transition (LST)", line=dict(color=C.PALETTE["grape"], width=2.6)))
fig.add_trace(go.Scatter(y=fourier, name="smooth: Fourier approximation", line=dict(color=C.PALETTE["cyan"], width=2.2, dash="dot")))
C.show(fig, height=330, title="Sharp vs smooth structural change")
c1, c2 = st.columns(2)
with c1:
    st.latex(r"\text{LST: } F(t)=\big[1+\exp(-\gamma(t/T-\tau))\big]^{-1}")
    C.eqcap("γ controls sharpness (γ→∞ is a step), τ locates the break. Used in the tFR test (xtpqroot fourier).")
with c2:
    st.latex(r"\text{Fourier: } d_t=a_0+\sum_{k}\Big[a_k\sin\tfrac{2\pi k t}{T}+b_k\cos\tfrac{2\pi k t}{T}\Big]")
    C.eqcap("A few frequencies k capture unknown, possibly multiple, smooth breaks without estimating dates.")

# ======================================================================
C.section("7 · A decision checklist", "Classify before you test", A)
st.markdown(
    "Answer these seven questions and the correct family is essentially pinned down:"
)
st.markdown(
    "1. **Level, trend, or regime** shift? → deterministic model A/B/C.\n"
    "2. **Slopes, cointegrating vector, or factor loadings** breaking?\n"
    "3. **One or several** breaks?\n"
    "4. **Known or estimated** dates? (trimming & search if estimated)\n"
    "5. **Common, grouped, or heterogeneous** across units?\n"
    "6. **All coefficients together (vector)** or **coefficient-by-coefficient**?\n"
    "7. **Sharp or smooth** transition?"
)
C.callout("Then add the two constants",
          "On top of the seven, always ask: is there <b>cross-sectional dependence</b> (almost "
          "always yes → CCE/PANIC/bootstrap) and are the series <b>non-stationary</b> "
          "(test first). Those two never go away in this literature.", A)

C.dev_footer()
