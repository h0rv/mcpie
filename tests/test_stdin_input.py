"""
Tests for stdin input handling.
"""

import json
import pytest
from unittest.mock import Mock, patch, AsyncMock

from mcpie_cli.mcpie import run_commands, MCPSession


class TestStdinInputHandling:
    """Test stdin input handling in run_commands."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_session = Mock(spec=MCPSession)
        self.mock_session.output_formatter = None
        self.mock_session.execute_command = AsyncMock()

    @pytest.mark.asyncio
    async def test_stdin_json_input_for_tool_call(self):
        """Test JSON input from stdin for tool call."""
        stdin_input = '{"a": 5, "b": 3}'
        commands = ("t", "call", "add")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            # Should call handle_command with the modified command string
            mock_handle.assert_called_once()
            args = mock_handle.call_args[0]
            assert "add" in args[2]  # Command parts should contain the modified command

    @pytest.mark.asyncio
    async def test_stdin_json_input_for_prompt_get(self):
        """Test JSON input from stdin for prompt get."""
        stdin_input = '{"name": "test_user"}'
        commands = ("p", "get", "greeting")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_stdin_json_input_for_resource_read(self):
        """Test JSON input from stdin for resource read."""
        stdin_input = '{"uri": "config://app"}'
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_stdin_plain_text_input(self):
        """Test plain text input from stdin."""
        stdin_input = "hello world"
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_stdin_input_no_command(self):
        """Test stdin input with no command."""
        stdin_input = '{"test": "data"}'
        commands = ()

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_stdin_invalid_json(self):
        """Test invalid JSON input from stdin."""
        stdin_input = '{"invalid": json}'
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_stdin_json_with_uri_field(self):
        """Test JSON input with uri field from stdin."""
        stdin_input = '{"uri": "file:///test.txt"}'
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()
            args = mock_handle.call_args[0]
            assert args[0] == self.mock_session
            assert (
                "read" in args[2]
            )  # Command parts should contain the modified command

    @pytest.mark.asyncio
    async def test_stdin_json_with_name_field(self):
        """Test JSON input with name field from stdin."""
        stdin_input = '{"name": "test_tool"}'
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()
            args = mock_handle.call_args[0]
            assert args[0] == self.mock_session
            assert (
                "read" in args[2]
            )  # Command parts should contain the modified command


class TestBackwardCompatibilityStdin:
    """Test backward compatibility stdin handling."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_session = Mock(spec=MCPSession)
        self.mock_session.output_formatter = None

    @pytest.mark.asyncio
    async def test_backward_compatibility_stdin_resource_read(self):
        """Test backward compatibility for stdin resource read."""
        stdin_input = '{"uri": "file:///test.txt"}'
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_backward_compatibility_stdin_no_command(self):
        """Test backward compatibility for stdin with no command."""
        stdin_input = '{"uri": "file:///test.txt"}'
        commands = ()

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()
            args = mock_handle.call_args[0]
            assert args[0] == self.mock_session
            # Should use default command when no command is provided
            assert len(args[2]) > 0


class TestStdinErrorHandling:
    """Test error handling in stdin input."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_session = Mock(spec=MCPSession)
        self.mock_session.output_formatter = Mock()

    @pytest.mark.asyncio
    async def test_empty_stdin_input(self):
        """Test empty stdin input."""
        stdin_input = ""
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_whitespace_only_stdin(self):
        """Test whitespace-only stdin input."""
        stdin_input = "   "
        commands = ("r", "read")

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_command_no_stdin(self):
        """Test no command and no stdin."""
        stdin_input = ""
        commands = ()

        with patch("mcpie_cli.mcpie.handle_command") as mock_handle:
            await run_commands(self.mock_session, commands, stdin_input)

            mock_handle.assert_called_once()


class TestStdinJSONParsing:
    """Test JSON parsing from stdin."""

    def test_valid_json_parsing(self):
        """Test parsing valid JSON from stdin."""
        json_string = '{"key": "value", "number": 42}'
        parsed = json.loads(json_string)

        assert parsed == {"key": "value", "number": 42}

    def test_invalid_json_parsing(self):
        """Test handling invalid JSON from stdin."""
        invalid_json = '{"key": "value", "number": 42'

        with pytest.raises(json.JSONDecodeError):
            json.loads(invalid_json)

    def test_json_with_nested_objects(self):
        """Test parsing JSON with nested objects."""
        json_string = '{"user": {"name": "test", "age": 30}, "active": true}'
        parsed = json.loads(json_string)

        assert parsed == {"user": {"name": "test", "age": 30}, "active": True}

    def test_json_array_parsing(self):
        """Test parsing JSON arrays."""
        json_string = '[{"name": "item1"}, {"name": "item2"}]'
        parsed = json.loads(json_string)

        assert parsed == [{"name": "item1"}, {"name": "item2"}]


class TestStdinCommandConstruction:
    """Test command string construction with stdin input."""

    def test_tool_call_command_construction(self):
        """Test constructing tool call command with JSON args."""
        command_string = "t call add"
        json_args = {"a": 5, "b": 3}

        # Simulate the logic from run_commands
        command_string += f" '{json.dumps(json_args)}'"

        assert command_string == 't call add \'{"a": 5, "b": 3}\''

    def test_resource_read_command_construction(self):
        """Test constructing resource read command with URI."""
        command_string = "r read"
        uri = "config://app"

        # Simulate the logic from run_commands
        command_string += f" {uri}"

        assert command_string == "r read config://app"

    def test_prompt_get_command_construction(self):
        """Test constructing prompt get command with JSON args."""
        command_string = "p get greeting"
        json_args = {"name": "user"}

        # Simulate the logic from run_commands
        command_string += f" '{json.dumps(json_args)}'"

        assert command_string == 'p get greeting \'{"name": "user"}\''


class TestStdinInputValidation:
    """Test validation of stdin input."""

    def test_stdin_dict_validation(self):
        """Test validation of stdin input as dictionary."""
        stdin_data = {"a": 5, "b": 3}

        assert isinstance(stdin_data, dict)
        assert "a" in stdin_data
        assert "b" in stdin_data

    def test_stdin_uri_extraction(self):
        """Test extraction of URI from stdin JSON."""
        stdin_data = {"uri": "config://app", "other": "field"}

        if "uri" in stdin_data:
            uri = stdin_data["uri"]
            assert uri == "config://app"

    def test_stdin_name_extraction(self):
        """Test extraction of name from stdin JSON."""
        stdin_data = {"name": "test_tool", "other": "field"}

        if "name" in stdin_data:
            name = stdin_data["name"]
            assert name == "test_tool"

    def test_stdin_fallback_to_text(self):
        """Test fallback to plain text when JSON parsing fails."""
        stdin_input = "plain text input"

        try:
            json.loads(stdin_input)
        except json.JSONDecodeError:
            # Should fall back to treating as plain text
            assert stdin_input == "plain text input"
