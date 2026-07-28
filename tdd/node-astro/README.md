# node-astro fixture

An Astro site with one page — enough to prove the Node runtime stack picks the
astro adapter, installs, runs the build, and finds `dist/`.

Deliberately not the docs site: this needs to install and build in seconds on
three runners, and it should fail for framework reasons rather than because
somebody edited a documentation page.
