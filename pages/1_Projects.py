"""Projects navigator — browse domains, areas, projects & links; with search."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from lib import data
from lib.theme import page_setup

cfg = page_setup("Projects", icon="🗂️")
link_types = cfg.get("link_types", {})

st.title("🗂️ Projects & Teams")
st.caption("Browse by domain or search across every project and resource.")

query = st.text_input("Search projects, areas, codenames, tags", placeholder="e.g. frac, Argus, BoP, telemetry")


def link_chip(link: dict) -> str:
    meta = link_types.get(link.get("type", "other"), link_types.get("other", {}))
    icon = meta.get("icon", "🔗")
    label = link.get("label") or meta.get("label", "Link")
    return f'<a class="s2l-chip" href="{link["url"]}" target="_blank">{icon} {label}</a>'


def project_card(domain_icon: str, domain: str, area: str, proj: dict) -> None:
    title = proj["name"]
    meta_bits = []
    if proj.get("codename"):
        meta_bits.append(f"codename: {proj['codename']}")
    if proj.get("number"):
        meta_bits.append(f"#{proj['number']}")
    meta = f" · {' · '.join(meta_bits)}" if meta_bits else ""
    tags = "".join(f'<span class="s2l-pill">{t}</span>' for t in proj.get("tags", []) or [])
    links = proj.get("links", []) or []
    links_html = "".join(link_chip(l) for l in links) if links else '<span class="s2l-sub">No links yet</span>'
    st.markdown(
        f"""
        <div class="s2l-card">
          <h4>{title}<span class="s2l-sub">{meta}</span></h4>
          <div class="s2l-sub">{domain_icon} {domain} › {area}</div>
          <div style="margin:.35rem 0 .5rem 0;">{proj.get('summary', '')}</div>
          <div>{links_html}</div>
          <div style="margin-top:.4rem;">{tags}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


if query:
    q = query.lower()
    rows = data.iter_projects()
    hits = []
    for r in rows:
        p = r["project"]
        haystack = " ".join(
            [
                p.get("name", ""),
                p.get("codename", ""),
                str(p.get("number", "")),
                p.get("summary", ""),
                r["domain"],
                r["area"],
                " ".join(p.get("tags", []) or []),
            ]
        ).lower()
        if q in haystack:
            hits.append(r)
    st.write(f"**{len(hits)}** match(es)")
    for r in hits:
        project_card(r["domain_icon"], r["domain"], r["area"], r["project"])
else:
    for dom in data.domains():
        with st.expander(f"{dom.get('icon', '')} {dom['name']} — {dom.get('summary', '')}", expanded=False):
            for area in dom.get("areas", []):
                st.markdown(f"**{area['name']}**")
                for proj in area.get("projects", []):
                    project_card(dom.get("icon", ""), dom["name"], area["name"], proj)
