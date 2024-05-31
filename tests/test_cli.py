from click import ClickException
from click.testing import CliRunner
from mf50.cli import doit


fox_seq = " 3 3 *** 3 3 *** 6 6 /// 6 6 /// 9 9 333 9 9 333 ; ; 666 ; ; 666"
tidal_seq = "~ ds5 ~ ds5 ~ fs4 fs4 fs4 ~ ds5 ~ ds5 ~ fs4 fs4 fs4 ~ fs5 ~ fs5 ~ b4 b4 b4 ~ fs5 ~ fs5 ~ b4 b4 b4 ~ a5 ~ a5 ~ ds5 ds5 ds5 ~ a5 ~ a5 ~ ds5 ds5 ds5 ~ b5 ~ b5 ~ fs5 fs5 fs5 ~ b5 ~ b5 ~ fs5 fs5 fs5"
freq_seq = "0 622 0 622 0 370 370 370 0 622 0 622 0 370 370 370 0 740 0 740 0 494 494 494 0 740 0 740 0 494 494 494 0 880 0 880 0 622 622 622 0 880 0 880 0 622 622 622 0 987 0 987 0 740 740 740 0 987 0 987 0 740 740 740"


def test_default():  # aka test_fox_to_tidal()
    runner = CliRunner()
    result = runner.invoke(doit, [])
    assert result.exit_code == 0
    assert result.output == f"{tidal_seq}\n"


def test_tidal_to_fox():
    runner = CliRunner()
    result = runner.invoke(
        doit, ["--sequence", tidal_seq, "--source", "tidal", "--dest", "fox"]
    )
    assert result.exit_code == 0
    assert result.output == f"{fox_seq}\n"


def test_tidal_to_freq():
    runner = CliRunner()
    result = runner.invoke(
        doit, ["--sequence", tidal_seq, "--source", "tidal", "--dest", "freq"]
    )
    assert result.exit_code == 0
    assert result.output == f"{freq_seq}\n"


def test_fox_to_freq():
    runner = CliRunner()
    result = runner.invoke(
        doit, ["--sequence", fox_seq, "--source", "fox", "--dest", "freq"]
    )
    assert result.exit_code == 0
    assert result.output == f"{freq_seq}\n"


def test_freq_to_tidal():
    runner = CliRunner()
    result = runner.invoke(
        doit, ["--sequence", freq_seq, "--source", "freq", "--dest", "tidal"]
    )
    assert result.exit_code == 0
    assert result.output == f"{tidal_seq}\n"


def test_freq_to_fox():
    runner = CliRunner()
    result = runner.invoke(
        doit, ["--sequence", freq_seq, "--source", "freq", "--dest", "fox"]
    )
    assert result.exit_code == 0
    assert result.output == f"{fox_seq}\n"


def test_bad_input():
    runner = CliRunner()
    result = runner.invoke(doit, ["--sequence", "blorb"])
    assert result.exit_code == 1
    assert result.output == f"Error: That does not appear to be a fox sequence.\n"
