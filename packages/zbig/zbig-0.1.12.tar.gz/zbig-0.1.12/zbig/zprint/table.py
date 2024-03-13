import unicodedata


# 算出有几个非英文字符
def wide_chars(s):
    return sum(unicodedata.east_asian_width(x) == "W" for x in s)


# 非英文字符都算2个长度, 加上去
def width(s) -> int:
    return len(s) + wide_chars(s)


# 获取最长
def get_max_lens(rows: list):
    # 初始化为 0
    max_len = [0] * len(rows[0])
    for row in rows:
        for i in range(len(row)):
            # 要转 str, 避免错误
            str_width = width(str(row[i]))
            # print(row[i])
            # print(str_width)
            if str_width > max_len[i]:
                max_len[i] = str_width
    return max_len


def table(rows: list, spliter: str):
    max_lens = get_max_lens(rows)
    for row in rows:
        # formated_row = [str(row[i]).ljust(max_lens[i]) for i in range(len(row))]
        # ljust 使用 len 判断长度, 支持非英文字符, 导致对每个非英文字符多填充了一个空白
        # 解决办法是算出有n个非英字符, just 长度-n
        formated_row = [
            str(row[i]).ljust(max_lens[i] - wide_chars(str(row[i])))
            for i in range(len(row))
        ]
        print(spliter.join(formated_row))


if __name__ == "__main__":
    data = [
        ["用户名", "服务器地址", "服务器的一些说明"],
        ["用户名User", "Host", "Description"],
        ["User", "Host", "Description"],
        ["root", "h.bigzhu.net", "dump"],
        ["root", "racknerd.bigzhu.net", "racknerd"],
        ["bigzhu", "ssh.entube.app", "digitalocean"],
    ]
    table(data, " ")
    # i = "服务器地址什么"
    # j = "qwertyuiop"
    # print(width(i))
    # print(len(i))
