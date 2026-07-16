import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["estimators"]
C.hero(
    "Break Estimators for Panel Coefficients",
    "Testing tells you a break exists; estimation tells you WHERE the dates are and WHAT the "
    "regime coefficients β(t) become. This is the modern (post-2016) strand — least-squares, "
    "fused-lasso, grouped, nonparametric, and quantile estimators.",
    A, tag="Estimation",
)

st.markdown(
    "All estimate the piecewise-constant coefficient model, differing only in **who breaks** "
    "and **how the dates are found**:"
)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta(t)+u_{it},\qquad \beta(t)=\beta_{j}\;\text{ for }\;T_{j-1}<t\le T_j")

# ======================================================================
C.section("1 · The workhorse — Bai & Perron least squares", "Bai & Perron (1998, 2003)", A)
st.markdown(
    "Every method here descends from Bai–Perron. With $m$ breaks partitioning the sample, "
    "estimate all break dates jointly by **minimising the total sum of squared residuals** over "
    "admissible partitions:"
)
st.latex(r"(\hat T_1,\dots,\hat T_m)=\arg\min_{T_1,\dots,T_m}\;\sum_{j=1}^{m+1}\sum_{t=T_{j-1}+1}^{T_j}\big(y_{t}-x_{t}'\beta_j\big)^2")
st.markdown(
    "- Solved efficiently by **dynamic programming** ($O(T^2)$ instead of combinatorial).\n"
    "- Number of breaks chosen by a **sequential sup-$F(\\ell+1\\mid\\ell)$** test or an "
    "information criterion.\n- **Trimming** $\\varepsilon$ keeps candidate dates away from the "
    "endpoints. Break dates are **super-consistent** ($\\hat T_j/T\\to\\lambda_j$ fast)."
)

# ======================================================================
C.section("2 · Adaptive group fused lasso — common breaks", "Qian & Su (2016) · xtbreakmodel(pls)", A)
st.markdown(
    "Recast break detection as **shrinkage**: penalise successive-period coefficient "
    "*differences* so that most are shrunk to exactly zero — the non-zero ones are the breaks. "
    "The **adaptive group fused lasso** objective:"
)
st.latex(r"\min_{\{\beta_t\}}\;\frac1N\sum_{i}\sum_{t}\big(y_{it}-x_{it}'\beta_t\big)^2+\lambda\sum_{t=2}^{T}w_t\,\lVert\beta_t-\beta_{t-1}\rVert")
st.latex(r"w_t=\lVert\dot\beta_t-\dot\beta_{t-1}\rVert^{-\kappa}\quad(\text{adaptive weights, }\kappa=2)")
C.eqcap("‖βₜ−βₜ₋₁‖ fused to zero ⇒ no break at t; non-zero ⇒ a break. λ chosen by a BIC-type IC. Adaptive weights give oracle efficiency (true breaks not over-penalised).")
# step-function coefficient path illustration
t = np.arange(60)
beta_true = np.where(t < 20, 1.0, np.where(t < 40, 2.2, 1.6))
beta_hat = beta_true + C.rng(1).normal(0, 0.05, 60)
fig = go.Figure()
fig.add_trace(go.Scatter(y=beta_hat, mode="markers", marker=dict(size=5, color="#C3CAD6"), name="raw period-by-period β̂ₜ"))
fig.add_trace(go.Scatter(y=beta_true, name="fused-lasso estimate (step function)",
                         line=dict(color=C.PALETTE["pink"], width=3, shape="hv")))
for b in (20, 40):
    fig.add_vline(x=b, line=dict(color=C.PALETTE["red"], dash="dash"))
C.show(fig, height=320, title="Fused lasso recovers a piecewise-constant coefficient path")

# ======================================================================
C.section("3 · CCE + common break (and endogenous regressors)", "Baltagi–Feng–Kao 2016/2019 · xtbreakmodel(bfk), xtbfkbreak", A)
st.markdown(
    "Baltagi–Feng–Kao extend **Pesaran's CCE** to heterogeneous panels with an **unknown common "
    "structural break** in the slopes. Ignoring a break makes CCE inconsistent; they estimate "
    "the break by sequential least squares on the CCE-transformed data. The 2019 paper adds "
    "**endogenous regressors** (via instruments), the case handled by `xtbfkbreak`:"
)
st.latex(r"y_{it}=x_{it}'\beta_i(K_0)+\gamma_i'f_t+\varepsilon_{it},\qquad \hat K_0=\arg\min_k\;\sum_i\big[SSR_i(1{:}k)+SSR_i(k{+}1{:}T)\big]")
C.eqcap("The cross-section averages proxy fₜ; the pooled SSR over the CCE-transformed data locates the common break. Robust to cross-section heteroskedasticity.")

# ======================================================================
C.section("4 · Heterogeneous breaks via latent groups — GAGFL", "Okui & Wang (2021) · xtbreakmodel(gagfl)", A)
st.markdown(
    "The most general design: units belong to $G$ **latent groups**; each group has its **own** "
    "break dates and regime coefficients, and group membership is unknown. GAGFL is a hybrid of "
    "**Grouped Fixed Effects (GFE)** and **adaptive group fused lasso**:"
)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta_{g_i}(t)+\varepsilon_{it},\qquad g_i\in\{1,\dots,G\}")
st.markdown(
    "**Three-stage algorithm** (iterated to convergence):\n"
    "1. **GFE initialisation** — k-means-style clustering (Bonhomme–Manresa) on time-varying "
    "coefficients, many random starts.\n"
    "2. **Group-specific AGFL** — fused-lasso break detection within each group (block coordinate "
    "descent).\n3. **Reassignment** — move each unit to the group whose coefficient path minimises "
    "its residual sum of squares."
)
# grouped patterns illustration
t = np.arange(80)
fig = go.Figure()
gA = np.where(t < 30, 1.0, 2.0)
gB = np.where(t < 55, 0.5, 1.8)
for k in range(3):
    fig.add_trace(go.Scatter(y=gA + 0.04*k, line=dict(color=C.PALETTE["teal"], width=1.6), opacity=.8, showlegend=(k==0), name="group A (break @30)"))
for k in range(3):
    fig.add_trace(go.Scatter(y=gB + 0.04*k, line=dict(color=C.PALETTE["pink"], width=1.6), opacity=.8, showlegend=(k==0), name="group B (break @55)"))
C.show(fig, height=300, title="GAGFL: latent groups with group-specific break dates")

# ======================================================================
C.section("5 · Nonparametric screening — SaRa", "Li, Xiao & Chen · xtbreakmodel(sara)", A)
st.markdown(
    "**Screening and Ranking (SaRa)** avoids global optimisation. At each time $t$ and bandwidth "
    "$h$, compare **local left vs right** coefficient estimates; large gaps flag breaks:"
)
st.latex(r"D(t,h)=\big\lVert \sqrt{N}\,\big(\hat\beta_R(t,h)-\hat\beta_L(t,h)\big)\big\rVert")
st.markdown(
    "Candidates are **$h$-local maximisers** of $D(t,h)$ pooled across several bandwidths, "
    "filtered by a median threshold, and the final number chosen by a BIC-type IC. Static panels "
    "use covariance estimation; dynamic panels use **GMM**. Nonparametric ⇒ robust to heavy tails "
    "and distributional misspecification."
)

# ======================================================================
C.section("6 · Coefficient-by-coefficient breaks — CBCL", "Kaddoura (2025) · xtcbc", A)
st.markdown(
    "Relaxes the vector-break assumption: **each** coefficient $\\beta_{k,t}$ gets its **own** "
    "number of breaks $m_k$ and dates. The objective applies the fused penalty **per coefficient**:"
)
st.latex(r"L_\lambda(\beta)=\frac1N\sum_i\sum_{t\ge2}\big(\tilde y_{it}-\bar x_{it}'\beta\big)^2+\lambda\sum_{t\ge2}\sum_{k}w_{k,t}\,\lvert\beta_{k,t}-\beta_{k,t-1}\rvert")
st.latex(r"\text{IC}_1(\lambda)=\hat\sigma^2(\lambda)+\phi\sum_k\big[\hat m_k(\lambda)+1\big],\qquad \phi=c\,\tfrac{\log N}{\sqrt N}")
C.eqcap("Genuinely stable coefficients are left unbroken. csdemean cross-section-demeans to absorb interactive fixed effects (Kaddoura–Westerlund 2023).")

# ======================================================================
C.section("7 · Nonstationary panels + multiple breaks in slopes AND loadings", "Baltagi–Feng–Wang (2025) · xtkpybreak", A)
st.markdown(
    "The most fully 3ʳᵈ-generation estimator: builds on **KPY (2011)** — CCE stays valid when "
    "factors are **I(1)** — and generalises **Bai–Perron** to nonstationary panels, estimating "
    "**multiple breaks in the slopes $K_0$ AND in the factor loadings $K_1$** jointly by least "
    "squares:"
)
st.latex(r"y_{it}=x_{it}'\beta_i(K_0)+\gamma_i(K_1)'f_t+\varepsilon_{it},\qquad f_t=f_{t-1}+\phi_t\;(\text{I}(1))")
st.markdown(
    "Because the CCE proxy survives I(1) factors, the unobserved factors become **extra "
    "regressors**, so breaks in slopes and loadings are just breaks in a linear regression — "
    "estimated by the dynamic-programming Bai–Perron algorithm. Break dates are consistent for "
    "both the nonstationary-factor and nonstationary-regressor cases. (Empirical example: a "
    "**common 1992 break** in international R&D spillovers, attributed to globalisation.)"
)
st.code("xtkpybreak cce  y x         // CCEMG/CCEP, robust to I(1) factors\n"
        "xtkpybreak break y x, nbreaks(2) loadings   // breaks in slopes AND loadings", language="stata")

# ======================================================================
C.section("8 · Breaks across quantiles — shrinkage quantile regression", "Zhang, Zhu, Feng & He (2022) · xtquantilebreak", A)
st.markdown(
    "Combines **quantile regression** with the **adaptive fused lasso** to detect breaks that may "
    "**differ across quantile levels** while sharing a common location shift. An $L_1$ penalty on "
    "individual effects plus an $L_1$-fusion penalty across time, pooled over multiple quantiles, "
    "detects **'partial' changes** and consistently estimates the number and dates of breaks:"
)
st.latex(r"\min\;\sum_{q}\sum_{i,t}\rho_{\tau_q}\!\big(y_{it}-\alpha_i-x_{it}'\beta_t(\tau_q)\big)+\lambda_1\sum_i|\alpha_i|+\lambda_2\sum_{t}w_t\big\lVert\beta_t-\beta_{t-1}\big\rVert")
C.eqcap("ρ_τ is the check function. Breaks common across individuals but allowed to vary across quantiles — captures distributional break heterogeneity a mean estimator misses.")

# ======================================================================
C.section("9 · Which estimator when", "Decision map", A)
st.markdown(
    "| Break heterogeneity | Estimator | Command |\n"
    "|---|---|---|\n"
    "| Common vector break | Qian–Su AGFL / Bai–Perron LS / SaRa | `xtbreakmodel` (pls/bfk/sara) |\n"
    "| Coefficient-by-coefficient | Kaddoura CBCL | `xtcbc` |\n"
    "| Latent groups | Okui–Wang GAGFL | `xtbreakmodel` (gagfl) |\n"
    "| CCE + break, endogenous x | Baltagi–Feng–Kao | `xtbfkbreak` |\n"
    "| Nonstationary + I(1) factors + loading breaks | Baltagi–Feng–Wang / KPY | `xtkpybreak` |\n"
    "| Breaks across quantiles | Zhang et al. shrinkage QR | `xtquantilebreak` |\n"
    "| Robust dynamic panel, breaks + CSD | — | `xtdynestimb` |"
)

C.dev_footer()
