# Sign (sub-action)

Purpose
- Unified signing step for macOS and Windows.
- macOS: imports certificates, signs the `.app` with `gon`, zips the `.app`, builds a `.pkg` (signed or unsigned), and notarizes on tag builds.
- Windows: signs the `.exe` and the NSIS installer using a provided PFX (base64) and password.

When it runs
- macOS: meaningful on `macOS` runners. Most operations only run when `sign != 'false'` AND the ref is a tag (`refs/tags/*`).
- Windows: meaningful on `Windows` runners. Runs when `sign != 'false'` AND `sign-windows-cert` is provided.

Inputs (union of previous per-OS signers)
- `sign` (default `false`) — enable/disable signing.
- `app-working-directory` (default `.`)
- `build-name` (required)
- macOS:
  - `sign-macos-apple-password` — app-specific password for Apple ID (`gon` uses this)
  - `sign-macos-app-id` — Developer ID Application subject
  - `sign-macos-app-cert` — Base64-encoded `.p12`
  - `sign-macos-app-cert-password` — Password for the Application certificate
  - `sign-macos-installer-id` — Developer ID Installer subject (optional)
  - `sign-macos-installer-cert` — Base64-encoded `.p12` (Installer)
  - `sign-macos-installer-cert-password` — Password for the Installer certificate
- Windows:
  - `sign-windows-cert` — Base64-encoded PFX contents
  - `sign-windows-cert-password` — Password for the PFX

Required project files (macOS)
- `build/darwin/gon-sign.json` — config for signing the `.app`
- `build/darwin/gon-notarize.json` — config for notarizing `.pkg` and `.app.zip`

Usage
```yaml
- name: Sign artifacts
  uses: snider/build/actions/sign@v3
  with:
    sign: 'true'
    app-working-directory: '.'
    build-name: 'wailsApp'
    # macOS
    sign-macos-apple-password: ${{ secrets.APPLE_PASSWORD }}
    sign-macos-app-id: ${{ secrets.MACOS_DEVELOPER_CERT_ID }}
    sign-macos-app-cert: ${{ secrets.MACOS_DEVELOPER_CERT }}
    sign-macos-app-cert-password: ${{ secrets.MACOS_DEVELOPER_CERT_PASSWORD }}
    sign-macos-installer-id: ${{ secrets.MACOS_INSTALLER_CERT_ID }}
    sign-macos-installer-cert: ${{ secrets.MACOS_INSTALLER_CERT }}
    sign-macos-installer-cert-password: ${{ secrets.MACOS_INSTALLER_CERT_PASSWORD }}
    # Windows
    sign-windows-cert: ${{ secrets.WIN_CERT_PFX_BASE64 }}
    sign-windows-cert-password: ${{ secrets.WIN_CERT_PASSWORD }}
```

Notes
- On macOS, `gon` must be installed (`actions/setup/go` installs it automatically on macOS).
- The `.app` zip is produced regardless of signing to ease distribution.
- Installer `.pkg` is signed when `sign == 'true'` and an installer ID is provided; otherwise an unsigned pkg is built on tags.
