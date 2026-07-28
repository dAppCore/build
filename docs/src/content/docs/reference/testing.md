---
title: Tests, coverage & benchmarks
description: Detected by default, reported on request.
---

The Go stack runs tests before it builds. A suite that fails should not be
followed by minutes of compiling and packaging something nobody will ship.

## Detection

`test` is `auto` by default: run them if the module has any `*_test.go`, and
say so if it does not.

| `test` | |
| :-- | :-- |
| `auto` | run when tests exist; emit a notice and continue when they do not |
| `true` | require tests — a module that should have them and does not fails |
| `false` | skip |

The middle setting is the useful one for a repository that has decided tests
are not optional. A silent skip and a pass look identical in a green tick;
`true` makes the difference visible.

## Coverage

Off by default, because a profile costs time and most builds do not read it.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool
    coverage: true
    coverage-threshold: 70
```

`coverage-threshold` fails the job below that percentage. `0`, the default,
measures without judging. The percentage is exposed as the `COVERAGE` output
either way.

## Codecov

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool
    codecov: true
    codecov-token: ${{ secrets.CODECOV_TOKEN }}
```

`codecov: true` implies `coverage: true` — there is nothing to upload
otherwise. Public repositories can upload without a token; private ones need
one. An upload failure does not fail the build, because a reporting outage is
not a defect in your code.

## Benchmarks

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool
    benchmarks: true
```

Runs with `-run='^$'` so no test executes twice — benchmarks are a separate
reading, and rerunning the suite would add noise and time. Results land in the
job summary and in `benchmarks.txt`.

Note what this does **not** do: compare against a previous run, or fail on a
regression. Runner hardware varies between jobs enough to make that a source of
false alarms rather than a signal. The numbers are for a human to read.

## The race detector

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: mytool
    race: true
```
