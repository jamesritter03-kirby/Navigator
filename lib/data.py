"""Data loading helpers for the S2L Navigator (config-driven)."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
ROOT_DIR = Path(__file__).resolve().parent.parent


def _load(name: str) -> dict[str, Any]:
    # Read fresh each call so YAML edits reflect on the next rerun (no restart needed).
    path = CONFIG_DIR / name
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def app_config() -> dict[str, Any]:
    return _load("app.yaml")


def domains() -> list[dict[str, Any]]:
    return _load("domains.yaml").get("domains", [])


def infrastructure() -> dict[str, Any]:
    return _load("infrastructure.yaml")


def hardware() -> dict[str, Any]:
    return _load("hardware.yaml")


def roadmap() -> dict[str, Any]:
    return _load("roadmap.yaml").get("roadmap", {})


def architecture() -> list[dict[str, Any]]:
    return _load("architecture.yaml").get("diagrams", [])


def edge_deploy() -> dict[str, Any]:
    return _load("edge_deploy.yaml").get("edge_deploy", {})


def features() -> list[dict[str, Any]]:
    return _load("features.yaml").get("features", [])


def asset_path(relative: str) -> Path:
    """Resolve a repo-relative asset path (e.g. a logo) to an absolute path."""
    return ROOT_DIR / relative


def iter_projects() -> list[dict[str, Any]]:
    """Flatten every project with its domain/area context for search."""
    rows: list[dict[str, Any]] = []
    for dom in domains():
        for area in dom.get("areas", []):
            for proj in area.get("projects", []):
                rows.append(
                    {
                        "domain": dom.get("name", ""),
                        "domain_icon": dom.get("icon", ""),
                        "area": area.get("name", ""),
                        "project": proj,
                    }
                )
    return rows
