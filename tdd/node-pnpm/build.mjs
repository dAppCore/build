// A build with no dependencies, so the fixture measures the package manager
// rather than a network install. It still exercises the real path: the
// manager resolves its lockfile, runs the script, and the action finds the
// directory that appeared.
import { mkdirSync, writeFileSync } from 'node:fs';

mkdirSync('dist', { recursive: true });
writeFileSync(
  'dist/index.html',
  '<!doctype html><title>fixture</title><p>Built by dAppCore/build.</p>\n',
);
console.log('built dist/index.html');
