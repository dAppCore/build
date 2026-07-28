# wails3-root fixture

A Wails v3 project in the shape the real ones take: the Go module in `go/`, the
frontend beside it, and the build described by a Taskfile rather than by CLI
flags.

It does two jobs.

**Discovery.** It holds detection honest about the two things it used to get
wrong: a module one directory down is still a Go project, and Go + a frontend is
not automatically v2.

**Compilation.** `go/main.go` links `wails/v3/pkg/application`, so building it
exercises the real cgo and webview toolchain rather than asserting that a stack
exists. Every wails3 reference in CI used to be a discovery assertion; nothing
proved the stack could build anything.

The frontend is a copy rather than a bundler run. That keeps the two-stage
shape a real project has — frontend first, then Go — without making the fixture
depend on a node toolchain to prove a Go and cgo path.
