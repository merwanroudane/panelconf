import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["unitroot"]
C.hero(
    "Panel Unit-Root & Stationarity Tests with Breaks",
    "Is the series I(1) when the panel is cross-sectionally dependent and its mean/trend "
    "shifts? These are the tests that answer it — the KPSS/stationarity family, the "
    "factor (PANIC) family, and the quantile & Fourier extensions.",
    A, tag="Testing · Integration",
)

st.markdown(
    "Two philosophies, opposite nulls — always state which you are using:"
)
c1, c2 = st.columns(2)
with c1:
    C.card("Stationarity null  ·  H₀: I(0)",
           "KPSS / Hadri family. <b>Reject ⇒ evidence of a unit root.</b> "
           "Attractive when theory predicts stationarity (convergence, PPP). "
           "→ <code>xtpkpss</code>.", A)
with c2:
    C.card("Unit-root null  ·  H₀: I(1)",
           "ADF / CADF / CIPS family. <b>Reject ⇒ evidence of stationarity.</b> "
           "The default in most applied work. → <code>xtpqroot</code>, PANIC.", A)

# ======================================================================
C.section("1 · Panel KPSS with multiple breaks", "Carrion-i-Silvestre, del Barrio-Castro & López-Bazo (2005) · xtpkpss", A)
st.markdown(
    "The panel generalisation of the KPSS stationarity test that allows **each unit** to have "
    "its **own number of breaks at its own dates**, in level and/or trend. The individual model "
    "with $m_i$ breaks is:"
)
st.latex(r"y_{it}=\alpha_i+\sum_{k=1}^{m_i}\theta_{i,k}DU_{i,k,t}+\beta_i t+\sum_{k=1}^{m_i}\gamma_{i,k}DT^{*}_{i,k,t}+\varepsilon_{it}")
C.eqcap("DU = level-shift dummy (1 after the k-th break), DT* = trend-shift dummy. Set the trend terms to zero for the level-only model.")
st.markdown("Each unit's KPSS statistic uses the partial sums of the OLS residuals; the panel statistic averages them and standardises:")
st.latex(r"LM_i(\lambda_i)=\frac{1}{\hat\omega_i^2\,T^2}\sum_{t=1}^{T}S_{it}^2,\qquad S_{it}=\sum_{s=1}^{t}\hat\varepsilon_{is}")
st.latex(r"Z(\lambda)=\frac{\sqrt{N}\Big(\overline{LM}-\bar\xi\Big)}{\sqrt{\bar\varsigma^2}}\;\xrightarrow{d}\;N(0,1),\qquad \overline{LM}=\frac1N\sum_i LM_i(\lambda_i)")
C.eqcap("ξ̄ and ς̄² are the mean and variance of the individual limiting distribution — they depend on the deterministic model and the break fractions λᵢ = (T_{b,1}/T, …).")
c1, c2 = st.columns(2)
with c1:
    C.card("Z(hom) — homogeneous LRV", "Pools a single long-run variance ω̄² across units. "
           "More powerful if the assumption holds.", A)
with c2:
    C.card("Z(het) — heterogeneous LRV", "Allows a different ωᵢ² per unit — robust to "
           "cross-unit variance heterogeneity.", A)
st.markdown(
    "**Break dates** are estimated per unit by minimising the SSR (Bai–Perron sequential "
    "procedure); the **number of breaks** is chosen by the modified BIC (**LWZ**, Liu–Wu–Zidek). "
    "CSD is handled by a **bootstrap** that preserves the cross-section covariance. "
    "Rejection is in the **right tail** — large positive $Z$ ⇒ against stationarity."
)
# illustration: KPSS partial sums with vs without break correction
rng = C.rng(9)
T = 120; TB = 60
e = rng.normal(0, 1, T)
y = np.where(np.arange(T) >= TB, 2.2, 0.0) + np.cumsum(0*e) + e  # stationary around a shifted mean
# residuals ignoring break vs modelling break
res_ignore = y - y.mean()
seg = np.where(np.arange(T) >= TB, y[TB:].mean(), y[:TB].mean())
res_model = y - seg
fig = go.Figure()
fig.add_trace(go.Scatter(y=np.cumsum(res_ignore), name="partial sums — break IGNORED (looks I(1))",
                         line=dict(color=C.PALETTE["red"], width=2.4)))
fig.add_trace(go.Scatter(y=np.cumsum(res_model), name="partial sums — break MODELLED (stays bounded)",
                         line=dict(color=C.PALETTE["teal"], width=2.4)))
fig.add_vline(x=TB, line=dict(color="#888", dash="dash"))
C.show(fig, height=330, title="Why the break correction matters (Perron critique in action)")
st.code("xtpkpss y, model(constbreak) maxbreaks(3) graph      // level breaks\n"
        "xtpkpss y, model(trendbreak) maxbreaks(5) trim(0.15)  // level + trend", language="stata")

# ======================================================================
C.section("2 · PANIC with structural breaks", "Bai–Ng (2004); Bai & Carrion-i-Silvestre (2009)", A)
st.markdown(
    "The factor route. You cannot run principal components on the *levels* if factors and "
    "idiosyncratic parts have different integration orders, so PANIC **differences first**, "
    "extracts factors, then **re-cumulates** and tests each part separately:"
)
st.latex(r"\Delta y_{it}=\Delta D_{it}+\lambda_i'\Delta f_t+\Delta e_{it}\;\;\xrightarrow{\text{PCA on }\Delta}\;\;\hat f_t,\hat\lambda_i")
st.latex(r"\hat f_t=\textstyle\sum_{s\le t}\Delta\hat f_s,\qquad \hat e_{it}=\sum_{s\le t}\Delta\hat e_{is}")
st.markdown(
    "- Test the **idiosyncratic** components with a pooled statistic $\\hat P_e$ (asymptotically "
    "independent across $i$ once the factor is removed).\n"
    "- Test the **common factors** for the number of stochastic trends with the **MQ** tests.\n"
    "- Bai–Carrion add break terms to $D_{it}$ before differencing — disentangling a shared "
    "stochastic trend from purely idiosyncratic unit roots."
)
C.callout("The payoff", "PANIC tells you <i>whether the non-stationarity is common or "
          "idiosyncratic</i> — a substantive economic result, not a nuisance.", A)

# ======================================================================
C.section("3 · Panel LM with level shifts", "Im–Lee–Tieslau (2005/2010)", A)
st.markdown(
    "A **score (LM)** panel unit-root test with the break placed **under the null**. Because "
    "the LM statistic is **invariant to the size and location of the level shifts**, estimated "
    "break dates do not distort its distribution — the flaw that plagued earlier ADF-with-break "
    "tests. The standardised bar-LM statistic is asymptotically $N(0,1)$."
)

# ======================================================================
C.section("4 · CIPS / CADF — the second-generation bridge", "Pesaran (2007)", A)
st.markdown(
    "Not a break test, but the reference point that the quantile and Fourier extensions build "
    "on. Augment each unit's ADF regression with the **cross-section averages** of levels and "
    "lagged differences (CADF), then average the $t$-statistics (CIPS):"
)
st.latex(r"\Delta y_{it}=a_i+\phi_i y_{i,t-1}+d_i\bar y_{t-1}+\sum_j c_{ij}\Delta\bar y_{t-j}+\sum_j b_{ij}\Delta y_{i,t-j}+\varepsilon_{it}")
st.latex(r"\text{CIPS}=\frac1N\sum_{i=1}^N t_i(\text{CADF}_i)")
st.markdown("The cross-section averages soak up a single common factor without estimating it. "
            "A 3ʳᵈ-generation test is, in spirit, *CIPS/PANIC + a break-date search*.")

# ======================================================================
C.section("5 · Quantile CIPS(τ) & the Fourier tFR test", "Yang–Wei–Cai (2022); Corakci–Omay (2023) · xtpqroot", A)
st.markdown(
    "**xtpqroot** delivers two frontier tests, both CSD-robust.\n\n"
    "**CIPS(τ)** pushes CADF into a **quantile** regression, testing the unit root at each "
    "quantile $\\tau$ to reveal **asymmetric persistence** — a variable can be mean-reverting in "
    "normal periods yet persistent in the tails:"
)
st.latex(r"Q_{\Delta y_{it}}(\tau\mid\mathcal F_{t-1})=a_i(\tau)+\rho_i(\tau)y_{i,t-1}+d_i(\tau)\bar y_{t-1}+\dots")
st.latex(r"\text{CIPS}(\tau)=\frac1N\sum_{i=1}^N t_i(\tau),\qquad H_0:\rho_i(\tau)=1\;\forall i")
# quantile persistence illustration
taus = np.array([.1,.2,.3,.4,.5,.6,.7,.8,.9])
rho = 0.80 + 0.22/(1+np.exp(-6*(taus-0.6)))    # persistent in upper tail
fig = go.Figure()
fig.add_trace(go.Scatter(x=taus, y=rho, mode="lines+markers",
                         line=dict(color=C.PALETTE["pink"], width=3),
                         marker=dict(size=9, color=C.PALETTE["pink"]), name="ρ(τ)"))
fig.add_hline(y=1.0, line=dict(color=C.PALETTE["red"], dash="dash"),
              annotation_text="unit root ρ=1")
fig.update_layout(xaxis_title="quantile τ", yaxis_title="persistence ρ(τ)")
C.show(fig, height=330, title="Asymmetric persistence across quantiles (CIPS(τ) intuition)")
C.eqcap("Reject at low τ but not high τ ⇒ mean-reverting in calm periods, persistent in extreme (upper-tail) episodes.")

st.markdown(
    "**tFR** allows **smooth (fractional Fourier) and sharp (logistic STR) breaks "
    "simultaneously**, with CSD handled by the sieve bootstrap (Chang 2004):"
)
st.latex(r"y_{it}=d_{it}(k^{fr},\gamma,\tau)+\rho_i y_{i,t-1}+\sum_j b_{ij}\Delta y_{i,t-j}+\varepsilon_{it}")
# Fourier + LST fit illustration
t = np.arange(120)
smooth = 0.6*np.sin(2*np.pi*0.7*t/120) + 0.4*np.cos(2*np.pi*0.7*t/120)
sharp = 1.2/(1+np.exp(-0.5*(t-70)))
dt = 0.5 + smooth + sharp
series = dt + C.rng(4).normal(0, 0.35, 120)
fig = go.Figure()
fig.add_trace(go.Scatter(y=series, mode="markers", marker=dict(size=5, color="#B9C2CE"), name="data"))
fig.add_trace(go.Scatter(y=dt, name="fitted: Fourier(k^fr) + LST(γ,τ)", line=dict(color=C.PALETTE["grape"], width=3)))
C.show(fig, height=320, title="tFR: smooth + sharp break captured together")
st.code("xtpqroot y, quantile(0.1 0.5 0.9) cdtest individual   // CIPS(tau) + CD test\n"
        "xtpqroot y, fourier model(trendshift) bootreps(2000)  // tFR smooth+sharp breaks", language="stata")

# ======================================================================
C.section("6 · A practical note on missing values", "Karavias–Tzavalis–Zhang (2022) · xtmunitroot", A)
st.markdown(
    "Real panels have gaps. The standard fix (drop units to balance) throws away information. "
    "Fixed-$T$ panel unit-root tests that **use the incomplete series directly** (via moment "
    "conditions robust to missingness) preserve power — relevant because most break tests here "
    "require a *balanced* panel, so imputation or a missing-robust test is a genuine pre-step."
)

C.dev_footer()
