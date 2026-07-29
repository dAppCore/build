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
    # callee -> input -> {caller: forwards?}, for the asymmetry report below.
    wiring: dict[str, dict[str, dict[str, bool]]] = {}

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

        # ${{ inputs.X }} where X is not declared in *this* file resolves to the
        # empty string. Nothing warns — not the runner, not the caller, not the
        # forwarding check above, which only asks whether a name a file declares
        # gets passed on. Forwarding an input the file never declared satisfies
        # it while passing nothing, so a chain can be repaired at one hop, report
        # sound, and still be severed at the next. That is how `task` was added
        # to the root action and forwarded from the orchestrator, and every
        # Wails v3 build carried on running its default target.
        for i, line in enumerate(path.read_text().split("\n"), 1):
            for ref in re.findall(r"inputs\.([A-Za-z0-9_-]+)", line):
                if ref not in declared:
                    problems.append(
                        f"{rel}:{i}: references inputs.{ref}, which this file does "
                        f"not declare — it will always be empty")
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
                wiring.setdefault(target_rel, {}).setdefault(name, {})[str(rel)] = (
                    name in forwarded)
                if name in declared and name not in forwarded:
                    if (target_rel, name) in PASSTHROUGH_EXEMPT:
                        continue
                    label = step.get("name", f"step {i}")
                    problems.append(
                        f"{rel}: '{label}' does not forward {name} to {target_rel} — "
                        f"the callee will use its own default")

    # Opt-in, and never a failure. The check above catches an input a caller
    # declares and forgets to wire; it cannot catch one a caller never declared
    # at all, because not declaring it is how a stack says it does not offer
    # the option — and `deb` reached the Go stack and not the Deno one exactly
    # that way. Most asymmetries are correct (wails3 does not take wails2's
    # options), so printing them on every run would only teach people to skip
    # the output. Reach for `--asymmetries` when wiring a new stack or hunting
    # an option that appears to do nothing.
    asymmetries: list[str] = []
    # Inputs no caller wires at all. The asymmetry report cannot show these —
    # it compares callers against each other, and unanimous silence looks like
    # agreement — yet they are the worse case: the option exists on the callee,
    # is documented there, and cannot be reached through the caller at all. A
    # workflow that sets one gets no error, because Actions ignores an unknown
    # `with:` key. That is how `task` reached the wails3 stack and never left
    # the root action, pinning every v3 build to <os>:build.
    unreachable: list[str] = []
    for callee, inputs in sorted(wiring.items()):
        for name, callers in sorted(inputs.items()):
            missing = sorted(c for c, ok in callers.items() if not ok)
            if not missing:
                continue
            if len(missing) == len(callers):
                unreachable.append(f"  {callee} :: {name}\n"
                                   f"      reached by no caller ({', '.join(missing)})")
                continue
            has = sorted(c for c, ok in callers.items() if ok)
            asymmetries.append(
                f"  {callee} :: {name}\n"
                f"      wired by  {', '.join(has)}\n"
                f"      not by    {', '.join(missing)}")

    if problems:
        print("\n".join(f"  {p}" for p in problems))
        print(f"\n{len(problems)} problem(s)")
        return 1

    print(f"checked {len(list(action_files()))} action.yml files — all sound")
    if "--asymmetries" in sys.argv:
        print(f"\n{len(asymmetries)} input(s) wired by some callers of a callee "
              f"and not others:\n")
        print("\n".join(asymmetries))
        print(f"\n{len(unreachable)} input(s) no caller wires — settable on the "
              f"callee, unreachable through it:\n")
        print("\n".join(unreachable))
    elif asymmetries or unreachable:
        print(f"({len(asymmetries)} caller asymmetries, {len(unreachable)} "
              f"unreachable inputs — run with --asymmetries to list them)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
