import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["static"]
C.hero(
    "Basic static panel models",
    "Pooled OLS, Fixed Effects, Random Effects, Between, and the heterogeneous-slope family. "
    "This is the regression that later gets a break put into it — so it must be understood first.",
    A, tag="Foundations",
)

# ---------------------------------------------------------------
C.section("1 · The common starting point", "The model", A)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta+\varepsilon_{it},\qquad i=1,\dots,N;\ t=1,\dots,T")
st.markdown(
    "Everything below differs only in **what it assumes about $\\alpha_i$** (the unit-specific "
    "intercept) and **whether $\\beta$ is the same for all units**."
)

# illustration: pooled vs FE
rng = C.rng(4)
fig = go.Figure()
cols = [C.PALETTE[k] for k in ["indigo", "teal", "pink", "orange"]]
allx, ally = [], []
for i in range(4):
    x = rng.uniform(0, 10, 12)
    a = 2 + 6 * i                      # different intercepts
    y = a + 1.2 * x + rng.normal(0, 1.0, 12)
    allx.append(x); ally.append(y)
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers",
                             marker=dict(size=8, color=cols[i]), name=f"unit {i+1}"))
    xs = np.linspace(0, 10, 10)
    fig.add_trace(go.Scatter(x=xs, y=a + 1.2 * xs, mode="lines",
                             line=dict(color=cols[i], width=2), showlegend=False))
X = np.concatenate(allx); Y = np.concatenate(ally)
b_pool = np.polyfit(X, Y, 1)
xs = np.linspace(0, 10, 10)
fig.add_trace(go.Scatter(x=xs, y=b_pool[0] * xs + b_pool[1], mode="lines",
                         line=dict(color=C.PALETTE["red"], width=4, dash="dash"),
                         name="Pooled OLS (biased!)"))
C.show(fig, height=400, title="Pooled OLS vs Fixed Effects: ignoring αᵢ distorts the slope")
C.callout("Read the picture",
          "Each unit has its own intercept and a true slope of 1.2. <b>Pooled OLS</b> (red dashed) "
          "ignores the intercepts and fits a much steeper line — a biased slope. <b>Fixed effects</b> "
          "estimates the common slope <i>within</i> each unit (the coloured lines), recovering 1.2.",
          A)

# ---------------------------------------------------------------
C.section("2 · Pooled OLS", "Assumes αᵢ = α for all i", A)
st.latex(r"y_{it}=\alpha+x_{it}'\beta+\varepsilon_{it}")
st.markdown(
    "Treats the panel as one big cross-section. **Valid only if** there is no unobserved "
    "unit-specific heterogeneity correlated with $x$. If $\\alpha_i$ exists and correlates with "
    "$x_{it}$, pooled OLS suffers **omitted-variable bias**."
)

# ---------------------------------------------------------------
C.section("3 · Fixed Effects (within / LSDV)", "αᵢ is a parameter, may correlate with x", A)
st.markdown("**Within transformation** — subtract each unit's own time-mean, killing $\\alpha_i$:")
st.latex(r"\ddot y_{it}=y_{it}-\bar y_{i\cdot},\qquad \ddot x_{it}=x_{it}-\bar x_{i\cdot}")
st.latex(r"\hat\beta_{FE}=\Big(\sum_{i}\sum_{t}\ddot x_{it}\ddot x_{it}'\Big)^{-1}\sum_i\sum_t \ddot x_{it}\ddot y_{it}")
st.markdown(
    "- **LSDV** (least-squares dummy variable) is numerically identical: include $N$ unit dummies.\n"
    "- **Cost:** any time-invariant regressor is wiped out (it cannot be identified).\n"
    "- **Key virtue:** $\\alpha_i$ is allowed to be **correlated** with $x_{it}$ — the usual case."
)
C.callout("Link forward", "The within transformation (or first-period deviation) is exactly how "
          "<b>xtcbc</b> and the fused-lasso break estimators eliminate the fixed effect before "
          "detecting breaks.", A)

# ---------------------------------------------------------------
C.section("4 · Random Effects", "αᵢ is random and uncorrelated with x", A)
st.latex(r"y_{it}=\alpha+x_{it}'\beta+\underbrace{u_i+\varepsilon_{it}}_{\text{composite error}},\qquad \mathrm{Cov}(u_i,x_{it})=0")
st.markdown(
    "Estimated by **GLS**, using a quasi-demeaning with weight $\\theta$:"
)
st.latex(r"y_{it}-\theta\bar y_{i\cdot}=\;(1-\theta)\alpha+(x_{it}-\theta\bar x_{i\cdot})'\beta+v_{it},\qquad \theta=1-\sqrt{\frac{\sigma^2_\varepsilon}{T\sigma^2_u+\sigma^2_\varepsilon}}")
st.markdown(
    "RE is **more efficient** than FE *if* its assumption holds, and it can estimate time-invariant "
    "regressors. But if $\\mathrm{Cov}(u_i,x_{it})\\neq0$ it is **inconsistent**."
)

# ---------------------------------------------------------------
C.section("5 · Between estimator", "Only the cross-sectional variation", A)
st.latex(r"\bar y_{i\cdot}=\alpha+\bar x_{i\cdot}'\beta+ \bar\varepsilon_{i\cdot}\qquad (\text{OLS on unit means, } N \text{ observations})")
st.markdown("Uses only long-run/cross-sectional differences; discards all within-unit dynamics. "
            "Rarely used alone, but it is the conceptual opposite of FE.")

# ---------------------------------------------------------------
C.section("6 · Choosing FE vs RE — the Hausman test", "The classic decision", A)
st.latex(r"H=\big(\hat\beta_{FE}-\hat\beta_{RE}\big)'\Big[\mathrm{Var}(\hat\beta_{FE})-\mathrm{Var}(\hat\beta_{RE})\Big]^{-1}\big(\hat\beta_{FE}-\hat\beta_{RE}\big)\ \xrightarrow{d}\ \chi^2_K")
C.eqcap("H₀: RE is consistent (αᵢ uncorrelated with x). Reject ⇒ use Fixed Effects.")
C.callout("Modern caveat",
          "The classic Hausman test assumes <b>no cross-sectional dependence</b> and homogeneous "
          "slopes. In modern macro panels both often fail — which is precisely why we move to the "
          "CCE / factor world.", A)

# ---------------------------------------------------------------
C.section("7 · Homogeneous vs heterogeneous slopes", "The bridge to modern panels", A)
st.markdown(
    "So far $\\beta$ was the **same for every unit**. In macro panels that is a strong claim. "
    "The heterogeneous-slope family lets $\\beta_i$ differ:"
)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta_i+\varepsilon_{it}")
c1, c2, c3 = st.columns(3)
with c1:
    C.card("Mean Group (MG)", "Estimate a separate regression per unit, then average: "
           "β̂_MG = (1/N)Σ β̂ᵢ. Fully heterogeneous; needs a decent T per unit. (Pesaran–Smith 1995)", A)
with c2:
    C.card("Pooled Mean Group (PMG)", "Long-run coefficients <b>restricted equal</b> across units, "
           "short-run dynamics free. A compromise. (Pesaran–Shin–Smith 1999) → <code>xtpmg</code>", A)
with c3:
    C.card("Dynamic Fixed Effects (DFE)", "All coefficients pooled except intercepts. Most "
           "restrictive; badly biased if slopes truly differ.", A)
C.callout("Why this matters for third generation",
          "The <b>CCE</b> estimators (CCEMG, CCEP) are the heterogeneous-slope family <i>plus</i> "
          "a fix for cross-sectional dependence. And it is the heterogeneous slope βᵢ(t) that "
          "later acquires a <b>structural break</b>.", A)

# ---------------------------------------------------------------
C.section("8 · Summary table", "The static models at a glance", A)
st.markdown(
    "| Model | Assumption on αᵢ | Slope | Time-invariant x? | Main risk |\n"
    "|---|---|---|---|---|\n"
    "| Pooled OLS | none (αᵢ=α) | common | yes | omitted heterogeneity bias |\n"
    "| Fixed Effects | parameter, may correlate with x | common | **no** | loses time-invariant vars |\n"
    "| Random Effects | random, uncorrelated with x | common | yes | inconsistent if assumption fails |\n"
    "| Between | — (uses means) | common | yes | throws away within variation |\n"
    "| Mean Group | free | **heterogeneous** | — | needs large T |\n"
    "| PMG | free | LR pooled, SR free | — | LR homogeneity may fail |"
)

C.dev_footer()
