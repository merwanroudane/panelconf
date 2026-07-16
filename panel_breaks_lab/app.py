"""
Panel Breaks — Interactive Simulation Lab
=========================================

Animated simulations that SHOW what each concept means:
common breaks, heterogeneous breaks, latent (grouped) breaks,
cross-sectional dependence, dummy vs Fourier, and regularization.

Every chart has a PLAY button.

Developer: Dr Merwan Roudane
Run with:  streamlit run app.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import common as C

st.set_page_config(
    page_title="Panel Breaks — Simulation Lab",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

C.inject_css()
C.sidebar_brand()

if not hasattr(st, "navigation"):
    st.error("This app needs Streamlit >= 1.36.  Run:  pip install --upgrade streamlit")
    st.stop()

pages = {
    "Start": [
        st.Page("views/home.py", title="Home & how to use", icon="🏠", default=True),
    ],
    "Types of break": [
        st.Page("views/common_break.py", title="Common break", icon="1️⃣"),
        st.Page("views/hetero_break.py", title="Heterogeneous breaks", icon="2️⃣"),
        st.Page("views/latent_break.py", title="Latent (grouped) breaks", icon="3️⃣"),
    ],
    "The two complications": [
        st.Page("views/csd.py", title="Cross-sectional dependence", icon="🌐"),
    ],
    "How to model a break": [
        st.Page("views/dummy_fourier.py", title="Dummy vs Fourier", icon="🌊"),
        st.Page("views/regularization.py", title="Regularization", icon="🎛️"),
        st.Page("views/methods.py", title="How a break date is found", icon="🎯"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
