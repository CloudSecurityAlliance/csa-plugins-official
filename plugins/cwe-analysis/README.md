# CWE Analysis Plugin

A Claude Code plugin for assigning CWEs to vulnerabilities with high quality. Helps CNAs, security researchers, and vendors identify the correct CWE(s) for a vulnerability, build weakness chains, validate assignments, and assess AI relevance.

## Installation

Add the CSA marketplace (if not already added):

```
/plugin marketplace add CloudSecurityAlliance/csa-plugins-official
```

Install this plugin:

```
/plugin install cwe-analysis@csa-plugins-official
```

## Features

- **6-phase guided workflow**: intake, code analysis, CWE identification, chain analysis, validation, report
- **Bundled CWE data**: ~944 CWEs from MITRE's Research Concepts view with AI relevance scores
- **Confidence framework**: every CWE assignment tagged with a confidence level (Confirmed → Uncertain)
- **Quality validation**: 5-point checklist catches common CWE mapping errors
- **Chain analysis**: map root cause → enabling weakness → exploited weakness with CWE relationships
- **AI relevance scoring**: two-view model (attacks ON AI vs attacks VIA AI) applied as post-classification overlay
- **Teaching mode**: explains reasoning and common mistakes as it works

## Usage

The plugin triggers when you ask to assign CWEs, classify vulnerabilities, or analyze weakness chains. You can run the full 6-phase workflow or jump to a specific phase:

1. **Intake** — understand the vulnerability
2. **Code Analysis** — examine the code path (optional)
3. **CWE Identification** — find candidate CWEs with confidence levels
4. **Chain Analysis** — build the weakness chain (optional)
5. **Validation** — quality checks against 5 failure modes
6. **Report** — generate CNA-ready output

## Directory Structure

```
cwe-analysis/
├── plugin.json              # Plugin manifest
├── LICENSE                   # Apache 2.0
├── FEEDBACK.md              # Bug reports and feedback
├── README.md                # This file
├── data/                    # Bundled CWE data
│   ├── CWE-AI-Classifications.csv
│   ├── CWE-Research-Concepts-1000.csv
│   ├── MITRE-CWE-LICENSE.txt
│   └── VERSION.txt
├── docs/                    # Design spec and implementation plan
├── scripts/
│   ├── cwe-tool.py          # CWE data query tool (6 subcommands)
│   └── test_cwe_tool.py     # Tests for cwe-tool.py
└── skills/
    └── cwe-analysis/
        ├── SKILL.md          # Main skill router
        ├── phases/           # 6 phase files
        └── references/       # 5 reference docs
```

## CWE Data Tool

The bundled `cwe-tool.py` script queries the CWE data:

```bash
cwe-tool.py lookup 79              # Full details for CWE-79
cwe-tool.py search sql injection   # Keyword search
cwe-tool.py candidates --impact "code execution" --abstraction Base
cwe-tool.py children 74            # Find more specific child CWEs
cwe-tool.py chain 1427 1426 78     # Show relationships between CWEs
cwe-tool.py ai-relevant --min-score 4  # List AI-relevant CWEs
```

## Data Updates

When MITRE publishes new CWE data:
1. Run `download-cwe-items.sh` and `cwe-ai classify` in the dataset repo
2. Copy the two CSVs into `data/`
3. Update `data/VERSION.txt`
