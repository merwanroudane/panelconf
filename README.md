# panelconf — Structural Breaks in Panel Data

A complete teaching & research toolkit for **third-generation panel econometrics**:
cross-sectional dependence **plus** structural breaks — interactive guides, lecture notes,
a diagram, and runnable Stata do-files.

**Developed by Dr Merwan Roudane** — author of the `xt*` panel structural-break Stata suite
(100+ modules).
[IDEAS/RePEc](https://ideas.repec.org/f/pro1421.html) · [GitHub](https://github.com/merwanroudane)

---

## 📦 What's in this repository

| Folder | What it is |
|---|---|
| **`/` (root)** | **Streamlit app — Structural Breaks guide** (the tests & estimators) |
| **`panel_preconcepts_guide/`** | **Streamlit app — Pre-concepts guide** (the foundations *before* 3rd generation) |
| **`panel_breaks_lab/`** | **Streamlit app — Animated Simulation Lab** (every chart has a ▶ PLAY button) |
| **`guides/`** | Self-contained HTML guides (open in any browser, work offline) |
| **`lecture/`** | Two LaTeX lectures (`.tex` + compiled `.pdf`) and the generations diagram |
| **`stata_do_files/`** | 21 beginner do-files — one per command, on real data |
| **`papers/`** | Reference index: every method → its source paper, with clickable DOIs |

---

## 1. Streamlit app — Structural Breaks (root)

The tests, estimators and methods for breaks in panels.

```bash
pip install -r requirements.txt
streamlit run app.py
```

**Pages:** Preliminary concepts · Anatomy of a break · Unit-root & stationarity tests ·
Cointegration tests · Fourier & smooth breaks · Break estimators · CSD & factors ·
Break-date estimation · Stata software map · References.

## 2. Streamlit app — Pre-concepts (`panel_preconcepts_guide/`)

Everything you must understand **before** third generation.

```bash
cd panel_preconcepts_guide
pip install -r requirements.txt
streamlit run app.py
```

**Pages:** N and T (asymptotics, Nickell bias, interactive N–T map) · Basic static models
(Pooled/FE/RE/Between/Hausman/MG/PMG) · Integration & cointegration · The three generations ·
Cross-sectional dependence & its degree (α exponent) · **CSA/CCE family vs common factors** ·
**CSD tests** (CD, LM, scaled LM, CD\*, Frees, α) · **Dummy vs Fourier** · **Regularization**
(lasso → fused lasso → GAGFL/CBC) · References.

## 3. HTML guides (`guides/`)

Single self-contained files — double-click to open, no internet needed.

| File | Language | Description |
|---|---|---|
| **`panel_breaks_decision_guide.html`** ⭐ | English | **Which method should I use?** — an *interactive* decision tool: answer 7 diagnostic questions and get the recommended command with the reason, alternatives and warnings. Plus a decision flowchart, 18 "use when / avoid when" method profiles, a comparison matrix, 6 red flags, and a cheat-sheet. |
| `panel_structural_breaks_guide_AR.html` | **العربية** | دليل شامل لأنواع التغيرات الهيكلية: مشترك/غير متجانس/مجموعات كامنة، Dummy vs Fourier vs Regularization، خريطة اختيار المنهج، جداول ومراجع |
| `panel_3rd_generation_lecture.html` | English | Third-generation lecture: generations, tests, estimators, interactive CSD+break demo |

## 3b. Streamlit app — Animated Simulation Lab (`panel_breaks_lab/`)

**Watch the concepts move.** Every chart has a **▶ PLAY** button.

```bash
cd panel_breaks_lab
pip install -r requirements.txt
streamlit run app.py
```

Units jumping together (common break) · jumping one by one (heterogeneous) · two hidden clusters
and GAGFL re-assigning them (latent groups) · independent series **synchronising** as a common
factor takes over, and a test's false-rejection rate exploding (CSD) · the break **morphing** from
gradual to sharp while Dummy and Fourier race (the winner switches) · turning **λ** up until
spurious breaks fuse away — then real ones die too (regularization) · and the **SSR grid search**
sweeping the sample to lock onto the break date.

## 4. Lecture notes (`lecture/`)

- **`Panel_Methods_Organized_Lecture.pdf`** — 13-page colour lecture: **a map of the whole field**.
  The ladder of relaxed assumptions (Pooled → FE → **MG/PMG** → **CCE/PANIC** → breaks → frontier).
  Every method gets: *the idea* · *when to use it* ✅ · *when NOT to* ❌ · *how it differs from its
  neighbour*. Includes MG vs PMG vs DFE, CSA vs factors, and a decision map.
- **`Third_Generation_Panel_Lecture.pdf`** — 20-page colour lecture on third-generation methods
  (pre-concepts, breaks, CSD, regularization, Fourier, tests, worked application, FAQ, exercises)
- Both `.tex` sources included (compile with `latexmk -pdf`)
- **`panel_three_generations.png`** — bilingual (عربي/English) three-generations diagram

## 5. Stata do-files (`stata_do_files/`)

18 beginner-friendly do-files — **one per command**, each using **real data**
(`webuse grunfeld`), with plain-language comments and simple options.

```stata
cd stata_do_files
do 00_START_HERE.do     // check the data loads
do 01_xtpkpss.do        // then any file
```

Install every command first: see **`INSTALL_commands.txt`**.
All 18 files were executed and verified on real data.

---

## 🧰 The commands covered (the `xt*` break-in-panels suite)

**Tests / detection:** `xtpkpss` · `xtpqroot` · `xtlmbreak` · `xtpcointegwe` ·
`xtpcointegboot` · `xtbreakcoint` · `xtccecoint` · `xtcadfcoint` · `xtnonlincoint` · `xtgets`

**Estimators:** `xtbreakmodel` · `xtcbc` · `xtkpybreak` · `xtbfkbreak` ·
`xtquantilebreak` · `xtdynestimb` · `xtpvarcoint`

**Second-generation estimators, Fourier ARDL & causality:** `xtfmg` (FE, MG, CCEMG, SURMG,
F-SURMG, **F-CCEMG**) · `xtpfardl` (Fourier panel ARDL / CS-ARDL, needs `xtdcce2`) ·
`xtpcaus` (Fourier Toda–Yamamoto & Panel Quantile Causality)

---

## 📚 Source papers (`papers/`)

**[`papers/README.md`](papers/README.md)** indexes every method → its source paper, with a
clickable **DOI** and the command that implements it.

> **Copyright note.** The paper PDFs are **not redistributed here**. Almost all are published by
> Elsevier, Wiley, Taylor & Francis or Oxford University Press, or distributed via JSTOR, and are
> protected by copyright — JSTOR's terms prohibit redistribution explicitly. Use the DOI links:
> they resolve to the publisher's official version. The single PDF included
> (`Karavias_Tzavalis_Zhang_2022_Econometrics.pdf`) is **open access under CC BY**.

## 📚 Built on

Carrion-i-Silvestre, del Barrio-Castro & López-Bazo (2005) · Westerlund (2006) ·
Westerlund & Edgerton (2007, 2008) · Kapetanios, Pesaran & Yamagata (2011) ·
Baltagi, Feng & Kao (2016, 2019) · Baltagi, Feng & Wang (2025) ·
Banerjee & Carrion-i-Silvestre (2015, 2017, 2025) · Okui & Wang (2021) ·
Qian & Su (2016) · Li, Xiao & Chen (SaRa) · Kaddoura (2025) · Zhang et al. (2022) ·
Corakci & Omay (2023) · Nazlioglu & Karul (2017) · Olayeni, Tiwari & Wohar (2021) ·
Omay, Emirmahmutoglu & Denaux (2017).

Please cite the original methodological papers when using the commands.
