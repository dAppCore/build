# wails3-root fixture

A Wails v3 project in the shape the real ones take: the Go module in `go/`, the
frontend beside it, and the build described by a Taskfile rather than by CLI
flags.

Exists to hold discovery honest about two things it used to get wrong:

- a module one directory down is still a Go project
- Go + a frontend is not automatically v2

Nothing here is built. The files carry only the markers discovery reads.
