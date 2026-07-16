import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import common as C

A = C.TOPIC["methods"]
C.hero(
    "🎯 How a break date is actually found",
    "Watch the SSR grid search sweep across the sample, split the data at every candidate date, "
    "and lock onto the true break. Then see why trimming matters and why the estimate is "
    "'super-consistent'.",
    A, tag="How to model a break",
)

C.section("The estimator", "One line of maths", A)
st.latex(r"\hat T_B=\arg\min_{T_B\in[\varepsilon T,\,(1-\varepsilon)T]}\ \mathrm{SSR}(T_B)")
st.markdown(
    "For **every** candidate date: split the sample, run OLS on each side, add the two residual "
    "sums of squares. The date with the **lowest total SSR** is the estimate. That is all."
)

# ---------------------------------------------------------------- main animation
C.section("Simulation — watch the search", "Animation", A)
c1, c2 = st.columns(2)
size = c1.slider("Break size (β jumps from 0.6 to …)", 0.8, 4.0, 2.2, 0.1)
nz = c2.slider("Noise", 0.2, 1.5, 0.5, 0.05)
C.play_hint("▶ PLAY — the vertical line is the candidate date being tried; the bottom panel is "
            "the SSR being built.")

T, TBtrue = 100, 62
rng = C.rng(14)
x = rng.normal(0, 1, T)
b = np.where(np.arange(T) >= TBtrue, size, 0.6)
y = b * x + rng.normal(0, nz, T)
cands = np.arange(15, 86)

ssr, fits = [], []
for tb in cands:
    tot, fit = 0.0, np.zeros(T)
    for lo, hi in [(0, tb), (tb, T)]:
        xx, yy = x[lo:hi], y[lo:hi]
        bb = np.sum(xx * yy) / np.sum(xx * xx)
        fit[lo:hi] = bb
        tot += np.sum((yy - bb * xx) ** 2)
    ssr.append(tot); fits.append(fit)
ssr = np.array(ssr)
best = int(cands[np.argmin(ssr)])

fig = make_subplots(rows=2, cols=1, row_heights=[0.5, 0.5], vertical_spacing=0.14,
                    subplot_titles=("Fitted β on each side of the candidate date",
                                    "Total SSR as the candidate sweeps"))
fig.add_trace(go.Scatter(x=np.arange(T), y=b, mode="lines", name="TRUE β path",
                         line=dict(color=C.PALETTE["ink"], width=2.2, dash="dot", shape="hv")),
              row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(T), y=fits[0], mode="lines", name="fitted β (2 regimes)",
                         line=dict(color=C.PALETTE["pink"], width=3, shape="hv")), row=1, col=1)
fig.add_trace(go.Scatter(x=[cands[0], cands[0]], y=[0, size + 1], mode="lines",
                         name="candidate date", line=dict(color=C.PALETTE["orange"], width=2.5)),
              row=1, col=1)
fig.add_trace(go.Scatter(x=[cands[0]], y=[ssr[0]], mode="lines", name="SSR",
                         line=dict(color=C.PALETTE["blue"], width=3)), row=2, col=1)
fig.add_trace(go.Scatter(x=[cands[0]], y=[ssr[0]], mode="markers", name="current candidate",
                         marker=dict(size=11, color=C.PALETTE["orange"])), row=2, col=1)
fig.update_yaxes(title_text="β", range=[0, size + 1], row=1, col=1)
fig.update_yaxes(title_text="total SSR", range=[ssr.min()*0.95, ssr.max()*1.03], row=2, col=1)
fig.update_xaxes(title_text="time", range=[0, T], row=1, col=1)
fig.update_xaxes(title_text="candidate break date", range=[0, T], row=2, col=1)

frames = []
for j, tb in enumerate(cands):
    frames.append(go.Frame(
        name=str(tb),
        data=[go.Scatter(x=np.arange(T), y=b, mode="lines",
                         line=dict(color=C.PALETTE["ink"], width=2.2, dash="dot", shape="hv")),
              go.Scatter(x=np.arange(T), y=fits[j], mode="lines",
                         line=dict(color=C.PALETTE["pink"], width=3, shape="hv")),
              go.Scatter(x=[tb, tb], y=[0, size + 1], mode="lines",
                         line=dict(color=C.PALETTE["orange"], width=2.5)),
              go.Scatter(x=cands[:j+1], y=ssr[:j+1], mode="lines",
                         line=dict(color=C.PALETTE["blue"], width=3)),
              go.Scatter(x=[tb], y=[ssr[j]], mode="markers",
                         marker=dict(size=11, color=C.PALETTE["orange"]))],
        traces=[0, 1, 2, 3, 4]))
C.show(C.animate(fig, frames, duration=90, slider_prefix="candidate T_B = ", height=620,
                 title=None))
st.success(f"✅ The SSR bottoms out at **T̂_B = {best}** — the truth is **{TBtrue}**. "
           f"The fitted β path (pink) matches the true step path only when the candidate sits on "
           f"the real break.")

if size < 1.2:
    C.callout("Break too small", "With a jump this small relative to the noise, the SSR curve is "
              "nearly flat — the minimum is unstable and the estimated date is close to random. "
              "<b>Detectability = break size ÷ noise.</b>", C.PALETTE["red"])
else:
    C.callout("What you're seeing",
              "As the candidate crosses the true break, both sub-samples suddenly become "
              "internally homogeneous, so the residuals collapse and the SSR <b>plunges</b>. "
              "That V-shaped minimum <i>is</i> the estimator.", A)

# ---------------------------------------------------------------- trimming
C.section("Why trimming is compulsory", "The endpoints", A)
st.markdown(
    "A 'break' 2 observations from the end is not identified — there is no sub-sample to estimate. "
    "So the search is **trimmed** to $[\\varepsilon T,(1-\\varepsilon)T]$, typically "
    "$\\varepsilon=0.10$–$0.15$."
)
trim = st.slider("Trimming ε", 0.02, 0.30, 0.15, 0.01)
lo_c, hi_c = int(trim * T), int((1 - trim) * T)
figt = go.Figure()
figt.add_trace(go.Scatter(x=cands, y=ssr, mode="lines", name="SSR",
                          line=dict(color=C.PALETTE["blue"], width=2.6)))
figt.add_vrect(x0=0, x1=lo_c, fillcolor=C.PALETTE["red"], opacity=.12, line_width=0,
               annotation_text="excluded", annotation_position="top left")
figt.add_vrect(x0=hi_c, x1=T, fillcolor=C.PALETTE["red"], opacity=.12, line_width=0,
               annotation_text="excluded", annotation_position="top right")
figt.add_vline(x=TBtrue, line=dict(color=C.PALETTE["teal"], dash="dash"),
               annotation_text="true T_B")
figt.update_layout(template="plotly_white", height=340, margin=dict(l=50, r=20, t=50, b=45),
                   paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                   xaxis=dict(title="candidate date", range=[0, T]), yaxis=dict(title="SSR"),
                   title=f"Search window: [{lo_c}, {hi_c}]  (ε = {trim})")
try:
    st.plotly_chart(figt, width="stretch")
except TypeError:
    st.plotly_chart(figt, use_container_width=True)
if TBtrue < lo_c or TBtrue > hi_c:
    st.error("⚠️ Your trimming is so wide that it **excludes the true break** — it can never be "
             "found. Trimming protects size, but it also blinds you near the ends.")
else:
    st.info(f"The true break ({TBtrue}) is inside the search window — it can be found. "
            "Smaller ε searches nearer the ends but inflates size; larger ε is safer but misses "
            "edge breaks.")

# ---------------------------------------------------------------- multiple
C.section("Several breaks", "Bai–Perron", A)
c1, c2 = st.columns(2)
with c1:
    C.card("Dynamic programming (Bai–Perron 2003)",
           "Trying every m-break partition is combinatorial. Dynamic programming stores optimal "
           "sub-segment SSRs and returns the <b>global</b> optimum in O(T²).", A)
with c2:
    C.card("Sequential detection",
           "Find the first break, then search the largest remaining segment, repeat. Fast and "
           "simple — but can miss closely-spaced breaks. (<code>xtbreakmodel, method(bfk)</code>)", A)
st.markdown("**How many breaks?** Either a sequential $\\sup F(\\ell+1\\mid\\ell)$ test, or an "
            "information criterion (BIC, or the **LWZ** used by `xtpkpss`).")

# ---------------------------------------------------------------- super-consistency
C.section("Why you can plug the estimated date in", "Super-consistency", A)
st.latex(r"T(\hat\lambda-\lambda_0)=O_p(1),\qquad \lambda=T_B/T")
C.callout("What this means in practice",
          "The break <b>fraction</b> converges <b>faster than the usual √T rate</b>. The practical "
          "consequence is remarkable: the slope estimates and test statistics computed <i>after</i> "
          "plugging in T̂_B have the <b>same limiting distribution as if the break date had been "
          "known all along</b>. You pay no penalty for having estimated it. In panels, pooling "
          "many units sharpens this further.", A)
C.callout("But the critical values still change",
          "Super-consistency does <b>not</b> mean you can ignore the search. Because the date was "
          "<i>chosen</i> by minimising SSR, the <b>test</b> distribution is non-standard "
          "(a sup-Wald / Brownian-bridge functional) and depends on the trimming ε and the "
          "deterministic model. That is why every paper tabulates its own critical values — and "
          "why you must declare the correct <code>model()</code> when you run the command.",
          C.PALETTE["red"])

C.dev_footer()
