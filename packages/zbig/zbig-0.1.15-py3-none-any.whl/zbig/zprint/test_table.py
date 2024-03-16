from .table import table


def test(capfd):
    data = [
        ["User", "Host", "Description"],
        ["root", "h.bigzhu.net", "dump"],
        ["root", "racknerd.bigzhu.net", "racknerd"],
        ["bigzhu", "ssh.entube.app", "digitalocean"],
    ]

    table(data, "~")
    out, err = capfd.readouterr()
    # print(repr(out))
    assert out == '''User  ~Host               ~Description \nroot  ~h.bigzhu.net       ~dump        \nroot  ~racknerd.bigzhu.net~racknerd    \nbigzhu~ssh.entube.app     ~digitalocean\n'''
    assert err == ''
