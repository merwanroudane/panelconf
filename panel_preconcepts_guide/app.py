"""
Panel Data Pre-Concepts — A Researcher's Guide
==============================================

Everything you must understand BEFORE third-generation panel methods:
N & T asymptotics, basic static models, integration & cointegration,
the three generations, cross-sectional dependence, the cross-sectional
average (CSA/CCE) family vs the common-factor approach, CSD tests,
dummy vs Fourier, and regularization.

Developer: Dr Merwan Roudane
Run with:  streamlit run app.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import common as C

st.set_page_config(
    page_title="Panel Pre-Concepts — Researcher's Guide",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

C.inject_css()
C.sidebar_brand()

if not hasattr(st, "navigation"):
    st.error("This app needs Streamlit >= 1.36.  Run:  pip install --upgrade streamlit")
    st.stop()

pages = {
    "Start here": [
        st.Page("views/home.py", title="Home & Roadmap", icon="🏠", default=True),
        st.Page("views/n_and_t.py", title="N and T: the two dimensions", icon="📐"),
        st.Page("views/static_models.py", title="Basic static panel models", icon="🧮"),
    ],
    "Time-series foundations": [
        st.Page("views/integration.py", title="Integration & cointegration", icon="📈"),
        st.Page("views/generations.py", title="The three generations", icon="🧬"),
    ],
    "Cross-sectional dependence": [
        st.Page("views/csd.py", title="What CSD is (and its degree)", icon="🌐"),
        st.Page("views/csa_vs_factor.py", title="CSA family vs common factors", icon="⚖️"),
        st.Page("views/csd_tests.py", title="CSD tests: all types", icon="🧪"),
    ],
    "Modelling toolkits": [
        st.Page("views/dummy_vs_fourier.py", title="Dummy vs Fourier", icon="🌊"),
        st.Page("views/regularization.py", title="Regularization explained", icon="🎛️"),
    ],
    "Reference": [
        st.Page("views/references.py", title="References", icon="📖"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
