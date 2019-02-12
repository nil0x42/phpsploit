import sys
import imp

sys.path.pop(0)


def test_windows_os():
    sys.platform = "Windows Vista"
    try:
        imp.load_source("phpsploit", "./phpsploit")
        import phpsploit
    except SystemExit as err:
        errmsg = str(err)
        assert "you should be a TARGET rather than an attacker" in errmsg
