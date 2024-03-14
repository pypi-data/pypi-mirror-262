import os
import json
from zkyutils.logger import log
from tqdm import tqdm


@log.log_decorator('读取json')
def read_json(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


@log.log_decorator('写入json')
def write_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@log.log_decorator('批量获取用户输入')
def get_input_list(msg):
    input_list = []
    data = input(msg)
    while data != '':
        input_list.append(data)
        data = input('')
    return input_list


@log.log_decorator('用户输入-按选项输入')
def get_input_by_option(msg, options, return_bool=False):
    yes_str_list = ['y', 'Y', 'yes', 'Yes', 'YES', '是']
    no_str_list = ['n', 'N', 'no', 'No', 'NO', '否']
    data = input(f'{msg}（可输入选项：{options}）')
    while data not in options:
        log.error(f'输入格式错误，请输入以下选项：{options}')
        data = input(f'{msg}（可输入选项：{options}）')
    if return_bool:
        if data in yes_str_list:
            return True
        elif data in no_str_list:
            return False
    return data


@log.log_decorator('新建进度条')
def new_progress(total, desc='进度'):
    return tqdm(total=total, desc=desc, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')


@log.log_decorator('更新进度条')
def update_progress(progress, value=1):
    progress.update(value)
