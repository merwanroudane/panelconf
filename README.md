# Structural Breaks in Panel Data — A Researcher's Guide

A multi-page Streamlit app that explains, from first principles to the research frontier,
the **pre-concepts, tests, estimators and methods** for structural breaks in panel data.
Grounded in the founding papers (Carrion-i-Silvestre et al. 2005; Westerlund 2006;
Kapetanios–Pesaran–Yamagata 2011; Baltagi–Feng–Kao 2016/2019; Baltagi–Feng–Wang 2025;
Banerjee–Carrion-i-Silvestre 2015/2017/2025; Okui–Wang 2021; Li–Xiao–Chen SaRa;
Zhang et al. 2022; Corakci–Omay 2023; Nazlioglu–Karul 2017; Olayeni et al. 2021;
Omay et al. 2017).

**Developed by Dr Merwan Roudane** — author of the `xt*` panel structural-break Stata suite
(ideas.repec.org/f/pro1421 · github.com/merwanroudane).

## Pages
1. **Home & Roadmap**
2. **Preliminary Concepts** — integration, spurious regression, cointegration, LRV, CSD, factors, quantiles, Fourier, bootstrap, the Perron critique
3. **Anatomy of a Break** — level/trend/regime; slope/vector/loading; single/multiple; known/unknown; common/grouped/heterogeneous; sharp/smooth
4. **Unit-Root & Stationarity Tests** — panel KPSS, PANIC, Im–Lee–Tieslau, CIPS, quantile CIPS(τ), tFR
5. **Cointegration Tests** — Westerlund, Westerlund–Edgerton, Banerjee–Carrion trilogy, nonlinear ECM
6. **Fourier & Smooth Breaks** — FFF, FFFFF, Fourier KPSS, tFR, F-CCEMG
7. **Break Estimators** — Bai–Perron, Qian–Su, BFK, GAGFL, SaRa, CBCL, BFW, shrinkage quantile
8. **CSD & Factors** — CD test, CCE, KPY I(1) factors, PANIC, interactive FE, bootstrap
9. **Break-Date Estimation & Inference** — SSR grid, dynamic programming, sup-F, ICs, super-consistency, pooling
10. **Stata Software Map** — the 14 commands, syntax, workflow
11. **References**

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually http://localhost:8501).
The app is **light-themed** (`.streamlit/config.toml`), uses `st.latex` for equations and
Plotly for all figures.
