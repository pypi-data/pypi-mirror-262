
from zbig import ztime


# print whith zh_now time
def cn_now(str_in: str):
    t = ztime.cn_now()
    print(f"{t} {str_in}", flush=True)


if __name__ == "__main__":
    cn_now("Hello, World!")
    cn_now("你好，世界！")
    cn_now("こんにちは世界！")
    cn_now("안녕하세요 세계!")
