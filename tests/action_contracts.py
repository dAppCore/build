#!/usr/bin/env python3
"""Structural checks on every action.yml in the repository.

These are the mistakes that pass YAML validation and then fail quietly at
runtime, which is the worst combination — a job goes green having produced
nothing, or a consumer reads an output that is always the empty string.
"""

import pathlib
import re
import sys

import yaml


class StrictLoader(yaml.SafeLoader):
    """SafeLoader that refuses duplicate keys.

    PyYAML takes the last one and says nothing; the Actions runner rejects the
    manifest. So a file can validate here, look fine, and fail every job that
    touches it — which is exactly what a stray `shell: bash` left behind by an
    edit did.
    """


def _no_duplicates(loader, node, deep=False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise yaml.constructor.ConstructorError(
                None, None, f"duplicate key {key!r}", key_node.start_mark)
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


StrictLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _no_duplicates)

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Passthroughs a caller deliberately does not make. Each one is a decision, so
# each one is named here rather than the check being loosened for all of them.
PASSTHROUGH_EXEMPT = {
    # Danet has no build task; compiling is the build, and naming an unrelated
    # `build` task in someone's deno.json would be mistaken for one.
    ("actions/build/deno/framework/danet/action.yml", "build-task"),
}


def action_files():
    yield ROOT / "action.yml"
    yield from sorted((ROOT / "actions").rglob("action.yml"))


def callee_path(uses: str) -> pathlib.Path | None:
    """Resolve a `uses:` on a sibling action in this repository to its manifest.

    Only same-repo references resolve; a third-party action is somebody else's
    contract and is not ours to check.
    """
    ref = uses.split("@", 1)[0]
    if not ref.startswith("dAppCore/build"):
        return None
    sub = ref[len("dAppCore/build"):].strip("/")
    path = (ROOT / sub / "action.yml") if sub else (ROOT / "action.yml")
    return path if path.is_file() else None


def main() -> int:
    problems: list[str] = []

    for path in action_files():
        rel = path.relative_to(ROOT)
        try:
            doc = yaml.load(path.read_text(), Loader=StrictLoader) or {}
        except yaml.YAMLError as exc:
            problems.append(f"{rel}: {exc}")
            continue

        # An output declared without a value resolves to "" forever. Nothing
        # warns; the consumer just sees empty. This is how HAS_ROOT_MAIN_GO
        # broke every discovery fixture at once.
        for name, spec in (doc.get("outputs") or {}).items():
            if not isinstance(spec, dict):
                problems.append(f"{rel}: output {name} is not a mapping")
            elif "value" not in spec:
                problems.append(f"{rel}: output {name} has no value — it will always be empty")

        # A composite step that runs a script must say which shell, or the
        # action fails to load on some runners and not others.
        steps = ((doc.get("runs") or {}).get("steps")) or []
        for i, step in enumerate(steps):
            if "run" in step and "shell" not in step:
                label = step.get("name", f"step {i}")
                problems.append(f"{rel}: '{label}' has run: without shell:")

        # A malformed ${{ }} expression is valid YAML and rejected by the
        # runner at load time — and because every referenced manifest is
        # validated up front, a broken adapter fails jobs that never call it.
        # format() with an unquoted first argument is the way that happens.
        for i, line in enumerate(path.read_text().split("\n"), 1):
            for call in re.findall(r"format\(\s*[^'\"\s)]", line):
                problems.append(
                    f"{rel}:{i}: format() first argument is not quoted — the runner will reject this manifest")

        # Inputs need a description or the marketplace listing renders blanks.
        declared = (doc.get("inputs") or {})
        for name, spec in declared.items():
            if not isinstance(spec, dict) or not spec.get("description"):
                problems.append(f"{rel}: input {name} has no description")

        # An input both sides declare and the caller forgets to forward leaves
        # the callee on its own default, silently. The caller looks like it
        # honours the option, the build ignores it, and nothing says so — which
        # is how `entry` reached the deno stack and never reached the danet
        # adapter, pinning every Danet build to run.ts.
        for i, step in enumerate(steps):
            uses = step.get("uses")
            if not isinstance(uses, str):
                continue
            target = callee_path(uses)
            if target is None:
                continue
            try:
                callee = yaml.load(target.read_text(), Loader=StrictLoader) or {}
            except yaml.YAMLError:
                continue  # reported when that file is checked in its own right
            forwarded = set((step.get("with") or {}).keys())
            target_rel = str(target.relative_to(ROOT))
            for name in (callee.get("inputs") or {}):
                if name in declared and name not in forwarded:
                    if (target_rel, name) in PASSTHROUGH_EXEMPT:
                        continue
                    label = step.get("name", f"step {i}")
                    problems.append(
                        f"{rel}: '{label}' does not forward {name} to {target_rel} — "
                        f"the callee will use its own default")

    if problems:
        print("\n".join(f"  {p}" for p in problems))
        print(f"\n{len(problems)} problem(s)")
        return 1

    print(f"checked {len(list(action_files()))} action.yml files — all sound")
    return 0


if __name__ == "__main__":
    sys.exit(main())
