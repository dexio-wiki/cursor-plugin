"""Copy the skills from a checkout of dexio-wiki/llm-wiki-skills into skills/.

    python3 scripts/sync_skills.py path/to/llm-wiki-skills

Replaces skills/ with the upstream copy and writes the upstream commit to .skills-upstream.
Prints "changed" or "unchanged". Standard library only.
"""
import filecmp
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def main():
    upstream = Path(sys.argv[1]).resolve()
    source = upstream / "skills"
    if not any(source.glob("*/SKILL.md")):
        sys.exit("no skills found under %s" % source)
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=upstream, capture_output=True,
                         text=True, check=True).stdout.strip()
    target = ROOT / "skills"
    if target.exists() and same_tree(source, target):
        print("unchanged")
        return
    shutil.rmtree(target, ignore_errors=True)
    shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    (ROOT / ".skills-upstream").write_text(sha + "\n")
    print("changed")


if __name__ == "__main__":
    main()
