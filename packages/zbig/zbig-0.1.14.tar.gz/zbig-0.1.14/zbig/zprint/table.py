import unicodedata
import curses
from collections.abc import Callable
from schedule import Job
import schedule
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


# 格式化并修复 ljust bug
def format_rows(rows: list, spliter: str) -> list:
    max_lens = get_max_lens(rows)
    formated_rows = []
    for row in rows:
        # formated_row = [str(row[i]).ljust(max_lens[i]) for i in range(len(row))]
        # ljust 使用 len 判断长度, 支持非英文字符, 导致对每个非英文字符多填充了一个空白
        # 解决办法是算出有n个非英字符, just 长度-n
        formated_row = [
            str(row[i]).ljust(max_lens[i] - wide_chars(str(row[i])))
            for i in range(len(row))
        ]
        formated_rows.append(spliter.join(formated_row))
    return formated_rows


def table(rows: list, spliter: str):
    for i in format_rows(rows, spliter):
        print(i)


# 刷新绘制, 不会重复输出表格内容
def curses_table(get_rows: Callable, job: Job, spliter: str = "    "):
    """
    get_rows 返回值为 rows 的函数
    job 定义的刷新周期, 比如 schedule.every(1).minutes
    """
    stdscr = curses.initscr()

    def do():
        stdscr.clear()
        rows = get_rows()
        for i in format_rows(rows, spliter):
            stdscr.addstr(i + "\n")
        stdscr.refresh()
        # stdscr.getkey()

    job.do(do)
    while True:
        schedule.run_pending()


if __name__ == "__main__":
    import time

    def get_rows():
        return [
            ["用户名", "服务器地址", "服务器的一些说明"],
            ["用户名User", f"{time.time()}", "Description"],
            ["User", "Host", "Description"],
            ["root", "h.bigzhu.net", "dump"],
            ["root", "racknerd.bigzhu.net", "racknerd"],
            ["bigzhu", "ssh.entube.app", "digitalocean"],
        ]

    # table(get_rows(), " ")
    curses_table(get_rows, schedule.every(4).seconds)
