import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["regular"]
C.hero(
    "🎛️ Regularization — the idea",
    "Don't tell the model where the break is. Let the coefficient change EVERY period, then "
    "PENALISE change — and watch the noise fuse away while the real breaks survive. Turn the "
    "penalty λ up and see it happen.",
    A, tag="How to model a break",
)

C.section("The idea", "Penalise change, keep what survives", A)
C.callout("The whole trick in one box",
          "Let β be free to change at <b>every</b> single period. Then add a penalty on the "
          "<b>differences</b> |βₜ − βₜ₋₁|. Most differences get shrunk to <b>exactly zero</b> — "
          "meaning 'no break here'. The few that <b>survive</b> the penalty are the break dates. "
          "<b>Break detection becomes automatic variable selection</b> — you never specify how "
          "many breaks there are.", A)
st.latex(r"\min_{\{\beta_t\}}\ \underbrace{\sum_{i,t}\big(y_{it}-x_{it}'\beta_t\big)^2}_{\text{fit the data}}\;+\;\lambda\underbrace{\sum_{t=2}^{T}\big|\beta_t-\beta_{t-1}\big|}_{\text{penalise CHANGE}}")

# ---------------------------------------------------------------- main animation
C.section("Simulation 1 — turn λ up and watch", "Animation", A)
st.markdown(
    "The truth is a **step path** with two real breaks. The grey dots are the noisy "
    "period-by-period estimates you'd get with **no** penalty. Now sweep λ:"
)
C.play_hint("▶ PLAY to raise λ from 0 → large. Watch over-segmentation → correct → over-smoothing.")

T = 70
t = np.arange(T)
beta_true = np.where(t < 24, 1.0, np.where(t < 47, 2.6, 1.7))
rng = C.rng(1)
raw = beta_true + rng.normal(0, 0.26, T)

lams = np.round(np.concatenate([np.arange(0, 1.0, 0.06), np.arange(1.0, 8.1, 0.5)]), 3)


def fuse(lam, iters=260):
    """Crude fused-lasso-like smoother, for illustration."""
    fit = raw.copy()
    for _ in range(iters):
        new = fit.copy()
        for k in range(T):
            nb = []
            if k > 0: nb.append(fit[k-1])
            if k < T-1: nb.append(fit[k+1])
            new[k] = (raw[k] + lam * sum(nb)) / (1 + lam * len(nb))
        fit = new
    d = np.diff(fit)
    d[np.abs(d) < 0.018 * (1 + lam)] = 0.0        # snap tiny changes to exactly zero
    return np.concatenate([[fit[0]], fit[0] + np.cumsum(d)])


paths = [fuse(l) for l in lams]
nbrk = [int((np.abs(np.diff(p)) > 0.05).sum()) for p in paths]

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=raw, mode="markers", name="unpenalised β̂ₜ (noisy)",
                         marker=dict(size=5, color="#C3CAD6")))
fig.add_trace(go.Scatter(x=t, y=beta_true, mode="lines", name="TRUE step path",
                         line=dict(color=C.PALETTE["ink"], width=2.2, dash="dot", shape="hv")))
fig.add_trace(go.Scatter(x=t, y=paths[0], mode="lines", name="fused-lasso path",
                         line=dict(color=C.PALETTE["green"], width=3.6)))
for b in (24, 47):
    fig.add_vline(x=b, line=dict(color=C.PALETTE["red"], dash="dash", width=1.2))
fig.update_layout(xaxis=dict(title="time t"), yaxis=dict(title="coefficient βₜ", range=[0.2, 3.4]))

frames = []
for j, l in enumerate(lams):
    n = nbrk[j]
    if n > 4:
        verdict = "λ too SMALL → over-segmentation (fitting noise)"
    elif n == 2:
        verdict = "✅ λ about right → the 2 true breaks survive"
    elif n == 0:
        verdict = "λ too LARGE → over-smoothing (real breaks penalised away)"
    else:
        verdict = f"{n} break(s) detected"
    frames.append(go.Frame(
        name=str(l),
        data=[go.Scatter(x=t, y=raw, mode="markers", marker=dict(size=5, color="#C3CAD6")),
              go.Scatter(x=t, y=beta_true, mode="lines",
                         line=dict(color=C.PALETTE["ink"], width=2.2, dash="dot", shape="hv")),
              go.Scatter(x=t, y=paths[j], mode="lines",
                         line=dict(color=C.PALETTE["green"], width=3.6))],
        layout=go.Layout(title=f"λ = {l}   →   {n} break(s) detected   —   {verdict}")))
C.show(C.animate(fig, frames, duration=180, slider_prefix="penalty λ = ", height=450,
                 title=f"λ = {lams[0]}   →   {nbrk[0]} break(s) detected"))

c1, c2, c3 = st.columns(3)
with c1:
    C.card("λ too small", "Almost nothing is fused. You 'detect' many <b>spurious</b> breaks — "
           "you are fitting noise. This is <b>over-segmentation</b>.", C.PALETTE["red"])
with c2:
    C.card("λ just right", "Noise is fused away; the <b>real</b> steps survive. This is the value "
           "an information criterion picks for you.", C.PALETTE["green"])
with c3:
    C.card("λ too large", "Everything is fused into one flat line — the real breaks are penalised "
           "away too. This is <b>under-segmentation</b>.", C.PALETTE["red"])

# ---------------------------------------------------------------- IC
C.section("Simulation 2 — how λ is actually chosen", "Animation", A)
st.markdown(
    "You don't eyeball λ. An **information criterion** trades fit against the number of breaks, "
    "and its minimum picks λ automatically:"
)
st.latex(r"\mathrm{IC}(\lambda)=\hat\sigma^2(\lambda)+\phi\cdot\#\{\text{breaks}(\lambda)\},\qquad \phi=c\,\frac{\log N}{\sqrt N}")
C.play_hint("▶ PLAY to build the IC curve and watch it settle on the optimum.")

sig2 = np.array([float(((raw - p) ** 2).mean()) for p in paths])
phi = 0.055
ic = sig2 + phi * np.array(nbrk)
jbest = int(np.argmin(ic))
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=[lams[0]], y=[sig2[0]], mode="lines", name="fit term σ̂²(λ)",
                          line=dict(color=C.PALETTE["blue"], width=2.4)))
fig2.add_trace(go.Scatter(x=[lams[0]], y=[phi * nbrk[0]], mode="lines", name="penalty term",
                          line=dict(color=C.PALETTE["orange"], width=2.4)))
fig2.add_trace(go.Scatter(x=[lams[0]], y=[ic[0]], mode="lines", name="IC = fit + penalty",
                          line=dict(color=C.PALETTE["green"], width=3.8)))
fig2.update_layout(xaxis=dict(title="penalty λ", range=[0, float(lams[-1])]),
                   yaxis=dict(title="criterion value"))
frames2 = [go.Frame(name=str(lams[j]),
                    data=[go.Scatter(x=lams[:j+1], y=sig2[:j+1], mode="lines",
                                     line=dict(color=C.PALETTE["blue"], width=2.4)),
                          go.Scatter(x=lams[:j+1], y=phi*np.array(nbrk[:j+1]), mode="lines",
                                     line=dict(color=C.PALETTE["orange"], width=2.4)),
                          go.Scatter(x=lams[:j+1], y=ic[:j+1], mode="lines",
                                     line=dict(color=C.PALETTE["green"], width=3.8))])
           for j in range(len(lams))]
C.show(C.animate(fig2, frames2, duration=140, slider_prefix="λ = ", height=380,
                 title="The IC minimum selects λ — no eyeballing required"))
st.success(f"✅ IC is minimised at **λ ≈ {lams[jbest]}**, which detects **{nbrk[jbest]} break(s)** "
           f"— the truth is 2.")

# ---------------------------------------------------------------- why zero
C.section("Why does the lasso hit EXACTLY zero?", "The geometry", A)
st.markdown(
    "Ridge shrinks but never to zero; the lasso does. The reason is **geometry**: the lasso's "
    "constraint region is a **diamond with sharp corners on the axes**, so the fit contours touch "
    "a **corner** — and a corner *is* a zero."
)
c1, c2 = st.columns([1, 1])
with c1:
    th = np.linspace(0, 2*np.pi, 200)
    figg = go.Figure()
    figg.add_trace(go.Scatter(x=np.cos(th), y=np.sin(th), fill="toself",
                              fillcolor="rgba(28,126,214,.14)",
                              line=dict(color=C.PALETTE["blue"], width=2.4), name="Ridge (circle)"))
    figg.add_trace(go.Scatter(x=[1, 0, -1, 0, 1], y=[0, 1, 0, -1, 0], fill="toself",
                              fillcolor="rgba(55,178,77,.14)",
                              line=dict(color=C.PALETTE["green"], width=2.4), name="Lasso (diamond)"))
    for r in (0.55, 0.85, 1.15):
        figg.add_trace(go.Scatter(x=1.5+r*1.5*np.cos(th), y=1.1+r*0.8*np.sin(th),
                                  line=dict(color=C.PALETTE["gray"], width=1, dash="dot"),
                                  showlegend=(r == 0.55), name="fit contours"))
    figg.add_trace(go.Scatter(x=[0], y=[1], mode="markers",
                              marker=dict(size=15, color=C.PALETTE["red"], symbol="star"),
                              name="corner → β₁ = 0"))
    figg.update_layout(template="plotly_white", height=340,
                       margin=dict(l=40, r=10, t=40, b=40),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       xaxis=dict(title="β₁", range=[-1.6, 3.2], scaleanchor="y"),
                       yaxis=dict(title="β₂", range=[-1.6, 2.4]),
                       title="Corners cause exact zeros")
    try:
        st.plotly_chart(figg, width="stretch")
    except TypeError:
        st.plotly_chart(figg, use_container_width=True)
with c2:
    st.markdown("The scalar solution is **soft-thresholding** — a whole zone is set to zero:")
    st.latex(r"\hat\beta^{\text{lasso}}=\mathrm{sign}(\hat\beta^{\text{OLS}})\big(|\hat\beta^{\text{OLS}}|-\lambda\big)^{+}")
    lam2 = st.slider("λ (threshold)", 0.0, 2.0, 0.6, 0.05)
    b = np.linspace(-3, 3, 300)
    figs = go.Figure()
    figs.add_trace(go.Scatter(x=b, y=b, name="OLS", line=dict(color=C.PALETTE["gray"], width=1.6, dash="dot")))
    figs.add_trace(go.Scatter(x=b, y=b/(1+lam2), name="Ridge",
                              line=dict(color=C.PALETTE["blue"], width=2.4)))
    figs.add_trace(go.Scatter(x=b, y=np.sign(b)*np.maximum(np.abs(b)-lam2, 0), name="Lasso",
                              line=dict(color=C.PALETTE["green"], width=3.2)))
    figs.update_layout(template="plotly_white", height=340, margin=dict(l=40, r=10, t=40, b=40),
                       paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       xaxis=dict(title="OLS estimate"), yaxis=dict(title="penalised estimate"),
                       title=f"Soft-thresholding at λ = {lam2}")
    try:
        st.plotly_chart(figs, width="stretch")
    except TypeError:
        st.plotly_chart(figs, use_container_width=True)

# ---------------------------------------------------------------- refinements
C.section("The two refinements that make it work", "Group + adaptive", A)
c1, c2 = st.columns(2)
with c1:
    st.latex(r"\lambda\sum_{t}\big\lVert\beta_t-\beta_{t-1}\big\rVert")
    C.card("Group fused lasso", "With K regressors, penalise the <b>vector norm</b> of the change — "
           "so all K coefficients break <b>together</b> (a vector break).", A)
with c2:
    st.latex(r"w_t=\big\lVert\dot\beta_t-\dot\beta_{t-1}\big\rVert^{-\kappa}")
    C.card("Adaptive weights (κ ≈ 2)", "Weight each difference by the inverse of a pilot estimate: "
           "big <b>true</b> jumps get a <b>small</b> penalty, noise gets a <b>big</b> one. This "
           "delivers the <b>oracle property</b>.", A)
C.callout("The oracle property",
          "With adaptive weights the estimator asymptotically finds the <b>true</b> breaks and "
          "estimates the regime coefficients <b>as if the dates had been known all along</b>. "
          "That is why adaptive weighting is not optional.", A)

# ---------------------------------------------------------------- methods
C.section("The methods built on this idea", "Software", A)
meth = [
    ("xtbreakmodel, method(pls)", "Qian & Su (2016) — adaptive group fused lasso with ONE common "
     "break schedule for all units."),
    ("xtbreakmodel, method(gagfl)", "Okui & Wang (2021) — units fall into <b>latent groups</b>, each "
     "with its own dates. Alternates grouped fixed effects with AGFL."),
    ("xtcbc", "Kaddoura (2025) — the penalty is applied <b>per coefficient</b>, so each βₖ gets its "
     "own breaks and stable coefficients are left unbroken."),
    ("xtquantilebreak", "Zhang et al. (2022) — quantile regression + adaptive fused lasso: breaks "
     "that differ across quantiles."),
]
for n, d in meth:
    C.card(n, d, A)

C.callout("Why regularization is the modern school",
          "Dummies need you to know the date. Fourier needs the break to be smooth. "
          "<b>Regularization needs neither</b> — it searches every period at once and lets the data "
          "select the breaks, which is why it scales to many candidate dates, many coefficients, "
          "and hidden groups.", A)

C.dev_footer()
