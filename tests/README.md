# mcpie Test Suite

This directory contains comprehensive unit tests for the mcpie CLI output controls and pipe-friendliness features.

## Test Files

### Core Tests
- `test_output_formatters.py` - Tests for all output formatter classes (JSON, Pretty, Table, YAML, Raw)
- `test_cli_options.py` - Tests for CLI option parsing and validation
- `test_stdin_input.py` - Tests for stdin input handling
- `test_exit_codes.py` - Tests for exit code behavior
- `test_integration.py` - Integration tests for complete CLI workflows

### Summary Tests
- `test_summary.py` - Comprehensive test showing all major features work together

## Running Tests

### Install Dependencies
```bash
uv sync --group dev
```

### Run All Tests
```bash
uv run python -m pytest tests/ -v
```

### Run Specific Test Files
```bash
uv run python -m pytest tests/test_output_formatters.py -v
uv run python -m pytest tests/test_cli_options.py -v
uv run python -m pytest tests/test_exit_codes.py -v
```

### Run Summary Test
```bash
uv run python tests/test_summary.py
```

### Run Custom Test Runner
```bash
uv run python run_tests.py
```

## Test Coverage

The test suite covers all major features specified in the output controls and pipe-friendliness spec:

### ✅ Output Formats
- JSON output (compact machine-readable)
- Pretty JSON output (indented with formatting)
- Table output (tabular view for lists)
- YAML output (YAML format)
- Raw output (extract just the relevant content)

### ✅ CLI Options
- `--output json|pretty|table|yaml|raw` - Output format selection
- `-q, --quiet` - Suppress non-essential output
- `-v, --verbose` - Verbose output mode
- `-o, --output-file` - Write output to file
- `--stdin` - Accept input from stdin

### ✅ Pipe-Friendly Features
- Clean stdout/stderr separation
- Stdin input handling (JSON and plain text)
- File output functionality
- Quiet mode for scripting

### ✅ Exit Codes
- `0` - Success
- `1` - CLI or transport error
- `2` - Server-side error
- `3` - Invalid JSON/input

### ✅ Integration Features
- Output formatter integration with MCPSession
- Complete CLI workflow testing
- Error handling and validation

## Test Structure

Each test file follows the pattern:
- Unit tests for individual components
- Integration tests for component interaction
- Error handling tests
- Edge case testing

The tests use mocking to isolate components and avoid external dependencies, making them fast and reliable.

## Example Test Output

```bash
$ uv run python tests/test_summary.py
✅ All major features are working correctly!
✅ Feature integration test passed!
```

## Notes

- Tests are designed to be independent and can run in any order
- Mock objects are used to avoid external dependencies
- All major features from the spec are covered
- Both unit and integration tests are included 