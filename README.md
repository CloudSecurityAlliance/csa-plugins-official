# CSA Plugins for Claude Code

A curated directory of Cloud Security Alliance plugins for Claude Code.

> **Warning:** Make sure you trust a plugin before installing, updating, or using it. CSA does not control what MCP servers, files, or other software are included in external plugins and cannot verify that they will work as intended or that they won't change. See each plugin's homepage for more information.

## Install

These plugins are built on the open `SKILL.md` format, so the analytical workflows run on any agent that reads it — but only Claude gets one-click marketplace installs.

**Claude Code** — `/plugin marketplace add CloudSecurityAlliance/csa-plugins-official`, then `/plugin install {plugin-name}@csa-plugins-official`. Or browse `/plugin` → Discover.

**Claude desktop/web** — Customize → Plugins → + → Add marketplace → Add from a repository → paste `CloudSecurityAlliance/csa-plugins-official` → Browse plugins → Install. No GitHub account needed (public repo); requires a paid Claude plan.

**Codex CLI** — clone, then symlink the skills into `~/.agents/skills/` (Codex needs each skill to be a direct child of that directory, and it follows symlinks):

```bash
git clone https://github.com/CloudSecurityAlliance/csa-plugins-official.git
mkdir -p ~/.agents/skills && ln -s "$PWD"/csa-plugins-official/plugins/*/skills/*/ ~/.agents/skills/
```

**Gemini CLI** — clone as above, then link each skill you want: `/skills link <repo>/plugins/cwe-analysis/skills/cwe-analysis --scope user`. Check with `/skills list`.

**ChatGPT desktop/web** — zip a single skill folder (e.g. `plugins/cwe-analysis/skills/cwe-analysis/`) and upload it via Skills → Create → Upload from your computer. Personal Skills require a Business, Enterprise, Edu, or Healthcare plan, and desktop and web don't sync skills.

Outside Claude Code you get the methodology but not the tooling: bundled scripts referenced as `${CLAUDE_PLUGIN_ROOT}/scripts/...` won't resolve, and the `secid` MCP server has to be wired into your client by hand.

## Structure

- **`/plugins`** - Internal plugins developed and maintained by CSA
- **`/external_plugins`** - Third-party plugins from partners and the community

## Available Plugins

| Plugin | Description | Install |
|--------|-------------|---------|
| [incident-analysis](plugins/incident-analysis/) | Comprehensive security incident analysis with OSINT collection, source cross-referencing, confidence classification, and deep analysis. | `/plugin install incident-analysis@csa-plugins-official` |
| [cwe-analysis](plugins/cwe-analysis/) | CWE assignment and vulnerability chain analysis for CNAs, security researchers, and vendors. | `/plugin install cwe-analysis@csa-plugins-official` |
| [security-knowledge-ingestion](plugins/security-knowledge-ingestion/) | Ingest security knowledge documents into structured data with reproducible recipes and SecID integration. | `/plugin install security-knowledge-ingestion@csa-plugins-official` |
| [nist-ir-8477-mapping](plugins/nist-ir-8477-mapping/) | Map relationships between security knowledge sources using NIST IR 8477 — four relationship styles, use case documentation, cross-model validation. | `/plugin install nist-ir-8477-mapping@csa-plugins-official` |
| [secid](plugins/secid/) | SecID — resolve CVEs, CWEs, ATT&CK techniques, NIST controls, and 700+ security knowledge sources. Local MCP server with internal resolver support. | `/plugin install secid@csa-plugins-official` |
| [vulnerability-audit](plugins/vulnerability-audit/) | AI-driven source-code vulnerability audit: a 5-stage methodology (recon, investigate, validate, disclose, learn) with adversarial false-positive filtering and conservative, cooperative disclosure. | `/plugin install vulnerability-audit@csa-plugins-official` |

## CSA research programs

Some of the plugins here (like `cwe-analysis`) emerge from CSA's
internal research programs in CVE assignment, CWE submissions,
vulnerability scoring (CVSS and AIVSS), CVE enrichment, and
AI-supported CNA operations. Additional plugins may surface here as
that work matures.

If you're interested in collaborating or learning more, contact
[kseifried@cloudsecurityalliance.org](mailto:kseifried@cloudsecurityalliance.org).

## Contributing

### Internal Plugins

Internal plugins are developed by CSA team members.

### External Plugins

To be decided. External plugin submissions will require an automated review and approval process.

## Plugin Structure

Each plugin follows a standard structure:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # Plugin metadata (required)
├── .mcp.json            # MCP server configuration (optional)
├── commands/            # Slash commands (optional)
├── agents/              # Agent definitions (optional)
├── skills/              # Skill definitions (optional)
└── README.md            # Documentation
```

## License

Please see each linked plugin for the relevant LICENSE file.
