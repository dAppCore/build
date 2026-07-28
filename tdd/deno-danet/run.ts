// run.ts is the entry file the Danet CLI generates, and what the adapter
// compiles by default.

import { DanetApplication } from '@danet/core';

import { AppModule } from './src/app.module.ts';

const application = new DanetApplication();
// init takes the module class, not an instance — Danet constructs it.
await application.init(AppModule);

// Compiled rather than served in CI: the fixture exists to prove the build
// produces a runnable binary, and a server that listens would never exit.
if (Deno.env.get('DANET_FIXTURE_SERVE') === '1') {
	await application.listen(3000);
} else {
	console.log('danet-fixture ok');
}
