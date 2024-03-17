import pytest

from pathlib import Path
from latexml_html_cleaner.main import main
from latexml_html_cleaner.clean_html import to_lijst, HTMLCleaner

__author__ = "EVLT"
__copyright__ = "EVLT"
__license__ = "MIT"


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts agains stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main("--version")
    captured = capsys.readouterr()
    assert "" in captured.out


def test_to_lijst():
    lijst_in = ["A", "B"]
    lijst_out = to_lijst(lijst_in)
    assert lijst_in == lijst_out


def test_to_lijst():
    letter_in = "A"
    lijst_out = to_lijst(letter_in)
    assert [letter_in] == lijst_out


def test_cleaner():
    tmp_filename = Path("tmp.html")
    parent_dir = tmp_filename.absolute().parent.stem
    tests_dir = Path("tests")
    voorbeeld_file = Path("example/voorbeeld.html")
    schoon_voorbeeld = Path("voorbeeld_clean.html")
    if parent_dir == tests_dir.as_posix():
        # we draaien vanuit de tests directory, dus benader voorbeeld vanuit main directory
        voorbeeld_file = Path("..") / voorbeeld_file
    else:
        # we draaien vanuit de  main directory, dus benader schoon voorbeeld met test directory
        schoon_voorbeeld = tests_dir / schoon_voorbeeld

    result = HTMLCleaner(filename=voorbeeld_file, output_filename=tmp_filename)
    with open(file=schoon_voorbeeld, mode="r", encoding="utf-8") as stream:
        expected = stream.read()

    assert result.clean_soup == expected

    tmp_filename.unlink(missing_ok=True)
