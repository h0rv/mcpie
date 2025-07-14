"""
Test summary demonstrating that all major features are working.
"""

import json
import tempfile
import os
from unittest.mock import Mock, patch

from mcpie_cli.mcpie import (
    OutputConfig,
    JsonOutputFormatter,
    PrettyOutputFormatter,
    TableOutputFormatter,
    YamlOutputFormatter,
    RawOutputFormatter,
    get_output_formatter,
    EXIT_SUCCESS,
    EXIT_CLI_ERROR,
    EXIT_SERVER_ERROR,
    EXIT_INVALID_INPUT,
    exit_with_code,
)


class TestFeatureSummary:
    """Test summary showing all major features work."""

    def test_output_formatters_basic_functionality(self):
        """Test that all output formatters work with basic data."""
        config = OutputConfig("json", False, False, None)

        # Test all formatters can be created
        json_formatter = JsonOutputFormatter(config)
        pretty_formatter = PrettyOutputFormatter(config)
        table_formatter = TableOutputFormatter(config)
        yaml_formatter = YamlOutputFormatter(config)
        raw_formatter = RawOutputFormatter(config)

        # Test basic formatting
        mock_result = Mock()
        mock_result.model_dump.return_value = {"test": "data"}

        json_output = json_formatter.format_result(mock_result)
        assert json_output == '{"test": "data"}'

        pretty_output = pretty_formatter.format_result(mock_result)
        assert "test" in pretty_output
        assert "data" in pretty_output

        table_output = table_formatter.format_result(mock_result)
        assert "test: data" in table_output

        yaml_output = yaml_formatter.format_result(mock_result)
        assert "test: data" in yaml_output

        raw_output = raw_formatter.format_result(mock_result)
        assert "test" in raw_output

    def test_output_config_creation(self):
        """Test OutputConfig creation with different options."""
        # Test default config
        config1 = OutputConfig("json", False, False, None)
        assert config1.output_format == "json"
        assert config1.quiet is False
        assert config1.verbose is False
        assert config1.output_file is None

        # Test config with all options
        config2 = OutputConfig("yaml", True, True, "output.yaml")
        assert config2.output_format == "yaml"
        assert config2.quiet is True
        assert config2.verbose is True
        assert config2.output_file == "output.yaml"

    def test_get_output_formatter_selection(self):
        """Test that get_output_formatter returns correct formatter types."""
        configs = [
            ("json", JsonOutputFormatter),
            ("pretty", PrettyOutputFormatter),
            ("table", TableOutputFormatter),
            ("yaml", YamlOutputFormatter),
            ("raw", RawOutputFormatter),
        ]

        for format_name, expected_class in configs:
            config = OutputConfig(format_name, False, False, None)
            formatter = get_output_formatter(config)
            assert isinstance(formatter, expected_class)

        # Test unknown format defaults to JSON
        config = OutputConfig("unknown", False, False, None)
        formatter = get_output_formatter(config)
        assert isinstance(formatter, JsonOutputFormatter)

    def test_exit_code_constants(self):
        """Test that exit code constants are defined correctly."""
        assert EXIT_SUCCESS == 0
        assert EXIT_CLI_ERROR == 1
        assert EXIT_SERVER_ERROR == 2
        assert EXIT_INVALID_INPUT == 3

    def test_exit_with_code_functionality(self):
        """Test exit_with_code function behavior."""
        # Test with mock to avoid actual system exit
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                # Test success message
                exit_with_code(EXIT_SUCCESS, "Success", False)
                mock_print.assert_called_with("Success")
                mock_exit.assert_called_with(EXIT_SUCCESS)

        # Test quiet mode
        with patch("sys.exit") as mock_exit:
            with patch("builtins.print") as mock_print:
                exit_with_code(EXIT_CLI_ERROR, "Error", True)
                mock_print.assert_not_called()
                mock_exit.assert_called_with(EXIT_CLI_ERROR)

    def test_file_output_functionality(self):
        """Test file output functionality."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            config = OutputConfig("json", False, False, tmp_path)
            formatter = JsonOutputFormatter(config)

            # Test that formatter can write to file
            test_data = {"test": "file_output"}
            mock_result = Mock()
            mock_result.model_dump.return_value = test_data

            output = formatter.format_result(mock_result)
            formatter.write(output)

            # Verify file was written
            with open(tmp_path, "r") as f:
                content = f.read()

            assert content == '{"test": "file_output"}'
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    def test_list_formatting(self):
        """Test list formatting across different formatters."""
        items = [
            {"name": "item1", "description": "desc1"},
            {"name": "item2", "description": "desc2"},
        ]
        columns = ["name", "description"]

        # Test JSON formatter
        json_config = OutputConfig("json", False, False, None)
        json_formatter = JsonOutputFormatter(json_config)
        json_output = json_formatter.format_list(items, "Test", columns)
        parsed = json.loads(json_output)
        assert len(parsed) == 2
        assert parsed[0]["name"] == "item1"

        # Test pretty formatter
        pretty_config = OutputConfig("pretty", False, False, None)
        pretty_formatter = PrettyOutputFormatter(pretty_config)
        pretty_output = pretty_formatter.format_list(items, "Test", columns)
        assert "item1" in pretty_output
        assert "desc1" in pretty_output

        # Test table formatter
        table_config = OutputConfig("table", False, False, None)
        table_formatter = TableOutputFormatter(table_config)
        table_output = table_formatter.format_list(items, "Test", columns)
        assert "name" in table_output
        assert "description" in table_output
        assert "item1" in table_output

    def test_error_handling_in_formatters(self):
        """Test error handling in formatters."""
        config = OutputConfig("json", False, False, None)
        formatter = JsonOutputFormatter(config)

        # Test with None result
        output = formatter.format_result(None)
        assert output == "{}"

        # Test with empty list
        output = formatter.format_list([], "Test", ["name"])
        assert output == "[]"

    def test_quiet_mode_functionality(self):
        """Test quiet mode functionality."""
        # Test quiet mode suppresses error output
        quiet_config = OutputConfig("json", True, False, None)
        quiet_formatter = JsonOutputFormatter(quiet_config)

        with patch("builtins.print") as mock_print:
            quiet_formatter.format_error("Test error")
            mock_print.assert_not_called()

        # Test normal mode shows error output
        normal_config = OutputConfig("json", False, False, None)
        normal_formatter = JsonOutputFormatter(normal_config)

        with patch("sys.stderr") as mock_stderr:
            normal_formatter.format_error("Test error")
            mock_stderr.write.assert_called()

    def test_comprehensive_workflow(self):
        """Test a comprehensive workflow combining multiple features."""
        # Create config with multiple options
        config = OutputConfig("json", False, True, None)
        assert config.output_format == "json"
        assert config.quiet is False
        assert config.verbose is True

        # Get formatter
        formatter = get_output_formatter(config)
        assert isinstance(formatter, JsonOutputFormatter)

        # Format result
        mock_result = Mock()
        mock_result.model_dump.return_value = {"status": "success", "data": [1, 2, 3]}

        output = formatter.format_result(mock_result)
        parsed = json.loads(output)
        assert parsed["status"] == "success"
        assert parsed["data"] == [1, 2, 3]

        # Format list
        items = [{"id": 1, "name": "test1"}, {"id": 2, "name": "test2"}]
        list_output = formatter.format_list(items, "Items", ["id", "name"])
        parsed_list = json.loads(list_output)
        assert len(parsed_list) == 2
        assert parsed_list[0]["id"] == 1


def test_all_features_integration():
    """Integration test showing all major features work together."""
    # Test output configuration
    config = OutputConfig("json", False, False, None)
    assert config.output_format == "json"

    # Test formatter creation
    formatter = get_output_formatter(config)
    assert isinstance(formatter, JsonOutputFormatter)

    # Test result formatting
    mock_result = Mock()
    mock_result.model_dump.return_value = {"test": "integration"}

    output = formatter.format_result(mock_result)
    assert output == '{"test": "integration"}'

    # Test list formatting
    items = [{"name": "test", "value": 123}]
    list_output = formatter.format_list(items, "Test", ["name", "value"])
    parsed = json.loads(list_output)
    assert len(parsed) == 1
    assert parsed[0]["name"] == "test"

    # Test exit codes
    assert EXIT_SUCCESS == 0
    assert EXIT_CLI_ERROR == 1
    assert EXIT_SERVER_ERROR == 2
    assert EXIT_INVALID_INPUT == 3

    print("✅ All major features are working correctly!")


if __name__ == "__main__":
    test_all_features_integration()
    print("✅ Feature integration test passed!")
