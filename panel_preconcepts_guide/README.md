# Panel Data Pre-Concepts — A Researcher's Guide

A multi-page Streamlit app covering **everything you need BEFORE third-generation panel
econometrics**: the N and T dimensions, basic static models, integration and cointegration,
the three generations and their characteristics, cross-sectional dependence and its degree,
the **CSA/CCE family vs the common-factor (PANIC/PC) family**, all the **CSD tests**,
**dummy vs Fourier**, and **regularization**.

Light theme throughout, `st.latex` for every equation, Plotly for every figure, and
interactive controls on most pages.

**Developed by Dr Merwan Roudane** — author of the `xt*` panel structural-break Stata suite
(ideas.repec.org/f/pro1421 · github.com/merwanroudane).

## Pages
| # | Page | Covers |
|---|---|---|
| 1 | Home & Roadmap | what the guide is, how it fits together |
| 2 | N and T | balanced/unbalanced, micro vs macro panels, the 4 asymptotic regimes, incidental parameters, Nickell bias, an interactive N–T map |
| 3 | Basic static models | Pooled OLS, Fixed Effects (within/LSDV), Random Effects, Between, Hausman, MG / PMG / DFE |
| 4 | Integration & cointegration | I(0) vs I(1), unit roots, spurious regression, cointegration & ECM, long-run variance, ADF vs KPSS |
| 5 | The three generations | what each assumes/relaxes, the characteristics table, an interactive demo, a timeline |
| 6 | Cross-sectional dependence | the common-factor error, why 1st-gen over-rejects, the degree (weak / semi-weak / strong, the α exponent) |
| 7 | **CSA vs common factors** | the CCE family (CCEMG, CCEP, CS-ARDL, CS-DL, dynamic CCE, F-CCEMG) vs the factor family (PANIC, IFE, CUP-FM, Moon–Perron) + the full comparison table |
| 8 | **CSD tests** | BP-LM, scaled LM, bias-corrected LM, Pesaran CD, CD*, Frees, Friedman, α exponent + a decision table |
| 9 | Dummy vs Fourier | sharp vs smooth, Gallant's theorem, fractional frequencies, logistic transition, interactive fit comparison |
| 10 | Regularization | overfitting, bias–variance, ridge vs lasso geometry, soft-thresholding, the fused lasso as a break detector, adaptive weights, BCD, GAGFL / CBC |
| 11 | References | grouped by theme |

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501.

## Companion
This is the *foundations* guide. Its sequel — the structural-break tests and estimators
themselves — is the **panel_break_guide** app (also by Dr Merwan Roudane).
