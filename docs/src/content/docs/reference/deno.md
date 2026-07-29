---
title: Optional Deno step
description: Environment-first, and skipped unless asked for.
---

Deno is not required and does nothing unless configured. It exists so a Deno
build or asset step can run before the main application build, and it is
configured through the environment rather than inputs — which means a job can
enable it without the action's signature changing.

Precedence: **environment > inputs > defaults**. With nothing set, Deno is
skipped.

| Variable | Meaning |
| :-- | :-- |
| `DENO_ENABLE` | `true`/`1`/`yes`/`on` — enable even without a build command. |
| `DENO_BUILD` | The command to run, e.g. `deno task build`. |
| `DENO_VERSION` | e.g. `v1.44.x`. |
| `DENO_WORKDIR` | Working directory. Defaults to `.`. |

Pass-throughs when present: `DENO_AUTH_TOKEN`, `DENO_DIR`, `HTTP_PROXY`,
`HTTPS_PROXY`, `NO_PROXY`.

## Job-level

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    env:
      DENO_VERSION: 'v1.44.x'
      DENO_WORKDIR: 'frontend'
      DENO_BUILD: 'deno task build'
    steps:
      - uses: actions/checkout@v7
      - uses: dAppCore/build@v4
        with:
          build-name: myApp
```

## From a previous step

```yaml
- run: |
    echo "DENO_ENABLE=true" >> "$GITHUB_ENV"
    echo "DENO_BUILD=deno task build" >> "$GITHUB_ENV"
- uses: dAppCore/build@v4
  with:
    build-name: myApp
```

## Private modules

```yaml
env:
  DENO_AUTH_TOKEN: ${{ secrets.DENO_AUTH_TOKEN }}
```
