"""
Structural Breaks in Panel Data — A Researcher's Guide
=====================================================

A multi-page Streamlit reference explaining the pre-concepts, tests,
estimators and methods for structural breaks in panel data, grounded in
the founding papers (Carrion-i-Silvestre et al. 2005; Westerlund 2006;
Kapetanios-Pesaran-Yamagata 2011; Baltagi-Feng-Kao 2016/2019;
Banerjee-Carrion-i-Silvestre 2015/2017/2025; Okui-Wang 2021;
Li-Xiao-Chen SaRa; Zhang et al. 2022; Corakci-Omay 2023; and more).

Developer: Dr Merwan Roudane
Run with:  streamlit run app.py
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
import common as C

st.set_page_config(
    page_title="Panel Breaks — Researcher's Guide",
    page_icon="☀",
    layout="wide",
    initial_sidebar_state="expanded",
)

C.inject_css()
C.sidebar_brand()

# ----------------------------------------------------------------------
# Multi-page navigation (Streamlit >= 1.36)
# ----------------------------------------------------------------------
if not hasattr(st, "navigation"):
    st.error(
        "This app needs Streamlit >= 1.36 for multi-page navigation.\n\n"
        "Please run:  pip install --upgrade streamlit"
    )
    st.stop()

pages = {
    "Start here": [
        st.Page("views/home.py", title="Home & Roadmap", icon="🏠", default=True),
        st.Page("views/preliminaries.py", title="Preliminary Concepts", icon="📚"),
        st.Page("views/anatomy.py", title="Anatomy of a Break", icon="🧱"),
    ],
    "Testing for breaks": [
        st.Page("views/unit_root.py", title="Unit-Root & Stationarity Tests", icon="📉"),
        st.Page("views/cointegration.py", title="Cointegration Tests", icon="🔗"),
        st.Page("views/fourier.py", title="Fourier & Smooth Breaks", icon="🌊"),
    ],
    "Estimating breaks": [
        st.Page("views/estimators.py", title="Break Estimators", icon="📐"),
        st.Page("views/csd_factors.py", title="Cross-Section Dependence & Factors", icon="🌐"),
        st.Page("views/breakdate.py", title="Break-Date Estimation & Inference", icon="🎯"),
    ],
    "Reference": [
        st.Page("views/software.py", title="Stata Software Map", icon="🧰"),
        st.Page("views/references.py", title="References & Papers", icon="📖"),
    ],
}

pg = st.navigation(pages, position="sidebar")
pg.run()
