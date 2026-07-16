import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["home"]
C.hero(
    "Panel Breaks — Interactive Simulation Lab",
    "Don't just read about structural breaks — WATCH them happen. Every page is an animated "
    "simulation with a PLAY button, so you can see exactly what a common break, a heterogeneous "
    "break, cross-sectional dependence, or a lasso penalty actually does to your data.",
    A, tag="Learn by watching",
)

c1, c2 = st.columns([2, 1])
with c1:
    st.markdown(
        "Structural-break econometrics is full of words that sound abstract — *common break*, "
        "*latent groups*, *cross-sectional dependence*, *fused lasso*. They stop being abstract "
        "the moment you **see** them move."
    )
    st.markdown(
        "Each page here simulates data where **you control the truth**, then animates what "
        "happens. Move a slider, press **▶ PLAY**, and watch."
    )
with c2:
    C.callout("Developed by",
              "<b>Dr Merwan Roudane</b><br>Author of the <b>xt*</b> panel structural-break "
              "Stata suite (100+ modules).<br>"
              '<a href="https://ideas.repec.org/f/pro1421.html">IDEAS/RePEc</a> · '
              '<a href="https://github.com/merwanroudane">GitHub</a>', A)

# ---------------------------------------------------------------- teaser
C.section("A taste — press PLAY", "The whole field in one animation", A)
st.markdown(
    "Six units. Watch the series **draw themselves through time**. At the dashed line every "
    "unit jumps *together* — that is a **common structural break**."
)
C.play_hint()

rng = C.rng(11)
N, T, TB = 6, 100, 55
t = np.arange(T)
series = []
for i in range(N):
    lvl = (i - 2.5) * 1.6
    jump = 4.0
    y = lvl + np.cumsum(rng.normal(0, .30, T)) + np.where(t >= TB, jump, 0.0)
    series.append(y)

fig = go.Figure()
for i in range(N):
    fig.add_trace(go.Scatter(x=[t[0]], y=[series[i][0]], mode="lines",
                             name=f"unit {i+1}",
                             line=dict(color=C.UNIT_COLORS[i], width=2.6)))
fig.add_vline(x=TB, line=dict(color=C.PALETTE["red"], dash="dash", width=2),
              annotation_text="break", annotation_position="top")
lo = min(s.min() for s in series) - 1
hi = max(s.max() for s in series) + 1
fig.update_layout(xaxis=dict(range=[0, T - 1], title="time"),
                  yaxis=dict(range=[lo, hi], title="y"))

frames = []
for k in range(2, T + 1, 2):
    frames.append(go.Frame(
        name=str(k),
        data=[go.Scatter(x=t[:k], y=series[i][:k], mode="lines",
                         line=dict(color=C.UNIT_COLORS[i], width=2.6)) for i in range(N)]))
C.show(C.animate(fig, frames, duration=45, slider_prefix="t = ", height=440,
                 title="A common structural break, drawn through time"))

C.callout("What you just saw",
          "Before the dashed line the six units wander independently around their own levels. "
          "At the line they <b>all jump at once</b>. That synchronised jump is the signature of a "
          "<b>common break</b> — and it is only <i>one</i> of the possibilities. The next pages "
          "show what happens when units break at <i>different</i> dates, in <i>groups</i>, or when "
          "they share a hidden common shock.", A)

# ---------------------------------------------------------------- map
C.section("What's in the lab", "Your route", A)
cards = [
    ("1️⃣ Common break", "All units break at the same date. Fewest parameters, most power — "
     "if it's true.", C.TOPIC["common"]),
    ("2️⃣ Heterogeneous breaks", "Every unit breaks on its own schedule. Realistic, but the "
     "parameters explode.", C.TOPIC["hetero"]),
    ("3️⃣ Latent (grouped) breaks", "Hidden clusters, each with its own date. The clever middle "
     "ground — GAGFL.", C.TOPIC["latent"]),
    ("🌐 Cross-sectional dependence", "Watch independent units synchronise as a common factor "
     "takes over — and see a test over-reject.", C.TOPIC["csd"]),
    ("🌊 Dummy vs Fourier", "Race the two methods as the break morphs from a sharp step to a "
     "slow transition.", C.TOPIC["fourier"]),
    ("🎛️ Regularization", "Turn the penalty λ up and watch spurious breaks fuse away — then "
     "watch real ones die too.", C.TOPIC["regular"]),
    ("🎯 Finding the date", "Watch the SSR grid search sweep the sample and lock onto the break.",
     C.TOPIC["methods"]),
]
cc = st.columns(3)
for i, (t_, b_, col) in enumerate(cards):
    with cc[i % 3]:
        C.card(t_, b_, col)

C.callout("How to use the lab",
          "Every chart has <b>▶ PLAY</b> and a <b>slider</b> underneath. Press PLAY to run the "
          "animation, or drag the slider to step through it frame by frame. The sliders "
          "<i>above</i> each chart change the <b>truth</b> of the simulation — change them and "
          "play again to see how the picture responds.", A)

C.dev_footer()
