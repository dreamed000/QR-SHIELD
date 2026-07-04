This file contains the updated linting and development command snippets for the new modern Python toolchain, replacing outdated Flake8/Pylint references:

- `pip install -e ".[dev]"`

- `python -m black core/ tests/ qrshield.py`

- `python -m isort core/ tests/ qrshield.py`

- `python -m ruff check --fix core/ tests/ qrshield.py`

- `python -m mypy --ignore-missing-imports --python-version=3.10 core/ tests/ qrshield.py`

- `python -m pre_commit run --all-files`

- `python -m bandit -r core/ -ll`
