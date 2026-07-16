import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["csa"]
C.hero(
    "CSA family vs the common-factor approach",
    "The two great routes to killing cross-sectional dependence: proxy the factors with "
    "cross-sectional averages (CCE), or estimate them with principal components (PANIC/IFE). "
    "This page explains both families and exactly how they differ.",
    A, tag="The central comparison",
)

C.callout("The difference in one line",
          "<b>CSA/CCE:</b> <i>don't estimate the factors</i> — subtract their footprint (the "
          "cross-section averages). &nbsp;&nbsp; <b>Factor/PC:</b> <i>estimate the factors</i> "
          "explicitly by principal components. Both remove the shared shock; they differ in "
          "assumptions, outputs, and what they let you say.", A)

# ================================================================
C.section("1 · The shared starting point", "Same model, two solutions", A)
st.latex(r"y_{it}=\beta_i'x_{it}+u_{it},\qquad u_{it}=\gamma_i'f_t+\varepsilon_{it},\qquad x_{it}=\Gamma_i'f_t+v_{it}")
st.markdown(
    "Both $y$ and $x$ load on the **same unobserved factors** $f_t$. That single fact is what makes "
    "the CSA trick possible."
)

# ================================================================
C.section("2 · The CSA family (cross-sectional averages)", "Pesaran's route", A)
st.markdown(
    "**The idea (Pesaran, 2006).** Average the model across units. Because $\\frac1N\\sum_i\\varepsilon_{it}"
    "\\to 0$ but the factor term does not, the cross-section averages become a **consistent proxy "
    "for the factor space**:"
)
st.latex(r"\bar y_t=\bar\beta'\bar x_t+\bar\gamma' f_t+\underbrace{\bar\varepsilon_t}_{\to 0}\;\;\Longrightarrow\;\; f_t \text{ is spanned by } (\bar y_t,\bar x_t)")
st.markdown("So just **add the averages as regressors** and estimate unit by unit:")
st.latex(r"y_{it}=\beta_i'x_{it}+\delta_{0i}\bar y_t+\delta_{1i}'\bar x_t+\varepsilon_{it}")
st.latex(r"\hat\beta_i=(X_i'\bar M X_i)^{-1}X_i'\bar M y_i,\qquad \bar M=I-\bar Z(\bar Z'\bar Z)^{-1}\bar Z',\quad \bar Z=[\bar y,\bar X]")
C.eqcap("M̄ projects out the factor proxy. No factor is ever estimated, and you never need to know r!")

st.markdown("#### The CSA family tree")
fam = [
    ("CCEMG", "CCE Mean Group — average the unit slopes: β̂ = (1/N)Σβ̂ᵢ. Fully heterogeneous slopes.", "Pesaran (2006)"),
    ("CCEP", "CCE Pooled — pool the slopes, weighting by X'M̄X. More efficient if slopes are homogeneous.", "Pesaran (2006)"),
    ("CS-ARDL", "Cross-sectionally augmented ARDL — dynamics + averages; gives long-run and short-run coefficients.", "Chudik–Pesaran"),
    ("CS-DL", "Cross-sectionally augmented Distributed Lag — estimates the long run directly, robust to lag misspecification.", "Chudik et al."),
    ("Dynamic CCE", "CCE with extra lags of the averages — needed when the model is dynamic.", "Chudik–Pesaran (2015)"),
    ("F-CCEMG", "Fourier CCEMG — CCE plus unit-specific Fourier terms to absorb heterogeneously-timed breaks.", "Guliyev (2026)"),
    ("CCE + breaks", "CCE with a common structural break in slopes (and I(1) factors).", "Baltagi–Feng–Kao; KPY; BFW"),
]
for n, d, r in fam:
    C.card(n, f"{d}<br><span style='color:#8A97A6'>{r}</span>", A)

C.callout("The remarkable KPY result",
          "Kapetanios, Pesaran & Yamagata (2011) proved CCE stays valid <b>even when the factors "
          "are I(1)</b> (non-stationary): the mean-group/pooled estimators keep the same limiting "
          "form and the same variance estimators as in the stationary case. This is the linchpin "
          "that lets <code>xtkpybreak</code> treat I(1) factors as ordinary regressors and then "
          "apply Bai–Perron.", A)

# CCE illustration
rng = C.rng(8)
T = 120
f = np.cumsum(rng.normal(0, 1, T))
zbar = f + rng.normal(0, 0.15, T)
raw = 0.8 * f + rng.normal(0, 0.6, T)
co = np.polyfit(zbar, raw, 1)
resid = raw - (co[0] * zbar + co[1])
fig = go.Figure()
fig.add_trace(go.Scatter(y=raw, name="one unit's series (factor-contaminated)",
                         line=dict(color=C.PALETTE["orange"], width=2)))
fig.add_trace(go.Scatter(y=zbar, name="cross-section average z̄ₜ (the proxy)",
                         line=dict(color=C.PALETTE["cyan"], width=2, dash="dot")))
fig.add_trace(go.Scatter(y=resid, name="after CCE de-factoring → factor gone",
                         line=dict(color=C.PALETTE["teal"], width=2)))
C.show(fig, height=340, title="CCE in action: the average proxies the factor and is partialled out")

st.markdown("#### The rank condition (the CSA family's key assumption)")
st.latex(r"\mathrm{rank}\big(\bar\Gamma\big)=r \le k+1")
C.eqcap("The average loading matrix must have full rank r: you need at least as many observables "
        "(y and the k regressors) as factors, otherwise the averages cannot span the factor space.")

# ================================================================
C.section("3 · The common-factor family (principal components)", "Bai & Ng's route", A)
st.markdown(
    "**The idea.** Don't proxy — *estimate* the factors by **principal components (PCA)**. But you "
    "cannot run PCA on the levels when $f_t$ and $e_{it}$ have different integration orders. "
    "PANIC's fix: **difference first**, extract, then **re-cumulate**:"
)
st.latex(r"\Delta y_{it}=\gamma_i'\Delta f_t+\Delta e_{it}\;\;\xrightarrow{\;\text{PCA on differences}\;}\;\;\Delta\hat f_t,\ \Delta\hat e_{it}")
st.latex(r"\hat f_t=\sum_{s\le t}\Delta\hat f_s,\qquad \hat e_{it}=\sum_{s\le t}\Delta\hat e_{is}")
st.markdown(
    "Then test the **common factors** and the **idiosyncratic components** for unit roots "
    "*separately*. You must choose the **number of factors** $r$ — by the Bai–Ng criteria:"
)
st.latex(r"\mathrm{IC}_{p2}(k)=\ln\!\big(V(k,\hat F^k)\big)+k\left(\frac{N+T}{NT}\right)\ln\!\big(\min\{N,T\}\big)")
C.eqcap("Minimise over k to get r̂. V(·) is the average residual variance using k factors.")

st.markdown("#### The factor family tree")
fam2 = [
    ("PANIC", "Difference → PCA → re-cumulate → test factors (MQ) and idiosyncratic (P̂ₑ) separately.", "Bai–Ng (2004)"),
    ("Interactive Fixed Effects (IFE)", "Estimate slopes AND the factor structure jointly by iterated principal components.", "Bai (2009)"),
    ("CUP-FM / CUP-BC", "Continuously-updated fully-modified / bias-corrected estimators for panel cointegration with factors.", "Bai–Kao–Ng (2009)"),
    ("Moon–Perron", "De-factor by projecting on estimated factors, then a pooled unit-root test.", "Moon–Perron (2004)"),
    ("PANIC with breaks", "PANIC + break terms in the deterministic part — a 3rd-generation test.", "Bai–Carrion (2009)"),
]
for n, d, r in fam2:
    C.card(n, f"{d}<br><span style='color:#8A97A6'>{r}</span>", C.PALETTE["grape"])

# scree plot
rng2 = C.rng(12)
eig = np.sort(rng2.random(10))[::-1] * 2
eig[:2] += np.array([8.0, 4.0])
fig = go.Figure()
fig.add_trace(go.Bar(x=[f"PC{i+1}" for i in range(10)], y=eig,
                     marker_color=[C.PALETTE["grape"] if i < 2 else "#C6CEDC" for i in range(10)]))
fig.update_layout(yaxis_title="eigenvalue")
C.show(fig, height=300, title="Scree plot: two dominant factors (r̂ = 2), the rest is noise")

# ================================================================
C.section("4 · The comparison — CSA vs factors", "The table to remember", A)
st.markdown(
    "| Aspect | **CSA / CCE family** | **Factor / PC family** |\n"
    "|---|---|---|\n"
    "| Are factors estimated? | ❌ No — only proxied by averages | ✅ Yes — by principal components |\n"
    "| Do you need to know **r**? | ❌ No (a big practical advantage) | ✅ Yes — choose by Bai–Ng IC |\n"
    "| Key assumption | **rank condition** on the average loadings | enough factors; N,T large for PCA |\n"
    "| Works with **I(1)** factors? | ✅ Yes (KPY 2011) | ✅ Yes (PANIC handles it by differencing) |\n"
    "| Small N behaviour | averages get noisy — needs decent N | PCA needs decent N and T |\n"
    "| Slope heterogeneity | natural (CCEMG averages unit slopes) | typically pooled/homogeneous |\n"
    "| What it tells you | a clean slope estimate | **plus** whether non-stationarity is common or idiosyncratic |\n"
    "| Computation | simple OLS with extra regressors | iterative PCA |\n"
    "| Typical commands | `xtkpybreak cce`, `xtccecoint`, CS-ARDL | `xtpcointegwe`, `xtbreakcoint`, PANIC |"
)

c1, c2 = st.columns(2)
with c1:
    C.callout("Use CSA/CCE when", "you want a simple, robust slope estimate; you don't want to "
              "commit to a number of factors; slopes are heterogeneous; factors may be I(1).", A)
with c2:
    C.callout("Use factors/PANIC when", "you want to know <b>where</b> the non-stationarity lives "
              "(common trend vs idiosyncratic) — a substantive economic result, not a nuisance.",
              C.PALETTE["grape"])

C.callout("They are cousins, not rivals",
          "Both remove the same object. Many third-generation commands use <b>both</b>: e.g. "
          "<code>xtcadfcoint</code> uses CCE averages <i>and</i> factors; <code>xtpcointegwe</code> "
          "estimates factors by PCA and selects r by Bai–Ng. Knowing which is under the hood tells "
          "you which assumption you are relying on.", A)

C.dev_footer()
