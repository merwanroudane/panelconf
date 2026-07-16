import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["csd"]
C.hero(
    "🌐 Cross-sectional dependence",
    "Units are not independent — they share hidden global shocks. Watch independent series "
    "SYNCHRONISE as a common factor takes over, then watch a first-generation test collapse "
    "because of it.",
    A, tag="The two complications",
)

C.section("The model", "How dependence is generated", A)
st.latex(r"y_{it}=\beta_i'x_{it}+u_{it},\qquad u_{it}=\underbrace{\gamma_i'f_t}_{\text{common}}+\underbrace{\varepsilon_{it}}_{\text{idiosyncratic}}")
st.markdown(
    "- $f_t$ — a few **unobserved common factors** (oil prices, crises, technology).\n"
    "- $\\gamma_i$ — unit-specific **loadings**: how exposed unit $i$ is to the shock.\n"
    "- $\\varepsilon_{it}$ — the genuinely unit-specific part."
)

# ---------------------------------------------------------------- animation 1
C.section("Simulation 1 — watch them synchronise", "Animation", A)
st.markdown(
    "The slider below the chart sweeps the **factor strength** from 0 to 1. At 0 the units are "
    "independent; at 1 they are driven by the same hidden shock."
)
C.play_hint("▶ PLAY and watch six independent series collapse into one co-moving bundle.")

rng = C.rng(6)
N, T = 6, 120
t = np.arange(T)
f = np.cumsum(rng.normal(0, 1, T))
f = (f - f.mean()) / f.std()
idio = [np.cumsum(rng.normal(0, 1, T)) for _ in range(N)]
idio = [(s - s.mean()) / s.std() for s in idio]
lams = [0.6 + rng.random() * 0.8 for _ in range(N)]
rhos = np.round(np.arange(0, 1.01, 0.05), 2)


def build(rho):
    return [rho * lams[i] * f + np.sqrt(max(1 - rho ** 2, 0)) * idio[i] for i in range(N)]


fig = go.Figure()
s0 = build(0.0)
for i in range(N):
    fig.add_trace(go.Scatter(x=t, y=s0[i], mode="lines", name=f"unit {i+1}",
                             line=dict(color=C.UNIT_COLORS[i], width=1.9)))
fig.add_trace(go.Scatter(x=t, y=f * 0, mode="lines", name="common factor fₜ",
                         line=dict(color=C.PALETTE["cyan"], width=4)))
fig.update_layout(xaxis=dict(title="time"), yaxis=dict(title="y", range=[-3.2, 3.2]))
frames = []
for r in rhos:
    s = build(r)
    frames.append(go.Frame(
        name=str(r),
        data=[go.Scatter(x=t, y=s[i], mode="lines",
                         line=dict(color=C.UNIT_COLORS[i], width=1.9)) for i in range(N)]
             + [go.Scatter(x=t, y=f * r, mode="lines",
                           line=dict(color=C.PALETTE["cyan"], width=4))]))
C.show(C.animate(fig, frames, duration=140, slider_prefix="factor strength ρ = ", height=440,
                 title="From independence (ρ=0) to strong dependence (ρ=1)"))
C.callout("What you're seeing",
          "At <b>ρ = 0</b> the six lines go their own way — spaghetti. As ρ rises they progressively "
          "lock onto the thick cyan line (the hidden factor). At <b>ρ = 1</b> they are essentially "
          "the <i>same</i> series with different amplitudes. <b>You have six series but almost one "
          "piece of information.</b>", A)

# ---------------------------------------------------------------- animation 2
C.section("Simulation 2 — why first-generation tests collapse", "Animation", A)
st.markdown(
    "First-generation tests (LLC, IPS, Pedroni) pool $N$ series **assuming independence**, so "
    "their variance formula divides by $N$ as if each unit were fresh evidence. Under a common "
    "factor there is far less independent information than $N$ — so the pooled statistic is too "
    "big and the test **over-rejects**."
)
C.play_hint("▶ PLAY to raise the dependence and watch the false-rejection rate explode.")

rho_grid = np.round(np.arange(0, 0.96, 0.05), 2)
size = 0.05 + 0.62 * rho_grid ** 1.7          # illustrative size distortion
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=[rho_grid[0]], y=[size[0]], mode="lines+markers",
                          line=dict(color=C.PALETTE["red"], width=3.5),
                          marker=dict(size=7, color=C.PALETTE["red"]),
                          name="actual rejection rate (1st-gen test)"))
fig2.add_hline(y=0.05, line=dict(color=C.PALETTE["teal"], dash="dash", width=2),
               annotation_text="nominal 5% — what it SHOULD be")
fig2.update_layout(xaxis=dict(title="degree of cross-sectional dependence", range=[-0.02, 1.0]),
                   yaxis=dict(title="P(reject a TRUE null)", range=[0, 0.72], tickformat=".0%"))
frames2 = [go.Frame(name=str(rho_grid[j]),
                    data=[go.Scatter(x=rho_grid[:j+1], y=size[:j+1], mode="lines+markers",
                                     line=dict(color=C.PALETTE["red"], width=3.5),
                                     marker=dict(size=7, color=C.PALETTE["red"]))])
           for j in range(len(rho_grid))]
C.show(C.animate(fig2, frames2, duration=160, slider_prefix="dependence = ", height=390,
                 title="Size distortion: the test rejects far more often than 5% (illustrative)"))
C.callout("The consequence",
          "A test that should reject a true null 5% of the time ends up rejecting it "
          "<b>50–65%</b> of the time. You will 'find' stationarity or cointegration that is "
          "<b>an artefact of the shared shock</b> — not economics. This is why the CD test is "
          "step one of any serious workflow.", C.PALETTE["red"])

# ---------------------------------------------------------------- remedies
C.section("The two remedies", "How dependence is removed", A)
c1, c2 = st.columns(2)
with c1:
    C.card("CCE — cross-sectional averages (Pesaran 2006)",
           "<b>Don't estimate the factors.</b> Their footprint is in the cross-section averages "
           "ȳₜ and x̄ₜ — so just add those as regressors and partial them out. You never need to "
           "know how many factors there are. <b>KPY (2011):</b> still valid even if fₜ is I(1).", A)
    st.latex(r"\hat\beta_i=(X_i'\bar M X_i)^{-1}X_i'\bar M y_i")
with c2:
    C.card("PANIC — principal components (Bai–Ng 2004)",
           "<b>Estimate the factors explicitly</b> by PCA. Because levels mix integration orders, "
           "difference first, extract, then re-cumulate — and test the common and idiosyncratic "
           "parts <i>separately</i>. Tells you <b>where</b> the non-stationarity lives.",
           C.PALETTE["grape"])
    st.latex(r"\Delta y_{it}\xrightarrow{\ \text{PCA}\ }\hat f_t=\textstyle\sum_{s\le t}\Delta\hat f_s")

st.markdown("Watch CCE remove the factor from one unit's series:")
C.play_hint("▶ PLAY to sweep how much of the factor CCE has partialled out.")

raw = 0.9 * f + 0.5 * idio[0]
zbar = f + C.rng(13).normal(0, 0.12, T)
steps = np.round(np.arange(0, 1.01, 0.05), 2)
co = np.polyfit(zbar, raw, 1)
proj = co[0] * zbar + co[1]
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=t, y=raw, mode="lines", name="unit's series (contaminated)",
                          line=dict(color=C.PALETTE["orange"], width=2.4)))
fig3.add_trace(go.Scatter(x=t, y=zbar, mode="lines", name="cross-section average z̄ₜ (the proxy)",
                          line=dict(color=C.PALETTE["cyan"], width=2, dash="dot")))
fig3.add_trace(go.Scatter(x=t, y=raw, mode="lines", name="after de-factoring",
                          line=dict(color=C.PALETTE["teal"], width=3)))
fig3.update_layout(xaxis=dict(title="time"), yaxis=dict(title="y", range=[-4, 4]))
frames3 = [go.Frame(name=str(s),
                    data=[go.Scatter(x=t, y=raw, mode="lines",
                                     line=dict(color=C.PALETTE["orange"], width=2.4)),
                          go.Scatter(x=t, y=zbar, mode="lines",
                                     line=dict(color=C.PALETTE["cyan"], width=2, dash="dot")),
                          go.Scatter(x=t, y=raw - s * proj, mode="lines",
                                     line=dict(color=C.PALETTE["teal"], width=3))])
           for s in steps]
C.show(C.animate(fig3, frames3, duration=140, slider_prefix="factor removed = ", height=400,
                 title="CCE de-factoring: the wandering common trend is subtracted away"))
C.callout("Result",
          "The orange series wanders because of the shared shock. As the average is partialled "
          "out, the teal series becomes what unit i would have looked like <b>without</b> the "
          "global shock — that is what CCE regressions actually estimate on.", A)

C.section("Testing for it first", "Always step 1", A)
st.latex(r"CD=\sqrt{\frac{2T}{N(N-1)}}\sum_{i<j}\hat\rho_{ij}\ \xrightarrow{d}\ N(0,1)")
st.code("xtset id year\nxtcd2 y            // Pesaran CD test — reject ⇒ 1st generation is dead",
        language="stata")

C.dev_footer()
