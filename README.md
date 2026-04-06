# CSA Plugins for Claude Code

A curated directory of Cloud Security Alliance plugins for Claude Code.

> **Warning:** Make sure you trust a plugin before installing, updating, or using it. CSA does not control what MCP servers, files, or other software are included in external plugins and cannot verify that they will work as intended or that they won't change. See each plugin's homepage for more information.

## Structure

- **`/plugins`** - Internal plugins developed and maintained by CSA
- **`/external_plugins`** - Third-party plugins from partners and the community

## Available Plugins

| Plugin | Description | Install |
|--------|-------------|---------|
| [incident-analysis](plugins/incident-analysis/) | Comprehensive security incident analysis with OSINT collection, source cross-referencing, confidence classification, and deep analysis. | `/plugin install incident-analysis@csa-plugins-official` |
| [cwe-analysis](plugins/cwe-analysis/) | CWE assignment and vulnerability chain analysis for CNAs, security researchers, and vendors. | `/plugin install cwe-analysis@csa-plugins-official` |
| [security-knowledge-ingestion](plugins/security-knowledge-ingestion/) | Ingest security knowledge documents into structured data with reproducible recipes and SecID integration. | `/plugin install security-knowledge-ingestion@csa-plugins-official` |

## Installation

First, add the CSA marketplace:

```
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
```

Then install any plugin:

```
/plugin install {plugin-name}@csa-plugins-official
```

Or browse for plugins in `/plugin > Discover`

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
