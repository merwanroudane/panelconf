"""
Shared palette, styling, and ANIMATION helpers for the
"Panel Breaks — Interactive Simulation Lab".

Developer: Dr Merwan Roudane
"""
import streamlit as st
import numpy as np
import plotly.graph_objects as go

PALETTE = {
    "indigo": "#4C6EF5", "blue": "#1C7ED6", "cyan": "#1098AD", "teal": "#0CA678",
    "green": "#37B24D", "lime": "#74B816", "yellow": "#F59F00", "orange": "#F76707",
    "red": "#E03131", "pink": "#E64980", "grape": "#9C36B5", "violet": "#7048E8",
    "gray": "#495057", "ink": "#1F2733", "muted": "#5C6B7A", "soft": "#F5F7FB",
}

TOPIC = {
    "home":     "#E8590C",
    "common":   "#1C7ED6",
    "hetero":   "#F76707",
    "latent":   "#9C36B5",
    "csd":      "#1098AD",
    "fourier":  "#7048E8",
    "regular":  "#37B24D",
    "methods":  "#E64980",
}

UNIT_COLORS = ["#4C6EF5", "#0CA678", "#E64980", "#F76707", "#9C36B5",
               "#1098AD", "#F59F00", "#E03131"]


def inject_css():
    st.markdown(
        """
        <style>
        html, body, [class*="css"] { font-family:'Inter','Segoe UI',system-ui,sans-serif; }
        .block-container { padding-top:2.2rem; padding-bottom:4rem; max-width:1180px; }
        .hero { border-radius:20px; padding:32px 38px; color:#fff; margin-bottom:20px;
                box-shadow:0 14px 40px -18px rgba(200,80,10,.55); }
        .hero h1 { font-size:2.05rem; margin:0 0 .3em; font-weight:800; line-height:1.15; }
        .hero p  { font-size:1.03rem; margin:0; opacity:.96; line-height:1.55; }
        .hero .tag { font-size:.72rem; letter-spacing:.18em; text-transform:uppercase;
                     font-weight:700; opacity:.85; margin-bottom:.8em; }
        .sec { border-left:6px solid var(--acc); padding:.1em 0 .1em 15px; margin:1.5em 0 .4em; }
        .sec h2 { margin:0; font-size:1.4rem; font-weight:800; color:#1F2733; }
        .sec .kick { font-family:ui-monospace,monospace; font-size:.71rem; letter-spacing:.14em;
                     text-transform:uppercase; font-weight:700; color:var(--acc); }
        .card { background:#fff; border:1px solid #E6E9F2; border-left:5px solid var(--acc);
                border-radius:13px; padding:16px 20px; margin:.5em 0;
                box-shadow:0 6px 20px -14px rgba(30,40,60,.35); }
        .card h4 { margin:0 0 .3em; font-size:1rem; font-weight:700; color:#1F2733; }
        .card p  { margin:.15em 0; color:#5C6B7A; font-size:.92rem; line-height:1.55; }
        .call { border-radius:12px; padding:13px 17px; margin:.9em 0; font-size:.94rem;
                border:1px solid var(--acc); background:var(--accsoft); }
        .call b.h { display:block; font-family:ui-monospace,monospace; font-size:.69rem;
                    letter-spacing:.13em; text-transform:uppercase; color:var(--acc);
                    margin-bottom:.25em; }
        .playhint { background:#FFF4E6; border:1px dashed #F76707; border-radius:10px;
                    padding:9px 14px; color:#D9480F; font-size:.88rem; font-weight:600;
                    margin:.5em 0 .9em; }
        .devfoot { margin-top:2.6rem; padding-top:.9rem; border-top:1px solid #E6E9F2;
                   color:#8A97A6; font-size:.8rem; font-family:ui-monospace,monospace; }
        </style>
        """, unsafe_allow_html=True)


def _hex(c):
    c = c.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _shift(color, f=0.82):
    r, g, b = _hex(color)
    return f"rgb({int(r*f)},{int(g*f)},{int(b*f)})"


def _soft(color, a=0.10):
    r, g, b = _hex(color)
    return f"rgba({r},{g},{b},{a})"


def hero(title, subtitle, color, tag="Interactive Simulation Lab"):
    st.markdown(
        f"""<div class="hero" style="background:linear-gradient(120deg,{color} 0%,{_shift(color)} 100%)">
        <div class="tag">{tag}</div><h1>{title}</h1><p>{subtitle}</p></div>""",
        unsafe_allow_html=True)


def section(title, kicker, color):
    st.markdown(f"""<div class="sec" style="--acc:{color}">
        <div class="kick">{kicker}</div><h2>{title}</h2></div>""", unsafe_allow_html=True)


def card(title, body, color):
    st.markdown(f"""<div class="card" style="--acc:{color}">
        <h4>{title}</h4><p>{body}</p></div>""", unsafe_allow_html=True)


def callout(title, body, color):
    st.markdown(f"""<div class="call" style="--acc:{color};--accsoft:{_soft(color)}">
        <b class="h">{title}</b>{body}</div>""", unsafe_allow_html=True)


def play_hint(text="▶ Press PLAY under the chart to start the animation."):
    st.markdown(f'<div class="playhint">{text}</div>', unsafe_allow_html=True)


def dev_footer():
    st.markdown(
        """<div class="devfoot">Developed by <b>Dr Merwan Roudane</b> ·
        author of the <b>xt*</b> panel structural-break Stata suite ·
        ideas.repec.org/f/pro1421 · github.com/merwanroudane</div>""",
        unsafe_allow_html=True)


def sidebar_brand():
    with st.sidebar:
        st.markdown(
            """<div style="padding:6px 2px 14px;border-bottom:1px solid #E6E9F2;margin-bottom:10px">
            <div style="font-weight:800;font-size:1.02rem;color:#1F2733">🎬 Breaks Lab</div>
            <div style="font-size:.78rem;color:#8A97A6">Interactive simulations</div>
            <div style="font-size:.72rem;color:#8A97A6;margin-top:6px">by <b>Dr Merwan Roudane</b></div>
            </div>""", unsafe_allow_html=True)


# ----------------------------------------------------------------------
# ANIMATION HELPERS
# ----------------------------------------------------------------------
def animate(fig, frames, duration=60, slider_prefix="", height=430, title=None,
            slider_labels=None):
    """Attach frames + a Play/Pause button + a slider to a figure."""
    fig.frames = frames
    steps = []
    for i, fr in enumerate(frames):
        lab = slider_labels[i] if slider_labels else fr.name
        steps.append(dict(method="animate", label=lab,
                          args=[[fr.name], {"frame": {"duration": 0, "redraw": True},
                                            "mode": "immediate",
                                            "transition": {"duration": 0}}]))
    fig.update_layout(
        template="plotly_white", height=height, title=title,
        margin=dict(l=50, r=24, t=70 if title else 50, b=90),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, Segoe UI, sans-serif", color="#1F2733", size=13),
        legend=dict(bgcolor="rgba(255,255,255,.65)", bordercolor="#E6E9F2", borderwidth=1),
        updatemenus=[dict(
            type="buttons", direction="left", showactive=False,
            x=0.02, y=-0.16, xanchor="left", yanchor="top",
            pad=dict(t=6, r=6),
            bgcolor="#FFF4E6", bordercolor="#F76707", borderwidth=1.5,
            font=dict(size=13, color="#D9480F"),
            buttons=[
                dict(label="▶  PLAY", method="animate",
                     args=[None, {"frame": {"duration": duration, "redraw": True},
                                  "fromcurrent": True,
                                  "transition": {"duration": 0}}]),
                dict(label="⏸  Pause", method="animate",
                     args=[[None], {"frame": {"duration": 0, "redraw": False},
                                    "mode": "immediate",
                                    "transition": {"duration": 0}}]),
            ])],
        sliders=[dict(active=0, x=0.16, y=-0.16, len=0.82, xanchor="left", yanchor="top",
                      pad=dict(t=6, b=6),
                      currentvalue=dict(prefix=slider_prefix, font=dict(size=13, color="#D9480F"),
                                        visible=True, xanchor="left"),
                      steps=steps)],
    )
    fig.update_xaxes(showgrid=True, gridcolor="#EEF1F7", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="#EEF1F7", zeroline=False)
    return fig


def show(fig):
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


def rng(seed=7):
    return np.random.default_rng(seed)
