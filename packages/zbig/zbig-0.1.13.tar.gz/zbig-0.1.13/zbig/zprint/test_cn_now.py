from .cn_now import cn_now
import re


def test_now_print(capfd):
    """Check that User instance has the particular properties."""
    cn_now('BigZhu')
    out, err = capfd.readouterr()
    assert re.match(
        r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2}) BigZhu$', out) is not None
    assert err == ''
