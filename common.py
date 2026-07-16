"""
Shared styling, palette, and UI helpers for the
"Structural Breaks in Panel Data" researcher guide.

Developer: Dr Merwan Roudane
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go

# ----------------------------------------------------------------------
# Palette  (Open-Color based — bright, harmonious, light-theme only)
# ----------------------------------------------------------------------
PALETTE = {
    "indigo":  "#4C6EF5",
    "blue":    "#1C7ED6",
    "cyan":    "#1098AD",
    "teal":    "#0CA678",
    "green":   "#37B24D",
    "lime":    "#74B816",
    "yellow":  "#F59F00",
    "orange":  "#F76707",
    "red":     "#E8590C",
    "pink":    "#E64980",
    "grape":   "#9C36B5",
    "violet":  "#7048E8",
    "gray":    "#495057",
    "ink":     "#1F2733",
    "muted":   "#5C6B7A",
    "paper":   "#FFFFFF",
    "soft":    "#F3F5FB",
}

# accent hue for each page/topic
TOPIC = {
    "home":          "#7048E8",
    "preliminaries": "#4C6EF5",
    "anatomy":       "#F59F00",
    "unitroot":      "#0CA678",
    "coint":         "#7048E8",
    "estimators":    "#E64980",
    "csd":           "#1098AD",
    "breakdate":     "#F76707",
    "fourier":       "#9C36B5",
    "software":      "#1C7ED6",
    "references":    "#495057",
}


def inject_css():
    """Global CSS — light, colorful, readable."""
    st.markdown(
        """
        <style>
        :root { --ink:#1F2733; --muted:#5C6B7A; }
        html, body, [class*="css"] { font-family:'Inter','Segoe UI',system-ui,sans-serif; }
        .block-container { padding-top:2.2rem; padding-bottom:4rem; max-width:1180px; }

        /* hero banner */
        .hero {
            border-radius:20px; padding:34px 40px; color:#fff; margin-bottom:22px;
            box-shadow:0 14px 40px -18px rgba(80,40,180,.55);
        }
        .hero h1 { font-size:2.15rem; margin:0 0 .35em; line-height:1.12; font-weight:800; }
        .hero p  { font-size:1.06rem; margin:0; opacity:.96; line-height:1.55; }
        .hero .tag { font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
                     font-weight:700; opacity:.85; margin-bottom:.9em; }

        /* section header */
        .sec {
            border-left:6px solid var(--acc); padding:.1em 0 .1em 16px; margin:1.6em 0 .4em;
        }
        .sec h2 { margin:0; font-size:1.5rem; font-weight:800; color:var(--ink); }
        .sec .kick { font-family:ui-monospace,monospace; font-size:.72rem; letter-spacing:.14em;
                     text-transform:uppercase; font-weight:700; color:var(--acc); margin-bottom:.2em; }

        /* cards */
        .card {
            background:#fff; border:1px solid #E6E9F2; border-left:5px solid var(--acc);
            border-radius:14px; padding:18px 22px; margin:.6em 0;
            box-shadow:0 6px 20px -14px rgba(30,40,60,.35);
        }
        .card h4 { margin:0 0 .35em; font-size:1.05rem; font-weight:700; color:var(--ink); }
        .card p  { margin:.2em 0; color:var(--muted); font-size:.95rem; line-height:1.55; }

        /* pill / chip */
        .chip { display:inline-block; font-family:ui-monospace,monospace; font-size:.74rem;
                font-weight:600; padding:.22em .6em; border-radius:7px; margin:.15em .25em .15em 0;
                background:var(--chipbg); color:var(--chipfg); border:1px solid var(--chipfg33); }

        /* callout */
        .call { border-radius:12px; padding:14px 18px; margin:1em 0; font-size:.95rem;
                border:1px solid var(--acc); background:var(--accsoft); }
        .call b.h { display:block; font-family:ui-monospace,monospace; font-size:.7rem;
                    letter-spacing:.13em; text-transform:uppercase; color:var(--acc); margin-bottom:.3em; }

        /* key-term */
        .kt { font-weight:700; color:var(--ink); border-bottom:2px dotted #C6CEDC; }

        /* equation caption */
        .eqcap { color:var(--muted); font-size:.86rem; margin:-.3em 0 1em; padding-left:4px; }

        /* dev footer */
        .devfoot { margin-top:3rem; padding-top:1rem; border-top:1px solid #E6E9F2;
                   color:#8A97A6; font-size:.82rem; font-family:ui-monospace,monospace; }
        a { color:#4C6EF5; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero(title, subtitle, color, tag="Structural Breaks in Panel Data"):
    grad = f"linear-gradient(120deg, {color} 0%, {_shift(color)} 100%)"
    st.markdown(
        f"""<div class="hero" style="background:{grad}">
        <div class="tag">{tag}</div>
        <h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True,
    )


def section(title, kicker, color):
    st.markdown(
        f"""<div class="sec" style="--acc:{color};--ink:#1F2733">
        <div class="kick">{kicker}</div><h2>{title}</h2></div>""",
        unsafe_allow_html=True,
    )


def card(title, body, color):
    st.markdown(
        f"""<div class="card" style="--acc:{color}">
        <h4>{title}</h4><p>{body}</p></div>""",
        unsafe_allow_html=True,
    )


def callout(title, body, color):
    st.markdown(
        f"""<div class="call" style="--acc:{color};--accsoft:{_soft(color)}">
        <b class="h">{title}</b>{body}</div>""",
        unsafe_allow_html=True,
    )


def chips(items, color):
    html = "".join(
        f'<span class="chip" style="--chipbg:{_soft(color)};--chipfg:{color};'
        f'--chipfg33:{color}44">{it}</span>'
        for it in items
    )
    st.markdown(html, unsafe_allow_html=True)


def eqcap(text):
    st.markdown(f'<div class="eqcap">{text}</div>', unsafe_allow_html=True)


def dev_footer():
    st.markdown(
        """<div class="devfoot">
        Developed by <b>Dr Merwan Roudane</b> &nbsp;·&nbsp;
        author of the <b>xt*</b> panel structural-break Stata suite &nbsp;·&nbsp;
        ideas.repec.org/f/pro1421 &nbsp;·&nbsp; github.com/merwanroudane
        </div>""",
        unsafe_allow_html=True,
    )


def base_layout(fig, height=380, title=None):
    """Apply a clean light template to a plotly figure."""
    fig.update_layout(
        template="plotly_white",
        height=height,
        title=title,
        margin=dict(l=48, r=24, t=48 if title else 24, b=44),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#1F2733", size=13),
        legend=dict(bgcolor="rgba(255,255,255,.6)", bordercolor="#E6E9F2", borderwidth=1),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#EEF1F7", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEF1F7", zeroline=False)
    return fig


def show(fig, **kw):
    # width="stretch" is the modern replacement for use_container_width=True;
    # fall back gracefully on older Streamlit builds.
    try:
        st.plotly_chart(base_layout(fig, **kw), width="stretch")
    except TypeError:
        st.plotly_chart(base_layout(fig, **kw), use_container_width=True)


def sidebar_brand():
    with st.sidebar:
        st.markdown(
            """<div style="padding:6px 2px 14px;border-bottom:1px solid #E6E9F2;margin-bottom:10px">
            <div style="font-weight:800;font-size:1.02rem;color:#1F2733">☀ Panel Breaks</div>
            <div style="font-size:.78rem;color:#8A97A6">A researcher's guide</div>
            <div style="font-size:.72rem;color:#8A97A6;margin-top:6px">
            by <b>Dr Merwan Roudane</b></div>
            </div>""",
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------
# small color helpers
# ----------------------------------------------------------------------
def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))


def _shift(color, f=0.82):
    r, g, b = _hex(color)
    return f"rgb({int(r*f)},{int(g*f)},{int(b*f)})"


def _soft(color, a=0.10):
    r, g, b = _hex(color)
    return f"rgba({r},{g},{b},{a})"


# reproducible RNG for illustrations
def rng(seed=7):
    return np.random.default_rng(seed)
