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

## Turning it off

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    package: false
```

Nothing is uploaded and no release is created, whatever the ref.
