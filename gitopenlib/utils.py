__version__ = "0.1.1"

"""
存放工具函数
"""
import json
from pathlib import Path, PosixPath


def get_paths_from_dir(dirs: str or list, types: str or list):
    """
    从指定目录下获取所有指定扩展名文件的路径，不递归子文件夹

    Args:
        dirs(list): 文件夹路径（绝对路径），单个用str表示，多个用list
        types(types): 指定文件的扩展名，单个用str表示，多个用list

    Returns:
        list: 文件路径字符串列表
    """

    if isinstance(dirs, str):
        dirs = [dirs]
    if isinstance(types, str):
        types = [types]

    result = []
    for d in dirs:
        for t in types:
            res = Path(d).glob("*." + t)
            result.extend(list(res))
    return result


def read_content(file_path: str or PosixPath):
    """
    从文本文件中读取内容，将内容转换为list，list的元素为每行的字符串

    Args:
        file_path(str or PosixPath): 文件路径

    return:
        list: 每行字符串组成的列表
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    return remove_0_str(
        [line.strip() for line in file_path.read_text(encoding="utf-8").split("\n")]
    )


def read_jsons(file_path: str or PosixPath):
    """
    从文本文件中读取内容，并转化为dict组成的list
    Args:
        file_path: 文件路径

    Returns:
        list: dict组成的list
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)
    result = remove_0_str(
        [line.strip() for line in file_path.read_text(encoding="utf-8").split("\n")]
    )

    return [json.loads(item) for item in result]


def remove_0_str(data: list):
    """
    去除list列表中为长度为0的字符串，用于字符串split后，列表中出现长度为0字符串的去除
    """

    return [item for item in data if len(str(item)) != 0]


if __name__ == "__main__":
    result = get_paths_from_dir("/Users/sunjiajia/Downloads", "py")
    print(result)
