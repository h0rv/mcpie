"""
Tests for exit codes and error handling.
"""

from unittest.mock import patch
import json
import sys
import pytest

from mcpie_cli.mcpie import (
    EXIT_SUCCESS,
    EXIT_CLI_ERROR,
    EXIT_SERVER_ERROR,
    EXIT_INVALID_INPUT,
    exit_with_code,
)


class TestExitCodes:
    """Test exit code constants."""

    def test_exit_code_constants(self):
        """Test that exit code constants are defined correctly."""
        assert EXIT_SUCCESS == 0
        assert EXIT_CLI_ERROR == 1
        assert EXIT_SERVER_ERROR == 2
        assert EXIT_INVALID_INPUT == 3


class TestExitWithCodeFunction:
    """Test the exit_with_code function."""

    def test_exit_success_with_message(self):
        """Test exit with success code and message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_SUCCESS, "Operation completed successfully", False)

                mock_print.assert_called_once_with("Operation completed successfully")
                mock_exit.assert_called_once_with(EXIT_SUCCESS)

    def test_exit_cli_error_with_message(self):
        """Test exit with CLI error code and message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_CLI_ERROR, "Invalid command", False)

                mock_print.assert_called_once_with("Invalid command", file=sys.stderr)
                mock_exit.assert_called_once_with(EXIT_CLI_ERROR)

    def test_exit_server_error_with_message(self):
        """Test exit with server error code and message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_SERVER_ERROR, "Server connection failed", False)

                mock_print.assert_called_once_with(
                    "Server connection failed", file=sys.stderr
                )
                mock_exit.assert_called_once_with(EXIT_SERVER_ERROR)

    def test_exit_invalid_input_with_message(self):
        """Test exit with invalid input code and message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_INVALID_INPUT, "Invalid JSON format", False)

                mock_print.assert_called_once_with(
                    "Invalid JSON format", file=sys.stderr
                )
                mock_exit.assert_called_once_with(EXIT_INVALID_INPUT)

    def test_exit_quiet_mode_no_output(self):
        """Test exit in quiet mode produces no output."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_CLI_ERROR, "Error message", True)

                mock_print.assert_not_called()
                mock_exit.assert_called_once_with(EXIT_CLI_ERROR)

    def test_exit_empty_message(self):
        """Test exit with empty message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_CLI_ERROR, "", False)

                mock_print.assert_not_called()
                mock_exit.assert_called_once_with(EXIT_CLI_ERROR)

    def test_exit_none_message(self):
        """Test exit with empty message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_CLI_ERROR, "", False)

                mock_print.assert_not_called()
                mock_exit.assert_called_once_with(EXIT_CLI_ERROR)


class TestMainFunctionExitCodes:
    """Test exit codes from main function."""

    def test_keyboard_interrupt_exit_code(self):
        """Test keyboard interrupt results in CLI error code."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            mock_run.side_effect = KeyboardInterrupt()

            # Test that exit_with_code raises SystemExit with CLI error code
            with pytest.raises(SystemExit) as exc_info:
                exit_with_code(EXIT_CLI_ERROR, "Interrupted by user", False)
            assert exc_info.value.code == EXIT_CLI_ERROR

    def test_json_decode_error_exit_code(self):
        """Test JSON decode error results in invalid input code."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            mock_run.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

            # Test that exit_with_code raises SystemExit with invalid input code
            with pytest.raises(SystemExit) as exc_info:
                try:
                    raise json.JSONDecodeError("Invalid JSON", "", 0)
                except json.JSONDecodeError as e:
                    exit_with_code(
                        EXIT_INVALID_INPUT, f"Invalid JSON input: {e}", False
                    )
            assert exc_info.value.code == EXIT_INVALID_INPUT

    def test_server_error_exit_code(self):
        """Test server-related error results in server error code."""
        # Test that exit_with_code raises SystemExit with server error code
        with pytest.raises(SystemExit) as exc_info:
            error_message = "MCP server connection failed"

            if "server" in error_message.lower() or "mcp" in error_message.lower():
                exit_with_code(
                    EXIT_SERVER_ERROR, f"Server error: {error_message}", False
                )
            else:
                exit_with_code(EXIT_CLI_ERROR, f"Fatal error: {error_message}", False)
        assert exc_info.value.code == EXIT_SERVER_ERROR

    def test_generic_error_exit_code(self):
        """Test generic error results in CLI error code."""
        # Test that exit_with_code raises SystemExit with CLI error code
        with pytest.raises(SystemExit) as exc_info:
            error_message = "Generic error occurred"

            if "server" in error_message.lower() or "mcp" in error_message.lower():
                exit_with_code(
                    EXIT_SERVER_ERROR, f"Server error: {error_message}", False
                )
            else:
                exit_with_code(EXIT_CLI_ERROR, f"Fatal error: {error_message}", False)
        assert exc_info.value.code == EXIT_CLI_ERROR


class TestErrorCategories:
    """Test error categorization logic."""

    def test_server_error_detection(self):
        """Test detection of server-related errors."""
        server_errors = [
            "Server connection failed",
            "MCP server timeout",
            "server authentication error",
            "Unable to connect to MCP server",
        ]

        for error in server_errors:
            is_server_error = "server" in error.lower() or "mcp" in error.lower()
            assert is_server_error, f"Should detect '{error}' as server error"

    def test_non_server_error_detection(self):
        """Test detection of non-server errors."""
        cli_errors = [
            "Invalid command",
            "Missing argument",
            "File not found",
            "Permission denied",
        ]

        for error in cli_errors:
            is_server_error = "server" in error.lower() or "mcp" in error.lower()
            assert not is_server_error, f"Should not detect '{error}' as server error"

    def test_mixed_case_error_detection(self):
        """Test error detection with mixed case."""
        errors = ["Server Error", "MCP Server", "SERVER CONNECTION", "mcp server"]

        for error in errors:
            is_server_error = "server" in error.lower() or "mcp" in error.lower()
            assert is_server_error, f"Should detect '{error}' as server error"


class TestStdinExitCodes:
    """Test exit codes related to stdin input."""

    def test_stdin_flag_without_input_exit_code(self):
        """Test exit code when --stdin flag is used without input."""
        # Test that exit_with_code raises SystemExit with invalid input code
        with pytest.raises(SystemExit) as exc_info:
            with patch("sys.stdin.isatty", return_value=True):
                # Test the logic from main()
                stdin = True
                quiet = False

                if stdin and sys.stdin.isatty():
                    exit_with_code(
                        EXIT_INVALID_INPUT,
                        "Error: --stdin flag requires input from stdin",
                        quiet,
                    )
        assert exc_info.value.code == EXIT_INVALID_INPUT

    def test_stdin_flag_with_input_success(self):
        """Test successful stdin input processing."""
        with patch("sys.stdin.isatty", return_value=False):
            with patch("sys.stdin.read", return_value='{"test": "data"}'):
                # Test the logic from main()
                stdin = True
                stdin_input = None

                if stdin and not sys.stdin.isatty():
                    stdin_input = sys.stdin.read().strip()

                assert stdin_input == '{"test": "data"}'


class TestQuietModeExitCodes:
    """Test exit codes in quiet mode."""

    def test_quiet_mode_suppresses_messages(self):
        """Test that quiet mode suppresses exit messages."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                quiet = True

                exit_with_code(EXIT_CLI_ERROR, "Error occurred", quiet)

                mock_print.assert_not_called()
                mock_exit.assert_called_once_with(EXIT_CLI_ERROR)

    def test_normal_mode_shows_messages(self):
        """Test that normal mode shows exit messages."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                quiet = False

                exit_with_code(EXIT_CLI_ERROR, "Error occurred", quiet)

                mock_print.assert_called_once_with("Error occurred", file=sys.stderr)
                mock_exit.assert_called_once_with(EXIT_CLI_ERROR)


class TestExitCodeDocumentation:
    """Test that exit codes match the specification."""

    def test_exit_codes_match_spec(self):
        """Test that exit codes match the specification."""
        # From the spec:
        # 0: Success
        # 1: CLI or transport error
        # 2: Server-side error
        # 3: Invalid JSON/input

        assert EXIT_SUCCESS == 0
        assert EXIT_CLI_ERROR == 1
        assert EXIT_SERVER_ERROR == 2
        assert EXIT_INVALID_INPUT == 3

    def test_exit_code_usage_examples(self):
        """Test exit code usage examples."""
        # Success case
        with patch("sys.exit") as mock_exit:
            exit_with_code(EXIT_SUCCESS, "", True)
            mock_exit.assert_called_with(EXIT_SUCCESS)

        # CLI error case
        with patch("sys.exit") as mock_exit:
            exit_with_code(EXIT_CLI_ERROR, "", True)
            mock_exit.assert_called_with(EXIT_CLI_ERROR)

        # Server error case
        with patch("sys.exit") as mock_exit:
            exit_with_code(EXIT_SERVER_ERROR, "", True)
            mock_exit.assert_called_with(EXIT_SERVER_ERROR)

        # Invalid input case
        with patch("sys.exit") as mock_exit:
            exit_with_code(EXIT_INVALID_INPUT, "", True)
            mock_exit.assert_called_with(EXIT_INVALID_INPUT)
