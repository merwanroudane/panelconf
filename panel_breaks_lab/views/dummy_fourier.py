import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["fourier"]
C.hero(
    "🌊 Dummy vs Fourier",
    "Two ways to write a break into a model: a sharp STEP at an estimated date, or smooth "
    "TRIGONOMETRIC terms that need no date at all. Watch them race as the break morphs from "
    "an instant jump to a slow transition.",
    A, tag="How to model a break",
)

C.section("The two philosophies", "Sharp vs smooth", A)
c1, c2 = st.columns(2)
with c1:
    C.card("🔲 Dummy — sharp", "A step at date T_B. The date must be estimated (SSR grid search), "
           "and you must choose how many breaks.", C.PALETTE["red"])
    st.latex(r"D_t=\mu+\theta\cdot\mathbf 1\{t>T_B\}")
with c2:
    C.card("〰️ Fourier — smooth", "A few sine/cosine terms. <b>No date, no count</b> — they "
           "approximate whatever smooth shape is there (Gallant 1981).", C.PALETTE["grape"])
    st.latex(r"d_t=a_0+a_1\sin\tfrac{2\pi kt}{T}+a_2\cos\tfrac{2\pi kt}{T}")

# ---------------------------------------------------------------- the race
C.section("The race — watch the break morph", "Animation 1", A)
st.markdown(
    "The animation sweeps the **transition speed γ** of a logistic break. On the left it is a "
    "**slow, gradual** change; on the right it becomes an **instant step**. Both methods try to "
    "fit it. Watch which one tracks the black truth."
)
C.play_hint("▶ PLAY — watch Fourier win on the left, and Dummy take over on the right.")

T = 140
t = np.arange(T)
TBtrue = 70
gammas = np.round(np.concatenate([np.arange(0.04, 0.30, 0.02),
                                  np.arange(0.30, 1.6, 0.12),
                                  np.arange(1.6, 8.1, 0.7)]), 3)
rng = C.rng(8)
eps = rng.normal(0, 0.16, T)

fits_d, fits_f, truths, sse_d, sse_f = [], [], [], [], []
for g in gammas:
    true = 2.0 / (1 + np.exp(-g * (t - TBtrue)))
    data = true + eps
    # dummy fit: grid search the break date
    best, bs = None, np.inf
    for tb in range(20, T - 20):
        m1, m2 = data[:tb].mean(), data[tb:].mean()
        s = ((data[:tb] - m1) ** 2).sum() + ((data[tb:] - m2) ** 2).sum()
        if s < bs:
            bs, best = s, tb
    dfit = np.where(t >= best, data[best:].mean(), data[:best].mean())
    # fourier fit: best k over a small grid
    bf, bfs = None, np.inf
    for k in np.arange(0.4, 2.6, 0.1):
        X = np.column_stack([np.ones(T), np.sin(2*np.pi*k*t/T), np.cos(2*np.pi*k*t/T)])
        co = np.linalg.lstsq(X, data, rcond=None)[0]
        ff = X @ co
        s = ((data - ff) ** 2).sum()
        if s < bfs:
            bfs, bf = s, ff
    truths.append(true); fits_d.append(dfit); fits_f.append(bf)
    sse_d.append(float(bs)); sse_f.append(float(bfs))

data0 = truths[0] + eps
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=data0, mode="markers", name="data",
                         marker=dict(size=3.5, color="#C9D0DA")))
fig.add_trace(go.Scatter(x=t, y=truths[0], mode="lines", name="TRUE break",
                         line=dict(color=C.PALETTE["ink"], width=3)))
fig.add_trace(go.Scatter(x=t, y=fits_d[0], mode="lines", name="Dummy fit",
                         line=dict(color=C.PALETTE["red"], width=2.4, shape="hv")))
fig.add_trace(go.Scatter(x=t, y=fits_f[0], mode="lines", name="Fourier fit",
                         line=dict(color=C.PALETTE["grape"], width=2.6)))
fig.update_layout(xaxis=dict(title="time"), yaxis=dict(title="y", range=[-0.7, 2.7]))
frames = []
for j, g in enumerate(gammas):
    d = truths[j] + eps
    win = "FOURIER wins" if sse_f[j] < sse_d[j] else "DUMMY wins"
    frames.append(go.Frame(
        name=str(g),
        data=[go.Scatter(x=t, y=d, mode="markers", marker=dict(size=3.5, color="#C9D0DA")),
              go.Scatter(x=t, y=truths[j], mode="lines",
                         line=dict(color=C.PALETTE["ink"], width=3)),
              go.Scatter(x=t, y=fits_d[j], mode="lines",
                         line=dict(color=C.PALETTE["red"], width=2.4, shape="hv")),
              go.Scatter(x=t, y=fits_f[j], mode="lines",
                         line=dict(color=C.PALETTE["grape"], width=2.6))],
        layout=go.Layout(title=f"γ = {g}  →  {win}   (SSR: dummy {sse_d[j]:.2f} vs fourier {sse_f[j]:.2f})")))
C.show(C.animate(fig, frames, duration=190, slider_prefix="transition speed γ = ", height=440,
                 title=f"γ = {gammas[0]}  →  {'FOURIER wins' if sse_f[0] < sse_d[0] else 'DUMMY wins'}"))

C.callout("What you're seeing",
          "<b>Small γ (gradual):</b> the truth is a slow S-curve. The dummy is forced to "
          "approximate it with one hard jump and misses badly; the Fourier curve bends with it. "
          "<b>Large γ (sharp):</b> the truth is a step. The dummy nails it exactly, while the "
          "Fourier curve <b>cannot turn a corner</b> — it smooths through and overshoots on both "
          "sides. <b>Neither method wins everywhere — the break's shape decides.</b>", A)

# ---------------------------------------------------------------- SSR race
C.section("The scoreboard", "Animation 2", A)
st.markdown("The same race, as a scoreboard: which method has the lower error at each γ?")
C.play_hint("▶ PLAY to watch the two error curves cross.")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=[gammas[0]], y=[sse_d[0]], mode="lines",
                          line=dict(color=C.PALETTE["red"], width=3), name="Dummy SSR"))
fig2.add_trace(go.Scatter(x=[gammas[0]], y=[sse_f[0]], mode="lines",
                          line=dict(color=C.PALETTE["grape"], width=3), name="Fourier SSR"))
fig2.update_layout(xaxis=dict(title="transition speed γ  (gradual → sharp)", type="log",
                              range=[np.log10(gammas[0]), np.log10(gammas[-1])]),
                   yaxis=dict(title="SSR (lower is better)"))
frames2 = [go.Frame(name=str(gammas[j]),
                    data=[go.Scatter(x=gammas[:j+1], y=sse_d[:j+1], mode="lines",
                                     line=dict(color=C.PALETTE["red"], width=3)),
                          go.Scatter(x=gammas[:j+1], y=sse_f[:j+1], mode="lines",
                                     line=dict(color=C.PALETTE["grape"], width=3))])
           for j in range(len(gammas))]
C.show(C.animate(fig2, frames2, duration=150, slider_prefix="γ = ", height=380,
                 title="Where the curves cross is where you should switch method"))

# ---------------------------------------------------------------- multiple breaks
C.section("Fourier's superpower: several breaks, one term", "Animation 3", A)
st.markdown(
    "**Gallant's theorem (1981):** a few low-frequency sine/cosine terms approximate *any* smooth, "
    "bounded deviation — including **several** gradual breaks. A single dummy cannot do this at all."
)
C.play_hint("▶ PLAY to sweep the frequency k against a TWO-break truth.")
T2 = 150
t2 = np.arange(T2)
true2 = 1.0/(1+np.exp(-0.25*(t2-40))) - 1.2/(1+np.exp(-0.3*(t2-105)))
d2 = true2 + C.rng(2).normal(0, 0.09, T2)
ks = np.round(np.arange(0.3, 3.05, 0.1), 2)
ffits, fsse = [], []
for k in ks:
    X = np.column_stack([np.ones(T2), np.sin(2*np.pi*k*t2/T2), np.cos(2*np.pi*k*t2/T2)])
    co = np.linalg.lstsq(X, d2, rcond=None)[0]
    ffits.append(X @ co); fsse.append(float(((d2 - X @ co) ** 2).sum()))
bk = int(np.argmin(fsse))
fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=t2, y=d2, mode="markers", name="data",
                          marker=dict(size=3.5, color="#C9D0DA")))
fig3.add_trace(go.Scatter(x=t2, y=true2, mode="lines", name="TRUE — two gradual breaks",
                          line=dict(color=C.PALETTE["ink"], width=3)))
fig3.add_trace(go.Scatter(x=t2, y=ffits[0], mode="lines", name="Fourier (one frequency)",
                          line=dict(color=C.PALETTE["grape"], width=3)))
fig3.update_layout(xaxis=dict(title="time"), yaxis=dict(title="y"))
frames3 = [go.Frame(name=str(ks[j]),
                    data=[go.Scatter(x=t2, y=d2, mode="markers",
                                     marker=dict(size=3.5, color="#C9D0DA")),
                          go.Scatter(x=t2, y=true2, mode="lines",
                                     line=dict(color=C.PALETTE["ink"], width=3)),
                          go.Scatter(x=t2, y=ffits[j], mode="lines",
                                     line=dict(color=C.PALETTE["grape"], width=3))])
           for j in range(len(ks))]
C.show(C.animate(fig3, frames3, duration=110, slider_prefix="frequency k = ", height=400,
                 title="ONE Fourier frequency capturing TWO gradual breaks"))
st.success(f"✅ Best fit at **k = {ks[bk]}** — a *fractional* frequency, and it captures **both** "
           f"breaks with a single term. No dates estimated, no break count specified.")
C.callout("Fractional frequencies",
          "Integer k (1, 2, 3…) is a coarse grid. The <b>FFFFF</b> approach (Olayeni, Tiwari & "
          "Wohar 2021) searches non-integer k ∈ [0.1, 5] and picks the SSR-minimising value — a "
          "much better fit to an unknown break shape. Used in <code>xtpqroot, fourier</code> and "
          "<code>xtpfardl</code>.", A)

# ---------------------------------------------------------------- decision
C.section("So which do I use?", "The rule", A)
st.markdown(
    "| | **Dummy** | **Fourier** |\n"
    "|---|---|---|\n"
    "| Break shape | sharp step | gradual bend |\n"
    "| Break date | must be estimated | **not needed** |\n"
    "| Number of breaks | must be chosen | one frequency covers several |\n"
    "| Different dates per unit | ❌ dummy explosion | ✅ unit-specific Fourier |\n"
    "| Tells you the date? | ✅ yes | ❌ no |\n"
    "| Best when | a clear policy date / crisis | unknown, gradual, or multiple |\n"
    "| Commands | `xtpkpss` · `xtlmbreak` · `xtpcointegwe` | `xtpqroot, fourier` · `xtpfardl` · `xtfmg fccemg` |"
)
C.callout("Best of both — the tFR test",
          "Corakci & Omay (2023) put a <b>fractional Fourier</b> term (smooth) and a <b>logistic "
          "transition</b> term (sharp) in the <i>same</i> regression, so the data decide which is "
          "present — you don't have to. That is <code>xtpqroot, fourier</code>.", A)

C.dev_footer()
