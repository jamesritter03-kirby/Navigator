"""Hardware catalog & infrastructure overview."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st

from lib import data
from lib.theme import page_setup, table

page_setup("Hardware & Infra", icon="🖥️")

st.title("🖥️ Hardware & Infrastructure")

tab_hw, tab_infra = st.tabs(["Edge Hardware", "Infrastructure & Apps"])

with tab_hw:
    hw = data.hardware()
    runtime = hw.get("edge_runtime", {})
    st.subheader("Standardized Edge Runtime")
    st.write(runtime.get("summary", ""))
    st.markdown(" ".join(f'<span class="s2l-pill">{s}</span>' for s in runtime.get("stack", [])), unsafe_allow_html=True)

    st.subheader("Edge Compute Models")
    table(
        [
            {
                "Model": d["model"],
                "Arch": d["arch"],
                "OS": d["os"],
                "Package Feed": d["package_feed"],
                "Notes": d.get("notes", ""),
            }
            for d in hw.get("edge_compute", [])
        ]
    )
    datasheets = [d for d in hw.get("edge_compute", []) if d.get("url")]
    if datasheets:
        st.markdown(
            "**Datasheets:** "
            + " · ".join(f"[{d['model']}]({d['url']})" for d in datasheets)
        )

    st.subheader("Remote I/O")
    table([{"Model": d["model"], "Summary": d["summary"]} for d in hw.get("remote_io", [])])

    st.subheader("Networking")
    table(
        [
            {"Component": d["component"], "Type": d["kind"], "Summary": d["summary"]}
            for d in hw.get("networking", [])
        ]
    )

with tab_infra:
    infra = data.infrastructure()

    st.subheader("Shared Platform Services")
    for s in infra.get("shared_services", []):
        st.markdown(
            f'<div class="s2l-card"><h4>{s["name"]} '
            f'<span class="s2l-sub">· {s["kind"]}</span></h4>'
            f'<div class="s2l-sub">{s["summary"]}</div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Azure")
    az = infra.get("azure", {})
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Subscriptions**")
        for sub in az.get("subscriptions", []):
            st.markdown(f"- **{sub['name']}** — {sub['summary']}")
    with c2:
        st.markdown("**Components**")
        for comp in az.get("components", []):
            st.markdown(f"- **{comp['name']}** — {comp['summary']}")

    st.subheader("On-Prem Applications")
    for a in infra.get("on_prem_apps", []):
        st.markdown(
            f'<div class="s2l-card"><h4>{a["name"]} '
            f'<span class="s2l-sub">· {a["kind"]}</span></h4>'
            f'<div class="s2l-sub">{a["summary"]}</div></div>',
            unsafe_allow_html=True,
        )

    st.subheader("Connectivity")
    for c in infra.get("connectivity", []):
        st.markdown(f"- **{c['name']}** — {c['summary']}")

    vms = infra.get("on_prem_vms", {})
    if vms:
        st.subheader("On-Prem VMs")
        st.caption("Naming: hdc + d/q (dev/qa) + s2 + role (doc/ras/web) + NN")
        for env_key, env_label in [("dev", "Dev"), ("qa", "QA")]:
            rows = vms.get(env_key, [])
            if rows:
                st.markdown(f"**{env_label}**")
                table(
                    [
                        {"Host": v.get("host", ""), "IP": v.get("ip", ""), "Role": v.get("role", "")}
                        for v in rows
                    ]
                )
