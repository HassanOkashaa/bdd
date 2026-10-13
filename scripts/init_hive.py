#!/usr/bin/env python3
"""Create empty hive state without changing existing project files (Python 3.9+)."""
import argparse
import json
from pathlib import Path
import sys
import unicodedata

DEFAULT_NAMES = {
    "queen": "Queen", "scout": "Scout", "product-lead": "Product Lead",
    "architect": "Architect", "designer": "Designer", "builder": "Builder",
    "inspector": "Inspector", "tester": "Tester", "guard": "Guard",
}


def parse_names(values):
    names = dict(DEFAULT_NAMES)
    for value in values:
        role, separator, name = value.partition("=")
        role, name = role.strip(), name.strip()
        if not separator or role not in DEFAULT_NAMES:
            raise ValueError("Use --bee-name ROLE=NAME; roles: " + ", ".join(DEFAULT_NAMES))
        if not name or len(name) > 64 or any(unicodedata.category(c).startswith("C") for c in name):
            raise ValueError("Bee names must be 1–64 characters without control characters")
        names[role] = name
    return names


def initialize(project, bee_names=()):
    names = parse_names(bee_names)
    project = Path(project).expanduser().resolve(strict=True)
    if not project.is_dir():
        raise NotADirectoryError(f"Not a project directory: {project}")
    hive = project / "hive"
    # Exclusive mkdir is the reservation, including against concurrent initializers.
    # A symlink or file at this path is also refused, never followed or overwritten.
    hive.mkdir()
    config = {
        "schema_version": 1,
        "mode": "discover",
        "max_parallel_workers": 1,
        "max_active_features": 1,
        "max_repair_rounds_per_feature": 3,
        "model_selection": "queen",
        "bee_names": names,
        "capabilities": {},
        "permissions": "Follow user authorization, project rules and host policy",
    }
    content = {
        "config.json": json.dumps(config, indent=2) + "\n",
        "features.json": "[]\n",
        "approvals.md": "# Approvals\n\nNo approvals recorded. Record scope, artifact/version, user decision and date.\n",
        "progress.md": "# Progress\n\nInitialized only. No project plan or completed work recorded.\n\nNext: inspect the project, discover capabilities and clarify the outcome.\n",
    }
    try:
        for folder in ("briefs", "reports", "research"):
            (hive / folder).mkdir()
            (hive / folder / ".gitkeep").touch(exist_ok=False)
        for name, text in content.items():
            with (hive / name).open("x", encoding="utf-8") as stream:
                stream.write(text)
    except OSError as exc:
        raise OSError(f"Setup incomplete at {hive}; inspect it before resuming. Existing project files were not modified. {exc}") from exc
    return hive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Existing project directory; hive/ must not exist")
    parser.add_argument("--bee-name", action="append", default=[], metavar="ROLE=NAME",
                        help="Optional display name; repeat for more roles. Defaults to role names.")
    args = parser.parse_args()
    try:
        hive = initialize(args.project, args.bee_name)
    except FileExistsError:
        print("Refusing to overwrite existing hive/ state. Read it and resume, or choose another project.", file=sys.stderr)
        return 2
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"Cannot initialize hive: {exc}", file=sys.stderr)
        return 2
    print(f"Created {hive}\nNext: ask your assistant to read SKILL.md and inspect this project.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
