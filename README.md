# S2L Navigator

A config-driven Streamlit app that acts as the central navigation hub for S2Labs
projects, teams, tools, architecture, roadmap, and hardware.

Everything is **data-driven** — edit the YAML files in `config/` to add projects,
links, diagrams, roadmap items, or hardware without changing code.

## Structure

```
app.py                 Home / landing
pages/                 Projects, Architecture, Roadmap, Hardware & Infra
config/                All editable data (domains, infrastructure, hardware, roadmap, architecture, app/brand)
lib/                   data loading + theming + Mermaid helpers
Graphics/              Logos
.streamlit/config.toml Brand theme
```

## Run

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Editing content

- **Add a project / Teams link** → `config/domains.yaml`
- **Add an architecture diagram** → `config/architecture.yaml` (Mermaid)
- **Update the roadmap** → `config/roadmap.yaml`
- **Hardware / infrastructure** → `config/hardware.yaml`, `config/infrastructure.yaml`
- **Brand colors / logos** → `config/app.yaml` and `.streamlit/config.toml`

## Notes

- Mermaid diagrams render via the mermaid.js CDN; if the deployment network blocks
  CDNs, vendor the script locally and update `lib/theme.py`.
- SSO (Entra ID) and M365 email integration are planned shared services — not yet wired in.
