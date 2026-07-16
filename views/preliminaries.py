import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["preliminaries"]
C.hero(
    "Preliminary Concepts",
    "Every idea the founding papers assume — integration, spurious regression, "
    "cointegration, cross-sectional dependence, factors and deterministics — explained "
    "from the ground up. Master this page and the rest of the guide reads easily.",
    A, tag="Foundations",
)

st.markdown(
    "The structural-break literature sits on top of four older ideas: **(1)** the "
    "integration order of a series, **(2)** the danger of spurious regression, "
    "**(3)** cointegration as genuine long-run comovement, and **(4)** cross-sectional "
    "dependence driven by common factors. We build each one, then add the pieces "
    "(long-run variance, principal components, quantiles, Fourier, bootstrap) that the "
    "specific tests need."
)

# ======================================================================
C.section("1 · The panel and its two dimensions", "Notation", A)
st.markdown(
    "A panel stacks a cross-section of $N$ units observed over $T$ time periods. "
    "The generic linear panel model is:"
)
st.latex(r"y_{it} = \alpha_i + x_{it}'\beta + u_{it}, \qquad i=1,\dots,N;\; t=1,\dots,T")
st.markdown(
    "- $\\alpha_i$ — **individual (fixed) effect**, a unit-specific intercept absorbing "
    "time-invariant heterogeneity.\n"
    "- $x_{it}$ — regressors; $\\beta$ — slope (possibly $\\beta_i$ if *heterogeneous*).\n"
    "- $u_{it}$ — error, which in modern work carries a **common-factor** structure.\n\n"
    "Two asymptotic regimes matter enormously for which test is valid:"
)
c1, c2 = st.columns(2)
with c1:
    C.card("Fixed-T, large-N", "N → ∞ with T fixed. Typical of micro panels and many "
           "macro panels. Break-date consistency then relies on many cross-sections. "
           "(Carrion et al. 2005; Kaddoura 2025; Baltagi–Feng–Kao.)", A)
with c2:
    C.card("Large-T (and large-N)", "T → ∞ (then or jointly with N). Needed for unit-root / "
           "cointegration asymptotics based on Brownian motion. (Westerlund 2006; KPY 2011; "
           "Banerjee–Carrion.)", A)

# ======================================================================
C.section("2 · Integration order: I(0) vs I(1)", "Stochastic trends", A)
st.markdown(
    "A series is **I(0)** (integrated of order zero, *stationary*) if it has a constant mean, "
    "constant variance, and autocovariances that die out. It is **I(1)** if it must be "
    "differenced once to become I(0). The canonical I(1) process is the **random walk**:"
)
st.latex(r"y_t = y_{t-1} + \varepsilon_t \;\;\Leftrightarrow\;\; \Delta y_t = \varepsilon_t,\qquad \varepsilon_t \sim (0,\sigma^2)")
st.markdown(
    "Equivalently, in an AR(1) $y_t=\\rho y_{t-1}+\\varepsilon_t$, a **unit root** means "
    "$\\rho=1$. When $\\rho=1$ shocks are **permanent** (the variance grows with $t$, "
    "$\\mathrm{Var}(y_t)=t\\sigma^2$); when $|\\rho|<1$ shocks are **transitory** and the "
    "series is mean-reverting."
)
rng = C.rng(3)
T = 160
e1 = rng.normal(0, 1, T)
i1 = np.cumsum(e1)                     # random walk (I(1))
i0 = np.zeros(T)
for k in range(1, T):
    i0[k] = 0.5 * i0[k-1] + e1[k]      # stationary AR(1), rho=0.5
tr = 0.08 * np.arange(T) + i0          # trend-stationary
fig = go.Figure()
fig.add_trace(go.Scatter(y=i1, name="I(1): random walk", line=dict(color=C.PALETTE["indigo"], width=2.4)))
fig.add_trace(go.Scatter(y=i0, name="I(0): AR(1), ρ=0.5", line=dict(color=C.PALETTE["teal"], width=2.4)))
fig.add_trace(go.Scatter(y=tr, name="trend-stationary", line=dict(color=C.PALETTE["orange"], width=2, dash="dot")))
C.show(fig, height=360, title="Integration orders — one is not like the others")
C.callout("Difference-stationary vs trend-stationary",
          "Both an I(1) series and a trend-stationary series <i>trend</i>, but they are "
          "fundamentally different. The I(1) series has a <b>stochastic trend</b> (remove it by "
          "differencing); the trend-stationary series has a <b>deterministic trend</b> (remove it by "
          "de-trending). Confusing the two is the root of the Perron critique — and of why breaks "
          "matter so much.", A)

# ======================================================================
C.section("3 · Testing for a unit root: ADF and the stationarity null", "Two families", A)
st.markdown("The **Augmented Dickey–Fuller (ADF)** regression tests $H_0:\\rho=1$ via:")
st.latex(r"\Delta y_t = \mu + \phi\, y_{t-1} + \sum_{j=1}^{p}\psi_j \Delta y_{t-j} + \varepsilon_t,\qquad H_0:\phi=0")
st.markdown(
    "The $t$-statistic on $\\phi$ has a non-standard (Dickey–Fuller) distribution. "
    "**Rejecting** $H_0$ means stationarity. The mirror-image approach reverses the null:"
)
st.latex(r"\textbf{KPSS: } y_t = \mu + \eta_t + \varepsilon_t,\quad \eta_t=\eta_{t-1}+v_t,\quad H_0:\sigma_v^2=0\;(\text{stationary})")
st.markdown(
    "KPSS builds a statistic from **partial sums** of residuals. Under stationarity these "
    "partial sums stay bounded; under a unit root they wander, inflating the statistic. "
    "This is the engine behind the **panel KPSS with breaks** (Carrion et al. 2005 → `xtpkpss`)."
)
S = np.cumsum(i0 - i0.mean())
Su = np.cumsum(i1 - i1.mean())
fig = go.Figure()
fig.add_trace(go.Scatter(y=S, name="partial sums, I(0) → bounded", line=dict(color=C.PALETTE["teal"], width=2.4)))
fig.add_trace(go.Scatter(y=Su, name="partial sums, I(1) → wander", line=dict(color=C.PALETTE["red"], width=2.4)))
C.show(fig, height=320, title="KPSS intuition: partial sums of residuals")
st.latex(r"\text{KPSS} = \frac{1}{T^2\hat\omega^2}\sum_{t=1}^{T} S_t^2,\qquad S_t=\sum_{s=1}^{t}\hat\varepsilon_s,\qquad \hat\omega^2=\text{long-run variance}")

# ======================================================================
C.section("4 · The long-run variance (LRV)", "The nuisance you cannot ignore", A)
st.markdown(
    "Almost every test here needs the **long-run variance** — the spectral density at "
    "frequency zero — because serial correlation changes the scale of the limiting "
    "distribution:"
)
st.latex(r"\omega^2 \;=\; \sum_{k=-\infty}^{\infty}\gamma(k)\;=\;\gamma(0)+2\sum_{k=1}^{\infty}\gamma(k),\qquad \gamma(k)=\mathrm{Cov}(u_t,u_{t-k})")
st.markdown(
    "It is estimated by a **kernel (HAC) estimator** with a bandwidth $\\ell$:"
)
st.latex(r"\hat\omega^2 = \hat\gamma(0) + 2\sum_{k=1}^{\ell} w\!\left(\tfrac{k}{\ell}\right)\hat\gamma(k)")
C.chips(["Bartlett kernel", "Quadratic-Spectral kernel", "Andrews–Schwarz bandwidth ⌊4(T/100)^{2/9}⌋",
         "Newey–West", "Fejér kernel (Westerlund–Edgerton)"], A)
C.callout("Why it recurs",
          "Panel KPSS, Westerlund's LM tests, McCoskey–Kao — all standardise by an estimate of "
          "$\\omega^2$. The homogeneous version pools one $\\omega^2$; the heterogeneous version "
          "allows a different $\\omega_i^2$ per unit (this is exactly the <b>Z(hom)</b> vs "
          "<b>Z(het)</b> split in <code>xtpkpss</code>).", A)

# ======================================================================
C.section("5 · Spurious regression", "The original sin of non-stationary data", A)
st.markdown(
    "Regress **two independent random walks** on each other and you will typically find a "
    "'significant' relationship that does not exist — high $R^2$, large $t$-statistics, "
    "strongly autocorrelated residuals. This is **spurious regression** (Granger–Newbold). "
    "It is why you cannot simply run OLS on I(1) levels."
)
rng2 = C.rng(20)
yy = np.cumsum(rng2.normal(0, 1, 200))
xx = np.cumsum(rng2.normal(0, 1, 200))
b = np.polyfit(xx, yy, 1)
fig = go.Figure()
fig.add_trace(go.Scatter(x=xx, y=yy, mode="markers",
                         marker=dict(color=C.PALETTE["grape"], size=6, opacity=.7),
                         name="two independent I(1) series"))
xs = np.linspace(xx.min(), xx.max(), 20)
fig.add_trace(go.Scatter(x=xs, y=b[0]*xs+b[1], mode="lines",
                         line=dict(color=C.PALETTE["red"], width=3), name="OLS fit (meaningless)"))
C.show(fig, height=340, title="Spurious regression: a relationship that isn't there")
st.markdown(
    "The resolution is **cointegration**: levels may be regressed on levels *only if* the "
    "regression error is itself I(0). Structural-break cointegration tests ask exactly this — "
    "*is the equilibrium error stationary, allowing the equilibrium to have shifted?*"
)

# ======================================================================
C.section("6 · Cointegration and error correction", "Genuine long-run comovement", A)
st.markdown(
    "Two (or more) I(1) series are **cointegrated** if a linear combination of them is I(0). "
    "That combination is the **long-run equilibrium**; deviations from it are transitory:"
)
st.latex(r"y_{it} = \alpha_i + \beta_i' x_{it} + e_{it},\qquad x_{it}\sim I(1),\quad e_{it}\sim I(0)\;\Rightarrow\;\text{cointegration}")
st.markdown("Equivalently, there is an **error-correction** representation with adjustment speed $\\phi_i<0$:")
st.latex(r"\Delta y_{it} = \phi_i\big(y_{i,t-1}-\beta_i'x_{i,t-1}\big) + \text{(short-run terms)} + \varepsilon_{it}")
st.markdown(
    "- **Residual-based** tests (McCoskey–Kao, Westerlund 2006) check whether $e_{it}$ is I(0). "
    "Null of **cointegration**.\n"
    "- **ECM-based** tests (Westerlund 2007) check whether $\\phi_i<0$. Null of **no cointegration**.\n\n"
    "A **structural break in cointegration** means $\\alpha_i$ and/or $\\beta_i$ shift at some date "
    "$T_B$ — the equilibrium itself moves."
)
rng3 = C.rng(5)
x = np.cumsum(rng3.normal(0, 1, 200))
e = np.zeros(200)
for k in range(1, 200):
    e[k] = 0.6 * e[k-1] + rng3.normal(0, 0.6)   # stationary equilibrium error
y = 1.0 + 0.8 * x + e
fig = go.Figure()
fig.add_trace(go.Scatter(y=y, name="y (I(1))", line=dict(color=C.PALETTE["indigo"], width=2)))
fig.add_trace(go.Scatter(y=0.8*x+1.0, name="0.8·x + 1 (long-run)", line=dict(color=C.PALETTE["teal"], width=2)))
fig.add_trace(go.Scatter(y=e, name="equilibrium error e (I(0))", line=dict(color=C.PALETTE["orange"], width=1.6)))
C.show(fig, height=340, title="Cointegration: y and x drift together; the gap is stationary")

# ======================================================================
C.section("7 · Cross-sectional dependence & common factors", "Second-generation panels", A)
st.markdown(
    "Units in a panel are rarely independent — they share global shocks (oil prices, crises, "
    "technology). The modern way to model this **cross-sectional dependence (CSD)** is a "
    "**common-factor** error structure:"
)
st.latex(r"u_{it} = \gamma_i' f_t + \varepsilon_{it}")
st.markdown(
    "- $f_t$ — a small number $r$ of **unobserved common factors** (can be I(1)).\n"
    "- $\\gamma_i$ — unit-specific **factor loadings**.\n"
    "- $\\varepsilon_{it}$ — idiosyncratic (unit-specific) error.\n\n"
    "Ignoring $f_t$ invalidates first-generation tests: they over-reject and their tabulated "
    "distributions no longer apply. Two remedies dominate the whole guide:"
)
c1, c2 = st.columns(2)
with c1:
    C.card("CCE — Common Correlated Effects (Pesaran 2006)",
           "Proxy the unobserved factors by the <b>cross-sectional averages</b> of the "
           "observables and add them as regressors. Remarkably, KPY (2011) show this stays "
           "valid even when f_t is I(1). Powers CCEMG/CCEP, xtkpybreak, xtbfkbreak.", A)
with c2:
    C.card("PANIC — factor extraction (Bai–Ng 2004)",
           "Estimate the factors by <b>principal components on the differenced data</b>, then "
           "re-cumulate and test the common and idiosyncratic parts separately for unit roots. "
           "Powers Bai–Carrion PANIC-with-breaks.", A)
st.markdown("The **Pesaran CD test** detects CSD before you choose a method:")
st.latex(r"CD = \sqrt{\frac{2T}{N(N-1)}}\sum_{i<j}\hat\rho_{ij}\;\xrightarrow{d}\;N(0,1),\qquad \hat\rho_{ij}=\text{pairwise residual correlation}")

# ======================================================================
C.section("8 · Principal components & the number of factors", "Extracting the unobserved", A)
st.markdown(
    "Given a $T\\times N$ matrix of (differenced) data $Z$, principal components estimate the "
    "factor space by the eigenvectors of $ZZ'$. The **number of factors** $r$ is chosen by "
    "the Bai–Ng (2002) information criteria, e.g."
)
st.latex(r"\mathrm{IC}_{p2}(k) = \ln\!\big(V(k,\hat F^k)\big) + k\left(\frac{N+T}{NT}\right)\ln\!\big(\min\{N,T\}\big)")
st.markdown(
    "where $V(k,\\hat F^k)$ is the average residual variance using $k$ factors. Minimising "
    "$\\mathrm{IC}_{p2}$ over $k$ delivers $\\hat r$. This step appears inside "
    "`xtpcointegwe`, `xtbreakcoint`, `xtcadfcoint` and the PANIC unit-root tests."
)

# ======================================================================
C.section("9 · Quantiles, Fourier and the bootstrap", "The specialised toolkit", A)
c1, c2, c3 = st.columns(3)
with c1:
    C.card("Quantile regression",
           "Estimates the conditional <i>quantile</i> function, not just the mean. Lets a "
           "unit-root test reveal <b>asymmetric persistence</b> — a series can be mean-reverting "
           "in calm times yet persistent in the tails (Koenker–Xiao; xtpqroot).", C.PALETTE["pink"])
with c2:
    C.card("Fourier approximation",
           "A few sine/cosine terms approximate <b>unknown, gradual (smooth) breaks</b> without "
           "estimating break dates. Fractional frequencies refine the fit (Nazlioglu–Karul; "
           "Olayeni et al.; xtpqroot fourier).", C.PALETTE["grape"])
with c3:
    C.card("Sieve / block bootstrap",
           "Resamples whole cross-section rows (or fits a VAR and resamples innovations) to "
           "reproduce the <b>contemporaneous dependence</b>, giving valid critical values under "
           "CSD (Chang 2004; Westerlund–Edgerton).", C.PALETTE["cyan"])
st.latex(r"\text{Fourier deterministic: }\; d_t = a_0 + a_1\sin\!\Big(\tfrac{2\pi k t}{T}\Big) + a_2\cos\!\Big(\tfrac{2\pi k t}{T}\Big)\;\;(k\text{ = frequency})")

# ======================================================================
C.section("10 · The bridge to breaks: the Perron critique", "Why the rest of the guide exists", A)
st.markdown(
    "Perron (1989) showed that an **unmodelled structural break biases you toward the "
    "unit-root null**: a series that is stationary around a *shifted* mean looks integrated to "
    "a test that assumes a constant mean. In panels the problem compounds across units and "
    "interacts with CSD. Hence the design principle of every tool ahead:"
)
C.callout("The unifying idea",
          "A modern panel break method = <b>remove the common factors</b> (CCE or PANIC) "
          "<b>+ let the deterministic part shift at estimated dates</b> (Bai–Perron) "
          "<b>+ use critical values that know the deterministic model</b>. "
          "The next pages are variations on this theme.", A)

C.dev_footer()
