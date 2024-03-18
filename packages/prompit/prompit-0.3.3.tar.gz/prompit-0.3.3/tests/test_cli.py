from io import StringIO
from contextlib import redirect_stdout
import src.prompit.cli as prompit_cli
import sys


def test_main():
    # Test --list
    sys.argv = ["prompit", "--list"]
    f = StringIO()
    with redirect_stdout(f):
        prompit_cli.main()
    out = f.getvalue()
    # Now `out` is the output of your function,
    # and you can assert things about it
    assert "selected files" in out
