import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["dummyfourier"]
C.hero(
    "Dummy vs Fourier",
    "There are two classical ways to write a structural break into a model: a step DUMMY at an "
    "estimated date (sharp), or FOURIER terms that bend smoothly (gradual). This page shows when "
    "each wins.",
    A, tag="Modelling toolkits",
)

# ================================================================
C.section("1 · The two philosophies", "Sharp vs smooth", A)
c1, c2 = st.columns(2)
with c1:
    C.card("🔲 Dummy approach — SHARP",
           "Add step dummies at estimated break dates. The break is <b>instantaneous</b>. "
           "You must decide <b>how many</b> breaks, and each estimated date changes the critical "
           "values.", C.PALETTE["red"])
    st.latex(r"D_{t}=\mu+\theta\,\mathbf 1\{t>T_B\}")
with c2:
    C.card("〰️ Fourier approach — SMOOTH",
           "Add a few sine/cosine terms. The break is <b>gradual</b>, and you never estimate a "
           "date — the trigonometric terms approximate whatever smooth shape is there.",
           C.PALETTE["grape"])
    st.latex(r"d_t=a_0+a_1\sin\!\Big(\tfrac{2\pi k t}{T}\Big)+a_2\cos\!\Big(\tfrac{2\pi k t}{T}\Big)")

# ================================================================
C.section("2 · See them fit the same data", "Interactive", A)
shape = st.radio("What is the TRUE break shape?",
                 ["Sharp jump (a policy date)", "Gradual transition (slow change)",
                  "Two gradual breaks"], horizontal=False)
T = 150
t = np.arange(T)
if shape.startswith("Sharp"):
    true = np.where(t >= 75, 1.5, 0.0)
elif shape.startswith("Gradual"):
    true = 1.5 / (1 + np.exp(-0.12 * (t - 75)))
else:
    true = 1.0 / (1 + np.exp(-0.25 * (t - 40))) - 1.2 / (1 + np.exp(-0.3 * (t - 105)))

rng = C.rng(4)
data = true + rng.normal(0, 0.22, T)

# dummy fit (single break, grid search on SSR)
best, bssr = None, np.inf
for tb in range(20, T - 20):
    m1, m2 = data[:tb].mean(), data[tb:].mean()
    s = ((data[:tb] - m1) ** 2).sum() + ((data[tb:] - m2) ** 2).sum()
    if s < bssr:
        bssr, best = s, tb
dummy_fit = np.where(t >= best, data[best:].mean(), data[:best].mean())

# fourier fit (k=1)
k = 1.0
Xf = np.column_stack([np.ones(T), np.sin(2 * np.pi * k * t / T), np.cos(2 * np.pi * k * t / T)])
coef = np.linalg.lstsq(Xf, data, rcond=None)[0]
four_fit = Xf @ coef

fig = go.Figure()
fig.add_trace(go.Scatter(y=data, mode="markers", marker=dict(size=4, color="#C3CAD6"), name="data"))
fig.add_trace(go.Scatter(y=true, name="TRUE break", line=dict(color=C.PALETTE["ink"], width=3)))
fig.add_trace(go.Scatter(y=dummy_fit, name=f"Dummy fit (T̂_B={best})",
                         line=dict(color=C.PALETTE["red"], width=2.4, shape="hv")))
fig.add_trace(go.Scatter(y=four_fit, name="Fourier fit (k=1)",
                         line=dict(color=C.PALETTE["grape"], width=2.4)))
C.show(fig, height=380, title="Same data, two ways to model the break")

sse_d = ((data - dummy_fit) ** 2).sum()
sse_f = ((data - four_fit) ** 2).sum()
c1, c2 = st.columns(2)
c1.metric("Dummy SSR", f"{sse_d:.1f}")
c2.metric("Fourier SSR", f"{sse_f:.1f}")
if shape.startswith("Sharp"):
    C.callout("Dummy wins here", "The truth IS a step. The dummy nails it exactly; the Fourier "
              "curve cannot turn a corner, so it smooths through the jump and misses the timing.",
              C.PALETTE["red"])
elif shape.startswith("Gradual"):
    C.callout("Fourier wins here", "The truth is a smooth S-curve. The single dummy is forced to "
              "approximate it with one hard jump; the Fourier term bends with it.",
              C.PALETTE["grape"])
else:
    C.callout("Fourier wins clearly", "There are TWO gradual breaks. A single dummy cannot "
              "represent them at all, while <b>one</b> Fourier frequency captures both — with no "
              "dates to estimate.", C.PALETTE["grape"])

# ================================================================
C.section("3 · Why one Fourier term can capture several breaks", "Gallant's theorem", A)
st.markdown(
    "**Gallant (1981):** a few low-frequency sine/cosine terms can approximate *any* smooth, "
    "bounded deviation — including several gradual breaks — because they form a basis for smooth "
    "functions. That is why you rarely need more than $n=1$ (Enders–Lee)."
)
st.latex(r"d_t=\alpha_0+\alpha_1 t+\sum_{k=1}^{n}\Big[a_k\sin\!\Big(\tfrac{2\pi k t}{T}\Big)+b_k\cos\!\Big(\tfrac{2\pi k t}{T}\Big)\Big]")
kk = st.slider("Fourier frequency k", 0.5, 3.0, 1.0, 0.1)
fig = go.Figure()
fig.add_trace(go.Scatter(y=np.sin(2 * np.pi * kk * t / T), name=f"sin(2π·{kk}·t/T)",
                         line=dict(color=C.PALETTE["grape"], width=2.6)))
fig.add_trace(go.Scatter(y=np.cos(2 * np.pi * kk * t / T), name=f"cos(2π·{kk}·t/T)",
                         line=dict(color=C.PALETTE["cyan"], width=2.6)))
C.show(fig, height=280, title=f"The Fourier basis at k = {kk}")
C.callout("Fractional frequencies",
          "Integer k (1, 2, 3…) is a coarse grid. The <b>fractional frequency</b> version searches "
          "non-integer k ∈ [0.1, 5] and picks the value minimising the SSR — a much better fit to "
          "an unknown break shape (Olayeni, Tiwari & Wohar 2021; the FFFFF panel cointegration "
          "test). Also used in <code>xtpqroot, fourier</code>.", A)

# ================================================================
C.section("4 · The logistic smooth transition (LST)", "The third option: tunable sharpness", A)
st.markdown("A logistic function nests both worlds — $\\gamma$ controls how sharp the break is:")
st.latex(r"F(t)=\Big[1+\exp\big(-\gamma\,(t/T-\tau)\big)\Big]^{-1}")
g = st.slider("γ (transition speed)", 0.5, 60.0, 5.0, 0.5)
fig = go.Figure()
for gg, col in [(g, "orange"), (0.5, "teal"), (60, "red")]:
    fig.add_trace(go.Scatter(y=1 / (1 + np.exp(-gg * (t / T - 0.5))),
                             name=f"γ = {gg}", line=dict(color=C.PALETTE[col],
                             width=3 if gg == g else 1.6, dash=None if gg == g else "dot")))
C.show(fig, height=300, title="γ → ∞ gives a step (sharp); small γ gives a gradual transition")
C.callout("Best of both — the tFR test",
          "Corakci & Omay (2023) combine a <b>fractional Fourier</b> term (smooth) with an "
          "<b>LST</b> term (sharp) in the same regression, so the data decide. That is what "
          "<code>xtpqroot, fourier</code> estimates: k^fr, γ and τ together.", A)

# ================================================================
C.section("5 · The decision table", "Which one, when", A)
st.markdown(
    "| | **Dummy (sharp)** | **Fourier (smooth)** |\n"
    "|---|---|---|\n"
    "| Break shape | instantaneous step | gradual bend |\n"
    "| Break date | must be **estimated** (SSR grid) | **not needed** |\n"
    "| Number of breaks | must be chosen (IC / sup-F) | one frequency covers several |\n"
    "| Critical values | depend on trimming & break count | depend on frequency k |\n"
    "| Handles heterogeneous timing? | badly (too many dummies) | ✅ yes (unit-specific Fourier) |\n"
    "| Best when | a clear policy date / crisis | unknown, gradual, or multiple breaks |\n"
    "| Risk | over-fitting with many dummies | misses a genuinely sharp jump |\n"
    "| Example commands | `xtpkpss model(constbreak)`, `xtlmbreak` | `xtpqroot, fourier`, `xtpfardl` |"
)
C.callout("A third way",
          "There is also <b>regularization</b> (the next page): let the coefficient change every "
          "period but <i>penalise</i> changes, so the data select the breaks automatically — no "
          "dummies to specify and no smoothness assumed.", A)

C.dev_footer()
