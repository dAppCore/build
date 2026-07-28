// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Documentation for dAppCore/build, served from GitHub Pages at
// https://dappco.re/build/. The base path is the repository name because this
// is a project page under the organisation's domain, not a site of its own.
export default defineConfig({
	site: 'https://dappco.re',
	base: '/build',
	integrations: [
		starlight({
			title: 'dAppCore/build',
			description:
				'One GitHub Action that detects your stack and builds it — Wails v3, Wails v2, and plain Go, on Linux, macOS and Windows.',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/dAppCore/build' },
			],
			customCss: ['./src/styles/lethean.css'],
			editLink: {
				baseUrl: 'https://github.com/dAppCore/build/edit/main/docs/',
			},
			sidebar: [
				{
					label: 'Start here',
					items: [
						{ label: 'What this is', link: '/' },
						{ label: 'Quickstart', slug: 'quickstart' },
						{ label: 'How detection works', slug: 'detection' },
					],
				},
				{
					label: 'Stacks',
					items: [
						{ label: 'Wails v3', slug: 'stacks/wails3' },
						{ label: 'Wails v2', slug: 'stacks/wails2' },
						{ label: 'C++', slug: 'stacks/cpp' },
						{ label: 'Go libraries', slug: 'stacks/core' },
					],
				},
				{
					label: 'Reference',
					items: [
						{ label: 'Inputs', slug: 'reference/inputs' },
						{ label: 'Sub-actions', slug: 'reference/sub-actions' },
						{ label: 'Packaging & releases', slug: 'reference/packaging' },
						{ label: 'Code signing', slug: 'reference/signing' },
						{ label: 'Optional Deno step', slug: 'reference/deno' },
					],
				},
			],
		}),
	],
});
