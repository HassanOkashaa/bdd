#!/usr/bin/env python3
"""Validate portable hive state without changing it. This checks structure, not truth."""
import argparse
import json
from pathlib import Path
import sys

from init_hive import DEFAULT_NAMES

STATUSES = {"pending", "building", "verifying", "blocked", "passed"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"nonstandard JSON constant {value}")


def validate(project):
    hive = Path(project).expanduser() / "hive"
    errors = []
    data = {}
    for name in ("config.json", "features.json"):
        try:
            data[name] = json.loads((hive / name).read_text(encoding="utf-8"), object_pairs_hook=unique_object, parse_constant=reject_constant)
        except (OSError, ValueError, RecursionError) as exc:
            errors.append(f"{name}: cannot read valid JSON: {exc}")
    config = data.get("config.json")
    if not isinstance(config, dict):
        errors.append("config.json: expected an object")
    else:
        if type(config.get("schema_version")) is not int or config["schema_version"] != 1:
            errors.append("config.json: schema_version must be 1")
        for key in ("max_parallel_workers", "max_active_features", "max_repair_rounds_per_feature"):
            if type(config.get(key)) is not int or config[key] < 1:
                errors.append(f"config.json: {key} must be a positive integer at the top level")
        for key in ("mode", "permissions"):
            if not nonempty(config.get(key)):
                errors.append(f"config.json: {key} must be a nonempty string")
        if config.get("model_selection") != "queen":
            errors.append("config.json: model_selection must be queen")
        if not isinstance(config.get("capabilities"), dict):
            errors.append("config.json: capabilities must be an object")
        names = config.get("bee_names")
        if not isinstance(names, dict) or not set(DEFAULT_NAMES).issubset(names) or not all(nonempty(k) and nonempty(v) for k, v in names.items()):
            errors.append("config.json: bee_names must retain every default role with a nonempty display name")
    features = data.get("features.json")
    if not isinstance(features, list):
        errors.append("features.json: expected a top-level array, not a wrapper object")
        return errors
    ids = set()
    graph = {}
    for number, feature in enumerate(features):
        label = f"features.json[{number}]"
        if not isinstance(feature, dict):
            errors.append(f"{label}: expected an object")
            continue
        identity = feature.get("id")
        if not nonempty(identity) or identity in ids:
            errors.append(f"{label}: id must be nonempty and unique")
        else:
            ids.add(identity)
        if not nonempty(feature.get("description")):
            errors.append(f"{label}: description is required")
        acceptance = feature.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance or not all(nonempty(x) for x in acceptance):
            errors.append(f"{label}: acceptance must be a nonempty list of strings")
        dependencies = feature.get("depends_on")
        if not isinstance(dependencies, list) or not all(nonempty(x) for x in dependencies):
            errors.append(f"{label}: depends_on must be a list of IDs")
        elif nonempty(identity):
            graph[identity] = dependencies
        status, passed = feature.get("status"), feature.get("passes")
        if not isinstance(status, str) or status not in STATUSES or type(passed) is not bool or passed != (status == "passed"):
            errors.append(f"{label}: status and passes are invalid or inconsistent")
        if "blocked_reason" not in feature or (feature["blocked_reason"] is not None and not nonempty(feature["blocked_reason"])):
            errors.append(f"{label}: blocked_reason must be null or a nonempty string")
        if status == "blocked" and not nonempty(feature.get("blocked_reason")):
            errors.append(f"{label}: blocked status needs a reason")
        evidence = feature.get("evidence")
        if not isinstance(evidence, list) or (passed is True and not evidence):
            errors.append(f"{label}: evidence must be an array and cannot be empty for a passed feature")
        elif isinstance(evidence, list):
            for item in evidence:
                if not isinstance(item, dict) or not all(nonempty(item.get(k)) for k in ("criterion", "command", "result", "revision", "report")):
                    errors.append(f"{label}: evidence needs criterion, command, result, revision and report strings")
    for identity, dependencies in graph.items():
        if len(set(dependencies)) != len(dependencies) or any(x not in ids for x in dependencies):
            errors.append(f"feature {identity!r}: dependencies must be unique existing IDs")
    remaining = set(graph)
    while remaining:
        ready = {identity for identity in remaining if not (set(graph[identity]) & remaining)}
        if not ready:
            errors.append("features.json: dependency cycle detected")
            break
        remaining -= ready
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", help="Project directory containing hive/")
    args = parser.parse_args()
    errors = validate(args.project)
    if errors:
        print("Invalid hive state; preserve originals and correct the listed structure before resuming:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 2
    print("Hive state structure is valid. Approval and verification evidence still require review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
