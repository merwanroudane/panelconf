import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["hetero"]
C.hero(
    "2️⃣ Heterogeneous breaks",
    "Every unit breaks on its OWN date. Realistic — shocks don't reach every country at the "
    "same speed — but the parameters explode and CCE stops working. Watch the units jump one "
    "by one.",
    A, tag="Types of break",
)

C.section("The model", "What 'heterogeneous' means", A)
st.latex(r"T_{Bi}\neq T_{Bj}\qquad\text{for some } i\neq j")
st.markdown(
    "Now the break date **carries an $i$ subscript**. Each unit $i$ has its own date $T_{Bi}$, "
    "its own jump size, and possibly its own regime coefficients:"
)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta_i(t)+\varepsilon_{it},\qquad "
         r"\beta_i(t)=\begin{cases}\beta_{i1} & t<T_{Bi}\\ \beta_{i2} & t\ge T_{Bi}\end{cases}")

C.callout("Real-world example",
          "The <b>energy transition</b>: Germany broke in 2011 (nuclear phase-out), Japan in 2012 "
          "(post-Fukushima), Spain in 2015 (renewables reform). Same kind of shock — three "
          "different dates. Imposing one common date would match none of them.", A)

# ---------------------------------------------------------------- sim
C.section("Simulation — watch them jump one by one", "Animation 1", A)
c1, c2 = st.columns(2)
spread = c1.slider("How spread out are the break dates?", 0, 40, 25,
                   help="0 = all units break at the same date (common). Large = fully heterogeneous.")
jump = c2.slider("Break size", 0.0, 8.0, 4.0, 0.5)
C.play_hint()

rng = C.rng(3)
N, T = 6, 100
t = np.arange(T)
centre = 50
if spread == 0:
    dates = [centre] * N
else:
    dates = list(np.linspace(centre - spread / 2, centre + spread / 2, N).astype(int))

series = [(i - 2.5) * 1.7 + np.cumsum(rng.normal(0, .30, T)) + np.where(t >= dates[i], jump, 0.0)
          for i in range(N)]

fig = go.Figure()
for i in range(N):
    fig.add_trace(go.Scatter(x=[t[0]], y=[series[i][0]], mode="lines",
                             name=f"unit {i+1} (T_B={dates[i]})",
                             line=dict(color=C.UNIT_COLORS[i], width=2.6)))
for i in range(N):
    fig.add_vline(x=dates[i], line=dict(color=C.UNIT_COLORS[i], dash="dot", width=1.2))
lo = min(s.min() for s in series) - 1
hi = max(s.max() for s in series) + 1
fig.update_layout(xaxis=dict(range=[0, T - 1], title="time"), yaxis=dict(range=[lo, hi], title="y"))
frames = [go.Frame(name=str(k),
                   data=[go.Scatter(x=t[:k], y=series[i][:k], mode="lines",
                                    line=dict(color=C.UNIT_COLORS[i], width=2.6))
                         for i in range(N)])
          for k in range(2, T + 1, 2)]
C.show(C.animate(fig, frames, duration=45, slider_prefix="t = ", height=430,
                 title="Heterogeneous breaks: each unit has its own dotted date"))

if spread == 0:
    C.callout("You set spread = 0", "All dates collapse to one — this is now the <b>common break</b> "
              "case. Slide 'spread' up and play again to see them separate.", A)
elif spread > 30:
    C.callout("Fully heterogeneous", "The units jump at clearly different times. Notice there is no "
              "single vertical line you could draw. A common-break method would be forced to pick "
              "one date that fits <b>nobody</b>.", C.PALETTE["red"])
else:
    C.callout("What you're seeing", "Each unit jumps at its own dotted line. The shock is the same "
              "<i>kind</i>, but it arrives at different <i>times</i>.", A)

# ---------------------------------------------------------------- cost
C.section("Why this is hard", "The parameter explosion", A)
st.markdown(
    "Compare what you must estimate:"
)
st.markdown(
    "| | Common break | Heterogeneous breaks |\n"
    "|---|---|---|\n"
    "| Break dates | **1** | **N** |\n"
    "| Regime coefficients | 2 | 2N |\n"
    "| Evidence per date | all N units | only unit *i*'s own T observations |\n"
    "| Works with CCE? | ✅ yes | ❌ no — CCE needs a common break |"
)
C.callout("Two real problems",
          "<b>1. Statistical:</b> each date is estimated from <i>one</i> unit's data only, so you "
          "need a long T per unit. <br><b>2. Practical:</b> the CCE approach (cross-section "
          "averages) assumes a common break — it cannot be applied directly here.",
          C.PALETTE["red"])

# ---------------------------------------------------------------- solution
C.section("The elegant solution: absorb them with Fourier", "Animation 2", A)
st.markdown(
    "You cannot put $N$ dummy sets in the model. But you **can** give each unit a couple of "
    "**Fourier terms** that bend with whatever its own transition looks like — while cross-section "
    "averages remove the common shock. That is **Fourier CCEMG** (`xtfmg fccemg`):"
)
st.latex(r"y_{it}=\beta_i'x_{it}+\underbrace{c_{0i}+c_{1i}\sin\tfrac{2\pi t}{T}+c_{2i}\cos\tfrac{2\pi t}{T}}_{\text{unit-specific: absorbs unit } i\text{'s break}}+\underbrace{\delta_i'\bar z_t}_{\text{CCE: kills the common shock}}+\varepsilon_{it}")
st.markdown("Watch a unit-specific Fourier curve bend to fit a unit's own break:")
C.play_hint("▶ PLAY to sweep the Fourier frequency k and watch it lock onto the break shape.")

Tf = 120
tf = np.arange(Tf)
true = 2.0 / (1 + np.exp(-0.18 * (tf - 62)))
data = true + C.rng(9).normal(0, 0.16, Tf)
ks = np.round(np.arange(0.3, 3.05, 0.1), 2)
fits = []
for k in ks:
    X = np.column_stack([np.ones(Tf), np.sin(2 * np.pi * k * tf / Tf), np.cos(2 * np.pi * k * tf / Tf)])
    co = np.linalg.lstsq(X, data, rcond=None)[0]
    fits.append(X @ co)
sse = [float(((data - f) ** 2).sum()) for f in fits]
best = int(np.argmin(sse))

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=tf, y=data, mode="markers", name="unit i's data",
                          marker=dict(size=4, color="#C3CAD6")))
fig2.add_trace(go.Scatter(x=tf, y=true, mode="lines", name="true (gradual) break",
                          line=dict(color=C.PALETTE["ink"], width=2.5, dash="dot")))
fig2.add_trace(go.Scatter(x=tf, y=fits[0], mode="lines", name="Fourier fit",
                          line=dict(color=C.PALETTE["grape"], width=3.2)))
fig2.update_layout(xaxis=dict(title="time"), yaxis=dict(title="y"))
frames2 = [go.Frame(name=str(ks[j]),
                    data=[go.Scatter(x=tf, y=data, mode="markers",
                                     marker=dict(size=4, color="#C3CAD6")),
                          go.Scatter(x=tf, y=true, mode="lines",
                                     line=dict(color=C.PALETTE["ink"], width=2.5, dash="dot")),
                          go.Scatter(x=tf, y=fits[j], mode="lines",
                                     line=dict(color=C.PALETTE["grape"], width=3.2))])
           for j in range(len(ks))]
C.show(C.animate(fig2, frames2, duration=110, slider_prefix="Fourier frequency k = ", height=400,
                 title="One unit's own break, absorbed by its own Fourier terms"))
st.success(f"✅ The SSR is minimised at **k = {ks[best]}** — the frequency the data chose by itself. "
           f"No break date was ever estimated.")

C.callout("The trade-off",
          "Fourier <b>absorbs</b> heterogeneously-timed breaks so your slope estimate is clean — "
          "but it does <b>not tell you the break dates</b>. If the dates are your research "
          "question, you need a grouped or dummy method instead.", A)

C.section("Which commands handle heterogeneous timing?", "Software", A)
c1, c2 = st.columns(2)
with c1:
    C.card("xtfmg fccemg", "Fourier CCE Mean Group (Guliyev 2026) — absorbs unit-specific breaks, "
           "removes the common shock. Lowest RMSE across weak/moderate/strong dependence.", A)
with c2:
    C.card("xtbreakmodel, method(gagfl)", "If the dates cluster into <b>groups</b> rather than being "
           "all different, GAGFL recovers the groups <i>and</i> their dates — see the next page.",
           C.TOPIC["latent"])

C.dev_footer()
