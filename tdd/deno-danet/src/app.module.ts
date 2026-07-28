// A Danet module and controller, reduced to the parts that make the decorator
// metadata real. If experimentalDecorators or emitDecoratorMetadata were
// missing from deno.json this would not compile — which is the point: the
// fixture fails on the same misconfiguration a real app would.

import { Controller, Get, Module } from '@danet/core';

@Controller('')
export class HelloController {
	@Get()
	hello(): string {
		return 'Hello from Danet';
	}
}

@Module({
	controllers: [HelloController],
})
export class AppModule {}
