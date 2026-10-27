"""Architecture diagrams — rendered from config for IT discussions."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from lib import data
from lib.theme import mermaid, page_setup

page_setup("Architecture", icon="🏛️")

st.title("🏛️ Architecture")

tab_features, tab_edge, tab_roc = st.tabs(
    ["Platform Features", "Edge Architecture", "Remote Ops Center"]
)

with tab_features:
    st.caption("Key capabilities and principles of the S2Labs platform architecture.")
    for group in data.features():
        st.subheader(f"{group.get('icon', '')} {group['category']}")
        cols = st.columns(2)
        for i, item in enumerate(group.get("items", [])):
            with cols[i % 2]:
                st.markdown(
                    f"""
                    <div class="s2l-card">
                      <h4>{item['name']}</h4>
                      <div class="s2l-sub">{item['detail']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def _render_diagrams(area: str, blurb: str) -> None:
    diagrams = [d for d in data.architecture() if d.get("area") == area]
    if not diagrams:
        st.info("No diagrams defined yet for this area.")
        return
    st.caption(blurb)
    labels = [d["title"] for d in diagrams]
    choice = st.radio("Diagram", labels, horizontal=True, key=f"diag_{area}")
    selected = next(d for d in diagrams if d["title"] == choice)

    st.subheader(selected["title"])
    if selected.get("description"):
        st.write(selected["description"])
    mermaid(selected["mermaid"], height=600)

    with st.expander("View Mermaid source"):
        st.code(selected["mermaid"], language="text")


with tab_edge:
    _render_diagrams(
        "edge",
        "Edge-side architecture: the standardized device runtime, configuration-based launcher, "
        "logic authoring tiers, and the deployment pipeline.",
    )

with tab_roc:
    _render_diagrams(
        "roc",
        "Remote Operations Center & cloud-side architecture: telemetry data flow and shared platform services.",
    )
