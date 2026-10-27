"""Edge Device Deployment — explains the s2labs-edge-device-deploy project."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from lib import data
from lib.theme import mermaid, page_setup, table

page_setup("Edge Deployment", icon="📦")

ed = data.edge_deploy()

st.title("📦 Edge Device Deployment")
st.caption(f"Project: {ed.get('repo', '')} · v{ed.get('version', '')}")
st.write(ed.get("summary", ""))

st.divider()

st.subheader("Three-Phase Workflow")
for ph in ed.get("workflow", []):
    st.markdown(
        f"""
        <div class="s2l-card">
          <h4>{ph['phase']} <span class="s2l-sub">· {ph['role']}</span></h4>
          <div class="s2l-sub">{ph['detail']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with st.expander("View workflow diagram"):
    diagram = next((d for d in data.architecture() if d["id"] == "deploy_workflow"), None)
    if diagram:
        mermaid(diagram["mermaid"], height=420)

st.divider()

col1, col2 = st.columns(2)
with col1:
    st.subheader("Supported Platforms")
    table(
        [
            {"Platform": p["name"], "OS": p["os"], "Packaging": p["pkg"], "Status": p["status"]}
            for p in ed.get("platforms", [])
        ]
    )
with col2:
    st.subheader("Provisioned Services")
    for s in ed.get("services", []):
        st.markdown(f"- **{s['name']}** — {s['summary']}")
    st.subheader("Hardware Options")
    for h in ed.get("hardware_options", []):
        st.markdown(f"- {h}")

st.divider()

st.subheader("Package Repositories")
for r in ed.get("repositories", []):
    st.markdown(f"- **{r['kind']}** — {r['detail']}")

st.subheader("Conventions & Rules")
for c in ed.get("conventions", []):
    st.markdown(f"- {c}")
