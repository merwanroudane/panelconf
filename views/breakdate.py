import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["breakdate"]
C.hero(
    "Break-Date Estimation & Inference",
    "How the dates themselves are found, how many breaks to keep, why the estimated date "
    "behaves as if known, and how individual statistics are pooled into a standard-normal "
    "panel test. The plumbing shared by every method in this guide.",
    A, tag="The shared machinery",
)

# ======================================================================
C.section("1 · Estimating a single break — SSR grid search", "The building block", A)
st.markdown(
    "For a candidate date $T_B$, split the sample, run OLS on each segment, and record the total "
    "residual sum of squares. The estimated break is the date that **minimises SSR** (equivalently "
    "**maximises** the Wald/LM statistic for a shift):"
)
st.latex(r"\hat T_B=\arg\min_{T_B\in[\varepsilon T,\,(1-\varepsilon)T]}\;\mathrm{SSR}(T_B)")
# U-shaped SSR illustration
rng = C.rng(14); T = 120; TBtrue = 68
x = rng.normal(0, 1, T)
b = np.where(np.arange(T) >= TBtrue, 2.0, 0.6)
y = b*x + rng.normal(0, 0.5, T)
cands = np.arange(15, 106)
ssr = []
for tb in cands:
    r = 0
    for lo, hi in [(0, tb), (tb, T)]:
        xs, ys = x[lo:hi], y[lo:hi]
        bb = np.sum(xs*ys)/np.sum(xs*xs)
        r += np.sum((ys-bb*xs)**2)
    ssr.append(r)
ssr = np.array(ssr)
fig = go.Figure()
fig.add_trace(go.Scatter(x=cands, y=ssr, line=dict(color=C.PALETTE["orange"], width=3), name="SSR(T_B)"))
fig.add_vline(x=cands[np.argmin(ssr)], line=dict(color=C.PALETTE["red"], dash="dash"),
              annotation_text=f"argmin = {cands[int(np.argmin(ssr))]}")
fig.add_vline(x=TBtrue, line=dict(color=C.PALETTE["teal"], dash="dot"), annotation_text="true 68")
fig.update_layout(xaxis_title="candidate break date T_B", yaxis_title="total SSR")
C.show(fig, height=330, title="The SSR is U-shaped in the candidate date — its minimum is the estimate")

# ======================================================================
C.section("2 · Trimming", "Keeping the search identified", A)
st.markdown(
    "A 'break' one observation from the end is not identified — a segment needs enough points. "
    "**Trimming** $\\varepsilon$ (typically **0.10–0.15**) restricts candidates to "
    "$[\\varepsilon T,(1-\\varepsilon)T]$. Smaller $\\varepsilon$ detects breaks nearer the ends "
    "but inflates size; larger $\\varepsilon$ is safer but misses edge breaks."
)

# ======================================================================
C.section("3 · Multiple breaks — dynamic programming & sequencing", "Bai & Perron (1998, 2003)", A)
st.markdown(
    "Searching all $m$-break partitions is combinatorial. Two efficient routes:"
)
c1, c2 = st.columns(2)
with c1:
    C.card("Dynamic programming (Bai–Perron 2003)",
           "Computes the global SSR-minimising partition for up to M breaks in O(T²) by storing "
           "optimal sub-segment SSRs. Returns the exact optimum — used in xtkpybreak.", A)
with c2:
    C.card("Sequential detection",
           "Find the first break; then search the largest remaining segment for the next; repeat. "
           "Fast and simple (BFK, xtbreakmodel bfk), though it can miss closely-spaced breaks.", A)

# ======================================================================
C.section("4 · How many breaks? — selecting the number", "Testing vs information criteria", A)
st.markdown("Two philosophies for choosing $m$:")
st.latex(r"\textbf{Sequential test: } \sup F(\ell+1\mid\ell)\quad\text{— add a break while the sup-F rejects}")
st.latex(r"\textbf{Information criterion: } \mathrm{IC}(m)=\ln\hat\sigma^2(m)+m\cdot p(N,T)")
st.markdown(
    "Common penalties: **BIC**, the modified **LWZ** (Liu–Wu–Zidek, used in `xtpkpss`), and the "
    "fused-lasso IC (a BIC-type $\\phi=c\\log N/\\sqrt N$ in `xtcbc`/Qian–Su). Too small a penalty "
    "**over-segments** (spurious breaks); too large **under-segments** (missed breaks)."
)

# ======================================================================
C.section("5 · The sup-Wald / sup-F test for a break", "Testing existence with unknown date", A)
st.markdown(
    "When the date is unknown under the alternative, the test statistic is the **supremum** of "
    "the pointwise Wald/F statistic over admissible dates:"
)
st.latex(r"\sup\!F=\max_{T_B\in[\varepsilon T,(1-\varepsilon)T]}F(T_B)")
st.markdown(
    "Its distribution is **non-standard** (a functional of a Brownian bridge) and depends on the "
    "trimming and the number of parameters that break — hence special critical-value tables "
    "(Andrews 1993; Bai–Perron)."
)
# sup-F illustration
Fstat = -(ssr - ssr.max()) / ssr.max() * 40 + rng.normal(0, 0.4, len(ssr))
fig = go.Figure()
fig.add_trace(go.Scatter(x=cands, y=Fstat, line=dict(color=C.PALETTE["grape"], width=2.6), name="F(T_B)"))
fig.add_hline(y=Fstat.max(), line=dict(color=C.PALETTE["red"], dash="dash"), annotation_text="sup-F")
fig.update_layout(xaxis_title="candidate date", yaxis_title="F statistic")
C.show(fig, height=300, title="sup-F: the test statistic is the peak of the pointwise F")

# ======================================================================
C.section("6 · Why the estimated date behaves as if known", "Super-consistency", A)
st.markdown(
    "The break **fraction** $\\hat\\lambda=\\hat T_B/T$ converges to the truth **faster than the "
    "usual $\\sqrt T$ rate** (super-consistency): $T(\\hat\\lambda-\\lambda_0)=O_p(1)$. "
    "Consequently the downstream slope estimates and test statistics have the **same limiting "
    "distribution as if the break date were known** — the theoretical reason we can plug $\\hat "
    "T_B$ into the next stage without penalty. In panels, estimating over **many units** (large "
    "$N$) sharpens this further."
)

# ======================================================================
C.section("7 · Pooling to a standard-normal panel test", "From N units to one Z", A)
st.markdown(
    "Individual break-and-factor-adjusted statistics $S_i$ are averaged across units. Each has a "
    "non-zero mean and finite variance under the null (functionals of Brownian motion / bridges "
    "shifted by the deterministic terms). A central limit theorem across $i$ standardises them:"
)
st.latex(r"Z=\frac{\sqrt N\big(\overline S-\mu\big)}{\sqrt{\varsigma^2}}\;\xrightarrow{d}\;N(0,1),\qquad \overline S=\frac1N\sum_{i=1}^N S_i")
C.callout("The deterministic model is baked into (μ, ς²)",
          "The mean μ and variance ς² of the individual limit <b>depend on the deterministic "
          "specification</b> — constant vs trend, and the number of breaks. That is why every "
          "paper tabulates a different (μ, ς²) per model and break count, and why you must "
          "declare the correct <code>model()</code> when you run the command.", A)

# ======================================================================
C.section("8 · Confidence intervals for the break date", "Reporting uncertainty", A)
st.markdown(
    "Bai (1997) gives an asymptotic distribution for $\\hat T_B$ that yields a **confidence "
    "interval** around the estimated date (narrower when the break is large relative to the error "
    "variance). Always report it: a point estimate of 'break in 1992' with a ±3-year interval is "
    "very different from ±0. Good practice is to **match the estimated date (and its CI) to a real "
    "regime change** — a crisis, a policy, a technological shift."
)

C.dev_footer()
