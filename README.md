# ASD-STE100 skill for Codex

A Codex adaptation of the local `asd-ste100-skill` project (source version 0.4.0). It rewrites ambiguous technical English using Simplified Technical English principles while preserving facts, conditions, and uncertainty.

This repository contains a **skill**: instructions, references, examples, and a Python linter. A plugin is a distribution package that can contain skills and optional connectors. No connector or plugin manifest is needed for this repository's local workflow. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) and [plugin architecture](https://developers.openai.com/plugins/concepts/plugins).

## Use in this repository

Codex discovers the skill in [`.agents/skills/asd-ste100/SKILL.md`](.agents/skills/asd-ste100/SKILL.md). Open this repository in Codex and invoke it with:

```text
Use $asd-ste100 to clarify this tool description: ...
Use $asd-ste100 to rewrite README.md in STE-flavored mode.
Use $asd-ste100 to review this instruction and show a before/after table: ...
```

Automatic selection is enabled by default for matching requests. If the new skill does not appear, restart Codex. File-edit requests update the requested files; chat rewrites return the rewritten text alone by default.

## Use in another project

Copy the entire `.agents/skills/asd-ste100` folder into that project's `.agents/skills/` directory. For personal discovery across repositories, copy it into your user skill directory (`~/.agents/skills/` in the current official documentation). Keep all references, scripts, and the included license together. This conversion only creates files in this repository; it does not change personal configuration.

## Linter

Python 3 is required only for optional linting. No third-party Python packages are needed.

```powershell
python ".agents/skills/asd-ste100/scripts/ste-lint.py" --json "document.md"
python ".agents/skills/asd-ste100/scripts/ste-lint.py" --selftest
python ".agents/skills/asd-ste100/scripts/ste-lint.py" ".agents/skills/asd-ste100/examples/linter-edge-cases.md"
```

The last command intentionally exits 1 and reports two dangling conjunctions. `--baseline N` tolerates N hard findings. `--disable rule1,rule2` suppresses named rules. Passive voice and compound tenses are advisory. The linter preserves hedges and modality and ignores fenced code.

The linter checks patterns, not meaning or official dictionary approval. Its sentence threshold is 25 words; the skill manually applies the 20-word instruction limit. A clean run does not prove that a rewrite preserved meaning or meets formal ASD-STE100 requirements.

## Adaptation and license

The source linter, examples, rule summary, and MIT license are preserved. The original detailed skill is retained as `references/rewrite-guide.md` with its metadata adapted for Codex. The new entrypoint adds Codex discovery, file-edit behavior, literal preservation, and path handling. UI metadata is in `agents/openai.yaml`.

The official ASD approved-word dictionary is not included. This skill provides STE-inspired clarity guidance, not certified aerospace documentation compliance.

MIT; original copyright notice retained in [LICENSE](LICENSE).
