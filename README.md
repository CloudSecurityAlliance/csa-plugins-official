# CSA Plugins for Claude

Free add-ons from the [Cloud Security Alliance](https://cloudsecurityalliance.org) (CSA) that give Claude new
security skills. Each plugin teaches Claude a method that CSA's researchers use, such as investigating a security
incident, classifying a vulnerability, or scoring a security questionnaire.

You install a plugin once. After that, describe what you need in plain English, and Claude uses the plugin when it
fits.

**On this page**

- [Install](#install)
- [Available plugins](#available-plugins)
- [Things to know before you start](#things-to-know-before-you-start)
- [Keep plugins up to date](#keep-plugins-up-to-date)
- [Get help or report a problem](#get-help-or-report-a-problem)
- [Using another AI assistant](#using-another-ai-assistant)
- [For developers and contributors](#for-developers-and-contributors)

## Install

### In Claude Code (two steps)

**Step 1. Add the CSA plugin marketplace.** You only do this once. Type this into Claude Code:

```text
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
```

**Step 2. Install a plugin.** Copy its install command from the [list of plugins](#available-plugins). For example:

```text
/plugin install cwe-analysis@csa-plugins-official
```

Claude Code shows what the plugin adds and asks where to install it. Choose **Install for you (user scope)** to have
the plugin in every project.

**Check that it worked.** Type `/` and look for the plugin's name in the list. You can also run `/plugin` and open the
**Installed** tab.

To browse instead, run `/plugin` and open the **Discover** tab. It lists every plugin from the marketplaces you have
added.

Plugins you install in the terminal also work in the Claude desktop app's **Code** tab and in VS Code on the same
computer.

### In the Claude app (claude.ai or desktop)

1. Open [Customize > Plugins](https://claude.ai/customize/plugins).
2. Select **Add**, then **Add marketplace**.
3. Enter `CloudSecurityAlliance/csa-plugins-official`.
4. Find the plugin you want and select **Add**.

On Team and Enterprise plans, your organization's Owner decides whether members can add marketplaces. If you don't see
**Add marketplace**, ask your Owner.

Plugins you add here are saved to your Claude account. They also appear in Claude Code when you sign in with the same
account.

### Using a plugin

Ask for what you need. For example:

- "Help me pick the right CWE for this bug report."
- "Investigate this cloud security incident and build a timeline: (paste a link to a news report)"
- "Map NIST CSF 2.0 to ISO 27001 and tell me where they differ."
- "Score this completed AI-CAIQ questionnaire."

To choose a plugin yourself, type `/` and pick it from the list. Plugin entries look like `plugin-name:skill-name`,
for example `/cwe-analysis:cwe-analysis`.

## Available plugins

Most plugins need nothing else once installed. The three that do are covered in
[Things to know before you start](#things-to-know-before-you-start).

| Plugin | Install command | What it does |
|--------|-----------------|--------------|
| [incident-analysis](plugins/incident-analysis/) | `/plugin install incident-analysis@csa-plugins-official` | Investigates a cloud or AI security incident from public reports. It gathers sources, checks how far each one can be trusted, builds a timeline, and writes a report with lessons learned and recommended defenses. |
| [cwe-analysis](plugins/cwe-analysis/) | `/plugin install cwe-analysis@csa-plugins-official` | Works out which type of weakness is behind a vulnerability, using MITRE's Common Weakness Enumeration (CWE), and explains why. Built for people who publish vulnerability records, security researchers, and software vendors. |
| [cve-analysis](plugins/cve-analysis/) | `/plugin install cve-analysis@csa-plugins-official` | Studies the whole public list of known vulnerabilities (CVE records) at once. It answers questions such as "Is the number of CVEs really growing?" and "Is the data getting better?" Needs setup first. |
| [security-knowledge-ingestion](plugins/security-knowledge-ingestion/) | `/plugin install security-knowledge-ingestion@csa-plugins-official` | Turns a security standard, regulation, or framework into structured data that you can search, compare, and reuse. It first checks whether [SecID](https://secid.cloudsecurityalliance.org/) already has that data. |
| [nist-ir-8477-mapping](plugins/nist-ir-8477-mapping/) | `/plugin install nist-ir-8477-mapping@csa-plugins-official` | Maps how two security frameworks or standards relate, for example which controls in one cover which controls in the other. It follows NIST's published mapping method (NIST IR 8477) and exports to Excel or to NIST's own format. |
| [secid](plugins/secid/) | `/plugin install secid@csa-plugins-official` | Looks up security identifiers, such as a CVE, a CWE, a MITRE ATT&CK technique, or a NIST control, across more than 700 sources, and links you to each one. Needs two Python packages first. |
| [vulnerability-audit](plugins/vulnerability-audit/) | `/plugin install vulnerability-audit@csa-plugins-official` | Reviews source code for security vulnerabilities, step by step. It challenges every finding to weed out false alarms, and helps you report real ones responsibly to the maintainers. Also installs `secid` and `cwe-analysis`, so it needs secid's Python packages too. |
| [valid-ai-ted-scorer](plugins/valid-ai-ted-scorer/) | `/plugin install valid-ai-ted-scorer@csa-plugins-official` | Scores a completed CSA security questionnaire (CAIQ or AI-CAIQ) question by question, and produces a scored spreadsheet and a summary PDF. The result is an informational, AI-assisted assessment, not a CSA certification. |

## Things to know before you start

### secid needs two Python packages

The secid plugin runs a small program on your computer. Install its two Python packages once:

```bash
python3 -m pip install mcp httpx
```

You need these for `vulnerability-audit` too, because it installs secid for you.

**If you only want secid, you can skip the install.** Connect Claude to SecID's hosted service instead: add
`https://secid.cloudsecurityalliance.org/mcp` as a remote MCP server (in the Claude app, a custom connector). It gives
the same results. The [secid README](plugins/secid/README.md) has the details.

### cve-analysis needs Python and a copy of the CVE list

- **Python 3.11 or later, with pandas:** `python3 -m pip install pandas`
- **A copy of the CVE list,** about 2 GB:
  `git clone --depth 1 https://github.com/CVEProject/cvelistV5.git`
- **Time:** each pass over the data takes about six minutes.

### valid-ai-ted-scorer is informational only

It assesses what was written in a questionnaire. It does not check that any control is in place, and it is not a CSA
certification, audit, or STAR Registry listing. Read its [known issues](plugins/valid-ai-ted-scorer/README.md#known-issues)
first. Its README also explains where your questionnaire data goes.

### Is it safe to install?

Plugins can run programs on your computer, so install only plugins you trust. Every plugin listed here is written and
maintained by CSA, and its full source is public in this repository. Before anything is installed, Claude Code shows
you what the plugin adds.

This marketplace may list third-party plugins in future. CSA does not control what those contain, so check each one's
homepage before you install it.

## Keep plugins up to date

Claude Code does not update plugins from this marketplace automatically unless you turn that on:

1. Run `/plugin`.
2. Open the **Marketplaces** tab and select `csa-plugins-official`.
3. Choose **Enable auto-update**. To update right away instead, choose **Update marketplace**.

In the Claude app, go to [Customize > Plugins](https://claude.ai/customize/plugins) and select **Check for updates**,
or turn on **Sync automatically**.

**To remove a plugin:** in Claude Code, run `/plugin`, open the **Installed** tab, select the plugin, and choose
**Uninstall**. In the Claude app, open the plugin, open its menu, and select **Remove**.

## Get help or report a problem

[Open an issue on GitHub](https://github.com/CloudSecurityAlliance/csa-plugins-official/issues/new). Start the title
with the plugin's name in square brackets, for example: `[cwe-analysis] Suggested the wrong CWE for a buffer overflow`.
Tell us what happened and what you expected to happen.

If something felt confusing, that is worth reporting too. If you disagree with how a plugin does its analysis, report
that as well: we treat a disagreement about method the same as a bug.

## Using another AI assistant

The plugins are built on the open `SKILL.md` format, so their methods work in other AI assistants too. Only Claude
gets the one-step marketplace install.

Outside Claude Code you get the method but not the tooling. Bundled scripts, referenced as
`${CLAUDE_PLUGIN_ROOT}/scripts/...`, won't run, and you have to connect the secid server to your assistant yourself.

**Codex CLI:** clone this repository, then link the skills into `~/.agents/skills/`. Codex needs each skill to sit
directly inside that folder, and it follows links.

```bash
git clone https://github.com/CloudSecurityAlliance/csa-plugins-official.git
mkdir -p ~/.agents/skills && ln -s "$PWD"/csa-plugins-official/plugins/*/skills/*/ ~/.agents/skills/
```

**Gemini CLI:** clone the repository as above, then link each skill you want, for example
`/skills link <repo>/plugins/cwe-analysis/skills/cwe-analysis --scope user`. Check with `/skills list`.

**ChatGPT (desktop or web):** zip a single skill folder, for example
`plugins/cwe-analysis/skills/cwe-analysis/`, and upload it under **Skills > Create > Upload from your computer**.
Personal skills need a Business, Enterprise, Edu, or Healthcare plan, and the desktop and web apps don't share
skills.

---

## For developers and contributors

### How this repository is organized

- **`plugins/`** holds the plugins that CSA writes and maintains, one folder each.
- **`external_plugins/`** is for third-party plugins. There are none yet.
- **`.claude-plugin/marketplace.json`** is the list of plugins that Claude reads when someone adds this marketplace.

Each plugin uses the standard Claude Code plugin layout:

```text
plugin-name/
├── .claude-plugin/
│   └── plugin.json      # name, version, description (required)
├── .mcp.json            # MCP server configuration (optional)
├── skills/              # skills (optional)
├── commands/            # slash commands (optional)
├── agents/              # agent definitions (optional)
├── scripts/             # helper scripts (optional)
├── README.md
├── FEEDBACK.md
└── LICENSE
```

[`CLAUDE.md`](CLAUDE.md) covers the conventions, how to run each plugin's tests, and the checklist for adding a
plugin.

### Contributing

Internal plugins are developed by CSA team members. The process for submitting a third-party plugin is still to be
decided. It will include an automated review and approval step.

### Where these plugins come from

Some plugins here, such as `cwe-analysis`, `cve-analysis`, and `vulnerability-audit`, come out of CSA's internal
research programs on CVE assignment, CWE submissions, vulnerability scoring (CVSS and AIVSS), CVE enrichment, CVE
corpus analysis, and AI-supported CNA operations. Those internal repositories remain the source of truth for each
method. The plugins here are their public, distilled form, and each plugin's README names its source. More plugins
may appear here as that work matures.

To collaborate or learn more, contact
[kseifried@cloudsecurityalliance.org](mailto:kseifried@cloudsecurityalliance.org).

### Licensing

The plugins here are **not all under the same licence**. A folder's own `LICENSE` file governs that folder.
[`LICENSING.md`](LICENSING.md) maps which licence applies where, and explains why no licence here covers the CSA name
or logo.
