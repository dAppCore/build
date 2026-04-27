# Makefile for testing GitHub Actions locally with act
# Requires: act (brew install act), Docker

.PHONY: help test test-all test-quick test-discovery test-options test-setup test-package test-smoke test-wails clean list \
	build-all build-go build-node build-deno build-cpp build-wails

# Default target
help:
	@echo "GitHub Actions Local Testing (via act)"
	@echo ""
	@echo "Quick start:"
	@echo "  make test-quick     Run fast tests (discovery, options)"
	@echo "  make test-all       Run all Linux tests"
	@echo ""
	@echo "Individual test targets:"
	@echo "  make test-discovery    Discovery sub-action tests"
	@echo "  make test-fixtures     Discovery fixture tests (stack detection)"
	@echo "  make test-options      Options computation tests"
	@echo "  make test-setup-go     Go/Wails setup tests"
	@echo "  make test-setup-npm    Node/npm setup tests"
	@echo "  make test-setup-conan  Conan setup tests"
	@echo "  make test-package      Package sub-action tests"
	@echo "  make test-smoke        Sub-actions smoke test"
	@echo "  make test-auto-stack   Auto stack routing smoke test"
	@echo "  make test-wails-env    Wails env mapping tests"
	@echo "  make test-wrapper      Wails2 wrapper tests"
	@echo ""
	@echo "Local Build Tests (no Docker):"
	@echo "  make build-all      Build all TDD hello worlds locally"
	@echo "  make build-go       Build Go CLI and HTTP projects"
	@echo "  make build-cpp      Build C++ project with CMake"
	@echo "  make build-node     Install and check Node.js project"
	@echo "  make build-deno     Type-check Deno project"
	@echo "  make build-wails    Build full Wails v2 project"
	@echo "  make build-clean    Remove build artifacts"
	@echo ""
	@echo "Utilities:"
	@echo "  make list           List all available CI jobs"
	@echo "  make dry-run        Dry run of all tests"
	@echo "  make pull-image     Pull the large Ubuntu image"
	@echo "  make clean          Remove all artifacts"
	@echo ""
	@echo "Options:"
	@echo "  ARCH=amd64          Run with x64 emulation (slower on M3)"
	@echo "  VERBOSE=1           Enable verbose output"
	@echo ""
	@echo "Examples:"
	@echo "  make build-all                    # Test local compilation"
	@echo "  make test-discovery               # Test via act/Docker"
	@echo "  make test-quick VERBOSE=1"
	@echo "  make test-setup-go ARCH=amd64"

# Architecture flag (default ARM64 for M3, can override with ARCH=amd64)
ifeq ($(ARCH),amd64)
  ARCH_FLAG := --container-architecture linux/amd64
else
  ARCH_FLAG := --container-architecture linux/arm64
endif

# Verbose flag
ifeq ($(VERBOSE),1)
  VERBOSE_FLAG := -v
else
  VERBOSE_FLAG :=
endif

# Base act command (specify workflow to avoid ambiguity with wails-build.yml and wails2.yml)
ACT := act -W .github/workflows/ci.yml $(ARCH_FLAG) $(VERBOSE_FLAG)

# Pull the large image first (saves time on subsequent runs)
pull-image:
	docker pull catthehacker/ubuntu:full-latest

# List all jobs in the workflow
list:
	@$(ACT) -l

# Dry run (shows what would execute without running)
dry-run:
	$(ACT) -n

# =============================================================================
# Quick Tests (fast, no heavy toolchain setup)
# =============================================================================

test-quick: test-discovery test-fixtures test-options
	@echo "✓ Quick tests passed"

# =============================================================================
# Discovery Tests
# =============================================================================

test-discovery:
	@echo "==> Running discovery tests..."
	$(ACT) -j discovery-tests

test-fixtures:
	@echo "==> Running discovery fixture tests..."
	$(ACT) -j discovery-fixture-tests

# =============================================================================
# Options Tests
# =============================================================================

test-options:
	@echo "==> Running options tests..."
	$(ACT) -j options-tests

# =============================================================================
# Setup Tests (require toolchain downloads)
# =============================================================================

test-setup: test-setup-go test-setup-npm test-setup-conan
	@echo "✓ Setup tests passed"

test-setup-go:
	@echo "==> Running Go/Wails setup tests..."
	$(ACT) -j setup-go-tests

test-setup-npm:
	@echo "==> Running npm setup tests..."
	$(ACT) -j setup-npm-tests

test-setup-conan:
	@echo "==> Running Conan setup tests..."
	$(ACT) -j setup-conan-tests

# =============================================================================
# Package Tests
# =============================================================================

test-package:
	@echo "==> Running package tests..."
	$(ACT) -j package-tests

test-package-smoke:
	@echo "==> Running package smoke test..."
	$(ACT) -j package-smoke-ubuntu

# =============================================================================
# Integration / Smoke Tests
# =============================================================================

test-smoke:
	@echo "==> Running sub-actions smoke test..."
	$(ACT) -j subactions-smoke

test-auto-stack:
	@echo "==> Running auto-stack routing smoke test..."
	$(ACT) -j auto-stack-smoke

# =============================================================================
# Wails-specific Tests
# =============================================================================

test-wails-env:
	@echo "==> Running Wails env mapping tests..."
	$(ACT) -j wails-env-mapping
	$(ACT) -j wails-env-mapping-wrapper

test-wrapper:
	@echo "==> Running Wails2 wrapper tests..."
	$(ACT) -j wrapper-wails2

test-matrix:
	@echo "==> Running matrix root action tests..."
	$(ACT) -j matrix-root-action

test-readme:
	@echo "==> Running README snippets validation..."
	$(ACT) -j readme-snippets

test-build-wails2:
	@echo "==> Running actual Wails2 build test..."
	$(ACT) -j build-wails2

# =============================================================================
# Full Test Suite
# =============================================================================

test-all: test-discovery test-fixtures test-options test-setup test-package test-smoke test-auto-stack test-wails-env
	@echo ""
	@echo "=========================================="
	@echo "✓ All Linux tests passed"
	@echo "=========================================="

# Alias
test: test-quick

# =============================================================================
# Local Build Tests (test compilation without Docker)
# =============================================================================

TDD := tdd
BUILD_DIR := $(TDD)/.build

build-all: build-go build-cpp build-node build-deno
	@echo ""
	@echo "=========================================="
	@echo "All TDD hello worlds compiled successfully"
	@echo "=========================================="

build-go:
	@echo "==> Building Go projects..."
	@mkdir -p $(BUILD_DIR)
	cd $(TDD)/go-cli && go build -o ../../$(BUILD_DIR)/go-cli .
	cd $(TDD)/go-http && go build -o ../../$(BUILD_DIR)/go-http .
	@echo "Go CLI:"
	@./$(BUILD_DIR)/go-cli "TDD Test"
	@echo "Go HTTP: compiled successfully (not running server)"

build-go-versions:
	@echo "==> Testing Go version compatibility..."
	@for v in 1.21 1.22 1.23; do \
		echo "Testing Go $$v..."; \
		cd $(TDD)/go-cli && go mod edit -go=$$v && go build -o /dev/null . && echo "  Go $$v: OK"; \
	done
	cd $(TDD)/go-cli && go mod edit -go=1.21

build-cpp:
	@echo "==> Building C++ projects..."
	@mkdir -p $(BUILD_DIR)/cpp
	cd $(BUILD_DIR)/cpp && cmake ../../cpp-hello && make
	@echo "C++ hello:"
	@./$(BUILD_DIR)/cpp/hello "TDD Test"

build-node:
	@echo "==> Building Node.js projects..."
	cd $(TDD)/node-http && npm install --silent
	@echo "Node HTTP: dependencies installed, checking syntax..."
	cd $(TDD)/node-http && node --check index.js
	@echo "Node HTTP: OK"

build-deno:
	@echo "==> Checking Deno projects..."
	@if command -v deno >/dev/null 2>&1; then \
		cd $(TDD)/deno-http && deno check main.ts; \
		echo "Deno HTTP: OK"; \
	else \
		echo "Deno not installed, skipping (install with: brew install deno)"; \
	fi

build-wails:
	@echo "==> Building Wails v2 project (requires frontend build first)..."
	@if [ ! -d "$(TDD)/wails2-root/frontend/dist" ]; then \
		echo "Building frontend..."; \
		cd $(TDD)/wails2-root/frontend && npm install --silent && npm run build; \
	fi
	cd $(TDD)/wails2-root && go build -o ../../$(BUILD_DIR)/wails2-app .
	@echo "Wails v2: compiled successfully"

build-clean:
	@echo "Cleaning build artifacts..."
	rm -rf $(BUILD_DIR)
	rm -rf $(TDD)/node-http/node_modules
	rm -rf $(TDD)/wails2-root/frontend/node_modules
	rm -rf $(TDD)/wails2-root/frontend/dist
	@echo "Done"

# =============================================================================
# Cleanup
# =============================================================================

clean: build-clean
	@echo "Cleaning up act artifacts..."
	rm -rf .act-*
	@echo "Done"
