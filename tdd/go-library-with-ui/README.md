# go-library-with-ui fixture

The shape of `dAppCore/go-build`, which discovery got wrong the first time it
was pointed at a real repository: a Go module at `go/` with **no** `func
main()`, a genuine frontend in `ui/`, and a `package.json` in a dot-directory
that describes tooling.

It used to answer `wails2`, on the reasoning "Go plus a package.json". Two
things were wrong with that. A Wails app produces a binary, so a module with no
command cannot be one. And a manifest inside a dot-directory describes tooling
— `.claude-plugin`, `.github` — not a frontend.

The right answer is `core`: a library, tested and vetted, no artifact.
