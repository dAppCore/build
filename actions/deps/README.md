# actions/deps — dappco.re bump tracker

Turns "an upstream `dappco.re/*` release exists" into a tracked work item.

The action scans a repo's `go.mod` for **direct** `dappco.re/*` requires, asks the
Go module proxy for the highest **stable** published version of each, and — if any
pin is behind — opens (or updates) a single `deps`-labelled issue whose body is a
checklist of the outstanding bumps. When every dependency is current again it
**closes** that issue.

The point: open `deps` issues across every repo ARE the ecosystem's version-bump
work queue. Filter by the label and you have the list, generated from CI + the
proxy — no hand-maintained dependency graph.

## Usage

Copy [`../workflows/deps-issue.yml`](../workflows/deps-issue.yml) to
`.github/workflows/deps.yml` in the consumer repo. It runs on a daily schedule,
on demand (`workflow_dispatch`, with a `dry-run` preview), and on an upstream
`repository_dispatch` of type `dep-bump`.

```yaml
- uses: dAppCore/build/actions/deps@v4
  with:
    go-mod-dir: go          # directory holding go.mod (Core repos: the go/ subdir)
  env:
    GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}   # needs `issues: write`
```

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| `go-mod-dir` | `go` | Directory containing `go.mod`; falls back to the repo root. |
| `label` | `deps` | Label used to find/track the single bump issue. |
| `title` | `chore(deps): dappco.re bumps available` | Exact issue title — the idempotency key (one open issue per repo). |
| `proxy` | `https://proxy.golang.org` | Module proxy base URL used to resolve the latest published version. |
| `dry-run` | `false` | When `true`, prints the computed title/body and touches no issues (no token needed). |

## Outputs

| Output | Description |
|--------|-------------|
| `stale-count` | Number of `dappco.re/*` deps with a newer release (`0` = all current). |
| `issue` | Issue number of the tracking issue when one was opened or updated. |

## Notes

- **Pull, not push.** Each repo self-reports its own stale deps from its own
  `go.mod` (the source of truth) using only the default `GITHUB_TOKEN` — no
  cross-repo dispatch secrets or hand-kept graph required. An upstream release
  *may* speed things up by firing a `dep-bump` `repository_dispatch`, but the
  daily poll is the safety net either way.
- **Direct deps only.** Indirect (`// indirect`) requires are excluded — they
  move when the direct dep that pulls them is bumped.
- **Stable only.** Pre-release and pseudo-versions are ignored when computing
  "latest", so a tracker never nags about an untagged commit.
