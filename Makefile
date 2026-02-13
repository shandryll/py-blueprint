# =================================================================================================
# PY-BLUEPRINT - Makefile (Windows/Linux/Mac compatible)
# =================================================================================================

# VARIABLES
VENV_DIR := .venv

# Detect OS for cross-platform commands
UNAME_S := $(shell uname -s 2>/dev/null || echo Windows)

.PHONY: help dev lint format test sync clean venv pre-commit

# =================================================================================================
# HELP
# =================================================================================================
help:
	@echo ""
	@echo "PY-BLUEPRINT - Available commands:"
	@echo ""
	@echo "  make venv     # Create virtual environment"
	@echo "  make sync     # Install/update dependencies"
	@echo "  make dev      # Start FastAPI server (http://0.0.0.0:8000)"
	@echo "  make lint     # Lint + auto-fix (using ruff)"
	@echo "  make format   # Format code (using ruff)"
	@echo "  make test     # Run tests (using pytest)"
	@echo "  make clean    # Clean caches + virtual environments"
	@echo "  make help     # Show this help"
	@echo ""

# =================================================================================================
# DEVELOPMENT
# =================================================================================================
dev:
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# =================================================================================================
# CODE QUALITY
# =================================================================================================
lint:
	uv run ruff check . --fix
	@echo "Lint completed!"

format:
	uv run ruff format .
	@echo "Code formatted!"

pre-commit: lint format
	@echo "Pre-commit: lint + format OK!"

# =================================================================================================
# TESTS
# =================================================================================================
test:
	uv run pytest

# =================================================================================================
# MANAGEMENT
# =================================================================================================
sync:
	uv sync --dev
	@echo "Dependencies synced!"

# =================================================================================================
# VIRTUAL ENVIRONMENT
# =================================================================================================
venv:
	@echo "Creating virtual environment..."
	@if [ -d "$(VENV_DIR)" ]; then \
		echo ".venv already exists! Run 'make clean' first."; \
	else \
		uv venv; \
		if [ -d "$(VENV_DIR)" ]; then \
			echo ""; \
			echo "SUCCESS: Virtual environment created: $(VENV_DIR)"; \
			echo ""; \
			echo "Activate with one of these commands:"; \
			echo "  Unix/Mac: source $(VENV_DIR)/bin/activate"; \
			echo "  Windows:  $(VENV_DIR)\\Scripts\\activate"; \
			echo ""; \
		else \
			echo "ERROR: .venv not created. Check uv installation."; \
		fi; \
	fi

clean:
	uv cache clean
	rm -rf .coverage htmlcov/ dist/ build/ .pytest_cache/ $(VENV_DIR)
	@echo "Project cleaned (including $(VENV_DIR))!"
