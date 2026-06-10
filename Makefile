# Basic workflow automation steps, primarily aimed at local development.

all: test black flake8 mypy

# Set up a virtual environment.
venv: dev-requirements.txt requirements.txt
	python -m venv --system-site-packages venv
	venv/bin/pip install --upgrade pip wheel setuptools pip-tools
	venv/bin/pip install -r dev-requirements.txt
	venv/bin/pip install -e .[dev]
	touch venv

.PHONY: clean
clean:
	rm -rf ./venv ./build

# Clean and re-initialize the venv
.PHONY: rebuild
rebuild: clean venv

# sync virtual environment with any new dependencies added to requirements.txt
.PHONY:
refresh-deps: venv
	venv/bin/pip-compile --rebuild --resolver=backtracking --no-emit-index-url --strip-extras -o requirements.txt pyproject.toml
	venv/bin/pip-compile --rebuild --resolver=backtracking --no-emit-index-url --extra dev -o dev-requirements.txt pyproject.toml
	# Re-sync requirements and reinstall this package
	venv/bin/pip-sync dev-requirements.txt
	venv/bin/pip install -e .

# Update a single dependency to its latest version everywhere
.PHONY:
full-refresh: venv
	venv/bin/pip-compile --upgrade-package $(DEPENDENCY) --rebuild --resolver=backtracking --no-emit-index-url -o requirements.txt pyproject.toml
	venv/bin/pip-compile --upgrade-package $(DEPENDENCY) --rebuild --resolver=backtracking --no-emit-index-url --extra dev -o dev-requirements.txt pyproject.toml
	# Re-sync requirements and reinstall this package
	venv/bin/pip-sync dev-requirements.txt
	venv/bin/pip install -e .

# Fully regenerates requirements files.
.PHONY:
full-refresh-all-deps: venv
	venv/bin/pip-compile --upgrade --rebuild --resolver=backtracking --no-emit-index-url -o requirements.txt pyproject.toml
	venv/bin/pip-compile --upgrade --rebuild --resolver=backtracking --no-emit-index-url --extra dev -o dev-requirements.txt pyproject.toml
	# Re-sync requirements and reinstall this package
	venv/bin/pip-sync dev-requirements.txt
	venv/bin/pip install -e .

# Run the configured pre-commit checks against the repo.
.PHONY:
pre-commit:
	pre-commit run --all-files

# Run unit tests
test: venv
	venv/bin/pytest \
		--cov=src \
		--cov-report term-missing \
		--cov-report html:build/coverage/ \
		--cov-report xml:build/coverage/coverage.xml \
		--md-report \
		--md-report-output=build/unit_test_results.md \
		--md-report-zeros=empty \
		--md-report-color=never

## Linters ##

# Check formatting with Black; fails if it would reformat but doesn't take action.
# Run the reformat target to actually change files.
black: venv
	venv/bin/black --check .

# Reformat using isort and black together.
reformat: 
	venv/bin/isort .
	venv/bin/black .

# flake8 (linter)
flake8: venv
	venv/bin/flake8 .

# mypy (type checks)
mypy: venv
	venv/bin/mypy src
