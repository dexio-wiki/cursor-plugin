"""Check the plugin against Cursor's plugin reference (cursor.com/docs/plugins/building).

    python3 scripts/check_plugin.py

Manifest name and paths, frontmatter on every skill and rule, and mcp.json. Exits 1 on a
problem. Standard library only.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGIN_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def frontmatter(path):
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        m = re.match(r"^([A-Za-z-]+):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip().strip('"')
    return fields


def main():
    errors = []
    manifest = json.loads((ROOT / ".cursor-plugin" / "plugin.json").read_text())
    if not PLUGIN_NAME.match(manifest.get("name", "")):
        errors.append("plugin.json: invalid name")
    if not manifest.get("description"):
        errors.append("plugin.json: no description")
    for field in ("logo", "rules", "skills", "mcpServers"):
        value = manifest.get(field)
        if not isinstance(value, str):
            errors.append("plugin.json: %s should be a path" % field)
            continue
        if value.startswith("/") or ".." in Path(value).parts or not (ROOT / value).exists():
            errors.append("plugin.json: bad %s path %r" % (field, value))

    skills = sorted((ROOT / manifest.get("skills", "skills")).glob("*/SKILL.md"))
    if not skills:
        errors.append("no skills found")
    for path in skills:
        fm = frontmatter(path) or {}
        where = path.relative_to(ROOT)
        if not SKILL_NAME.match(fm.get("name", "")) or fm.get("name") != path.parent.name:
            errors.append("%s: name missing or not the folder name" % where)
        if not fm.get("description"):
            errors.append("%s: no description" % where)

    for path in sorted((ROOT / manifest.get("rules", "rules")).glob("*.mdc")):
        fm = frontmatter(path)
        if not fm or not fm.get("description"):
            errors.append("%s: no description in frontmatter" % path.relative_to(ROOT))
        elif fm.get("alwaysApply") not in ("true", "false"):
            errors.append("%s: alwaysApply should be true or false" % path.relative_to(ROOT))

    servers = json.loads((ROOT / manifest.get("mcpServers", "mcp.json")).read_text())
    if not servers.get("mcpServers"):
        errors.append("mcp.json: no servers")
    for name, server in servers.get("mcpServers", {}).items():
        if not (server.get("url") or server.get("command")):
            errors.append("mcp.json: server %r has no url or command" % name)

    for e in errors:
        print(e)
    print("%d skills checked, %d problems" % (len(skills), len(errors)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
