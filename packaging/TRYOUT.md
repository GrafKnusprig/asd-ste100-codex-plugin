# Try ASD-STE100 in Codex

This kit contains one skills-only plugin and a local marketplace catalog. It does not install itself. No account connection, API key, or server is required. Python 3 is optional for the bundled linter.

## ChatGPT desktop app / Codex

1. Extract the entire tryout ZIP into a folder. Preserve hidden folders, including `.agents` and `.codex-plugin`.
2. Open the extracted folder as your Codex project. The folder containing this README is the marketplace root.
3. Restart the desktop app if the local source does not appear. Open the Plugins Directory and choose **ASD-STE100 Tryout**.
4. Select **ASD-STE100 Technical English** and install it when you are ready to test.
5. Start a new Codex conversation and select the skill from the skill picker, or use `$asd-ste100` if that name is shown. Plugin namespaces can affect the displayed invocation name; use the name in your picker.

Local marketplace support varies by client and version. These instructions target clients with local plugin support, not an ordinary browser chat that cannot read your extracted files.

## Codex CLI with plugin commands

From the extracted kit's root, the recipient can register the catalog:

```powershell
codex plugin marketplace add .
```

On clients exposing `codex plugin add`, install from that catalog:

```powershell
codex plugin add asd-ste100@asd-ste100-tryout
```

If your version does not expose that command, use the desktop Plugins Directory. These are recipient setup commands; the build process does not run them.

## Example prompts

```text
Use $asd-ste100 to clarify: The request may have failed because the configured endpoint could be unavailable.

Use $asd-ste100 in STE-flavored mode to rewrite the following scientific note. Preserve all technical terms, caveats, and acceptance conditions: ...

Use $asd-ste100 to review this tool description. Show the original, revised text, and reasons for each change: ...
```

Check that the rewrite preserves "may", "could", negation, numbers, conditions, and requirement strength. Clear input may remain unchanged. The skill should not add facts or turn an architectural caveat into a command.

For an optional linter check from this folder:

```powershell
python "plugins/asd-ste100/skills/asd-ste100/scripts/ste-lint.py" --selftest
```

The linter checks structural patterns. It does not verify semantic equivalence or official dictionary approval.

## Files and attribution

`plugins/asd-ste100/` is the complete plugin. Its root `plugin.json` is the portable manifest; `.codex-plugin/plugin.json` provides Codex compatibility metadata. `.agents/plugins/marketplace.json` makes the plugin available for an explicit install; its policy is `AVAILABLE`, not `INSTALLED_BY_DEFAULT`.

The original skill resources are adapted from source version 0.4.0, copyright 2026 Dustin Yuchen Teng, under the included MIT license. This plugin is not an official ASD or OpenAI product.

Packaging and local marketplace guidance: https://developers.openai.com/plugins/build/plugins
