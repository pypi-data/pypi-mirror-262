#!/usr/bin/env python3
import json
import os
import time
from zbig.zhash.args import args_hash
# 使用 json 缓存函数


# 默认 4 小时: 14400 秒
def cache(life_second=14400):
    # check is file modify time in 4 hours
    def check_file_is_alive(file_name: str) -> bool:
        file = f"{file_name}.json"
        if not os.path.exists(file):
            # print("file not exist")
            return False
        # get the modify time of the file
        modify_time = os.path.getmtime(file)
        # get the current time
        current_time = time.time()
        # check if the file modify time is out of 4 hours ago
        return current_time - modify_time <= life_second

    def read_from_file(file_name: str):
        with open(f"{file_name}.json", "r") as outfile:
            data = json.load(outfile)
        return data

    def save_to_file(file_name: str, content):
        with open(f"{file_name}.json", "w") as outfile:
            json.dump(content, outfile)

    def decorator(fn):
        def wrapped(*args, **kwargs):
            # 用函数名和入参作为 key
            hash_name = args_hash(*args, **kwargs)
            global file_name
            file_name = f"{fn.__name__}_{hash_name}"
            if check_file_is_alive(file_name):
                res = read_from_file(file_name)
                if res:
                    # print("get data from file")
                    return res
            res = fn(*args, **kwargs)
            save_to_file(file_name, res)
            return res

        return wrapped

    return decorator


@cache()
def get_token(name: str):
    # imaginary API call to get token
    return {"name": name, "time": time.time()}


if __name__ == "__main__":
    print(get_token("bigzhu"))
    print(get_token("bigzhu2"))
