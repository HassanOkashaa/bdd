#!/usr/bin/env python3
"""Create empty hive state without changing existing project files (Python 3.9+)."""
import argparse
import json
from pathlib import Path
import sys


def initialize(project):
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
    args = parser.parse_args()
    try:
        hive = initialize(args.project)
    except FileExistsError:
        print("Refusing to overwrite existing hive/ state. Read it and resume, or choose another project.", file=sys.stderr)
        return 2
    except (OSError, RuntimeError) as exc:
        print(f"Cannot initialize hive: {exc}", file=sys.stderr)
        return 2
    print(f"Created {hive}\nNext: ask your assistant to read SKILL.md and inspect this project.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
