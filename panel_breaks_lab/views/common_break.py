import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["common"]
C.hero(
    "1️⃣ Common break",
    "Every unit breaks at the SAME date. This is the strongest assumption — and the most "
    "powerful, if it is true. Watch all units jump together, then break the assumption and "
    "see what it costs.",
    A, tag="Types of break",
)

C.section("The model", "What 'common' means", A)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta(t)+\varepsilon_{it},\qquad "
         r"\beta(t)=\begin{cases}\beta_1 & t<T_B\\ \beta_2 & t\ge T_B\end{cases}")
st.markdown(
    "The key restriction is that **$T_B$ carries no $i$ subscript** — the break date is the same "
    "for every unit:"
)
st.latex(r"T_{B1}=T_{B2}=\dots=T_{BN}=T_B")
C.callout("Real-world example",
          "The <b>2008 global financial crisis</b> or <b>COVID-19 in 2020</b>: a worldwide shock "
          "that hits every country in the same year. Also technology or policy shocks adopted "
          "simultaneously (e.g. the euro in 1999).", A)

# ---------------------------------------------------------------- sim
C.section("Simulation — watch them jump together", "Animation 1", A)
c1, c2, c3 = st.columns(3)
TB = c1.slider("Break date T_B", 20, 80, 55)
jump = c2.slider("Break size (jump)", 0.0, 8.0, 4.0, 0.5)
noise = c3.slider("Noise", 0.1, 1.5, 0.35, 0.05)
C.play_hint()

rng = C.rng(11)
N, T = 6, 100
t = np.arange(T)
series = [(i - 2.5) * 1.6 + np.cumsum(rng.normal(0, noise, T)) + np.where(t >= TB, jump, 0.0)
          for i in range(N)]

fig = go.Figure()
for i in range(N):
    fig.add_trace(go.Scatter(x=[t[0]], y=[series[i][0]], mode="lines", name=f"unit {i+1}",
                             line=dict(color=C.UNIT_COLORS[i], width=2.6)))
fig.add_vline(x=TB, line=dict(color=C.PALETTE["red"], dash="dash", width=2),
              annotation_text=f"T_B = {TB}", annotation_position="top")
lo = min(s.min() for s in series) - 1
hi = max(s.max() for s in series) + 1
fig.update_layout(xaxis=dict(range=[0, T - 1], title="time"), yaxis=dict(range=[lo, hi], title="y"))
frames = [go.Frame(name=str(k),
                   data=[go.Scatter(x=t[:k], y=series[i][:k], mode="lines",
                                    line=dict(color=C.UNIT_COLORS[i], width=2.6))
                         for i in range(N)])
          for k in range(2, T + 1, 2)]
C.show(C.animate(fig, frames, duration=45, slider_prefix="t = ", height=430,
                 title="Common break: one date, every unit"))

if jump < 1.0:
    C.callout("Break size is tiny", "With a jump this small the break is buried in the noise — "
              "no test will find it, and the estimated date will be close to random. "
              "<b>Detectability depends on the break size relative to the noise.</b>",
              C.PALETTE["red"])
else:
    C.callout("What you're seeing", "All six units are flat-ish, then jump <b>at the same instant</b>. "
              "Because every unit contributes information about the <i>same</i> date, the date is "
              "pinned down very precisely — this is why common-break methods are so powerful.", A)

# ---------------------------------------------------------------- why power
C.section("Why the common assumption buys power", "N units, one date", A)
st.markdown(
    "With a common break there is **one** break date to estimate no matter how large $N$ is. "
    "Every extra unit adds evidence about that *same* date, so the estimate sharpens as "
    "$N$ grows — the break fraction is **super-consistent**:"
)
st.latex(r"T(\hat\lambda-\lambda_0)=O_p(1),\qquad \lambda=T_B/T")
st.markdown("Watch the estimated date tighten as more units are used:")
C.play_hint("▶ PLAY to add units one by one and watch the SSR minimum sharpen.")

# SSR sharpening animation
rng2 = C.rng(5)
Tn, TBt = 100, 55
xs = rng2.normal(0, 1, (12, Tn))
ys = []
for i in range(12):
    b = np.where(np.arange(Tn) >= TBt, 2.2, 0.6)
    ys.append(b * xs[i] + rng2.normal(0, 1.0, Tn))
cands = np.arange(15, 86)


def ssr_upto(nunits):
    tot = []
    for tb in cands:
        s = 0.0
        for i in range(nunits):
            for lo_, hi_ in [(0, tb), (tb, Tn)]:
                xx, yy = xs[i][lo_:hi_], ys[i][lo_:hi_]
                bb = np.sum(xx * yy) / np.sum(xx * xx)
                s += np.sum((yy - bb * xx) ** 2)
        tot.append(s)
    tot = np.array(tot)
    return (tot - tot.min()) / (tot.max() - tot.min())


curves = [ssr_upto(n) for n in range(1, 13)]
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=cands, y=curves[0], mode="lines",
                          line=dict(color=C.PALETTE["blue"], width=3), name="normalised SSR"))
fig2.add_vline(x=TBt, line=dict(color=C.PALETTE["red"], dash="dash", width=2),
               annotation_text="true T_B")
fig2.update_layout(xaxis=dict(title="candidate break date", range=[15, 85]),
                   yaxis=dict(title="normalised SSR", range=[-0.05, 1.05]))
frames2 = [go.Frame(name=str(n + 1),
                    data=[go.Scatter(x=cands, y=curves[n], mode="lines",
                                     line=dict(color=C.PALETTE["blue"], width=3))])
           for n in range(12)]
C.show(C.animate(fig2, frames2, duration=420, slider_prefix="units used N = ", height=380,
                 title="More units ⇒ a sharper, deeper SSR minimum at the true date"))
C.callout("The payoff",
          "With <b>1 unit</b> the SSR curve is shallow and wobbly — the minimum could land anywhere. "
          "By <b>12 units</b> it is a deep, narrow V locked exactly on the true date. That is the "
          "power of pooling a <i>common</i> break.", A)

# ---------------------------------------------------------------- cost
C.section("The cost if the assumption is wrong", "Don't impose it blindly", A)
C.callout("The danger",
          "If units actually break at <b>different</b> dates but you impose a common break, the "
          "estimator is <b>inconsistent</b>: it finds some 'average' date that matches nobody, and "
          "the regime coefficients are biased toward each other. Test the assumption — don't "
          "assume it.", C.PALETTE["red"])

C.section("Which commands assume a common break?", "Software", A)
c1, c2 = st.columns(2)
with c1:
    C.card("xtbreakmodel, method(pls) / (bfk) / (sara)",
           "Qian–Su adaptive group fused lasso, Baltagi–Feng–Kao sequential least squares, and "
           "the SaRa nonparametric screen — all assume one common schedule.", A)
with c2:
    C.card("xtkpybreak · xtbfkbreak",
           "CCE with a common break — and (xtkpybreak) valid even when the common factors are "
           "I(1), with breaks in the loadings too.", A)

C.dev_footer()
