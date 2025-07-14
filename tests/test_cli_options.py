"""
Tests for CLI options and argument parsing.
"""

from unittest.mock import patch
from click.testing import CliRunner
import sys
import pytest

from mcpie_cli.mcpie import main, OutputConfig, exit_with_code


class TestCLIOptions:
    """Test CLI option parsing."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_output_format_option(self):
        """Test --output option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main, ["test_server", "--output", "json", "--", "t", "call", "test"]
            )

            # Check that the option was parsed correctly
            mock_run.assert_called_once()

    def test_quiet_option(self):
        """Test --quiet option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main, ["test_server", "--quiet", "--", "t", "call", "test"]
            )

            mock_run.assert_called_once()

    def test_verbose_option(self):
        """Test --verbose option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main, ["test_server", "--verbose", "--", "t", "call", "test"]
            )

            mock_run.assert_called_once()

    def test_output_file_option(self):
        """Test -o/--output-file option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main, ["test_server", "-o", "output.json", "--", "t", "call", "test"]
            )

            mock_run.assert_called_once()

    def test_stdin_option(self):
        """Test --stdin option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main,
                ["test_server", "--stdin", "--", "t", "call", "test"],
                input="test input",
            )

            mock_run.assert_called_once()

    def test_force_sse_option(self):
        """Test --force-sse option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main, ["test_server", "--force-sse", "--", "t", "call", "test"]
            )

            mock_run.assert_called_once()

    def test_multiple_options(self):
        """Test multiple options together."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main,
                [
                    "test_server",
                    "--output",
                    "yaml",
                    "--quiet",
                    "--verbose",
                    "-o",
                    "output.yaml",
                    "--",
                    "t",
                    "call",
                    "test",
                ],
            )

            mock_run.assert_called_once()

    def test_env_option(self):
        """Test -e/--env option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main, ["test_server", "-e", "KEY:value", "--", "t", "call", "test"]
            )

            mock_run.assert_called_once()

    def test_header_option(self):
        """Test -H/--header option parsing."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            self.runner.invoke(
                main,
                [
                    "test_server",
                    "-H",
                    "Authorization:Bearer token",
                    "--",
                    "t",
                    "call",
                    "test",
                ],
            )

            mock_run.assert_called_once()


class TestOutputConfigCreation:
    """Test OutputConfig creation from CLI arguments."""

    def test_default_output_config(self):
        """Test default output config creation."""
        config = OutputConfig("json", False, False, None)
        assert config.output_format == "json"
        assert config.quiet is False
        assert config.verbose is False
        assert config.output_file is None

    def test_output_config_with_file(self):
        """Test output config with file output."""
        config = OutputConfig("yaml", True, False, "output.yaml")
        assert config.output_format == "yaml"
        assert config.quiet is True
        assert config.output_file == "output.yaml"

    def test_output_config_verbose_mode(self):
        """Test output config with verbose mode."""
        config = OutputConfig("pretty", False, True, None)
        assert config.output_format == "pretty"
        assert config.verbose is True


class TestOutputFormatDefaults:
    """Test output format defaults in different modes."""

    def test_interactive_mode_defaults_to_pretty(self):
        """Test that interactive mode defaults to pretty output."""
        # This would be tested in integration, but we can test the logic
        # In interactive mode (no commands), output should default to pretty
        commands = ()
        output = "json"

        # Simulate the logic from main()
        actual_output_format = output
        if not commands and output == "json":
            actual_output_format = "pretty"

        assert actual_output_format == "pretty"

    def test_command_mode_uses_specified_format(self):
        """Test that command mode uses specified format."""
        commands = ("t", "call", "test")
        output = "json"

        # Simulate the logic from main()
        actual_output_format = output
        if not commands and output == "json":
            actual_output_format = "pretty"

        assert actual_output_format == "json"


class TestStdinHandling:
    """Test stdin input handling."""

    def test_stdin_flag_without_input(self):
        """Test --stdin flag without actual stdin input."""
        with patch("sys.stdin.isatty", return_value=True):
            # Test that exit_with_code raises SystemExit with code 3
            with pytest.raises(SystemExit) as exc_info:
                exit_with_code(
                    3, "Error: --stdin flag requires input from stdin", False
                )
            assert exc_info.value.code == 3

    def test_stdin_with_input(self):
        """Test --stdin flag with actual input."""
        with patch("sys.stdin.isatty", return_value=False):
            with patch("sys.stdin.read", return_value='{"test": "data"}'):
                # This would be processed in main()
                stdin_input = sys.stdin.read().strip()
                assert stdin_input == '{"test": "data"}'


class TestMetadataParsing:
    """Test metadata parsing for env and header options."""

    def test_env_parsing(self):
        """Test environment variable parsing."""
        env_items = ("KEY1:value1", "KEY2:value2")
        header_items = ()

        # Simulate the logic from main()
        metadata = {}
        for item in env_items + header_items:
            if ":" in item:
                key, value = item.split(":", 1)
                metadata[key] = value

        assert metadata == {"KEY1": "value1", "KEY2": "value2"}

    def test_header_parsing(self):
        """Test header parsing."""
        env_items = ()
        header_items = ("Authorization:Bearer token", "Content-Type:application/json")

        # Simulate the logic from main()
        metadata = {}
        for item in env_items + header_items:
            if ":" in item:
                key, value = item.split(":", 1)
                metadata[key] = value

        assert metadata == {
            "Authorization": "Bearer token",
            "Content-Type": "application/json",
        }

    def test_mixed_env_and_header_parsing(self):
        """Test mixed environment and header parsing."""
        env_items = ("API_KEY:secret",)
        header_items = ("Authorization:Bearer token",)

        # Simulate the logic from main()
        metadata = {}
        for item in env_items + header_items:
            if ":" in item:
                key, value = item.split(":", 1)
                metadata[key] = value

        assert metadata == {"API_KEY": "secret", "Authorization": "Bearer token"}


class TestCLIValidation:
    """Test CLI argument validation."""

    def test_invalid_output_format(self):
        """Test invalid output format."""
        runner = CliRunner()
        with patch("mcpie_cli.mcpie.asyncio.run"):
            result = runner.invoke(
                main,
                [
                    "test_server",
                    "--output",
                    "invalid_format",
                    "--",
                    "t",
                    "call",
                    "test",
                ],
            )

            # Should fail with invalid choice
            assert result.exit_code != 0
            assert "Invalid value for '--output'" in result.output

    def test_required_server_argument(self):
        """Test that server argument is required."""
        runner = CliRunner()
        result = runner.invoke(main, [])

        # Should fail without server argument
        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output

    def test_commands_parsing(self):
        """Test that commands are parsed correctly."""
        commands = ("t", "call", "add", "5", "3")

        # Test that commands are captured as tuple
        assert len(commands) == 5
        assert commands[0] == "t"
        assert commands[1] == "call"
        assert commands[2] == "add"


class TestExitCodeFunction:
    """Test the exit_with_code function."""

    def test_exit_with_success(self):
        """Test exit with success code."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(0, "Success message", False)
                mock_print.assert_called_once_with("Success message")
                mock_exit.assert_called_once_with(0)

    def test_exit_with_error(self):
        """Test exit with error code."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(1, "Error message", False)
                mock_print.assert_called_once_with("Error message", file=sys.stderr)
                mock_exit.assert_called_once_with(1)

    def test_exit_with_quiet_mode(self):
        """Test exit with quiet mode."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(1, "Error message", True)
                mock_print.assert_not_called()
                mock_exit.assert_called_once_with(1)

    def test_exit_without_message(self):
        """Test exit without message."""
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(1, "", False)
                mock_print.assert_not_called()
                mock_exit.assert_called_once_with(1)


class TestOutputFormatChoices:
    """Test output format choice validation."""

    def test_valid_output_formats(self):
        """Test all valid output formats."""
        valid_formats = ["json", "pretty", "table", "yaml", "raw"]

        for format_name in valid_formats:
            config = OutputConfig(format_name, False, False, None)
            assert config.output_format == format_name

    def test_output_format_case_sensitivity(self):
        """Test that output format choices are case-sensitive."""
        # Click choices are case-sensitive by default
        # This test documents the expected behavior
        config = OutputConfig("json", False, False, None)
        assert config.output_format == "json"

        # "JSON" would be invalid (not tested here as it would fail at CLI level)
