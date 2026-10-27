"""Shared UI helpers: branding, theming (light/dark), and Mermaid rendering."""
from __future__ import annotations

import html
import json
import uuid
from typing import Any

import streamlit as st
import streamlit.components.v1 as components

from lib import data

# Source of truth for the theme. A plain (non-widget) session_state key reliably
# survives page navigation, unlike widget-key state which can be dropped on switch.
_THEME_KEY = "theme_dark"


def is_dark() -> bool:
    """Whether dark mode is currently active (for picking theme-aware assets)."""
    return bool(st.session_state.get(_THEME_KEY, False))


def _sync_theme() -> None:
    st.session_state[_THEME_KEY] = st.session_state["ui_theme_toggle"]


def _palette(brand: dict[str, str], dark: bool) -> dict[str, str]:
    """Resolve the active color palette for the current mode."""
    if dark:
        return {
            "blue": brand["blue"],
            "green": brand["green"],
            "gray": "#9AA7B8",
            "ink": "#E8ECF3",
            "surface": "#1C2230",
            "bg": "#11151F",
            "card": "#1A2030",
            "border": "#2A3346",
            "mermaid": "dark",
        }
    return {
        "blue": brand["blue"],
        "green": brand["green"],
        "gray": brand["gray"],
        "ink": brand["ink"],
        "surface": brand["surface"],
        "bg": "#FFFFFF",
        "card": "#FFFFFF",
        "border": "#E3E8F0",
        "mermaid": "default",
    }


def page_setup(title: str, icon: str = "🧭") -> dict[str, Any]:
    """Configure the page, render the theme toggle, inject brand CSS, return config."""
    cfg = data.app_config()
    st.set_page_config(
        page_title=f"{cfg['app']['name']} · {title}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.session_state.setdefault(_THEME_KEY, False)
    # Mirror the persistent value into the widget key before it renders, so the
    # toggle (and logo) stay correct even if widget state was dropped on page switch.
    st.session_state["ui_theme_toggle"] = st.session_state[_THEME_KEY]
    dark = st.session_state[_THEME_KEY]
    _sidebar_brand(cfg, dark)
    st.sidebar.toggle("🌙 Dark mode", key="ui_theme_toggle", on_change=_sync_theme)
    dark = st.session_state[_THEME_KEY]

    pal = _palette(cfg["brand"], dark)
    st.session_state["_mermaid_theme"] = pal["mermaid"]
    st.session_state["_mermaid_bg"] = pal["bg"]
    _inject_css(pal)
    return cfg


def _inject_css(pal: dict[str, str]) -> None:
    st.markdown(
        f"""
        <style>
        :root {{
            --s2l-blue: {pal['blue']};
            --s2l-green: {pal['green']};
            --s2l-gray: {pal['gray']};
        }}
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{
            background: {pal['bg']};
        }}
        [data-testid="stSidebar"] {{ background: {pal['surface']}; }}
        [data-testid="stAppViewContainer"], [data-testid="stSidebar"],
        .stMarkdown, p, span, li, label, h1, h2, h3, h4, h5, h6 {{
            color: {pal['ink']};
        }}
        a {{ color: {pal['blue']}; }}
        .s2l-card {{
            border: 1px solid {pal['border']};
            border-left: 4px solid {pal['blue']};
            border-radius: 10px;
            padding: 0.9rem 1.1rem;
            margin-bottom: 0.75rem;
            background: {pal['card']};
            box-shadow: 0 1px 2px rgba(0,0,0,0.08);
        }}
        .s2l-card h4 {{ margin: 0 0 0.25rem 0; color: {pal['ink']}; }}
        .s2l-card .s2l-sub {{ color: {pal['gray']}; font-size: 0.85rem; }}
        .s2l-sub {{ color: {pal['gray']}; }}
        .s2l-pill {{
            display: inline-block; padding: 1px 8px; margin: 2px 4px 2px 0;
            border-radius: 999px; font-size: 0.72rem; background: {pal['surface']};
            color: {pal['gray']}; border: 1px solid {pal['border']};
        }}
        .s2l-chip {{
            display: inline-block; padding: 2px 10px; margin: 2px 6px 2px 0;
            border-radius: 6px; font-size: 0.8rem; font-weight: 600;
            background: {pal['green']}; color: #0A2A0A; text-decoration: none;
        }}
        .s2l-chip:hover {{ filter: brightness(0.95); }}
        .s2l-table {{
            width: 100%; border-collapse: collapse; font-size: 0.86rem;
            margin-bottom: 0.75rem;
        }}
        .s2l-table th {{
            text-align: left; background: {pal['surface']}; color: {pal['ink']};
            border: 1px solid {pal['border']}; padding: 6px 10px; font-weight: 600;
        }}
        .s2l-table td {{
            border: 1px solid {pal['border']}; padding: 6px 10px; color: {pal['ink']};
        }}
        .s2l-table tr:nth-child(even) td {{ background: {pal['surface']}; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def _sidebar_brand(cfg: dict[str, Any], dark: bool = False) -> None:
    key = "logo_stacked_dark" if dark else "logo_stacked"
    logo = data.asset_path(cfg["app"].get(key, cfg["app"]["logo_stacked"]))
    if logo.exists():
        st.sidebar.image(str(logo), width="stretch")
    st.sidebar.caption(cfg["app"]["tagline"])


def table(rows: list[dict[str, Any]]) -> None:
    """Render a list of dicts as a theme-aware HTML table (respects light/dark)."""
    if not rows:
        st.caption("No data.")
        return
    headers = list(rows[0].keys())
    thead = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(r.get(h, '')))}</td>" for h in headers) + "</tr>"
        for r in rows
    )
    st.markdown(
        f'<table class="s2l-table"><thead><tr>{thead}</tr></thead><tbody>{body}</tbody></table>',
        unsafe_allow_html=True,
    )


def mermaid(code: str, height: int = 520) -> None:
    """Render a Mermaid diagram via the CDN-hosted mermaid.js runtime."""
    theme = st.session_state.get("_mermaid_theme", "default")
    bg = st.session_state.get("_mermaid_bg", "#FFFFFF")
    uid = f"m{uuid.uuid4().hex}"
    payload = json.dumps(code)
    html = f"""
    <div id="{uid}-wrap" style="width:100%;overflow:auto;background:{bg};">
      <pre id="{uid}" class="mermaid" style="text-align:center;background:{bg};"></pre>
    </div>
    <div id="{uid}-err" style="color:#c0392b;font-family:monospace;font-size:12px;"></div>
    <script type="module">
      try {{
        const mermaid = (await import('https://cdn.jsdelivr.net/npm/mermaid@11.6.0/dist/mermaid.esm.min.mjs')).default;
        mermaid.initialize({{ startOnLoad: false, theme: '{theme}', securityLevel: 'loose' }});
        const el = document.getElementById('{uid}');
        const code = {payload};
        let done = false;
        async function render() {{
          // Skip while the container is hidden/zero-width (e.g. inside an inactive tab);
          // rendering then would produce NaN layout and an error diagram.
          if (done || document.body.clientWidth === 0) return;
          done = true;
          el.textContent = code;
          await mermaid.run({{ nodes: [el] }});
        }}
        await render();
        if (!done) {{
          const ro = new ResizeObserver(() => render().then(() => {{ if (done) ro.disconnect(); }}));
          ro.observe(document.body);
        }}
      }} catch (e) {{
        document.getElementById('{uid}-err').textContent =
          'Mermaid failed to render: ' + e;
      }}
    </script>
    """
    components.html(html, height=height, scrolling=True)
