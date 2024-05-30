from click import ClickException
from click.testing import CliRunner
from mf50.cli import doit


fox_seq = " 3 3 *** 3 3 *** 6 6 /// 6 6 /// 9 9 333 9 9 333 ; ; 666 ; ; 666"
tidal_seq = "~ ds5 ~ ds5 ~ fs4 fs4 fs4 ~ ds5 ~ ds5 ~ fs4 fs4 fs4 ~ fs5 ~ fs5 ~ b4 b4 b4 ~ fs5 ~ fs5 ~ b4 b4 b4 ~ a5 ~ a5 ~ ds5 ds5 ds5 ~ a5 ~ a5 ~ ds5 ds5 ds5 ~ b5 ~ b5 ~ fs5 fs5 fs5 ~ b5 ~ b5 ~ fs5 fs5 fs5"


def test_default():
    runner = CliRunner()
    result = runner.invoke(doit, [])
    assert result.exit_code == 0
    assert result.output == f"{tidal_seq}\n"


def test_tidal_source():
    runner = CliRunner()
    result = runner.invoke(doit, ["--sequence", tidal_seq, "--source", "tidal"])
    assert result.exit_code == 0
    assert result.output == f"{fox_seq}\n"


def test_bad_input():
    runner = CliRunner()
    result = runner.invoke(doit, ["--sequence", "blorb"])
    assert result.exit_code == 1
    assert result.output == f"Error: That does not appear to be a fox sequence.\n"
