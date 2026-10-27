"""S2L Navigator — home / landing page."""
from __future__ import annotations

import streamlit as st

from lib import data
from lib.theme import is_dark, page_setup

cfg = page_setup("Home", icon="🧭")

logo_key = "logo_horizontal_dark" if is_dark() else "logo_horizontal"
logo = data.asset_path(cfg["app"].get(logo_key, cfg["app"]["logo_horizontal"]))
col_logo, col_title = st.columns([1, 2], vertical_alignment="center")
with col_logo:
    if logo.exists():
        st.image(str(logo), width="stretch")
with col_title:
    st.title(cfg["app"]["name"])
    st.write(cfg["app"]["tagline"])

st.divider()

# Quick metrics
doms = data.domains()
projects = data.iter_projects()
links = sum(len(r["project"].get("links", []) or []) for r in projects)
m1, m2, m3 = st.columns(3)
m1.metric("Domains", len(doms))
m2.metric("Projects", len(projects))
m3.metric("Linked resources", links)

st.subheader("Jump to")
nav = [
    ("🗂️ Projects", "Browse domains, areas & teams", "pages/1_Projects.py"),
    ("🏛️ Architecture", "Diagrams for IT reviews", "pages/2_Architecture.py"),
    ("🗺️ Roadmap", "Monthly IT meeting view", "pages/3_Roadmap.py"),
    ("🖥️ Hardware & Infra", "Edge devices & services", "pages/4_Hardware.py"),
    ("📦 Edge Deployment", "Build & provisioning pipeline", "pages/5_Edge_Deploy.py"),
]
cols = st.columns(len(nav))
for col, (label, desc, target) in zip(cols, nav):
    with col:
        st.markdown(f"**{label}**")
        st.caption(desc)
        st.page_link(target, label="Open", icon="➡️")

st.divider()

st.subheader("Domains at a glance")
grid = st.columns(3)
for i, dom in enumerate(doms):
    with grid[i % 3]:
        area_count = len(dom.get("areas", []))
        proj_count = sum(len(a.get("projects", [])) for a in dom.get("areas", []))
        st.markdown(
            f"""
            <div class="s2l-card">
              <h4>{dom.get('icon', '')} {dom['name']}</h4>
              <div class="s2l-sub">{dom.get('summary', '')}</div>
              <div style="margin-top:.4rem;">
                <span class="s2l-pill">{area_count} areas</span>
                <span class="s2l-pill">{proj_count} projects</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
