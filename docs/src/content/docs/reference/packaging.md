---
title: Packaging & releases
description: Artifact naming, and what happens on a tag.
---

## Artifact names

Composed from discovery, so a matrix build produces names you can tell apart
without reading the job title:

```
<build-name>_<OS>_<ARCH>_<TAG or SHORT_SHA>
```

```
myApp_Ubuntu-22.04_amd64_ab12cd3
myApp_macos_arm64_v1.2.3
```

Branch and pull-request builds use the short SHA; tag builds use the tag.

## Releases

A release is published **only** on a `refs/tags/*` ref. Branch and PR builds
upload artifacts and stop there, so nothing you push to a branch can create a
release by accident.

```yaml
on:
  push:
    branches: [main]
    tags: ["v*"]
```

With that trigger, `main` gives you downloadable artifacts and `v1.2.3` gives
you a release.

## Release assets

Each platform stages its binary as one zip, `<prefix>-<os>-<arch>.zip`, holding
the binary under its own name. Two things follow from that shape.

The name carries no version, so `/releases/latest/download/core-linux-amd64.zip`
resolves — which is what makes a release usable as a download source rather than
only as a record. And the archive extracts to `core`, not `core-linux-amd64`,
because the second is a name nobody wants to type or put on `PATH`.

`zip` does the work on Linux and macOS and keeps the executable bit. Windows has
no `zip`, so PowerShell's `Compress-Archive` covers it — it ships with the OS.
7-Zip is deliberately not used: it happens to be on GitHub's images, which is
exactly what makes assuming it a trap on any other runner.

## Debian packages

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: core
    deb: true
    deb-maintainer: "Lethean <dev@lethean.io>"
    deb-description: "Core developer CLI"
```

A zip is a download; a `.deb` is an install:

```bash
sudo apt install ./core_1.2.3_amd64.deb
core --version
sudo apt remove core
```

The package goes on PATH, is recorded in the package database, and comes off
cleanly — none of which unzipping does.

Linux runners only, and only on a tag. A macOS or Windows Debian package is not
a thing, so the step says so and skips rather than failing the job for asking.

`dpkg-deb` builds it, since it is already on every Ubuntu runner. Architecture is
translated from GOARCH, because the two vocabularies agree on `amd64` and
`arm64` and disagree on the rest — `386` has to ship as `i386` or apt will not
install it on the machine it was built for.

Currently wired for the Go stack. Other stacks accept the input and ignore it.

## Turning it off

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    package: false
```

Nothing is uploaded and no release is created, whatever the ref.
