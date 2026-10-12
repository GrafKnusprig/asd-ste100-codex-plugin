#!/usr/bin/env python3
"""Build and validate shareable plugin ZIPs without installing anything."""

import hashlib
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / ".agents" / "skills" / "asd-ste100"
PACKAGING = ROOT / "packaging"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def collect_files():
    manifest = read_json(PACKAGING / "plugin.json")
    overlay = read_json(PACKAGING / ".codex-plugin" / "plugin.json")
    assert manifest["name"] == overlay["name"] == SOURCE.name
    assert manifest["version"] == overlay["version"]
    assert re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"])
    assert overlay["skills"] == "./skills/"
    assert manifest["license"] == "MIT"
    files = {
        "plugin.json": (PACKAGING / "plugin.json").read_bytes(),
        ".codex-plugin/plugin.json": (PACKAGING / ".codex-plugin" / "plugin.json").read_bytes(),
        "LICENSE": (ROOT / "LICENSE").read_bytes(),
        "README.md": (PACKAGING / "PLUGIN-README.md").read_bytes(),
    }
    for path in sorted(SOURCE.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Do not distribute symlinks: {path}")
        if not path.is_file() or "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        relative = path.relative_to(SOURCE).as_posix()
        content = path.read_bytes()
        if relative == "SKILL.md":
            # The same source is usable both as a repository skill and a plugin.
            content = content.decode("utf-8").replace(
                ".agents/skills/asd-ste100/scripts/ste-lint.py",
                "skills/asd-ste100/scripts/ste-lint.py",
            ).replace("from this repository root:", "from the installed plugin root:").encode("utf-8")
        files[f"skills/asd-ste100/{relative}"] = content
    return manifest, files


def write_zip(path, files):
    # Stable ordering and timestamps make repeated builds byte-for-byte reproducible.
    with ZipFile(path, "w", compression=ZIP_DEFLATED) as archive:
        for name, data in sorted(files.items()):
            info = ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data)


def validate_archive(path, expected):
    with ZipFile(path) as archive:
        assert archive.testzip() is None, "ZIP integrity failure"
        assert set(archive.namelist()) == set(expected), "Unexpected package contents"
        for name in archive.namelist():
            assert not name.startswith("/") and ".." not in Path(name).parts
            assert archive.read(name) == expected[name], name
        prefix = "" if "plugin.json" in expected else "plugins/asd-ste100/"
        portable = json.loads(archive.read(prefix + "plugin.json"))
        overlay = json.loads(archive.read(prefix + ".codex-plugin/plugin.json"))
        assert portable["name"] == overlay["name"]
        if prefix:
            catalog = json.loads(archive.read(".agents/plugins/marketplace.json"))
            candidate = catalog["plugins"][0]
            assert candidate["name"] == portable["name"]
            assert candidate["policy"]["installation"] == "AVAILABLE"
            assert candidate["source"]["path"].removeprefix("./") + "/" == prefix
        # Validate and execute the bundled bytes without installing or extracting
        # host-recognized configuration folders.
        skill_prefix = prefix + "skills/asd-ste100/"
        entry = archive.read(skill_prefix + "SKILL.md").decode("utf-8")
        assert entry.startswith("---\nname: asd-ste100\ndescription: ")
        for name in archive.namelist():
            if name.startswith(skill_prefix) and name.endswith(".md"):
                for target in re.findall(r"\]\(([^)]+)\)", archive.read(name).decode("utf-8")):
                    if "://" not in target:
                        resolved = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                        assert resolved in expected, (name, target)
        linter = archive.read(skill_prefix + "scripts/ste-lint.py").decode("utf-8")
        subprocess.run([sys.executable, "-c", linter, "--selftest"], check=True)
        fixture = subprocess.run([
            sys.executable, "-c", linter, "--json",
        ], input=archive.read(skill_prefix + "examples/linter-edge-cases.md").decode("utf-8"), capture_output=True, text=True)
        payload = json.loads(fixture.stdout)
        assert fixture.returncode == 1 and payload["hard_count"] == 2
        assert all(item["rule"] == "dangling-conjunction" for item in payload["violations"])


def main():
    manifest, plugin_files = collect_files()
    version = manifest["version"]
    catalog = read_json(PACKAGING / "marketplace.json")
    assert catalog["plugins"][0]["source"]["path"] == "./plugins/asd-ste100"
    kit_files = {f"plugins/asd-ste100/{name}": data for name, data in plugin_files.items()}
    kit_files[".agents/plugins/marketplace.json"] = (PACKAGING / "marketplace.json").read_bytes()
    kit_files["README.md"] = (PACKAGING / "TRYOUT.md").read_bytes()
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    hashes = []
    for name, files in [(f"asd-ste100-{version}.zip", plugin_files), (f"asd-ste100-tryout-{version}.zip", kit_files)]:
        destination = output / name
        write_zip(destination, files)
        validate_archive(destination, files)
        hashes.append(f"{hashlib.sha256(destination.read_bytes()).hexdigest()}  {name}")
        print(f"Validated {destination} ({len(files)} files)")
    (output / "SHA256SUMS.txt").write_text("\n".join(hashes) + "\n", encoding="utf-8")
    print("Build complete. No plugins were installed or registered.")


if __name__ == "__main__":
    main()
