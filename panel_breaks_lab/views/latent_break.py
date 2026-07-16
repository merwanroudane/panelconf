import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["latent"]
C.hero(
    "3️⃣ Latent (grouped) breaks",
    "The clever middle ground: units are neither all identical nor all different — they fall "
    "into HIDDEN GROUPS, each with its own break date. And you don't know who belongs to which "
    "group. Watch the algorithm discover them.",
    A, tag="Types of break",
)

C.section("The model", "Between common and heterogeneous", A)
st.latex(r"y_{it}=\alpha_i+x_{it}'\beta_{g_i}(t)+\varepsilon_{it},\qquad g_i\in\{1,\dots,G\}")
st.latex(r"T_{Bi}=T_{g}\quad\text{if}\quad i\in G_g")
st.markdown(
    "Unit $i$ belongs to an **unknown** group $g_i$, and all members of a group share that "
    "group's break date. **Both** the membership and the dates are estimated."
)
C.callout("Real-world example",
          "<b>Group 1</b> (USA, Canada, UK) broke in <b>2008</b> — the financial crisis. "
          "<b>Group 2</b> (Spain, Italy, Greece) broke in <b>2011</b> — the sovereign-debt crisis. "
          "Not one common date; not six different dates. <b>Two hidden clusters.</b>", A)

# ---------------------------------------------------------------- sim
C.section("Simulation — two hidden groups", "Animation 1", A)
c1, c2, c3 = st.columns(3)
d1 = c1.slider("Group A break date", 15, 50, 30)
d2 = c2.slider("Group B break date", 50, 85, 65)
noise = c3.slider("Noise", 0.1, 1.2, 0.30, 0.05)
C.play_hint()

rng = C.rng(4)
T = 100
t = np.arange(T)
GA, GB = C.PALETTE["teal"], C.PALETTE["pink"]
units = []
for i in range(6):
    grp = 0 if i < 3 else 1
    d = d1 if grp == 0 else d2
    base = (i % 3 - 1) * 1.2 + (0 if grp == 0 else 0.4)
    y = base + np.cumsum(rng.normal(0, noise, T)) + np.where(t >= d, 3.6, 0.0)
    units.append((y, grp))

fig = go.Figure()
for i, (y, grp) in enumerate(units):
    fig.add_trace(go.Scatter(x=[t[0]], y=[y[0]], mode="lines",
                             name=f"unit {i+1} · group {'A' if grp==0 else 'B'}",
                             line=dict(color=GA if grp == 0 else GB, width=2.6)))
fig.add_vline(x=d1, line=dict(color=GA, dash="dash", width=2), annotation_text="Group A break")
fig.add_vline(x=d2, line=dict(color=GB, dash="dash", width=2), annotation_text="Group B break")
lo = min(y.min() for y, _ in units) - 1
hi = max(y.max() for y, _ in units) + 1
fig.update_layout(xaxis=dict(range=[0, T - 1], title="time"), yaxis=dict(range=[lo, hi], title="y"))
frames = [go.Frame(name=str(k),
                   data=[go.Scatter(x=t[:k], y=units[i][0][:k], mode="lines",
                                    line=dict(color=GA if units[i][1] == 0 else GB, width=2.6))
                         for i in range(6)])
          for k in range(2, T + 1, 2)]
C.show(C.animate(fig, frames, duration=45, slider_prefix="t = ", height=430,
                 title="Two latent groups, two different break dates"))
C.callout("What you're seeing",
          "The <b>teal</b> units jump together at one date; the <b>pink</b> units jump together at "
          "another. Within a group: common. Across groups: different. <b>In real data the colours "
          "are invisible</b> — you don't know who is teal and who is pink. That is exactly the "
          "problem GAGFL solves.", A)

# ---------------------------------------------------------------- the problem
C.section("The problem: the colours are hidden", "Animation 2", A)
st.markdown(
    "This is what you actually receive — **the same data with no group labels**. Press PLAY and "
    "try to spot the two clusters by eye:"
)
C.play_hint("▶ PLAY — can you see two groups? (This is what the algorithm has to work with.)")
fig1b = go.Figure()
for i in range(6):
    fig1b.add_trace(go.Scatter(x=[t[0]], y=[units[i][0][0]], mode="lines", showlegend=False,
                               line=dict(color="#8A97A6", width=2.2)))
fig1b.update_layout(xaxis=dict(range=[0, T - 1], title="time"),
                    yaxis=dict(range=[lo, hi], title="y"))
frames1b = [go.Frame(name=str(k),
                     data=[go.Scatter(x=t[:k], y=units[i][0][:k], mode="lines",
                                      line=dict(color="#8A97A6", width=2.2)) for i in range(6)])
            for k in range(2, T + 1, 2)]
C.show(C.animate(fig1b, frames1b, duration=45, slider_prefix="t = ", height=380,
                 title="The same data — but the groups are LATENT (unlabelled)"))

# ---------------------------------------------------------------- GAGFL
C.section("How GAGFL discovers them", "Okui & Wang (2021)", A)
st.markdown(
    "**GAGFL = Grouped Adaptive Group Fused Lasso.** Three stages, repeated until nothing changes:"
)
c1, c2, c3 = st.columns(3)
with c1:
    C.card("1 · GFE initialisation",
           "Cluster units into G groups (k-means style, Bonhomme–Manresa) on their estimated "
           "coefficient paths. Many random starts avoid bad local minima.", A)
with c2:
    C.card("2 · Group-specific AGFL",
           "Inside each group, run the adaptive group fused lasso to find <i>that group's</i> "
           "break dates — automatically, no number specified.", A)
with c3:
    C.card("3 · Reassignment",
           "Move each unit to whichever group's coefficient path fits it best (lowest SSR). "
           "Then go back to stage 2.", A)
st.markdown("Watch the iterations converge — units are re-coloured as they find their true group:")
C.play_hint("▶ PLAY to watch the algorithm re-assign units to their correct group.")

# animation: misassignment shrinking over iterations
iters = 8
rng3 = C.rng(21)
true_grp = np.array([0, 0, 0, 1, 1, 1])
assign_hist = []
cur = np.array([0, 1, 0, 1, 0, 1])          # bad start
assign_hist.append(cur.copy())
for it in range(1, iters):
    nxt = cur.copy()
    wrong = np.where(nxt != true_grp)[0]
    if len(wrong):                            # fix one or two per iteration
        fix = wrong[:max(1, len(wrong) // 2)]
        nxt[fix] = true_grp[fix]
    cur = nxt
    assign_hist.append(cur.copy())

fig3 = go.Figure()
xs = np.arange(1, 7)
fig3.add_trace(go.Bar(x=xs, y=[1] * 6,
                      marker_color=[GA if g == 0 else GB for g in assign_hist[0]],
                      text=["A" if g == 0 else "B" for g in assign_hist[0]],
                      textposition="inside", textfont=dict(size=16, color="#fff"),
                      showlegend=False))
fig3.update_layout(xaxis=dict(title="unit", tickvals=list(xs)),
                   yaxis=dict(title="", range=[0, 1.4], showticklabels=False))
frames3 = []
for it in range(iters):
    nwrong = int((assign_hist[it] != true_grp).sum())
    frames3.append(go.Frame(
        name=str(it),
        data=[go.Bar(x=xs, y=[1] * 6,
                     marker_color=[GA if g == 0 else GB for g in assign_hist[it]],
                     text=["A" if g == 0 else "B" for g in assign_hist[it]],
                     textposition="inside", textfont=dict(size=16, color="#fff"),
                     showlegend=False)],
        layout=go.Layout(title=f"Iteration {it} — misassigned units: {nwrong}")))
C.show(C.animate(fig3, frames3, duration=650, slider_prefix="iteration ", height=330,
                 title="Iteration 0 — misassigned units: 3"))
st.success("✅ True grouping is **A A A B B B**. The algorithm starts wrong and converges to it — "
           "recovering the memberships *and* each group's break dates.")

# ---------------------------------------------------------------- spectrum
C.section("The full spectrum", "Where grouped sits", A)
st.markdown(
    "| | Common | **Grouped (latent)** | Heterogeneous |\n"
    "|---|---|---|---|\n"
    "| Break schedules | 1 | **G** | N |\n"
    "| Flexibility | lowest | **middle** | highest |\n"
    "| Power | highest | **good** | lowest |\n"
    "| Needs to know membership? | — | **no — estimated** | — |\n"
    "| Command | `xtbreakmodel, pls` | **`xtbreakmodel, gagfl`** | `xtfmg fccemg` |"
)
C.callout("Why grouped is often the sweet spot",
          "Common breaks are usually <b>too rigid</b> (countries don't all react in the same year) "
          "and fully heterogeneous breaks are <b>too costly</b> (N dates from N short series). "
          "Latent groups give real heterogeneity at a fraction of the parameter cost — and "
          "<b>G = 1 nests the common-break case</b>, so you lose nothing by allowing it.", A)

st.code("* choose G by BIC over a small grid\n"
        "xtbreakmodel y x, method(gagfl) groups(2)\n"
        "xtbreakmodel y x, method(gagfl) groups(3)", language="stata")

C.dev_footer()
