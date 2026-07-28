package main

import "strings"

// Greet exists so the fixture has something worth testing and benchmarking.
// The build fixture proved a binary comes out; this proves the test, coverage
// and benchmark steps have real work to do.
func Greet(names ...string) string {
	if len(names) == 0 {
		return "Hello, World!"
	}
	return "Hello, " + strings.Join(names, " and ") + "!"
}
