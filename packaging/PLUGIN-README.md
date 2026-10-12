# ASD-STE100 Technical English

A skills-only Codex plugin for clarifying technical English while preserving meaning. It includes rewrite instructions, references, examples, and an optional Python 3 linter. No connectors, API keys, MCP servers, or hooks are required.

For an easy local trial, use the companion `asd-ste100-tryout-0.1.0.zip`, which includes a marketplace catalog and recipient instructions. This standalone plugin ZIP contains the plugin files only; extracting it does not install it.

Once installed, select the bundled skill from Codex's skill picker and ask it to rewrite or review technical text. Use STE-flavored mode for scientific or architecture notes. Technical vocabulary, uncertainty, conditions, and requirement strength must remain intact.

The root `plugin.json` uses the portable Agent Plugins format. `.codex-plugin/plugin.json` supplies Codex compatibility metadata. The `skills/asd-ste100/` folder contains the complete skill and its original MIT license.

This is STE-inspired clarity guidance, not certified ASD-STE100 compliance. The official approved-word dictionary is not included.

Adapted from [danyuchn/asd-ste100-skill](https://github.com/danyuchn/asd-ste100-skill), using the local source copy marked version 0.4.0. Original copyright 2026 Dustin Yuchen Teng; the MIT license and copyright notice are included in LICENSE.

The upstream project cites ASD-STE100 and other writing references; these citations remain in `skills/asd-ste100/references/writing-rules.md`. Earlier code provenance has not been independently established. The upstream MIT license does not license the official ASD standard or its dictionary, which have separate rights.
