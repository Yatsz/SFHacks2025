from unittest.mock import Mock, patch

import pytest

from inputs import load_input
from inputs.base import Sensor


class MockInput(Sensor):
    async def raw_to_text(self, raw_input):
        pass

    def formatted_latest_buffer(self):
        return None


def test_load_input_success():
    with (
        patch("os.path.dirname") as mock_dirname,
        patch("os.listdir") as mock_listdir,
        patch("importlib.import_module") as mock_import,
    ):
        mock_dirname.return_value = "/test/dir"
        mock_listdir.return_value = ["mock_input.py"]
        mock_module = Mock()
        mock_module.MockInput = MockInput
        mock_import.return_value = mock_module

        result = load_input("MockInput")

        mock_import.assert_called_once_with("inputs.plugins.mock_input")
        assert result == MockInput


def test_load_input_not_found():
    with patch("os.path.dirname") as mock_dirname, patch("os.listdir") as mock_listdir:
        mock_dirname.return_value = "/test/dir"
        mock_listdir.return_value = []

        with pytest.raises(ValueError, match="Input type NonexistentInput not found"):
            load_input("NonexistentInput")


def test_load_input_multiple_plugins():
    with (
        patch("os.path.dirname") as mock_dirname,
        patch("os.listdir") as mock_listdir,
        patch("importlib.import_module") as mock_import,
    ):
        mock_dirname.return_value = "/test/dir"
        mock_listdir.return_value = ["input1.py", "input2.py"]

        mock_module1 = Mock()
        mock_module1.Input1 = type("Input1", (Sensor,), {})

        mock_module2 = Mock()
        mock_module2.Input2 = type("Input2", (Sensor,), {})

        mock_import.side_effect = [mock_module1, mock_module2]

        result = load_input("Input2")

        assert mock_import.call_count == 2
        assert result == mock_module2.Input2


def test_load_input_non_input_class():
    with (
        patch("os.path.dirname") as mock_dirname,
        patch("os.listdir") as mock_listdir,
        patch("importlib.import_module") as mock_import,
    ):
        mock_dirname.return_value = "/test/dir"
        mock_listdir.return_value = ["mock.py"]

        class NonInput:
            pass

        mock_module = Mock()
        mock_module.NonInput = NonInput
        mock_import.return_value = mock_module

        with pytest.raises(ValueError, match="Input type NonInput not found"):
            load_input("NonInput")
