import streamlit as st
import numpy as np
import plotly.graph_objects as go
import common as C

A = C.TOPIC["generations"]
C.hero(
    "The three generations and their characteristics",
    "Panel unit-root and cointegration tests are sorted into three generations — not by age, "
    "but by which convenient assumption each one is finally willing to drop.",
    A, tag="Foundations",
)

# ---------------------------------------------------------------
C.section("1 · The organising principle", "One assumption at a time", A)
C.callout("The single idea",
          "Each generation <b>relaxes one more assumption</b> of the one before it. "
          "1st assumes units are independent. 2nd allows them to be dependent. "
          "3rd allows dependence <b>and</b> structural breaks.", A)

G1, G2, G3 = C.PALETTE["indigo"], C.PALETTE["teal"], C.PALETTE["orange"]
c1, c2, c3 = st.columns(3)
with c1:
    C.card("1️⃣ First generation",
           "<b>Assumes cross-sectional independence.</b> Power comes purely from stacking N series. "
           "Fails badly (over-rejects) if units share shocks.", G1)
    C.chips(["LLC", "IPS", "Breitung", "Fisher-ADF/PP", "Hadri", "Pedroni", "Kao"], G1)
with c2:
    C.card("2️⃣ Second generation",
           "<b>Allows cross-sectional dependence</b> via a common-factor structure — removed by "
           "cross-section averages (CCE) or principal components (PANIC). Still assumes no breaks.", G2)
    C.chips(["CADF/CIPS", "PANIC", "Moon–Perron", "Choi", "Westerlund ECM", "IFE (Bai 2009)"], G2)
with c3:
    C.card("3️⃣ Third generation",
           "<b>Allows dependence AND structural breaks</b>, with break dates estimated rather than "
           "assumed. The frontier.", G3)
    C.chips(["Carrion et al. (2005)", "Bai–Carrion PANIC", "Westerlund (2006)",
             "Westerlund–Edgerton", "Banerjee–Carrion", "Baltagi–Feng–Wang"], G3)

# ---------------------------------------------------------------
C.section("2 · The characteristics table", "What each generation assumes", A)
st.markdown(
    "| Characteristic | 1st generation | 2nd generation | 3rd generation |\n"
    "|---|---|---|---|\n"
    "| Cross-sectional dependence | ❌ assumed away | ✅ allowed | ✅ allowed |\n"
    "| Structural breaks | ❌ none | ❌ none | ✅ allowed & estimated |\n"
    "| How dependence is handled | — | CCE averages / factors / bootstrap | same, plus break terms |\n"
    "| Break dates | — | — | estimated (SSR grid, Bai–Perron) |\n"
    "| Deterministic component | constant / trend | constant / trend | constant / trend **+ shifts** |\n"
    "| Critical values | standard tables | factor/bootstrap-based | depend on model **and** break count |\n"
    "| Typical failure if misused | over-rejects under CSD | loses power under breaks | (computationally heavier) |\n"
    "| Example unit-root test | IPS | CIPS | Carrion et al. / `xtpqroot` |\n"
    "| Example cointegration test | Pedroni | Westerlund (2007) | Banerjee–Carrion / `xtpcointegwe` |"
)

# ---------------------------------------------------------------
C.section("3 · See the difference", "Toggle the two complications", A)
st.markdown(
    "Below are 5 units. Turn each complication on/off to see what a generation must cope with."
)
cc1, cc2 = st.columns(2)
csd = cc1.toggle("Cross-sectional dependence (a shared factor)", value=False)
brk = cc2.toggle("Structural break", value=False)

rng = C.rng(11)
N, T, TB = 5, 120, 60
t = np.arange(T)
F = np.cumsum(rng.normal(0, 1, T))
fig = go.Figure()
cols = [C.PALETTE[k] for k in ["indigo", "teal", "pink", "orange", "grape"]]
for i in range(N):
    lam = 0.6 + rng.random() * 0.9
    idio = np.cumsum(rng.normal(0, 0.6, T))
    shift = (1.8 + rng.random() * 1.2) * (1 if rng.random() < .5 else -1)
    y = idio + (lam * F if csd else 0) + (np.where(t >= TB, shift, 0.0) if brk else 0.0)
    fig.add_trace(go.Scatter(x=t, y=y, mode="lines", name=f"unit {i+1}",
                             line=dict(color=cols[i], width=2)))
if brk:
    fig.add_vline(x=TB, line=dict(color=C.PALETTE["red"], dash="dash", width=2),
                  annotation_text="break")
C.show(fig, height=380)

if not csd and not brk:
    C.callout("1st generation world", "Units are independent and stable — the only case where "
              "LLC/IPS are valid.", G1)
elif csd and not brk:
    C.callout("2nd generation world", "The series move <b>together</b> (a shared factor). "
              "1st-generation tests now over-reject; you need CIPS / PANIC.", G2)
elif not csd and brk:
    C.callout("Break-only world", "Every series jumps. A stationary series around a shifted mean "
              "<b>looks</b> like a unit root — the Perron critique.", C.PALETTE["yellow"])
else:
    C.callout("3rd generation world", "Both at once: shared factors <b>and</b> a break. "
              "Only third-generation methods are valid here.", G3)

# ---------------------------------------------------------------
C.section("4 · Timeline", "How the field moved", A)
events = [
    (1992, "KPSS", G1), (2002, "LLC", G1), (2003, "IPS", G1), (2004, "Pedroni/Kao", G1),
    (2004, "PANIC (Bai–Ng)", G2), (2006, "CCE (Pesaran)", G2), (2007, "CIPS (Pesaran)", G2),
    (2005, "Carrion et al.", G3), (2006, "Westerlund", G3), (2009, "Bai–Carrion", G3),
    (2011, "KPY I(1) factors", G3), (2016, "Qian–Su / BFK", G3), (2021, "Okui–Wang GAGFL", G3),
    (2025, "Kaddoura CBC / BFW", G3),
]
fig = go.Figure()
for gen, col, yy in [("1st", G1, 1), ("2nd", G2, 2), ("3rd", G3, 3)]:
    xs = [e[0] for e in events if e[2] == col]
    ts = [e[1] for e in events if e[2] == col]
    fig.add_trace(go.Scatter(x=xs, y=[yy] * len(xs), mode="markers+text", text=ts,
                             textposition="top center", textfont=dict(size=9, color=col),
                             marker=dict(size=13, color=col, line=dict(width=2, color="white")),
                             name=f"{gen} generation"))
fig.update_layout(yaxis=dict(tickvals=[1, 2, 3], ticktext=["1st gen", "2nd gen", "3rd gen"],
                             range=[0.5, 3.6]),
                  xaxis_title="year", height=340)
C.show(fig, height=340, title="The three generations over time")

C.callout("Cumulative, not competing",
          "A 3rd-generation test does not abandon the factor machinery of the 2nd — it "
          "<b>carries it</b> and adds break-date estimation. If your data has factors but no "
          "breaks, a 2nd-generation test is more powerful; if it has breaks you ignore, you lose "
          "power badly.", A)

C.dev_footer()
