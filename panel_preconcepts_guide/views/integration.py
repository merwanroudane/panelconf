import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["integration"]
C.hero(
    "Integration and cointegration",
    "Why levels are dangerous, what a unit root really means, and how cointegration rescues "
    "regressions on non-stationary data. The time-series backbone of every panel test.",
    A, tag="Foundations",
)

# ---------------------------------------------------------------
C.section("1 · Stationary or not?", "I(0) vs I(1)", A)
st.markdown(
    "A series is **I(0)** (*stationary*) if its mean and variance are constant and shocks die out. "
    "It is **I(1)** if it must be differenced once to become stationary."
)
st.latex(r"\text{I(1): } y_t=y_{t-1}+\varepsilon_t \iff \Delta y_t=\varepsilon_t")
st.latex(r"\text{AR(1): } y_t=\rho y_{t-1}+\varepsilon_t,\qquad \rho=1 \Rightarrow \text{unit root}")
st.markdown(
    "With $\\rho=1$, shocks are **permanent** and the variance *grows with time*, "
    "$\\mathrm{Var}(y_t)=t\\sigma^2$. With $|\\rho|<1$, shocks fade and the series reverts to its mean."
)
rng = C.rng(3)
T = 160
e = rng.normal(0, 1, T)
i1 = np.cumsum(e)
i0 = np.zeros(T)
for k in range(1, T):
    i0[k] = 0.5 * i0[k - 1] + e[k]
fig = go.Figure()
fig.add_trace(go.Scatter(y=i1, name="I(1) — random walk (wanders)",
                         line=dict(color=C.PALETTE["red"], width=2.6)))
fig.add_trace(go.Scatter(y=i0, name="I(0) — AR(1), ρ=0.5 (reverts)",
                         line=dict(color=C.PALETTE["teal"], width=2.6)))
fig.add_hline(y=0, line=dict(color=C.PALETTE["gray"], dash="dot"))
C.show(fig, height=340, title="One reverts to its mean; the other never does")

# interactive rho
st.markdown("**Try it:** move $\\rho$ and watch persistence appear.")
rho = st.slider("ρ (persistence)", 0.0, 1.0, 0.5, 0.05)
y = np.zeros(T)
for k in range(1, T):
    y[k] = rho * y[k - 1] + e[k]
fig = go.Figure()
fig.add_trace(go.Scatter(y=y, line=dict(color=C.PALETTE["orange"], width=2.6), name=f"ρ = {rho}"))
fig.add_hline(y=0, line=dict(color=C.PALETTE["gray"], dash="dot"))
C.show(fig, height=280, title=f"AR(1) with ρ = {rho}" + ("  →  UNIT ROOT" if rho >= 0.999 else ""))

# ---------------------------------------------------------------
C.section("2 · Spurious regression", "The original sin", A)
st.markdown(
    "Regress two **independent** random walks on each other and you typically get a high $R^2$ and "
    "a huge $t$-statistic — for a relationship that **does not exist**."
)
rng2 = C.rng(20)
yy = np.cumsum(rng2.normal(0, 1, 200))
xx = np.cumsum(rng2.normal(0, 1, 200))
b = np.polyfit(xx, yy, 1)
r2 = np.corrcoef(xx, yy)[0, 1] ** 2
fig = go.Figure()
fig.add_trace(go.Scatter(x=xx, y=yy, mode="markers",
                         marker=dict(color=C.PALETTE["grape"], size=6, opacity=.7),
                         name="two INDEPENDENT random walks"))
xs = np.linspace(xx.min(), xx.max(), 20)
fig.add_trace(go.Scatter(x=xs, y=b[0] * xs + b[1], mode="lines",
                         line=dict(color=C.PALETTE["red"], width=3),
                         name=f"OLS fit — R² = {r2:.2f} (meaningless)"))
C.show(fig, height=340, title="Spurious regression: a 'relationship' that isn't there")
C.callout("The tell-tale sign",
          "Spurious regressions leave <b>I(1) residuals</b> — strongly autocorrelated errors. "
          "That is exactly what cointegration tests check.", A)

# ---------------------------------------------------------------
C.section("3 · Cointegration", "When levels ARE allowed", A)
st.markdown(
    "Two I(1) series are **cointegrated** if a linear combination of them is I(0): they wander, but "
    "they wander **together**, and the gap between them is stationary."
)
st.latex(r"y_{it}=\alpha_i+\beta_i' x_{it}+e_{it},\qquad x_{it}\sim I(1),\quad e_{it}\sim I(0)")
st.markdown("Equivalently, there is an **error-correction** representation:")
st.latex(r"\Delta y_{it}=\underbrace{\phi_i}_{\text{adjustment speed}<0}\big(y_{i,t-1}-\beta_i'x_{i,t-1}\big)+\text{(short run)}+\varepsilon_{it}")
C.eqcap("φᵢ measures how fast a deviation from equilibrium is corrected. φᵢ = 0 means no cointegration.")

rng3 = C.rng(5)
x = np.cumsum(rng3.normal(0, 1, 200))
e = np.zeros(200)
for k in range(1, 200):
    e[k] = 0.6 * e[k - 1] + rng3.normal(0, 0.6)
y = 1.0 + 0.8 * x + e
fig = go.Figure()
fig.add_trace(go.Scatter(y=y, name="y (I(1))", line=dict(color=C.PALETTE["indigo"], width=2)))
fig.add_trace(go.Scatter(y=0.8 * x + 1.0, name="long-run 0.8·x + 1",
                         line=dict(color=C.PALETTE["teal"], width=2)))
fig.add_trace(go.Scatter(y=e, name="equilibrium error e (I(0)) — stationary",
                         line=dict(color=C.PALETTE["orange"], width=1.6)))
C.show(fig, height=340, title="Cointegration: they drift together and the gap is stationary")

# ---------------------------------------------------------------
C.section("4 · Two test families (and their opposite nulls)", "ADF vs KPSS", A)
st.markdown(
    "| Family | $H_0$ | Reject means | Panel version |\n"
    "|---|---|---|---|\n"
    "| ADF / Dickey–Fuller | unit root | stationarity | IPS, CIPS, `xtpqroot` |\n"
    "| KPSS / Hadri | stationarity | unit root | Hadri, Carrion et al., `xtpkpss` |"
)
st.latex(r"\text{ADF: }\Delta y_t=\mu+\phi y_{t-1}+\sum_{j=1}^{p}\psi_j\Delta y_{t-j}+\varepsilon_t,\qquad H_0:\phi=0")
st.latex(r"\text{KPSS: }\;\text{KPSS}=\frac{1}{T^2\hat\omega^2}\sum_{t=1}^{T}S_t^2,\qquad S_t=\sum_{s=1}^{t}\hat\varepsilon_s")
C.callout("Confirmatory analysis (best practice)",
          "Unit-root tests have low power. Run <b>both</b> an ADF-type and a KPSS-type test. "
          "If they agree, your conclusion is robust. If both reject (or neither), the data are "
          "uninformative — say so.", A)

# ---------------------------------------------------------------
C.section("5 · The long-run variance (LRV)", "The nuisance behind every statistic", A)
st.latex(r"\omega^2=\sum_{k=-\infty}^{\infty}\gamma(k)=\gamma(0)+2\sum_{k=1}^{\infty}\gamma(k),\qquad \gamma(k)=\mathrm{Cov}(u_t,u_{t-k})")
st.latex(r"\hat\omega^2=\hat\gamma(0)+2\sum_{k=1}^{\ell}w\!\left(\tfrac{k}{\ell}\right)\hat\gamma(k)")
st.markdown(
    "Estimated with a **kernel (HAC)** and a bandwidth $\\ell$ — commonly the Bartlett or "
    "Quadratic-Spectral kernel with $\\ell=\\lfloor 4(T/100)^{2/9}\\rfloor$ (Andrews–Schwarz)."
)
C.chips(["Bartlett kernel", "Quadratic-Spectral", "Newey–West", "Andrews–Schwarz bandwidth",
         "homogeneous ω² vs heterogeneous ωᵢ²"], A)
C.callout("Where you meet it again",
          "The <b>homogeneous vs heterogeneous</b> LRV choice is exactly the "
          "<code>Z(hom)</code> vs <code>Z(het)</code> split reported by <code>xtpkpss</code>.", A)

C.dev_footer()
