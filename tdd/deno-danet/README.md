# deno-danet fixture

A Danet application, small enough to compile in seconds and real enough to be
worth compiling: a `@Module` and a `@Controller` with a `@Get`, which only work
if `experimentalDecorators` and `emitDecoratorMetadata` are set in `deno.json`.

Danet's own starter defines `launch-server` and `test` and **no** build task —
a Deno server has nothing to bundle. So the artifact here is a `deno compile`
binary, which is what the adapter produces.

`run.ts` only listens when `DANET_FIXTURE_SERVE=1`, because a fixture that
bound a port in CI would never exit.
