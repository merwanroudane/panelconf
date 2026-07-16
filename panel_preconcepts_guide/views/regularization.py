import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["regular"]
C.hero(
    "Regularization explained",
    "From overfitting and the bias–variance trade-off, to ridge, lasso, and the fused lasso — "
    "and how a penalty quietly turns into an automatic structural-break detector.",
    A, tag="Modelling toolkits",
)

# ================================================================
C.section("1 · The problem: overfitting", "Why we need a penalty at all", A)
C.callout("The intuition",
          "Give a model as many free parameters as data points and it fits your sample "
          "<b>perfectly</b> — and predicts the future <b>terribly</b>. It has memorised the noise. "
          "<b>Regularization</b> adds a penalty for complexity: a little bias, a lot less variance.",
          A)
st.markdown("The prediction error decomposes as:")
st.latex(r"\mathbb{E}\big[(y-\hat y)^2\big]=\underbrace{\text{Bias}^2}_{\text{grows with }\lambda}+\underbrace{\text{Variance}}_{\text{falls with }\lambda}+\underbrace{\sigma^2}_{\text{irreducible}}")
lam = np.linspace(0, 10, 200)
bias2 = 0.05 * lam ** 2
var = 6 / (1 + lam) ** 1.4
tot = bias2 + var + 0.5
fig = go.Figure()
fig.add_trace(go.Scatter(x=lam, y=bias2, name="Bias²", line=dict(color=C.PALETTE["red"], width=2.4)))
fig.add_trace(go.Scatter(x=lam, y=var, name="Variance", line=dict(color=C.PALETTE["blue"], width=2.4)))
fig.add_trace(go.Scatter(x=lam, y=tot, name="Total error", line=dict(color=C.PALETTE["green"], width=3.4)))
fig.add_vline(x=lam[int(np.argmin(tot))], line=dict(color=C.PALETTE["grape"], dash="dash"),
              annotation_text="λ* (optimal)")
fig.update_layout(xaxis_title="penalty λ", yaxis_title="error")
C.show(fig, height=340, title="The bias–variance trade-off: there is an optimal λ")

st.markdown("Every regularized estimator has the same shape — **fit + penalty**:")
st.latex(r"\min_{\beta}\ \underbrace{\sum_{i,t}\big(y_{it}-x_{it}'\beta\big)^2}_{\text{fidelity to the data}}\;+\;\lambda\cdot\underbrace{\mathrm{pen}(\beta)}_{\text{complexity}}")
C.eqcap("λ = 0 gives ordinary least squares. Larger λ forces a simpler model. λ is chosen by an information criterion or cross-validation.")

# ================================================================
C.section("2 · Ridge vs Lasso", "Two penalties, one crucial difference", A)
c1, c2 = st.columns(2)
with c1:
    st.latex(r"\text{Ridge }(\ell_2):\quad \lambda\sum_k\beta_k^2")
    C.card("Ridge", "Shrinks all coefficients toward zero — but <b>never exactly to zero</b>. "
           "Good for handling collinearity; does <b>not</b> select variables.", C.PALETTE["blue"])
with c2:
    st.latex(r"\text{Lasso }(\ell_1):\quad \lambda\sum_k|\beta_k|")
    C.card("Lasso", "Shrinks some coefficients <b>exactly to zero</b> — so it performs "
           "<b>variable selection</b>. This is the property we exploit for breaks.", C.PALETTE["green"])

st.markdown("#### Why the lasso hits exactly zero")
st.markdown(
    "The lasso constraint region $\\sum_k|\\beta_k|\\le c$ is a **diamond** with sharp corners "
    "*on the axes*; ridge's region $\\sum_k\\beta_k^2\\le c$ is a **circle** with no corners. The "
    "elliptical fit contours touch the diamond at a **corner** with positive probability — and a "
    "corner means a coefficient is exactly zero."
)
th = np.linspace(0, 2 * np.pi, 200)
fig = go.Figure()
fig.add_trace(go.Scatter(x=np.cos(th), y=np.sin(th), fill="toself",
                         fillcolor="rgba(28,126,214,.15)", line=dict(color=C.PALETTE["blue"], width=2.5),
                         name="Ridge region (circle)"))
fig.add_trace(go.Scatter(x=[1, 0, -1, 0, 1], y=[0, 1, 0, -1, 0], fill="toself",
                         fillcolor="rgba(55,178,77,.15)", line=dict(color=C.PALETTE["green"], width=2.5),
                         name="Lasso region (diamond)"))
for r in (0.55, 0.85, 1.15):
    fig.add_trace(go.Scatter(x=1.5 + r * 1.5 * np.cos(th), y=1.1 + r * 0.8 * np.sin(th),
                             line=dict(color=C.PALETTE["gray"], width=1, dash="dot"),
                             showlegend=(r == 0.55), name="OLS fit contours"))
fig.add_trace(go.Scatter(x=[0], y=[1], mode="markers",
                         marker=dict(size=14, color=C.PALETTE["red"], symbol="star"),
                         name="corner solution → β₁ = 0"))
fig.update_layout(xaxis_title="β₁", yaxis_title="β₂",
                  xaxis=dict(range=[-1.6, 3.2], scaleanchor="y"), yaxis=dict(range=[-1.6, 2.4]))
C.show(fig, height=400, title="The geometry: corners cause exact zeros")

st.markdown("For a single (orthonormal) coefficient the lasso solution is **soft-thresholding**:")
st.latex(r"\hat\beta^{\text{lasso}}=\mathrm{sign}\big(\hat\beta^{\text{OLS}}\big)\cdot\big(|\hat\beta^{\text{OLS}}|-\lambda\big)^{+}")
lam2 = st.slider("λ (threshold)", 0.0, 2.0, 0.6, 0.05)
b_ols = np.linspace(-3, 3, 300)
b_lasso = np.sign(b_ols) * np.maximum(np.abs(b_ols) - lam2, 0)
b_ridge = b_ols / (1 + lam2)
fig = go.Figure()
fig.add_trace(go.Scatter(x=b_ols, y=b_ols, name="OLS (45°)",
                         line=dict(color=C.PALETTE["gray"], width=1.6, dash="dot")))
fig.add_trace(go.Scatter(x=b_ols, y=b_ridge, name="Ridge (shrinks, never 0)",
                         line=dict(color=C.PALETTE["blue"], width=2.6)))
fig.add_trace(go.Scatter(x=b_ols, y=b_lasso, name="Lasso (exactly 0 in the middle)",
                         line=dict(color=C.PALETTE["green"], width=3.2)))
fig.update_layout(xaxis_title="OLS estimate", yaxis_title="penalised estimate")
C.show(fig, height=330, title=f"Soft-thresholding at λ = {lam2}: a whole zone is set to zero")

# ================================================================
C.section("3 · The fused lasso = a break detector", "The key move", A)
C.callout("The whole idea in one box",
          "Let the coefficient change <b>every period</b>, but penalise the <b>differences</b> "
          "|βₜ − βₜ₋₁|. Most differences get shrunk to <b>exactly zero</b> (the coefficient is "
          "constant there); the few that survive are the <b>break dates</b>. "
          "Break detection becomes automatic variable selection — you never specify how many "
          "breaks there are.", A)
st.latex(r"\min_{\{\beta_t\}}\ \sum_{i,t}\big(y_{it}-x_{it}'\beta_t\big)^2+\lambda\sum_{t=2}^{T}\big|\beta_t-\beta_{t-1}\big|")

lam3 = st.slider("λ — the fused-lasso penalty", 0.0, 3.0, 0.8, 0.05)
T = 60
t = np.arange(T)
beta_true = np.where(t < 20, 1.0, np.where(t < 40, 2.3, 1.6))
rngv = C.rng(1)
beta_raw = beta_true + rngv.normal(0, 0.22, T)
# crude fused-lasso-like smoother for illustration
fit = beta_raw.copy()
for _ in range(400):
    new = fit.copy()
    for k in range(T):
        lo = fit[k - 1] if k > 0 else None
        hi = fit[k + 1] if k < T - 1 else None
        nb = [v for v in (lo, hi) if v is not None]
        target = (beta_raw[k] + lam3 * sum(nb)) / (1 + lam3 * len(nb))
        new[k] = target
    fit = new
# snap tiny differences to zero (fusing)
d = np.diff(fit)
d[np.abs(d) < 0.02 * (1 + lam3)] = 0
fit_s = np.concatenate([[fit[0]], fit[0] + np.cumsum(d)])
nbreaks = int((np.abs(np.diff(fit_s)) > 0.05).sum())

fig = go.Figure()
fig.add_trace(go.Scatter(y=beta_raw, mode="markers", marker=dict(size=5, color="#C3CAD6"),
                         name="raw period-by-period β̂ₜ"))
fig.add_trace(go.Scatter(y=beta_true, name="TRUE step path",
                         line=dict(color=C.PALETTE["ink"], width=2, dash="dot", shape="hv")))
fig.add_trace(go.Scatter(y=fit_s, name=f"fused-lasso path (λ={lam3})",
                         line=dict(color=C.PALETTE["green"], width=3.2)))
for b in (20, 40):
    fig.add_vline(x=b, line=dict(color=C.PALETTE["red"], dash="dash", width=1))
fig.update_layout(xaxis_title="time t", yaxis_title="coefficient βₜ")
C.show(fig, height=360, title=f"λ = {lam3} → roughly {nbreaks} surviving change(s)")
if lam3 < 0.2:
    C.callout("λ too small", "Almost nothing is fused — you are fitting the noise and will "
              "'detect' many spurious breaks (<b>over-segmentation</b>).", C.PALETTE["red"])
elif lam3 > 2.2:
    C.callout("λ too large", "Everything is fused into one flat line — the real breaks are "
              "penalised away (<b>under-segmentation</b>).", C.PALETTE["red"])
else:
    C.callout("λ about right", "Noise is fused away while the genuine steps survive. This is what "
              "the information criterion picks for you.", C.PALETTE["teal"])

# ================================================================
C.section("4 · The refinements that make it work", "Group, adaptive, and the IC", A)
c1, c2 = st.columns(2)
with c1:
    st.latex(r"\lambda\sum_{t=2}^{T}\big\lVert\beta_t-\beta_{t-1}\big\rVert")
    C.card("Group fused lasso", "With K regressors, penalise the <b>vector norm</b> of the change. "
           "All K coefficients then break <i>together</i> — a <b>vector break</b>.", A)
with c2:
    st.latex(r"w_t=\big\lVert\dot\beta_t-\dot\beta_{t-1}\big\rVert^{-\kappa}")
    C.card("Adaptive weights", "Weight each difference by the inverse of a pilot estimate "
           "(κ ≈ 2). Big true jumps get a <b>small</b> penalty; noise gets a <b>big</b> one. "
           "This delivers the <b>oracle property</b>.", A)
st.markdown("Putting it together — the workhorse objective of modern panel break estimation:")
st.latex(r"\min_{\{\beta_t\}}\ \frac1N\sum_{i,t}\big(y_{it}-x_{it}'\beta_t\big)^2+\lambda\sum_{t=2}^{T}w_t\big\lVert\beta_t-\beta_{t-1}\big\rVert")
st.markdown("And $\\lambda$ is selected by a **BIC-type information criterion**, e.g.")
st.latex(r"\mathrm{IC}(\lambda)=\hat\sigma^2(\lambda)+\phi\cdot\#\{\text{breaks}(\lambda)\},\qquad \phi=c\,\frac{\log N}{\sqrt N}")
C.callout("The oracle property",
          "With adaptive weights the estimator asymptotically finds the <b>true</b> breaks and "
          "estimates the regime coefficients <b>as if the break dates had been known all along</b>. "
          "That is why adaptive weighting is not optional.", A)

# ================================================================
C.section("5 · How it is computed", "Block coordinate descent", A)
st.markdown(
    "The objective is convex but **non-smooth** (the absolute value has a kink), so there is no "
    "closed form. **Block coordinate descent (BCD)** updates one period's $\\beta_t$ at a time, "
    "holding the others fixed, using a soft-thresholding step; a full sweep $t=1,\\dots,T$ is "
    "repeated until the path stops changing. If the update's norm falls below $\\lambda w_{t-1}$, "
    "the block is **fused** to the previous period ($\\beta_t=\\beta_{t-1}$) — i.e. *no break here*."
)

# ================================================================
C.section("6 · Where you meet it in panel econometrics", "The methods built on this", A)
meth = [
    ("PLS / AGFL — Qian & Su (2016)",
     "The adaptive group fused lasso with ONE common break schedule for all units (vector break). "
     "→ <code>xtbreakmodel, method(pls)</code>"),
    ("GAGFL — Okui & Wang (2021)",
     "Units belong to G <b>latent groups</b>; each group gets its own break dates. Three stages: "
     "(1) grouped fixed-effects k-means initialisation, (2) group-specific AGFL by BCD, "
     "(3) reassign units to the best-fitting group; repeat. G chosen by BIC. "
     "→ <code>xtbreakmodel, method(gagfl) groups(#)</code>"),
    ("CBC / CBCL — Kaddoura (2025)",
     "Applies the fused penalty <b>separately to each coefficient</b>, so each βₖ has its own "
     "number of breaks mₖ and dates; genuinely stable coefficients are left unbroken. "
     "→ <code>xtcbc</code>"),
    ("Shrinkage quantile breaks — Zhang et al. (2022)",
     "Quantile regression + adaptive fused lasso: breaks may differ across quantile levels. "
     "→ <code>xtquantilebreak</code>"),
]
for n, d in meth:
    C.card(n, d, A)

C.callout("Dummy vs Fourier vs regularization — the final word",
          "<b>Dummies</b> when you have a discrete, known-ish event. <b>Fourier</b> when the change "
          "is gradual or the number/timing is unknown. <b>Regularization</b> when you want the data "
          "to <i>select</i> the breaks automatically from many candidates — and especially when you "
          "suspect that only <i>some</i> coefficients or <i>some</i> groups of units break.", A)

C.dev_footer()
