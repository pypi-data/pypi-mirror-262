from .cn_now import cn_now
import re


def test_now():
    now_str = cn_now()
    assert bool(
        re. match(r'^(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})$', now_str))
