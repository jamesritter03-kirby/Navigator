"""Roadmap — grouped by period for the monthly IT meeting."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from lib import data
from lib.theme import mermaid, page_setup

page_setup("Roadmap", icon="🗺️")

STATUS = {
    "done": ("✅", "#6CBE6C"),
    "in-progress": ("🔄", "#24409A"),
    "planned": ("🗓️", "#6E7B8B"),
}

st.title("🗺️ Roadmap")
st.caption("Defined in config/roadmap.yaml. Use for the monthly IT review.")


def _render_track(periods: list) -> None:
    if not periods:
        st.info("No roadmap items defined yet for this track.")
        return
    timeline_lines = ["timeline", "    title S2L Roadmap"]
    for block in periods:
        titles = " : ".join(item["title"] for item in block.get("items", []))
        timeline_lines.append(f"    {block['period']} : {titles}")
    mermaid("\n".join(timeline_lines), height=360)

    st.divider()

    for block in periods:
        st.subheader(block["period"])
        for item in block.get("items", []):
            icon, color = STATUS.get(item.get("status", "planned"), ("•", "#6E7B8B"))
            owner = f" · owner: {item['owner']}" if item.get("owner") else ""
            st.markdown(
                f"""
                <div class="s2l-card" style="border-left-color:{color};">
                  <h4>{icon} {item['title']}
                    <span class="s2l-sub">({item.get('status', 'planned')}{owner})</span>
                  </h4>
                  <div class="s2l-sub">{item.get('detail', '')}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


rm = data.roadmap()
tab_edge, tab_roc = st.tabs(["Edge Platform", "Remote Ops Center"])
with tab_edge:
    _render_track(rm.get("edge", []))
with tab_roc:
    _render_track(rm.get("roc", []))
