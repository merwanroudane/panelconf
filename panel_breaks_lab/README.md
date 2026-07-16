# Panel Breaks — Interactive Simulation Lab 🎬

Animated Streamlit simulations that **show** what structural-break concepts mean.
Every chart has a **▶ PLAY** button.

**Developed by Dr Merwan Roudane** — author of the `xt*` panel structural-break Stata suite
(ideas.repec.org/f/pro1421 · github.com/merwanroudane).

## Pages
| Page | Animation |
|---|---|
| 🏠 Home | Six units drawing through time, all jumping together |
| 1️⃣ Common break | Units jump at one date + SSR minimum sharpening as N grows |
| 2️⃣ Heterogeneous breaks | Units jump one by one + Fourier absorbing a unit's own break |
| 3️⃣ Latent (grouped) breaks | Two hidden groups + GAGFL re-assigning units to their true group |
| 🌐 Cross-sectional dependence | Independent series **synchronising** as the factor takes over; size distortion exploding; CCE de-factoring |
| 🌊 Dummy vs Fourier | The break **morphs** from gradual to sharp — watch the winner switch; one Fourier frequency capturing two breaks |
| 🎛️ Regularization | Turn λ up: over-segmentation → correct → over-smoothing; the IC picking λ; lasso geometry |
| 🎯 Finding the date | The SSR grid search sweeping the sample and locking onto the break |

## Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Light theme, Plotly animations, `st.latex` for the maths, explanation for every part.
