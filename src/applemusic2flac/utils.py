# applemusic2flac/utils.py
"""Utility functions for the applemusic2flac package."""
import re


def make_safe_filename(name: str) -> str:
    """Convert string to a safe filename by replacing special characters."""
    return re.sub(r'[\\/:*?"<>|]', "_", name)

def parse_number(num_str: str) -> list[int]:
    """Parse a string in the format "number/total" into component numbers."""
    # 如果不是字符串或字符串为空, 返回默认值 [1, -1]
    if not isinstance(num_str, str) or not num_str.strip():
        return [1, -1]
    # 分割字符串并移除首尾空白
    parts = [part.strip() for part in num_str.split("/")]
    # 默认值
    num = 1
    total = -1
    # 如果有第一个部分且是数字, 转换为整数
    if parts[0] and parts[0].isdigit():
        num = int(parts[0])
    # 如果有第二个部分且是数字, 转换为整数
    if len(parts) > 1 and parts[1] and parts[1].isdigit():
        total = int(parts[1])
    return [num, total]