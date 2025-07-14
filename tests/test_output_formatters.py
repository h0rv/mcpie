"""
Tests for output formatters.
"""

import json
import tempfile
from unittest.mock import Mock, patch

from mcpie_cli.mcpie import (
    OutputConfig,
    JsonOutputFormatter,
    PrettyOutputFormatter,
    TableOutputFormatter,
    YamlOutputFormatter,
    RawOutputFormatter,
    get_output_formatter,
)
from mcp.types import Result


class TestOutputConfig:
    """Test the OutputConfig class."""

    def test_output_config_initialization(self):
        """Test OutputConfig initialization with various parameters."""
        config = OutputConfig(
            output_format="json", quiet=False, verbose=True, output_file=None
        )

        assert config.output_format == "json"
        assert config.quiet is False
        assert config.verbose is True
        assert config.output_file is None

    def test_output_config_with_file(self):
        """Test OutputConfig with output file."""
        config = OutputConfig(
            output_format="json", quiet=True, verbose=False, output_file="output.json"
        )

        assert config.output_file == "output.json"
        assert config.quiet is True


class TestJsonOutputFormatter:
    """Test the JsonOutputFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = OutputConfig("json", False, False, None)
        self.formatter = JsonOutputFormatter(self.config)

    def test_format_empty_result(self):
        """Test formatting empty result."""
        result = self.formatter.format_result(None)
        assert result == "{}"

    def test_format_simple_result(self):
        """Test formatting a simple result."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {
            "content": [{"type": "text", "text": "test"}]
        }

        result = self.formatter.format_result(mock_result)
        expected = json.dumps({"content": [{"type": "text", "text": "test"}]})
        assert result == expected

    def test_format_empty_list(self):
        """Test formatting empty list."""
        result = self.formatter.format_list([], "Test", ["name"])
        assert result == "[]"

    def test_format_list_with_items(self):
        """Test formatting list with items."""
        items = [
            Mock(name="item1", description="desc1"),
            Mock(name="item2", description="desc2"),
        ]
        items[0].model_dump.return_value = {"name": "item1", "description": "desc1"}
        items[1].model_dump.return_value = {"name": "item2", "description": "desc2"}

        result = self.formatter.format_list(items, "Test", ["name", "description"])
        expected = json.dumps(
            [
                {"name": "item1", "description": "desc1"},
                {"name": "item2", "description": "desc2"},
            ]
        )
        assert result == expected

    def test_format_list_with_dicts(self):
        """Test formatting list with dict items."""
        items = [
            {"name": "item1", "description": "desc1"},
            {"name": "item2", "description": "desc2"},
        ]

        result = self.formatter.format_list(items, "Test", ["name", "description"])
        expected = json.dumps(
            [
                {"name": "item1", "description": "desc1"},
                {"name": "item2", "description": "desc2"},
            ]
        )
        assert result == expected


class TestPrettyOutputFormatter:
    """Test the PrettyOutputFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = OutputConfig("pretty", False, False, None)
        self.formatter = PrettyOutputFormatter(self.config)

    def test_format_pretty_result(self):
        """Test formatting with pretty indentation."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {
            "content": [{"type": "text", "text": "test"}]
        }

        result = self.formatter.format_result(mock_result)
        expected = json.dumps({"content": [{"type": "text", "text": "test"}]}, indent=2)
        assert result == expected

    def test_format_pretty_list(self):
        """Test formatting list with pretty indentation."""
        items = [{"name": "item1", "description": "desc1"}]

        result = self.formatter.format_list(items, "Test", ["name", "description"])
        expected = json.dumps([{"name": "item1", "description": "desc1"}], indent=2)
        assert result == expected


class TestTableOutputFormatter:
    """Test the TableOutputFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = OutputConfig("table", False, False, None)
        self.formatter = TableOutputFormatter(self.config)

    def test_format_empty_list(self):
        """Test formatting empty list as table."""
        result = self.formatter.format_list([], "Test", ["name"])
        assert result == "No test available"

    def test_format_simple_table(self):
        """Test formatting simple table."""
        items = [
            {"name": "item1", "description": "desc1"},
            {"name": "item2", "description": "desc2"},
        ]

        result = self.formatter.format_list(items, "Test", ["name", "description"])

        # Check that result contains table-like structure
        lines = result.split("\n")
        assert len(lines) >= 4  # Header, separator, and data rows
        assert "name" in lines[0]
        assert "description" in lines[0]
        assert "item1" in lines[2]
        assert "item2" in lines[3]

    def test_format_result_as_key_value(self):
        """Test formatting single result as key-value pairs."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {"key1": "value1", "key2": "value2"}

        result = self.formatter.format_result(mock_result)
        assert "key1: value1" in result
        assert "key2: value2" in result


class TestYamlOutputFormatter:
    """Test the YamlOutputFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = OutputConfig("yaml", False, False, None)
        self.formatter = YamlOutputFormatter(self.config)

    def test_format_empty_result(self):
        """Test formatting empty result as YAML."""
        result = self.formatter.format_result(None)
        assert result == "null"

    def test_format_yaml_result(self):
        """Test formatting result as YAML."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {
            "content": [{"type": "text", "text": "test"}]
        }

        result = self.formatter.format_result(mock_result)
        assert "content:" in result
        assert "type: text" in result
        assert "text: test" in result

    def test_format_yaml_list(self):
        """Test formatting list as YAML."""
        items = [{"name": "item1", "description": "desc1"}]

        result = self.formatter.format_list(items, "Test", ["name", "description"])
        assert "name: item1" in result
        assert "description: desc1" in result


class TestRawOutputFormatter:
    """Test the RawOutputFormatter class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.config = OutputConfig("raw", False, False, None)
        self.formatter = RawOutputFormatter(self.config)

    def test_format_empty_result(self):
        """Test formatting empty result as raw."""
        result = self.formatter.format_result(None)
        assert result == ""

    def test_format_text_content(self):
        """Test extracting text content from result."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {
            "content": [{"type": "text", "text": "Hello World"}]
        }

        result = self.formatter.format_result(mock_result)
        assert result == "Hello World"

    def test_format_resource_content(self):
        """Test extracting resource content."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {"contents": [{"text": "Config data"}]}

        result = self.formatter.format_result(mock_result)
        assert result == "Config data"

    def test_format_structured_content(self):
        """Test extracting structured content result."""
        mock_result = Mock(spec=Result)
        mock_result.model_dump.return_value = {"structuredContent": {"result": 42}}

        result = self.formatter.format_result(mock_result)
        assert result == "42"

    def test_format_raw_list(self):
        """Test formatting list in raw mode."""
        items = [Mock(name="item1"), Mock(name="item2")]
        items[0].name = "item1"
        items[1].name = "item2"

        result = self.formatter.format_list(items, "Test", ["name"])
        assert result == "item1\nitem2"

    def test_format_raw_list_with_dicts(self):
        """Test formatting list of dicts in raw mode."""
        items = [{"name": "item1"}, {"uri": "uri2"}]

        result = self.formatter.format_list(items, "Test", ["name", "uri"])
        assert result == "item1\nuri2"


class TestFileOutput:
    """Test file output functionality."""

    def test_file_output_writing(self):
        """Test writing output to file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            config = OutputConfig("json", False, False, tmp.name)
            formatter = JsonOutputFormatter(config)

            mock_result = Mock(spec=Result)
            mock_result.model_dump.return_value = {"test": "data"}

            output = formatter.format_result(mock_result)
            formatter.write(output)

            # Read the file content
            with open(tmp.name, "r") as f:
                content = f.read()

            assert content == '{"test": "data"}'


class TestGetOutputFormatter:
    """Test the get_output_formatter function."""

    def test_get_json_formatter(self):
        """Test getting JSON formatter."""
        config = OutputConfig("json", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, JsonOutputFormatter)

    def test_get_pretty_formatter(self):
        """Test getting pretty formatter."""
        config = OutputConfig("pretty", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, PrettyOutputFormatter)

    def test_get_table_formatter(self):
        """Test getting table formatter."""
        config = OutputConfig("table", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, TableOutputFormatter)

    def test_get_yaml_formatter(self):
        """Test getting YAML formatter."""
        config = OutputConfig("yaml", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, YamlOutputFormatter)

    def test_get_raw_formatter(self):
        """Test getting raw formatter."""
        config = OutputConfig("raw", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, RawOutputFormatter)

    def test_get_default_formatter(self):
        """Test getting default formatter for unknown format."""
        config = OutputConfig("unknown", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, JsonOutputFormatter)


class TestErrorHandling:
    """Test error handling in formatters."""

    def test_format_error_quiet_mode(self):
        """Test error formatting in quiet mode."""
        config = OutputConfig("json", True, False, None)
        formatter = JsonOutputFormatter(config)

        # Should not output anything in quiet mode
        with patch("builtins.print") as mock_print:
            formatter.format_error("Test error")
            mock_print.assert_not_called()

    def test_format_error_normal_mode(self):
        """Test error formatting in normal mode."""
        config = OutputConfig("json", False, False, None)
        formatter = JsonOutputFormatter(config)

        with patch("sys.stderr") as mock_stderr:
            formatter.format_error("Test error")
            # Should write to stderr
            mock_stderr.write.assert_called()
