# applemusic2flac/ffmpeg.py
"""Module for ffmpeg operations."""
import json
import logging
from typing import Any

from ffmpeg import FFmpeg

from .dataclass import TrackMetadata


def ffmpeg_get_metadata(file_path: str) -> dict[str, Any]:
    """
    Get metadata from a media file using ffprobe.

    Args:
        file_path: Path to the media file to analyze.

    Returns
    -------
        A dictionary containing the file's metadata or an empty dict if an error occurs.
    """
    # 创建 FFmpeg 实例，指定使用 ffprobe
    ffmpeg_get_metadata = FFmpeg(executable="ffprobe").input(
        file_path,
        print_format="json",  # 输出 JSON 格式
        show_format=None,    # 显示文件格式信息
        show_streams=None,   # 显示流信息
        v="quiet"            # 等价于 -v quiet，减少日志输出
    )

    try:
        # 执行 ffprobe 并获取输出
        result = ffmpeg_get_metadata.execute()

        # 检查输出是否为空
        if not result.strip():
            logging.error("[ffprobe] 无输出, 可能文件无法读取或不是音频: %s", file_path)
            return {}

        # 解析 JSON 输出并返回
        return json.loads(result)
    except Exception:
        # 捕获所有可能的异常 (包括 JSONDecodeError 或 FFmpeg 执行错误)
        logging.exception("[ffprobe] 错误")
        return {}



def ffmpeg_convert_flac(src_file: str, dst_file: str, track_metadata: TrackMetadata) -> None:
    """
    Convert audio file to FLAC format with specified bit depth and metadata tags.

    Args:
        src_file (str): Path to the source audio file
        dst_file (str): Path where the output FLAC file will be saved
        bit_depth (int): Bit depth for the output file (16 or 32)
        track_metadata (TrackMetadata): Object containing metadata tags to be added to the FLAC file

    Returns
    -------
        None
    """
    # 根据位深度选择采样格式
    sample_fmt = "s16" if track_metadata.bit_depth == 16 else "s32"  # noqa: PLR2004

    options = {}
    index = 0
    for field_name, field_value in track_metadata.__dict__.items():
        if field_value is None or field_name in ["bit_depth", "sample_rate"]:
            continue
        options[f"metadata:g:{index}"] = f"{field_name}={field_value!s}"
        index += 1
    options["c:a"] = "flac"
    options["c:a"] = "flac"                           # 音频编码器设为 FLAC
    options["map_metadata"] = "-1"                    # 不复制输入文件的元数据
    options["sample_fmt"] = sample_fmt                # 设置采样格式
    options["compression_level"] = "5"                # 设置压缩级别
    options["ar"] = str(track_metadata.sample_rate)   # 设置采样率

    ffmpeg_convert_flac = (FFmpeg()
                           .option("y","-vn")
                           .input(src_file)
                           .output(
                               dst_file,
                               options))

    try:
        ffmpeg_convert_flac.execute()
    except Exception:
        logging.exception("转码失败: ")
