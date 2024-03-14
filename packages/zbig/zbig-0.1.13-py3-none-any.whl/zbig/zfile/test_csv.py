from .csv import read_csv


def test_read_csv():
    header, rows = read_csv("hosts.csv")
    assert header == ['User', 'Host', 'Description']
    assert rows == [['bigzhu', 'ssh.entube.app', 'digitalocean'], ['root', 'google.com', 'just test']]
