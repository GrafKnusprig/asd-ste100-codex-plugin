# ASD-STE100 skill for Codex

A Codex adaptation of the local `asd-ste100-skill` project (source version 0.4.0). It rewrites ambiguous technical English using Simplified Technical English principles while preserving facts, conditions, and uncertainty.

This repository contains a **skill** and build sources for a distributable **Codex plugin**. The plugin bundles the instructions, references, examples, and Python linter. See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) and [plugin packaging documentation](https://developers.openai.com/plugins/build/plugins).

## Build and share the plugin

```powershell
python scripts/build_plugin.py
```

The build creates and validates:

- `dist/asd-ste100-0.1.0.zip`: the standalone plugin, with portable and Codex compatibility manifests.
- `dist/asd-ste100-tryout-0.1.0.zip`: the recommended file to send to a tester. It contains the plugin, a local marketplace catalog, and setup instructions.
- `dist/SHA256SUMS.txt`: checksums for both ZIPs.

The tester extracts the tryout kit and follows its README. The full instructions are also in [packaging/TRYOUT.md](packaging/TRYOUT.md). Packaging does not install, enable, register, or publish the plugin. The catalog uses `AVAILABLE`, so installation remains the tester's choice. No catalog is added to this repository's active `.agents/plugins` location.

The source skill remains in `.agents/skills/asd-ste100`. Build-time copies adapt linter example paths for the plugin layout. Manifests and recipient instructions live in `packaging/`; generated ZIPs are ignored by Git. Rebuild after changing the skill. Change the version in both manifest files when preparing a new version, and update version-specific README examples.

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

Adapted from [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), using the local source copy marked version 0.4.0. The upstream MIT license credits Dustin Yuchen Teng (copyright 2026). The original copyright notice and license are included in this repository and both distribution packages.

The upstream project describes its guidance as based on ASD-STE100 and lists its reference sources. Those citations are retained in the bundled `references/writing-rules.md`. We have not independently established any earlier code provenance beyond the upstream repository and its notices. The official ASD-STE100 standard has separate rights; the upstream MIT license does not license that standard or its dictionary.

The source linter, examples, rule summary, and MIT license are preserved. The original detailed skill is retained as `references/rewrite-guide.md` with its metadata adapted for Codex. The new entrypoint adds Codex discovery, file-edit behavior, literal preservation, and path handling. UI metadata is in `agents/openai.yaml`.

The official ASD approved-word dictionary is not included. This skill provides STE-inspired clarity guidance, not certified aerospace documentation compliance.

MIT; original copyright notice retained in [LICENSE](LICENSE).
