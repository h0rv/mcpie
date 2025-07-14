"""
Integration tests for the complete CLI functionality.
"""

from unittest.mock import Mock, patch, AsyncMock
from click.testing import CliRunner
import tempfile
import os
import json

from mcpie_cli.mcpie import main


class TestCLIIntegration:
    """Integration tests for the complete CLI."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_json_output_format_integration(self):
        """Test JSON output format end-to-end."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main, ["test_server", "--output", "json", "--", "t", "call", "test"]
                )

                # Should have created MCPSession with json output config
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.output_format == "json"

    def test_quiet_mode_integration(self):
        """Test quiet mode end-to-end."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main, ["test_server", "--quiet", "--", "t", "call", "test"]
                )

                # Should have created MCPSession with quiet=True
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.quiet is True

    def test_output_file_integration(self):
        """Test output file functionality end-to-end."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
                mock_session = Mock()
                mock_session.connect = AsyncMock()
                mock_session.disconnect = AsyncMock()
                mock_session_class.return_value = mock_session

                with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                    mock_run_commands.return_value = None

                    self.runner.invoke(
                        main, ["test_server", "-o", tmp_path, "--", "t", "call", "test"]
                    )

                    # Should have created MCPSession with output file
                    mock_session_class.assert_called_once()
                    call_args = mock_session_class.call_args
                    output_config = call_args[1]["output_config"]
                    assert output_config.output_file == tmp_path
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_stdin_integration(self):
        """Test stdin functionality end-to-end."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main,
                    ["test_server", "--stdin", "--", "t", "call", "test"],
                    input='{"test": "data"}',
                )

                # Should have called run_commands with stdin input
                mock_run_commands.assert_called_once()
                call_args = mock_run_commands.call_args[0]
                stdin_input = call_args[2] if len(call_args) > 2 else None
                assert stdin_input == '{"test": "data"}'

    def test_verbose_mode_integration(self):
        """Test verbose mode end-to-end."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main, ["test_server", "--verbose", "--", "t", "call", "test"]
                )

                # Should have created MCPSession with verbose=True
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.verbose is True

    def test_multiple_options_integration(self):
        """Test multiple options working together."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main,
                    [
                        "test_server",
                        "--output",
                        "yaml",
                        "--quiet",
                        "--verbose",
                        "--",
                        "t",
                        "call",
                        "test",
                    ],
                )

                # Should have created MCPSession with all options
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.output_format == "yaml"
                assert output_config.quiet is True
                assert output_config.verbose is True

    def test_env_and_header_parsing_integration(self):
        """Test environment and header parsing end-to-end."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main,
                    [
                        "test_server",
                        "-e",
                        "API_KEY:secret",
                        "-H",
                        "Authorization:Bearer token",
                        "--",
                        "t",
                        "call",
                        "test",
                    ],
                )

                # Should have created MCPSession with metadata
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                metadata = call_args[0][1]  # Second positional argument
                assert metadata == {
                    "API_KEY": "secret",
                    "Authorization": "Bearer token",
                }

    def test_interactive_mode_default_output(self):
        """Test that interactive mode defaults to pretty output."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_repl") as mock_run_repl:
                mock_run_repl.return_value = None

                self.runner.invoke(main, ["test_server"])

                # Should have created MCPSession with pretty output for interactive mode
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.output_format == "pretty"

    def test_command_mode_keeps_json_output(self):
        """Test that command mode keeps JSON as default output."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(main, ["test_server", "--", "t", "call", "test"])

                # Should have created MCPSession with json output for command mode
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.output_format == "json"


class TestErrorHandlingIntegration:
    """Integration tests for error handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_invalid_output_format_error(self):
        """Test invalid output format produces proper error."""
        result = self.runner.invoke(
            main, ["test_server", "--output", "invalid", "--", "t", "call", "test"]
        )

        assert result.exit_code != 0
        assert "Invalid value for '--output'" in result.output

    def test_missing_server_argument_error(self):
        """Test missing server argument produces proper error."""
        result = self.runner.invoke(main, [])

        assert result.exit_code != 0
        assert "Missing argument" in result.output or "Usage:" in result.output

    def test_stdin_without_input_error(self):
        """Test --stdin without input produces proper error."""
        result = self.runner.invoke(
            main, ["test_server", "--stdin", "--", "t", "call", "test"]
        )

        # Should exit with invalid input code
        assert result.exit_code == 3  # EXIT_INVALID_INPUT
        assert "Error: --stdin flag requires input from stdin" in result.output

    def test_keyboard_interrupt_handling(self):
        """Test keyboard interrupt handling."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            mock_run.side_effect = KeyboardInterrupt()

            with patch("mcpie_cli.mcpie.exit_with_code") as mock_exit:
                self.runner.invoke(main, ["test_server", "--", "t", "call", "test"])

                # Should have called exit_with_code with CLI error code
                mock_exit.assert_called_once()
                args = mock_exit.call_args[0]
                assert args[0] == 1  # EXIT_CLI_ERROR

    def test_json_decode_error_handling(self):
        """Test JSON decode error handling."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            mock_run.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)

            with patch("mcpie_cli.mcpie.exit_with_code") as mock_exit:
                self.runner.invoke(main, ["test_server", "--", "t", "call", "test"])

                # Should have called exit_with_code with invalid input code
                mock_exit.assert_called_once()
                args = mock_exit.call_args[0]
                assert args[0] == 3  # EXIT_INVALID_INPUT

    def test_server_error_handling(self):
        """Test server error handling."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            mock_run.side_effect = Exception("MCP server connection failed")

            with patch("mcpie_cli.mcpie.exit_with_code") as mock_exit:
                self.runner.invoke(main, ["test_server", "--", "t", "call", "test"])

                # Should have called exit_with_code with server error code
                mock_exit.assert_called_once()
                args = mock_exit.call_args[0]
                assert args[0] == 2  # EXIT_SERVER_ERROR

    def test_generic_error_handling(self):
        """Test generic error handling."""
        with patch("mcpie_cli.mcpie.asyncio.run") as mock_run:
            mock_run.side_effect = Exception("Generic error")

            with patch("mcpie_cli.mcpie.exit_with_code") as mock_exit:
                self.runner.invoke(main, ["test_server", "--", "t", "call", "test"])

                # Should have called exit_with_code with CLI error code
                mock_exit.assert_called_once()
                args = mock_exit.call_args[0]
                assert args[0] == 1  # EXIT_CLI_ERROR


class TestOutputFormatterIntegration:
    """Integration tests for output formatter usage."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_output_formatter_creation(self):
        """Test that output formatter is created correctly."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main, ["test_server", "--output", "yaml", "--", "t", "call", "test"]
                )

                # Should have created MCPSession with output formatter
                mock_session_class.assert_called_once()
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config is not None
                assert output_config.output_format == "yaml"

    def test_file_output_configuration(self):
        """Test file output configuration."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name

        try:
            with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
                mock_session = Mock()
                mock_session.connect = AsyncMock()
                mock_session.disconnect = AsyncMock()
                mock_session_class.return_value = mock_session

                with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                    mock_run_commands.return_value = None

                    self.runner.invoke(
                        main,
                        [
                            "test_server",
                            "--output",
                            "json",
                            "-o",
                            tmp_path,
                            "--",
                            "t",
                            "call",
                            "test",
                        ],
                    )

                    # Should have created MCPSession with file output
                    mock_session_class.assert_called_once()
                    call_args = mock_session_class.call_args
                    output_config = call_args[1]["output_config"]
                    assert output_config.output_file == tmp_path
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)


class TestCLIWorkflow:
    """Integration tests for complete CLI workflows."""

    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()

    def test_complete_tool_call_workflow(self):
        """Test complete tool call workflow."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main,
                    [
                        "test_server",
                        "--output",
                        "json",
                        "--quiet",
                        "--",
                        "t",
                        "call",
                        "add",
                        "5",
                        "3",
                    ],
                )

                # Should have gone through complete workflow
                mock_session.connect.assert_called_once()
                mock_run_commands.assert_called_once()
                mock_session.disconnect.assert_called_once()

    def test_complete_stdin_workflow(self):
        """Test complete stdin workflow."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_commands") as mock_run_commands:
                mock_run_commands.return_value = None

                self.runner.invoke(
                    main,
                    [
                        "test_server",
                        "--stdin",
                        "--output",
                        "raw",
                        "--",
                        "t",
                        "call",
                        "add",
                    ],
                    input='{"a": 5, "b": 3}',
                )

                # Should have processed stdin input
                mock_run_commands.assert_called_once()
                args = mock_run_commands.call_args[0]
                stdin_input = args[2] if len(args) > 2 else None
                assert stdin_input == '{"a": 5, "b": 3}'

    def test_complete_interactive_workflow(self):
        """Test complete interactive workflow."""
        with patch("mcpie_cli.mcpie.MCPSession") as mock_session_class:
            mock_session = Mock()
            mock_session.connect = AsyncMock()
            mock_session.disconnect = AsyncMock()
            mock_session_class.return_value = mock_session

            with patch("mcpie_cli.mcpie.run_repl") as mock_run_repl:
                mock_run_repl.return_value = None

                self.runner.invoke(main, ["test_server"])

                # Should have gone through interactive workflow
                mock_session.connect.assert_called_once()
                mock_run_repl.assert_called_once()
                mock_session.disconnect.assert_called_once()

                # Should have configured for interactive mode
                call_args = mock_session_class.call_args
                output_config = call_args[1]["output_config"]
                assert output_config.output_format == "pretty"
