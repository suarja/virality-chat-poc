# Project Structure Documentation

## Directory Structure

```
virality-chat-poc/
├── src/
│   └── virality_chat_poc/      # Main package code
│       ├── models/             # Pydantic models
│       ├── pipeline/           # Analysis pipeline
│       └── utils/              # Utility functions
├── tests/                      # All test files
│   ├── mock_gemini.py         # Mock data generators
│   └── generate_mock_analyses.py
├── scripts/                    # Project scripts
│   ├── setup_project.py       # Project setup
│   ├── validate_setup.py      # Validation
│   └── run_*.py              # Various run scripts
├── data/                      # Data directory
│   ├── raw/                   # Raw data
│   └── processed/             # Processed data
├── logs/                      # Log files
├── docs/                      # Documentation
├── notebooks/                 # Jupyter notebooks
└── memory-bank/              # Memory bank files
```

## Key Components

1. **Source Code (`src/virality_chat_poc/`)**

   - Contains all the main package code
   - Models, pipeline, and utilities

2. **Tests (`tests/`)**

   - All test files are centralized here
   - Includes mock data generators
   - Unit tests and integration tests

3. **Scripts (`scripts/`)**

   - Project setup and validation
   - Pipeline execution scripts
   - Evaluation scripts

4. **Data Management**

   - Raw data in `data/raw/`
   - Processed data in `data/processed/`
   - Logs in `logs/`

5. **Documentation**
   - Technical documentation in `docs/`
   - Jupyter notebooks in `notebooks/`
   - Memory bank in `memory-bank/`

## File Organization Principles

1. **Centralized Testing**

   - All test files are in the `tests/` directory
   - Mock data generators are part of the test suite
   - Test utilities are shared across test files

2. **Clear Separation of Concerns**

   - Source code is isolated in `src/`
   - Scripts are in `scripts/`
   - Data and logs have dedicated directories

3. **Documentation Strategy**
   - Technical docs in `docs/`
   - Interactive examples in `notebooks/`
   - Project memory in `memory-bank/`

## Development Guidelines

1. **Adding New Features**

   - Place implementation in appropriate `src/` subdirectory
   - Add tests in `tests/`
   - Update documentation in `docs/`

2. **Running Tests**

   - Use pytest from project root
   - Mock data available in `tests/`

3. **Project Setup**
   - Use `scripts/setup_project.py`
   - Validate with `scripts/validate_setup.py`
