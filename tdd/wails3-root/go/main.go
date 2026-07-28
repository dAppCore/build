// A Wails v3 application reduced to the part that matters here: it links the
// real application package, so building it proves the wails3 stack can drive a
// cgo + webview toolchain end to end. It is never run.

package main

import (
	"embed"
	"log"

	"github.com/wailsapp/wails/v3/pkg/application"
)

// The frontend is embedded from go/assets rather than built by npm. A real
// project compiles its frontend first and embeds the output; the Taskfile
// models that with a copy, so the build has the same shape without making the
// fixture depend on a node toolchain.
//
//go:embed all:assets
var assets embed.FS

func main() {
	app := application.New(application.Options{
		Name:        "wails3-fixture",
		Description: "Build fixture for dAppCore/build",
		Assets: application.AssetOptions{
			Handler: application.AssetFileServerFS(assets),
		},
	})

	app.Window.New()

	if err := app.Run(); err != nil {
		log.Fatal(err)
	}
}
