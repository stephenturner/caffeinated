from click.testing import CliRunner
from caffeinated.cli import caffeinated


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(caffeinated, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("caffeinated, version ")


def test_help():
    """Test that the help message is displayed correctly."""
    runner = CliRunner()
    result = runner.invoke(caffeinated, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output
    assert "-c, --caffeine" in result.output
    assert "-b, --bedtime" in result.output


def test_valid_input():
    """Test the CLI with valid input."""
    runner = CliRunner()
    result = runner.invoke(caffeinated, ["-c", "90", "-b", "10PM"])
    assert result.exit_code == 0
    assert "You would have" in result.output
    assert "mg of caffeine in your system" in result.output


def test_missing_caffeine_argument():
    """Test the CLI with missing caffeine argument."""
    runner = CliRunner()
    result = runner.invoke(caffeinated, ["-b", "10PM"])
    assert result.exit_code == 1  # exit_code 2 is typical for usage errors


def test_missing_bedtime_argument():
    """Test the CLI with missing bedtime argument."""
    runner = CliRunner()
    result = runner.invoke(caffeinated, ["-c", "90"])
    assert result.exit_code == 1  # exit_code 2 is typical for usage errors


def test_invalid_caffeine_input():
    """Test the CLI with invalid caffeine input (e.g., non-integer)."""
    runner = CliRunner()
    result = runner.invoke(caffeinated, ["-c", "invalid", "-b", "10PM"])
    assert result.exit_code == 2
    assert "Error: Invalid value for '-c' / '--caffeine'" in result.output


def test_invalid_bedtime_input():
    """Test the CLI with invalid bedtime input."""
    runner = CliRunner()
    result = runner.invoke(caffeinated, ["-c", "90", "-b", "25PM"])  # Invalid time format
    assert result.exit_code == 1