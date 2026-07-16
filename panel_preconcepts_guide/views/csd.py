import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["csd"]
C.hero(
    "Cross-sectional dependence (CSD)",
    "What it is, why it destroys first-generation tests, how it is modelled with common factors, "
    "and — the modern question — how STRONG it is.",
    A, tag="The dependence machinery",
)

# ---------------------------------------------------------------
C.section("1 · What CSD is", "The definition", A)
st.markdown(
    "Units in a panel are rarely independent. Countries share oil shocks and crises; firms share "
    "technology and business cycles. Formally, **cross-sectional dependence** means the errors are "
    "correlated *across units* at the same time:"
)
st.latex(r"\mathrm{Cov}(u_{it},\,u_{jt})\neq 0\qquad\text{for some } i\neq j")
st.markdown("The modern way to *generate* this dependence is a **common-factor** error structure:")
st.latex(r"u_{it}=\gamma_i' f_t+\varepsilon_{it}")
st.markdown(
    "- $f_t$ — a small number $r$ of **unobserved common factors** (global shocks). May be I(1).\n"
    "- $\\gamma_i$ — unit-specific **factor loadings** (how exposed unit $i$ is).\n"
    "- $\\varepsilon_{it}$ — the **idiosyncratic** error (genuinely unit-specific).\n\n"
    "The regressors usually load on the same factors, $x_{it}=\\Gamma_i' f_t+v_{it}$ — which is "
    "exactly what makes the cross-sectional-average proxy work (next page)."
)

rng = C.rng(6)
T, N = 120, 8
f = np.cumsum(rng.normal(0, 1, T))
fig = go.Figure()
for i in range(N):
    lam = 0.5 + rng.random()
    y = lam * f + rng.normal(0, 0.7, T)
    fig.add_trace(go.Scatter(y=y, line=dict(color="#B7C6D6", width=1), opacity=.75,
                             showlegend=False))
fig.add_trace(go.Scatter(y=f, name="common factor fₜ (drives them all)",
                         line=dict(color=C.PALETTE["cyan"], width=3.6)))
C.show(fig, height=340, title="One common factor hiding behind many co-moving units")

# ---------------------------------------------------------------
C.section("2 · Why it destroys first-generation tests", "The consequence", A)
C.callout("The failure mechanism",
          "First-generation tests pool N series <b>assuming independence</b>, so their variance "
          "formula divides by N as if there were N independent pieces of information. With a shared "
          "factor there is far <b>less</b> independent information than N. The pooled statistic is "
          "therefore too large ⇒ the test <b>over-rejects</b> the unit-root null and you 'find' "
          "stationarity or cointegration that is an artefact of the common shock.", A)
st.markdown(
    "**Effective sample size intuition.** If every unit is driven by one factor, adding more units "
    "adds almost no new information — yet the test behaves as if each new unit were fresh evidence."
)
# size distortion illustration
rho_cs = np.linspace(0, 0.9, 30)
size = 0.05 + 0.55 * rho_cs**1.6
fig = go.Figure()
fig.add_trace(go.Scatter(x=rho_cs, y=size, mode="lines",
                         line=dict(color=C.PALETTE["red"], width=3),
                         name="actual rejection rate (1st-gen test)"))
fig.add_hline(y=0.05, line=dict(color=C.PALETTE["teal"], dash="dash"),
              annotation_text="nominal 5% level")
fig.update_layout(xaxis_title="degree of cross-sectional correlation",
                  yaxis_title="rejection rate under H₀")
C.show(fig, height=310, title="Size distortion: the test rejects far too often (illustrative)")

# ---------------------------------------------------------------
C.section("3 · The degree of dependence", "Classic binary vs modern", A)
C.callout("Classic vs modern question",
          "<b>Classic:</b> 'is there dependence — yes or no?' &nbsp;&nbsp; "
          "<b>Modern:</b> 'how <i>strong</i> is it?' — because the answer decides which estimator "
          "is even valid.", A)
st.markdown(
    "The strength is indexed by the **exponent $\\alpha$** in how fast the loadings accumulate "
    "(Bailey, Kapetanios & Pesaran):"
)
st.latex(r"\sum_{i=1}^{N}|\gamma_i| = O\!\left(N^{\alpha}\right),\qquad 0\le\alpha\le 1")

c1, c2, c3 = st.columns(3)
with c1:
    C.card("α = 1 — STRONG", "Loadings bounded away from zero for a non-negligible share of units. "
           "A genuine common factor. <b>CCE / PANIC are designed for this.</b>", C.PALETTE["red"])
with c2:
    C.card("½ < α < 1 — SEMI-WEAK", "Loadings shrink, but slowly. Banerjee–Carrion (2017) study "
           "CCE performance precisely across this range.", C.PALETTE["yellow"])
with c3:
    C.card("α ≤ ½ — WEAK / SPATIAL", "Local dependence (neighbours only). Handled by spatial models "
           "or robust standard errors, not factors.", C.PALETTE["teal"])

alpha = st.slider("α — strength of dependence", 0.0, 1.0, 0.9, 0.05)
Ns = np.arange(10, 400)
fig = go.Figure()
fig.add_trace(go.Scatter(x=Ns, y=Ns**alpha, mode="lines",
                         line=dict(color=C.PALETTE["grape"], width=3), name=f"Σ|γᵢ| ~ N^{alpha}"))
fig.add_trace(go.Scatter(x=Ns, y=Ns**1.0, mode="lines",
                         line=dict(color=C.PALETTE["red"], width=2, dash="dot"), name="strong (α=1)"))
fig.add_trace(go.Scatter(x=Ns, y=Ns**0.5, mode="lines",
                         line=dict(color=C.PALETTE["teal"], width=2, dash="dot"), name="weak (α=0.5)"))
fig.update_layout(xaxis_title="N", yaxis_title="Σ|γᵢ|")
C.show(fig, height=320, title=f"How the loadings accumulate at α = {alpha}")
lab = ("STRONG — use CCE/PANIC" if alpha > 0.85 else
       "SEMI-WEAK — CCE still usually works, check robustness" if alpha > 0.5 else
       "WEAK/SPATIAL — factors are not the right tool")
C.callout("Your α implies", lab, A)

# ---------------------------------------------------------------
C.section("4 · Two remedies (preview)", "Where we go next", A)
c1, c2 = st.columns(2)
with c1:
    C.card("CSA / CCE — cross-sectional averages",
           "Don't estimate the factors: proxy them with the cross-section averages of the "
           "observables and add them as regressors. Simple, robust, works even with I(1) factors.",
           C.PALETTE["pink"])
with c2:
    C.card("Common factors — PANIC / PC",
           "Estimate the factors explicitly by principal components, then test the common and "
           "idiosyncratic parts separately. Tells you <i>where</i> the non-stationarity lives.",
           C.PALETTE["grape"])
st.info("These two families — and exactly how they differ — are the subject of the next page.")

C.dev_footer()
