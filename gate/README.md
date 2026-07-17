# gate/ — juncture CI gates

Shared GitLab CI includes that fire at the three points in a repo's life. Each
one contributes the canonical stage order (`lint → test → build → release`) plus
a hidden job template you extend with your repo's own commands — the gate owns
*when* it runs, your repo owns *what* it runs.

| File | Juncture | Fires on | Provides | Purpose |
|------|----------|----------|----------|---------|
| `push.yml` | push | branch push (no open MR) | `.gate-push` (stage `build`) | standard flow — does it still build |
| `pr.yml` | merge request | `merge_request_event` | `.gate-lint` (stage `lint`), `.gate-test` (stage `test`) | the merge gate: lint, then test |
| `release.yml` | release | git tag | `.gate-release` (stage `release`) | build the downloadable artifacts |

## Include

```yaml
include:
  - { project: 'dappcore/devops/build', file: '/gate/push.yml',    ref: dev }
  - { project: 'dappcore/devops/build', file: '/gate/pr.yml',      ref: dev }
  - { project: 'dappcore/devops/build', file: '/gate/release.yml', ref: dev }

build: { extends: .gate-push,    script: [ make build ] }
lint:  { extends: .gate-lint,    script: [ 'cd go', 'test -z "$(gofmt -l .)"', 'go vet ./...' ] }
test:  { extends: .gate-test,    script: [ 'cd go', 'go test -count=1 ./...' ] }
```

## Why lint blocks test

`lint` and `test` sit in adjacent stages. GitLab only starts the `test` stage
once every job in the `lint` stage has passed — so **a red linter skips the tests
and blocks the merge** without wasting a test run. Turn on the project setting
*Settings → Merge requests → Pipelines must succeed* so the MR cannot merge until
this pipeline is green (no admin override in GitLab CE).

`gitlab/graphify.yml` is the fourth include — the auxiliary code-graph refresh
(runs on `dev`/`main`, `allow_failure: true`), orthogonal to these gates.
