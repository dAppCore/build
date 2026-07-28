package main

import "testing"

func TestGreet_NoNames(t *testing.T) {
	if got := Greet(); got != "Hello, World!" {
		t.Fatalf("Greet() = %q", got)
	}
}

func TestGreet_OneName(t *testing.T) {
	if got := Greet("Ada"); got != "Hello, Ada!" {
		t.Fatalf("Greet(Ada) = %q", got)
	}
}

func TestGreet_TwoNames(t *testing.T) {
	if got := Greet("Ada", "Grace"); got != "Hello, Ada and Grace!" {
		t.Fatalf("Greet(Ada, Grace) = %q", got)
	}
}

func BenchmarkGreet(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_ = Greet("Ada", "Grace")
	}
}
