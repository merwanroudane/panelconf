import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["fourier"]
C.hero(
    "Fourier & Smooth Structural Breaks",
    "Breaks are rarely instantaneous and their number and form are rarely known. A handful of "
    "trigonometric terms approximate unknown, gradual change — no break dates to estimate. "
    "This is the smooth-break branch of the literature.",
    A, tag="Testing · Smooth change",
)

# ======================================================================
C.section("1 · The idea — approximate, don't estimate, the break", "Flexible Fourier Form", A)
st.markdown(
    "Instead of specifying dummies at estimated dates, add a **Flexible Fourier Form (FFF)** to "
    "the deterministic component. A theorem (Gallant 1981) says a few low-frequency sine/cosine "
    "terms can approximate *any* smooth, bounded deviation — including several gradual breaks:"
)
st.latex(r"d_t = \alpha_0 + \alpha_1 t + \sum_{k=1}^{n}\Big[a_k\sin\!\Big(\tfrac{2\pi k t}{T}\Big)+b_k\cos\!\Big(\tfrac{2\pi k t}{T}\Big)\Big]")
st.markdown(
    "In practice a **single frequency** ($n=1$) is often enough (Enders–Lee). The unit-root / "
    "cointegration regression is then run with $d_t$ as the deterministic term, and critical "
    "values depend on the chosen frequency."
)
# illustration: Fourier approximating two smooth breaks
t = np.arange(150)
true = 1.0/(1+np.exp(-0.25*(t-40))) - 1.2/(1+np.exp(-0.3*(t-100)))  # two gradual breaks
fk = 0.9*np.sin(2*np.pi*1.4*t/150) + 0.5*np.cos(2*np.pi*1.4*t/150)
fk = fk - fk.mean() + true.mean()
fig = go.Figure()
fig.add_trace(go.Scatter(y=true, name="true smooth breaks (2 gradual shifts)", line=dict(color=C.PALETTE["ink"], width=3)))
fig.add_trace(go.Scatter(y=fk, name="Fourier approximation (k=1.4)", line=dict(color=C.PALETTE["grape"], width=2.4, dash="dot")))
C.show(fig, height=330, title="A single Fourier frequency captures multiple smooth breaks")

# ======================================================================
C.section("2 · Fractional frequencies", "Olayeni, Tiwari & Wohar (2021) · FFFFF", A)
st.markdown(
    "Integer frequencies ($k=1,2,\\dots$) are a coarse grid. The **Fractional Frequency "
    "Flexible Fourier Form (FFFFF)** searches over **non-integer** $k\\in[0.1,5]$, choosing the "
    "value that minimises the SSR — a far more flexible fit to the true (unknown) break shape. "
    "Applied to **panel cointegration** it sharpens power when breaks are gradual and "
    "irregular."
)
t = np.arange(150)
fig = go.Figure()
for k, c in [(1.0, "blue"), (2.0, "cyan"), (1.3, "grape")]:
    s = np.sin(2*np.pi*k*t/150)
    fig.add_trace(go.Scatter(y=s, name=f"k = {k}", line=dict(color=C.PALETTE[c], width=2.2)))
C.show(fig, height=300, title="Integer (1, 2) vs fractional (1.3) Fourier frequencies")
C.eqcap("A fractional k lets the single Fourier term bend to a break that neither k=1 nor k=2 fits well.")
st.code("* FFFFF-style panel cointegration with smooth breaks\n"
        "xtpfardl y x, ...        // Fourier-augmented panel ARDL / CS-ARDL", language="stata")

# ======================================================================
C.section("3 · Fourier panel stationarity", "Nazlioglu & Karul (2017)", A)
st.markdown(
    "A **panel KPSS stationarity test with gradual (smooth) shifts** modelled by a Fourier "
    "approximation, robust to CSD. The panel statistic has a **standard normal** limit, and the "
    "Fourier terms replace the need to estimate the number and location of sharp breaks:"
)
st.latex(r"y_{it}=\alpha_i+\gamma_{1i}\sin\!\Big(\tfrac{2\pi k t}{T}\Big)+\gamma_{2i}\cos\!\Big(\tfrac{2\pi k t}{T}\Big)+\varepsilon_{it}")
st.latex(r"FZ=\frac{\sqrt N(\overline{FLM}-\bar\xi)}{\bar\varsigma}\;\xrightarrow{d}\;N(0,1)")
C.eqcap("H₀: stationarity around a smoothly-shifting mean. Good size/power even in small samples when errors are i.i.d.")

# ======================================================================
C.section("4 · Combining smooth AND sharp — the tFR test", "Corakci & Omay (2023) · xtpqroot fourier", A)
st.markdown(
    "Real data can contain **both** a gradual transition and an abrupt jump. The **tFR** test "
    "combines a **fractional Fourier** term (smooth) with a **logistic smooth-transition (LST)** "
    "term (sharp), estimated together:"
)
st.latex(r"d_{it}=\mu_i+\underbrace{\theta_i F\!\left(\gamma,\tau\right)}_{\text{sharp (LST)}}+\underbrace{a_i\sin\tfrac{2\pi k^{fr}t}{T}+b_i\cos\tfrac{2\pi k^{fr}t}{T}}_{\text{smooth (Fourier)}}")
st.latex(r"F(t)=\big[1+\exp(-\gamma(t/T-\tau))\big]^{-1}")
st.markdown(
    "- $\\gamma$ — transition **speed**: $\\gamma\\to\\infty$ is a step (sharp); small $\\gamma$ is "
    "gradual.\n- $\\tau$ — **location** of the sharp break (fraction of the sample).\n"
    "- $k^{fr}$ — fractional Fourier **frequency** for the smooth part.\n\n"
    "CSD is handled by the **sieve bootstrap**. Estimated per-unit break dates (sharp = LST "
    "threshold; smooth = Fourier turning points) are reported."
)
t = np.arange(150)
smooth = 0.7*np.sin(2*np.pi*0.8*t/150)
sharp = 1.3/(1+np.exp(-2.0*(t-95)/5))
fig = go.Figure()
fig.add_trace(go.Scatter(y=smooth, name="smooth (Fourier)", line=dict(color=C.PALETTE["cyan"], width=2.2)))
fig.add_trace(go.Scatter(y=sharp, name="sharp (LST, γ large)", line=dict(color=C.PALETTE["red"], width=2.2)))
fig.add_trace(go.Scatter(y=0.4+smooth+sharp, name="combined d_t", line=dict(color=C.PALETTE["grape"], width=3)))
C.show(fig, height=320, title="tFR deterministic: smooth + sharp, estimated jointly")

# ======================================================================
C.section("5 · Fourier meets CCE — heterogeneous-date breaks", "Guliyev (2026) F-CCEMG", A)
st.markdown(
    "When breaks occur at **different dates across units**, dummies are hopeless (too many "
    "parameters). A neat solution: augment the **CCE** regression with **unit-specific Fourier "
    "terms** — the cross-section averages filter the common factor while the Fourier terms "
    "**absorb the heterogeneously-timed breaks**. The **F-CCEMG** estimator attains the lowest "
    "RMSE across weak/moderate/strong dependence in Monte Carlo, with near-nominal coverage."
)
st.latex(r"y_{it}=\beta_i'x_{it}+\underbrace{c_{0i}+c_{1i}\sin\tfrac{2\pi t}{T}+c_{2i}\cos\tfrac{2\pi t}{T}}_{\text{unit-specific breaks}}+\underbrace{\delta_i'\bar z_t}_{\text{CCE factor proxy}}+\varepsilon_{it}")
C.callout("When to prefer smooth-break tools",
          "Choose Fourier / smooth-break methods when (i) you suspect <b>gradual</b> change, "
          "(ii) the <b>number and dates</b> of breaks are genuinely unknown, or (iii) breaks are "
          "<b>heterogeneously timed</b> across units. Choose sharp-break (dummy) methods when you "
          "have clear discrete events (a policy date, a crisis).", A)

C.dev_footer()
