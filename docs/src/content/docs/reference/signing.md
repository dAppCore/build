---
title: Code signing
description: macOS notarisation and Windows signtool, both tag-gated.
---

Signing is off by default and gated on tags even when enabled, so branch builds
never touch your certificates.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    sign: true
```

## macOS

Runs on tags only:

1. Import the code-signing and installer certificates
2. Sign the `.app` with `gon`
3. Zip the `.app`
4. Build the `.pkg` installer
5. Notarise with `gon`

Needs certificates and an Apple ID in secrets. `gon` is installed by
`setup/go` on macOS runners.

## Windows

Decodes a base64 certificate from secrets and signs the `.exe` and the
installer with `signtool` from the Windows SDK.

## Checking it before you need it

Both platforms have a dry-run diagnostic in the repository's own CI: it reports
whether `gon` and `signtool.exe` were found, and stays green either way. Useful
for confirming a runner has what it needs before a release depends on it.

## Forks

Every check in the repository's CI runs without secrets, so a fork's builds
pass. Signing is simply skipped where the secrets are absent.
