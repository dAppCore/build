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
2. Sign the `.app` with `codesign`
3. Zip the `.app`
4. Build the `.pkg` installer
5. Notarise with `xcrun notarytool` and staple the ticket, when `notarize` is on

`codesign` and `notarytool` both ship with the Xcode command line tools, so
there is nothing to install and no configuration file to write.

`gon` used to do steps 2 and 5. It has been unmaintained since 2022, and
`notarytool` is Apple's supported path — it also staples, so the app validates
on first launch without a network round trip. The two `gon-*.json` files are no
longer read; what they configured is inputs now.

```yaml
- uses: dAppCore/build@v4
  with:
    build-name: myApp
    build-platform: darwin/universal
    sign: true
    notarize: true
    dmg: true
    sign-macos-app-id: ${{ secrets.MACOS_APP_ID }}
    sign-macos-app-cert: ${{ secrets.MACOS_APP_CERT }}
    sign-macos-app-cert-password: ${{ secrets.MACOS_APP_CERT_PASSWORD }}
    sign-macos-app-email: ${{ secrets.APPLE_ID }}
    sign-macos-app-team-id: ${{ secrets.APPLE_TEAM_ID }}
    sign-macos-apple-password: ${{ secrets.APPLE_APP_PASSWORD }}
```

`build/darwin/entitlements.plist` is passed to `codesign --entitlements` when
it exists and skipped when it does not.

### Sparkle

`sign-sparkle: true` signs a bundled Sparkle framework. Sparkle ships XPC
services and helper apps inside the framework and the outer signature does not
cover them — a bundle missing those individual signatures passes `codesign` and
then fails notarisation.

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
