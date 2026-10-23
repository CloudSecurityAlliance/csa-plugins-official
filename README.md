# CSA Plugins for Claude

Free add-ons from the [Cloud Security Alliance](https://cloudsecurityalliance.org) (CSA) that give your AI assistant
new security skills, each one a method that CSA's researchers use, such as investigating a security incident,
classifying a vulnerability, or scoring a security questionnaire. You install a plugin once and then describe what you
need in plain English. On the command line, we have tested them in Claude Code, and tested installing them in Codex and
Gemini CLI. You can also add them in the Claude app and in ChatGPT; we have checked those steps against the vendors' documentation
but have not yet run the plugins there ourselves.

**On this page**

- [Install in the Claude app](#install-in-the-claude-app-web-or-desktop) (web or desktop)
- [Install in ChatGPT](#install-in-chatgpt-web-or-desktop) (web or desktop)
- [Install from the command line](#install-from-the-command-line): Claude Code, Codex, Gemini CLI
- [Available plugins](#available-plugins)
- [Using a plugin](#using-a-plugin)
- [Setting up your computer](#setting-up-your-computer) (only three plugins need this)
- [Is it safe to install?](#is-it-safe-to-install)
- [Keep plugins up to date](#keep-plugins-up-to-date)
- [Get help or report a problem](#get-help-or-report-a-problem)
- [For developers and contributors](#for-developers-and-contributors)

## Install in the Claude app (web or desktop)

Add the CSA plugin marketplace to Claude once, then add the plugins you want. This works at
[claude.ai](https://claude.ai) and in the Claude desktop app.

> [!NOTE]
> **Who it is for:** anyone on a paid Claude plan. Anthropic says plugins are available on Pro, Max, Team and
> Enterprise.
>
> **Tested?** Not yet in the app. We checked every step below against Anthropic's documentation on 2026-10-23, but
> have not yet run these plugins in the Claude app ourselves. If a step does not match what you see, please
> [tell us](#get-help-or-report-a-problem).
>
> **What you need first:** **Code execution and file creation** turned on. CSA's plugins are made of skills, and
> Anthropic says skills need it. On Pro and Max, turn it on in
> [Settings → Capabilities](https://claude.ai/settings/capabilities). On Team plans it is on by default. On Enterprise,
> an Owner checks it under **Organization settings → Plugins & skills**, on the **Policy** tab.
>
> *Steps verified against Anthropic's [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude)
> and [Plugins](https://claude.com/docs/plugins/overview) documentation on 2026-10-23.* If the menus have moved, follow
> [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude), which has
> screenshots.

### Step 1. Add the CSA marketplace

You only do this once. Anthropic asks you to connect a GitHub account only for a private repository; this one is public.

1. Open [Claude](https://claude.ai) in your browser or in the desktop app, and sign in.
2. Go to **Customize** in the left sidebar, then the **Plugins** tab
   ([direct link](https://claude.ai/customize/plugins)).
3. Select **Add**, then **Add marketplace**.
4. Choose **Add from a repository**.
5. Enter this repository name, then confirm:

```text
CloudSecurityAlliance/csa-plugins-official
```

The CSA plugins now appear on the **Discover** tab, alongside the others. Working in Cowork? Open the **Cowork** tab
first, then **Customize**.

### Step 2. Add a plugin

1. On the **Plugins** tab, open **Discover**.
2. Select the CSA plugin you want. The [list of plugins](#available-plugins) says what each one does.
3. Read what it contains, then select **Add**.

Repeat for each plugin you want. `vulnerability-audit` uses `secid` and `cwe-analysis`: Claude Code adds those two for
you, but we have not confirmed that the app does, so add them yourself.

### Use a plugin in the Claude app

Describe your task in plain English. Claude uses a plugin's skill when the task matches it. For example:

```text
Help me pick the right CWE for this bug report: (paste the report here)
```

To pick a skill yourself, type `/` in the message box, or select **+**. The list shows each skill with the name of the
plugin it came from. Type the plugin's name to narrow the list, then select the skill.
[Using a plugin](#using-a-plugin) has more example requests.

### Good to know (Claude app)

- **Your plugins follow you to Claude Code.** Plugins you add are saved to your Claude account. They sync to Claude
  Code version 2.1.273 or later when you sign in there with the same account, but not when Claude Code signs in with
  an API key or runs through a cloud provider such as Amazon Bedrock.
- **In chat, programs a plugin runs on your computer don't run.** A plugin's skills and commands work in chat. Its
  local programs (local MCP servers), agents and hooks run only in Cowork and Claude Code. This affects two plugins:
  - `secid`, whose lookup server is a local program. In chat, connect SecID's hosted service instead, as
    [Setting up your computer](#step-2-install-the-packages-your-plugin-needs) explains. In Cowork and Claude Code,
    `secid` needs Python on your computer.
  - `vulnerability-audit`, which uses `secid` for its lookups.
- **On Team and Enterprise plans,** an Owner decides whether members can add their own marketplaces, and can limit
  which ones. On Enterprise plans, an admin may also limit which plugins your group sees, or turn off local programs
  entirely.
- **Only add plugins from sources you trust.** Anthropic reviews the plugins in its own directory, but not plugins
  added from a repository like this one. See [Is it safe to install?](#is-it-safe-to-install)
- **Updating and removing:** see [Keep plugins up to date](#keep-plugins-up-to-date). To remove the whole CSA
  marketplace, find it in the **Plugins** section, open the menu button in its right corner, and select **Remove**.

### Troubleshooting (Claude app)

<details>
<summary>I don't see Add marketplace</summary>

- Plugins need a paid plan: Pro, Max, Team or Enterprise.
- On Team and Enterprise, an Owner controls whether members can add their own marketplaces. Ask your Owner.
- If the menus have moved, follow Anthropic's
  [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude), which has
  screenshots.

</details>

<details>
<summary>Claude refuses the repository</summary>

- Check the name: `CloudSecurityAlliance/csa-plugins-official`. The full address,
  `https://github.com/CloudSecurityAlliance/csa-plugins-official`, also works.
- If your organization limits which marketplaces can be added, Claude refuses any it doesn't allow. Ask an Owner
  which sources are permitted.
- You can add up to 25 marketplaces yourself. If you have reached that, remove one you no longer use.

</details>

<details>
<summary>The plugin doesn't appear</summary>

- **In Claude:** look on the **Discover** tab. Plugins are recorded for the organization you are in, so if you belong
  to more than one, check that you are in the right one. On Enterprise plans, an admin may limit which plugins your
  group sees, and a security scan can block a plugin.
- **In Cowork:** plugins load the next time you start a task.
- **In Claude Code:** you need version 2.1.273 or later, signed in with your Claude account. Run `/reload-plugins`, or
  start Claude Code again.

</details>

<details>
<summary>A skill is grayed out</summary>

- **Agents and hooks** run only in Cowork and Claude Code, so chat shows them grayed out. Use Cowork or Claude Code
  for those.
- **If skills are grayed out,** code execution may be off. On Pro and Max, turn on **Code execution and file
  creation** in [Settings → Capabilities](https://claude.ai/settings/capabilities). On Team plans it is on by default.
  On Enterprise, an Owner checks it under **Organization settings → Plugins & skills**, on the **Policy** tab.
- **If you turned the plugin off,** open it in [Customize → Plugins](https://claude.ai/customize/plugins) and turn its
  toggle back on.

</details>

Anthropic's documentation:
[Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) (with screenshots),
[Plugins](https://claude.com/docs/plugins/overview), and
[Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Install in ChatGPT (web or desktop)

> [!NOTE]
> **Who it is for:** ChatGPT Business, Enterprise, Healthcare and Edu workspaces. OpenAI offers skills on those plans,
> and importing a marketplace needs a workspace admin, so neither route below works on Free, Plus or Pro.
>
> **We have not tested these plugins in ChatGPT.** Route B has not been tried with this marketplace at all.
>
> *Steps verified against OpenAI's [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt),
> [Plugins in ChatGPT](https://help.openai.com/en/articles/20001256) and
> [Importing and syncing plugin marketplaces from GitHub](https://help.openai.com/articles/20001504) on 2026-10-23.*
> If the menus have moved, follow those pages. Only *Plugins in ChatGPT* has a screenshot, and it is not of these
> steps.

There are two routes:

- **[Route A](#route-a-upload-a-plugins-skill):** any eligible member uploads one plugin's skill at a time.
- **[Route B](#route-b-an-admin-imports-the-csa-marketplace-not-yet-tested):** a workspace admin imports the whole CSA
  marketplace from GitHub, and members install plugins from the workspace's directory. **Not yet tested.**

### Route A: upload a plugin's skill

**You need:** a Business, Enterprise, Healthcare or Edu plan. In Enterprise and Edu workspaces, your role also needs
the **Enable skills** and **Enable skill uploading** permissions, which an admin sets in
[Permissions & roles](https://chatgpt.com/admin/permissions).

1. Download this repository as a ZIP
   ([direct download](https://github.com/CloudSecurityAlliance/csa-plugins-official/archive/refs/heads/main.zip); on
   the repository's page, it is under **Code** → **Download ZIP**). Unzip it: on a Mac, double-click it; on Windows,
   right-click it and select **Extract All**.
2. In the unzipped folder, find the plugin's skill folder in the [table below](#skill-folders-for-chatgpt), for
   example `plugins/cwe-analysis/skills/cwe-analysis`.
3. Zip that folder itself, not the whole download. On a Mac, Control-click it and choose **Compress**. On Windows,
   right-click it, select **Show more options** if you see it, then **Send to** → **Compressed (zipped) folder**.
4. In ChatGPT, select **Plugins** in the sidebar, open the **Skills** tab, select **Create**, then
   **Upload from your computer**, and choose your zip.
5. Wait for ChatGPT's scan. Most skills are ready straight away. If it says **Needs Review**, read the information
   shown before you use the skill. If it says **Blocked**, ChatGPT won't run it: please
   [tell us](#get-help-or-report-a-problem).

Then describe your task. ChatGPT uses installed skills automatically when they help. To choose one yourself, try an
**@** mention, or select **+** and type its name: OpenAI documents both for plugins, but its skills page doesn't
mention them.

### Skill folders for ChatGPT

The paths are inside the unzipped download, whose top folder is `csa-plugins-official-main`.

| Plugin | Skill folder to zip | Notes |
|--------|---------------------|-------|
| incident-analysis | `plugins/incident-analysis/skills/incident-analysis` | |
| cwe-analysis | `plugins/cwe-analysis/skills/cwe-analysis` | Its CWE lookup tool and data sit outside this folder, so they aren't included. |
| cve-analysis | `plugins/cve-analysis/skills/cve-analysis` | Its analysis scripts sit outside this folder, and it needs a 2 GB copy of the CVE list. |
| security-knowledge-ingestion | `plugins/security-knowledge-ingestion/skills/security-knowledge-ingestion` | |
| nist-ir-8477-mapping | `plugins/nist-ir-8477-mapping/skills/nist-ir-8477-mapping` | |
| secid | none | Use SecID's hosted service instead (below). |
| vulnerability-audit | `plugins/vulnerability-audit/skills/audit` and `plugins/vulnerability-audit/skills/validate-findings` | Two skills: zip and upload each one. It also uses cwe-analysis and SecID. |
| valid-ai-ted-scorer | `plugins/valid-ai-ted-scorer/skills/caiq-scorer` | About 24 MB (about 5 MB zipped), because it carries CSA's reference data. We have not checked whether ChatGPT accepts a skill that large. |

**SecID in ChatGPT.** `secid` has no skill: its lookups come from a server. SecID's hosted server is
`https://secid.cloudsecurityalliance.org/mcp`, and ChatGPT on the web can connect it as a custom MCP server. On
Business plans only admins and owners can add one; on Enterprise and Edu, admins can let chosen members do it. Follow
OpenAI's [Connecting custom MCP servers in ChatGPT](https://help.openai.com/articles/12584461). We have not tested this.

### Route B: an admin imports the CSA marketplace (not yet tested)

> [!WARNING]
> **Not yet tested with this marketplace.** OpenAI's import accepts the `.claude-plugin/marketplace.json` format that
> this repository uses, but nobody has imported it into a ChatGPT workspace yet. If you do, please
> [tell us what happened](#get-help-or-report-a-problem).
>
> Import adds every valid plugin in the repository without asking about each one, and the daily sync can add new
> plugins later. As OpenAI advises, review the repository before you import it.

**For workspace admins:**

1. Go to the [Admin console](https://admin.openai.com/), select your ChatGPT workspace, and open **Plugins**.
2. Select **Add**, then **Import marketplace**.
3. In **Source**, enter the address below. Leave **Path** and **Branch, tag, or commit** empty.

```text
https://github.com/CloudSecurityAlliance/csa-plugins-official
```

4. Select **Import marketplace**, and authorize GitHub access when asked.
5. Review **Import results**. Then open each imported plugin and set its **Installation policy**: **Available** lets
   members install it, and **Installed** installs it for them. New plugins start as **Available**.

The marketplace syncs from GitHub once a day. To sync now, open **Plugins** in the Admin console, then
**Marketplaces**, select the CSA marketplace, and select **Sync now**. Deleting the marketplace in ChatGPT deletes
every plugin imported from it.

**For members**, once your admin has imported it (your role needs the **Use plugins** permission):

1. Select **Plugins** in the ChatGPT sidebar ([direct link](https://chatgpt.com/plugins)).
2. Open **Your workspace**.
3. Select a CSA plugin and review what it includes.
4. Select **Install plugin**.

ChatGPT then uses the plugin when it fits your request. To choose it yourself, use an **@** mention, select **+** and
type its name, or select **Plugins** in the message box.

### Good to know (ChatGPT)

- **Desktop only.** ChatGPT labels an imported plugin **Desktop only** when it declares a server, as `secid` does, and
  a Desktop-only plugin can't run in ChatGPT on the web. `secid`'s server is a program that runs on your computer and
  needs Python, and we don't know yet whether ChatGPT's desktop app starts it.
- **In Route A, helper scripts and data stay behind.** A skill folder holds a plugin's method. Scripts and data that
  some plugins keep beside it aren't in your zip.
- **`valid-ai-ted-scorer` is large:** about 24 MB, or about 5 MB zipped. We have not checked whether ChatGPT accepts
  it.
- **We have not tested these plugins in ChatGPT.** They are built for Claude.

### Troubleshooting (ChatGPT)

<details>
<summary>I don't see Skills, or I can't upload</summary>

- Skills need a Business, Enterprise, Healthcare or Edu plan.
- In Enterprise and Edu workspaces, ask an admin to allow **Enable skills** and **Enable skill uploading** for your
  role.
- If the menus have moved, follow OpenAI's
  [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt).

</details>

<details>
<summary>The upload fails, or the skill is Blocked</summary>

- Zip the skill folder itself: not the whole download, and not the plugin folder above it. The folder you zip holds a
  file named `SKILL.md`.
- A **Blocked** skill can't be used. [Tell us](#get-help-or-report-a-problem) which plugin it was.

</details>

<details>
<summary>A CSA plugin doesn't appear under Your workspace</summary>

- Ask your admin whether the marketplace has been imported (Route B), and to check the plugin's installation policy
  and your role's settings. A plugin an admin has restricted can show **Disabled by admin**.

</details>

<details>
<summary>A plugin says Desktop only</summary>

- It needs the ChatGPT desktop app and can't run on the web. For SecID lookups on the web, connect
  [SecID's hosted service](#skill-folders-for-chatgpt) instead.

</details>

<details>
<summary>The import reports errors</summary>

- The import report explains why a plugin couldn't be imported; the other valid plugins still import. After a sync,
  **Completed — N errors** means some plugins couldn't be processed. Please
  [send us the error](#get-help-or-report-a-problem).

</details>

OpenAI's documentation:
[Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt),
[Plugins in ChatGPT](https://help.openai.com/en/articles/20001256) (one screenshot),
[Importing and syncing plugin marketplaces from GitHub](https://help.openai.com/articles/20001504) and
[Connecting custom MCP servers in ChatGPT](https://help.openai.com/articles/12584461) (one screenshot). GitHub's
[Downloading source code archives](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives)
has screenshots of the ZIP download.

## Install from the command line

For Claude Code, Codex and Gemini CLI. (Using the Claude app or ChatGPT instead? See the two sections above.)

### Claude Code

It takes two steps.

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
computer. You don't need to install them again.

### Codex and Gemini CLI

The plugins are written in the open `SKILL.md` format, so they work outside Claude too. We tested the Codex and Gemini
steps below in October 2026, with Codex CLI 0.163 and Gemini CLI 0.61.

Two things work differently outside Claude Code:

- **The secid lookup server doesn't start.** Connect SecID's hosted server instead, with the command for your app
  below. There is nothing to install.
- **Some bundled helper scripts may not be found.** They are written for Claude Code. The plugins' methods still work.

#### Codex (CLI and desktop app)

```text
codex plugin marketplace add CloudSecurityAlliance/csa-plugins-official
codex plugin add cwe-analysis@csa-plugins-official
```

Then start a new Codex session. In the Codex desktop app, install plugins from **Plugins** once the marketplace is
added. Codex does not install a plugin's dependencies for you: for `vulnerability-audit`, also add `cwe-analysis` and
connect SecID.

To connect SecID: `codex mcp add secid --url https://secid.cloudsecurityalliance.org/mcp`

#### Gemini CLI

Gemini installs skills one at a time:

```text
gemini skills install https://github.com/CloudSecurityAlliance/csa-plugins-official.git --path plugins/cwe-analysis/skills/cwe-analysis
```

For another plugin, change both `cwe-analysis` parts to its name. Three plugins differ: `vulnerability-audit` has two
skills (`skills/audit` and `skills/validate-findings`), `valid-ai-ted-scorer`'s skill is `skills/caiq-scorer`, and
`secid` has no skill (connect SecID's server instead). Check what is installed with `gemini skills list`.

To connect SecID: `gemini mcp add --transport http --scope user secid https://secid.cloudsecurityalliance.org/mcp`

**Antigravity CLI** replaced Gemini CLI for unpaid and Google One users in June 2026. Put skill folders in
`~/.gemini/antigravity-cli/skills/`, as Google's [migration guide](https://antigravity.google/docs/cli/gcli-migration/)
describes. We have not tested Antigravity.

## Available plugins

Each plugin's name links to its README, or to its folder where it has no README yet. To find a plugin:

- **in the Claude app,** look for its name on the **Discover** tab;
- **in ChatGPT,** upload its [skill folder](#skill-folders-for-chatgpt);
- **in Claude Code,** use the install command in the table.

Most plugins work as soon as they are installed. Three also need Python on your computer. The table says which ones,
and [Setting up your computer](#setting-up-your-computer) shows how to get it.

| Plugin | Install command | What it does |
|--------|-----------------|--------------|
| [incident-analysis](plugins/incident-analysis/) | `/plugin install incident-analysis@csa-plugins-official` | Investigates a cloud or AI security incident from public reports. It gathers sources, checks how far each one can be trusted, builds a timeline, and writes a report with lessons learned and recommended defenses. |
| [cwe-analysis](plugins/cwe-analysis/README.md) | `/plugin install cwe-analysis@csa-plugins-official` | Works out which type of weakness is behind a vulnerability, using MITRE's Common Weakness Enumeration (CWE), and explains why. Built for people who publish vulnerability records, security researchers, and software vendors. |
| [cve-analysis](plugins/cve-analysis/README.md) | `/plugin install cve-analysis@csa-plugins-official` | Studies the whole public list of known vulnerabilities (CVE records) at once. It answers questions such as "Is the number of CVEs really growing?" and "Is the data getting better?" **Needs Python and a copy of the CVE list:** see [Setting up your computer](#setting-up-your-computer). |
| [security-knowledge-ingestion](plugins/security-knowledge-ingestion/) | `/plugin install security-knowledge-ingestion@csa-plugins-official` | Turns a security standard, regulation, or framework into structured data that you can search, compare, and reuse. It first checks whether [SecID](https://secid.cloudsecurityalliance.org/) already has that data. |
| [nist-ir-8477-mapping](plugins/nist-ir-8477-mapping/) | `/plugin install nist-ir-8477-mapping@csa-plugins-official` | Maps how two security frameworks or standards relate, for example which controls in one cover which controls in the other. It follows NIST's published mapping method (NIST IR 8477) and exports to Excel or to NIST's own format. |
| [secid](plugins/secid/README.md) | `/plugin install secid@csa-plugins-official` | Looks up security identifiers, such as a CVE, a CWE, a MITRE ATT&CK technique, or a NIST control, across more than 700 sources, and links you to each one. **Needs Python:** see [Setting up your computer](#setting-up-your-computer). |
| [vulnerability-audit](plugins/vulnerability-audit/README.md) | `/plugin install vulnerability-audit@csa-plugins-official` | Reviews source code for security vulnerabilities, step by step. It challenges every finding to weed out false alarms, and helps you report real ones responsibly to the maintainers. Also installs `secid` and `cwe-analysis`. **Needs Python** (for secid): see [Setting up your computer](#setting-up-your-computer). |
| [valid-ai-ted-scorer](plugins/valid-ai-ted-scorer/README.md) | `/plugin install valid-ai-ted-scorer@csa-plugins-official` | Scores a completed CSA security questionnaire (CAIQ or AI-CAIQ) question by question, and produces a scored spreadsheet and a summary PDF. The result is an informational, AI-assisted assessment of what was written, not a CSA certification or audit. Read its [README](plugins/valid-ai-ted-scorer/README.md) first: it lists known issues and explains where your questionnaire data goes. |

## Using a plugin

Ask for what you need. For example:

- "Help me pick the right CWE for this bug report."
- "Investigate this cloud security incident and build a timeline: (paste a link to a news report)"
- "Map NIST CSF 2.0 to ISO 27001 and tell me where they differ."
- "Score this completed AI-CAIQ questionnaire."

To choose a plugin yourself, type `/` and pick it from the list. Plugin entries look like `plugin-name:skill-name`,
for example `/cwe-analysis:cwe-analysis`.

## Setting up your computer

Only three plugins need this: `secid`, `vulnerability-audit` (because it installs `secid`), and `cve-analysis`. They
run small Python programs on your computer. The other plugins need nothing extra.

**Claude Code can do these steps for you.** Ask it, for example, "Install the Python packages the secid plugin
needs," and approve the commands it shows you.

### Step 1. Get Python 3.11 or later

First check whether you already have it. Open a terminal (on a Mac, the **Terminal** app; on Windows, **PowerShell**)
and type:

```text
python3 --version
```

If it shows `Python 3.11` or a higher number, go to step 2. If it shows an older version, says the command is not
found, or opens the Microsoft Store, install Python:

- **Mac or Windows:** download it from [python.org/downloads](https://www.python.org/downloads/). On Windows, if the
  installer offers to add Python to your PATH, say yes.
- **Linux:** use your distribution's package manager, for example `sudo apt install python3 python3-pip` on Ubuntu or
  Debian.

Then close your terminal, open a new one, and check again.

### Step 2. Install the packages your plugin needs

| Plugin | Type this in your terminal |
|--------|----------------------------|
| `secid` or `vulnerability-audit` | `python3 -m pip install mcp httpx` |
| `cve-analysis` | `python3 -m pip install pandas` |

If pip refuses with a message about an "externally managed environment" (common on Linux, and with Python from
Homebrew), add `--user --break-system-packages` to the end of the command. Despite the name, `--user` puts the
packages in your own account and leaves the system's Python alone.

Restart Claude Code afterwards, so that secid can start.

**Only want secid lookups? You can skip steps 1 and 2.** Connect Claude to SecID's hosted service instead: add
`https://secid.cloudsecurityalliance.org/mcp` as a remote MCP server (in the Claude app, a custom connector). It gives
the same results. The [secid README](plugins/secid/README.md) has the details. This does not work for
`vulnerability-audit`, which needs the secid plugin itself.

### Step 3. Download the CVE list (cve-analysis only)

cve-analysis reads the public CVE list from your computer. Download it once (about 2 GB):

```text
git clone --depth 1 https://github.com/CVEProject/cvelistV5.git
```

If `git` is not installed, get it from [git-scm.com](https://git-scm.com/downloads). On a Mac, typing `git` offers to
install it for you. When you start an analysis, tell Claude where the folder is. Each pass over the data takes about
six minutes.

## Is it safe to install?

Plugins can run programs on your computer, so install only plugins you trust. Every plugin listed here is written and
maintained by CSA, and its full source is public in this repository. Before anything is installed, the Claude app and
Claude Code show you what the plugin adds.

This marketplace may list third-party plugins in future. CSA does not control what those contain, so check each one's
homepage before you install it.

**Your data.** "Evidence" below means whatever you give a plugin: a questionnaire, a bug report, source code, a
document. Raw evidence never goes to CSA. When the plugin reads your evidence, it is processed by the AI model you run it with, under your agreement with that provider. The one thing that does reach CSA is a SecID lookup: `secid`, and
`vulnerability-audit` and `security-knowledge-ingestion` when they use it, send the identifier you look up, such as a
CVE number, to CSA's SecID service and nothing else.

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
