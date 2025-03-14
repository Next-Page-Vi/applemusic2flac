# applemusic2flac/utils.py
"""Utility functions for the applemusic2flac package."""
import re
from pathlib import Path
from typing import Optional


def make_safe_filename(name: str) -> str:
    """Convert string to a safe filename by replacing special characters."""
    return re.sub(r'[\\/:*?"<>|]', "_", name)

def parse_number(num_str: str) -> tuple[int, Optional[int]]:
    """Parse a string in the format "part_1/part_2" into component numbers."""
    # 检查字符串是否为空
    if num_str is None or not num_str.strip():
        return 1, None

    # 设置默认值
    part_1, part_2 = 1, None

    # 分割字符串并移除首尾空白
    parts = [part.strip() for part in num_str.split("/")]

    # 处理第一部分
    if parts[0] and parts[0].isdigit():
        part_1 = int(parts[0])

    # 处理第二部分
    if len(parts) > 1 and parts[1] and parts[1].isdigit():
        part_2 = int(parts[1])

    return part_1, part_2


def get_unique_foldername(base_path: Path, folder_name: str) -> str:
    """获取唯一的文件夹名，如果已存在则添加 (1), (2) 等后缀
    
    Args:
        base_path: 基础路径
        folder_name: 希望使用的文件夹名
        
    Returns:
        不冲突的唯一文件夹名
    """
    if not (base_path / folder_name).exists():
        return folder_name
    
    counter = 1
    while (base_path / f"{folder_name} ({counter})").exists():
        counter += 1
    
    return f"{folder_name} ({counter})"