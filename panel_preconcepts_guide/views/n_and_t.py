import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["nt"]
C.hero(
    "N and T — the two dimensions",
    "Almost every mistake in applied panel work starts here: using a method whose asymptotics "
    "do not match the shape of your data. This page makes N and T concrete.",
    A, tag="Foundations",
)

# ---------------------------------------------------------------
C.section("1 · The panel structure", "Notation", A)
st.markdown("A panel follows the same $N$ units over $T$ periods, giving $N\\times T$ observations:")
st.latex(r"y_{it},\; x_{it}\qquad i=1,\dots,N \;(\text{units}),\qquad t=1,\dots,T\;(\text{time})")
st.markdown(
    "- **$N$** — the *cross-section* dimension: countries, firms, households, regions.\n"
    "- **$T$** — the *time* dimension: years, quarters, months.\n"
    "- **Balanced** panel: every unit is observed in every period ($NT$ observations).\n"
    "- **Unbalanced** panel: some cells are missing. *Most break commands require a balanced panel.*"
)
C.callout("Why it matters immediately",
          "A method proved for <b>N → ∞ with T fixed</b> is <b>not</b> justified on a panel with "
          "N = 12 and T = 50 — and vice versa. Matching the asymptotics to your data shape is the "
          "first decision you make.", A)

# ---------------------------------------------------------------
C.section("2 · The four asymptotic regimes", "Which theory applies", A)
st.markdown("Econometric theory 'lets a dimension grow' to derive distributions. Four cases:")
st.latex(r"""
\begin{aligned}
&\text{(i) } N\to\infty,\; T \text{ fixed} &&\text{micro panels; fixed-}T\text{ theory}\\
&\text{(ii) } T\to\infty,\; N \text{ fixed} &&\text{time-series-like}\\
&\text{(iii) } T\to\infty \text{ then } N\to\infty &&\text{sequential limits}\\
&\text{(iv) } (N,T)\to\infty \text{ jointly} &&\text{joint limits (with } N/T\to c)
\end{aligned}
""")
c1, c2 = st.columns(2)
with c1:
    C.card("Fixed-T, large-N (micro panel)",
           "N → ∞, T small. Consistency comes from <b>many units</b>. Used by Carrion et al. (2005), "
           "Kaddoura CBC (2025), Baltagi–Feng–Kao. Brownian-motion limits are <i>not</i> available.", A)
with c2:
    C.card("Large-T (macro panel)",
           "T → ∞ (alone or with N). Needed for <b>unit-root and cointegration</b> asymptotics, "
           "which are built on Brownian motion. Used by Westerlund (2006), KPY (2011), "
           "Banerjee–Carrion.", A)

# ---------------------------------------------------------------
C.section("3 · The N–T map of your data", "Locate yourself", A)
st.markdown("Move the sliders to place your own panel on the map and see which world you are in.")
cc1, cc2 = st.columns(2)
Nv = cc1.slider("N (number of units)", 5, 300, 30)
Tv = cc2.slider("T (number of periods)", 3, 120, 40)

fig = go.Figure()
# regions
fig.add_shape(type="rect", x0=3, y0=50, x1=15, y1=300, fillcolor=C.PALETTE["teal"],
              opacity=.10, line=dict(width=0))
fig.add_shape(type="rect", x0=15, y0=15, x1=120, y1=300, fillcolor=C.PALETTE["grape"],
              opacity=.10, line=dict(width=0))
fig.add_shape(type="rect", x0=3, y0=5, x1=15, y1=50, fillcolor=C.PALETTE["yellow"],
              opacity=.12, line=dict(width=0))
fig.add_shape(type="rect", x0=15, y0=5, x1=120, y1=15, fillcolor=C.PALETTE["blue"],
              opacity=.10, line=dict(width=0))
ann = [
    (7, 160, "MICRO panel<br>large N, small T", C.PALETTE["teal"]),
    (55, 160, "MACRO panel<br>both large  →  3rd generation", C.PALETTE["grape"]),
    (7, 18, "small N, small T<br>(be careful)", C.PALETTE["yellow"]),
    (55, 9, "few units, long T<br>(time-series-like)", C.PALETTE["blue"]),
]
for x, y, t, col in ann:
    fig.add_annotation(x=x, y=y, text=t, showarrow=False,
                       font=dict(size=11, color=col), align="center")
fig.add_trace(go.Scatter(x=[Tv], y=[Nv], mode="markers+text",
                         marker=dict(size=20, color=C.PALETTE["red"],
                                     line=dict(width=2, color="white")),
                         text=[f"  your panel (N={Nv}, T={Tv})"], textposition="middle right",
                         textfont=dict(size=12, color=C.PALETTE["red"]), name="your panel"))
fig.update_layout(xaxis_title="T  (time periods)", yaxis_title="N  (units)",
                  xaxis=dict(range=[3, 120]), yaxis=dict(range=[5, 300]), showlegend=False)
C.show(fig, height=420, title="Where does your panel live?")

if Tv < 15:
    C.callout("Your T is short", "Unit-root and cointegration tests need a reasonable T "
              "(rule of thumb T ≥ 20–30). With very short T, prefer fixed-T methods "
              "(e.g. CBC, Baltagi–Feng–Kao) and avoid Brownian-motion-based tests.", C.PALETTE["yellow"])
elif Nv < 10:
    C.callout("Your N is small", "Cross-sectional-average (CCE) methods need a decent N to make "
              "the averages informative. With very small N, consider SUR/time-series methods "
              "or bootstrap inference.", C.PALETTE["yellow"])
else:
    C.callout("Good shape", "With both N and T reasonably large you are in the macro-panel world "
              "where second- and third-generation methods (CCE, PANIC, breaks) are designed to work.",
              C.PALETTE["teal"])

# ---------------------------------------------------------------
C.section("4 · Two classic small-T problems", "Why T matters for bias", A)
c1, c2 = st.columns(2)
with c1:
    st.markdown("**Incidental parameters problem**")
    st.markdown(
        "With $T$ fixed, each unit adds a new parameter $\\alpha_i$ that never gets more data. "
        "The number of parameters grows with $N$, so nonlinear fixed-effects estimators are "
        "**inconsistent** as $N\\to\\infty$ with $T$ fixed."
    )
    st.latex(r"\#\{\alpha_i\}=N \;\longrightarrow\; \infty \quad\text{while each uses only } T \text{ obs.}")
with c2:
    st.markdown("**Nickell bias (dynamic panels)**")
    st.markdown(
        "In a dynamic FE model the within transformation correlates the lagged dependent variable "
        "with the demeaned error, giving a bias of order $1/T$:"
    )
    st.latex(r"y_{it}=\rho y_{i,t-1}+\alpha_i+\varepsilon_{it}\;\Rightarrow\;\mathrm{Bias}(\hat\rho_{FE})=O\!\left(\tfrac{1}{T}\right)")
    C.eqcap("It vanishes only as T → ∞. For small T use GMM (Arellano–Bond) or bias-corrected estimators.")

# Nickell bias illustration
Ts = np.arange(5, 61)
bias = -(1 + 0.6) / (Ts - 1)
fig = go.Figure()
fig.add_trace(go.Scatter(x=Ts, y=bias, mode="lines",
                         line=dict(color=C.PALETTE["red"], width=3), name="approx. bias"))
fig.add_hline(y=0, line=dict(color=C.PALETTE["gray"], dash="dash"))
fig.update_layout(xaxis_title="T", yaxis_title="approximate bias in ρ̂ (FE)")
C.show(fig, height=300, title="Nickell bias shrinks as T grows (illustrative)")

# ---------------------------------------------------------------
C.section("5 · Rule-of-thumb table", "What to use when", A)
st.markdown(
    "| Data shape | Typical field | Use | Avoid |\n"
    "|---|---|---|---|\n"
    "| Large N, small T ($N\\gg T$) | micro / firm panels | FE, GMM, fixed-T break methods (CBC) | unit-root/cointegration tests |\n"
    "| Both moderate/large | macro panels | CCE, PANIC, 2nd/3rd-generation tests | naive pooled OLS |\n"
    "| Small N, large T | few countries | SUR, time-series methods, bootstrap | CCE (averages too noisy) |\n"
    "| Small N, small T | — | descriptive work only | almost everything asymptotic |"
)

C.dev_footer()
