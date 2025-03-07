# applemusic2flac/metadata.py
"""
Metadata handling module for Apple Music to FLAC conversion.

This module provides utilities for extracting and processing audio metadata
using ffprobe, including functions to parse track numbers, extract tags,
and retrieve audio format information like channels and sample rate.
"""
import json
import logging
import subprocess
from json import JSONDecodeError


def ffprobe_get_metadata(file_path: str) -> dict:
    """
    Get metadata from a media file using ffprobe.

    Args:
        file_path: Path to the media file to analyze.

    Returns
    -------
        A dictionary containing the file's metadata or an empty dict if an error occurs.
    """
    cmd = [
        "ffprobe",
        "-v",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file_path,
    ]
    try:
        result = subprocess.run(
            cmd, capture_output=True, check=True, encoding="utf-8", errors="replace"
        )
        if not result.stdout.strip():
            logging.error("[ffprobe] 无输出, 可能文件无法读取或不是音频: %s", file_path)
            return {}
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, JSONDecodeError, Exception):
        logging.exception("[ffprobe] 错误:")
        return {}


def parse_number(disc_str: str) -> list[int]:
    """
    Parse a string in the format "number/total" into component numbers.

    Args:
        disc_str: String containing number information (e.g., "1/5").

    Returns
    -------
        A list containing [number, total]. If number is missing or invalid, defaults to 1.
        If total is missing or invalid, defaults to -1.
    """
    # 如果不是字符串或字符串为空, 返回默认值 [1, -1]
    if not isinstance(disc_str, str) or not disc_str.strip():
        return [1, -1]
    # 分割字符串并移除首尾空白
    parts = [part.strip() for part in disc_str.split("/")]
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


def extract_tags_from_metadata(metadata: dict) -> dict:
    """
    Extract audio tags from ffprobe metadata output.

    Args:
        metadata: Dictionary containing metadata from ffprobe.

    Returns
    -------
        A dictionary containing extracted audio tags.
    """
    tags = {}
    fmt = metadata.get("format", {})
    format_tags = fmt.get("tags", {})

    tags["tracknumber"] = parse_number(
        format_tags.get("track", format_tags.get("tracknumber", ""))
    )[0]
    tags["discnumber"] = parse_number(
        format_tags.get("disc", format_tags.get("discnumber", ""))
    )[0]

    if parse_number(format_tags.get("totaldiscs", ""))[1] == -1:
        tags["totaldiscs"] = ""
    else:
        tags["totaldiscs"] = parse_number(format_tags.get("totaldiscs", ""))[1]
    if parse_number(format_tags.get("totaltracks", ""))[1] == -1:
        tags["totaltracks"] = ""
    else:
        tags["totaltracks"] = parse_number(format_tags.get("totaltracks", ""))[1]
    tags["artist"] = format_tags.get("artist", "")
    tags["title"] = format_tags.get("title", "")
    tags["album"] = format_tags.get("album", "")

    tags["performer"] = format_tags.get("performer", "")
    tags["copyright"] = format_tags.get("copyright", "")
    tags["date"] = format_tags.get("date", "")
    tags["isrc"] = format_tags.get("isrc", "")
    tags["upc"] = format_tags.get("upc", "")
    tags["label"] = format_tags.get("label", "")
    tags["albumartist"] = format_tags.get("albumartist", "")
    tags["composer"] = format_tags.get("composer", "")
    tags["genre"] = format_tags.get("genre", "")

    return tags


def get_channels_and_samplerate(metadata: dict) -> tuple[int, int]:
    """
    Extract channel count and sample rate from audio metadata.

    Args:
        metadata: Dictionary containing metadata from ffprobe.

    Returns
    -------
        A tuple containing (channels, sample_rate).
        Defaults to (2, 44100) if no audio stream is found.
    """
    streams = metadata.get("streams", [])
    for stream in streams:
        if stream.get("codec_type") == "audio":
            return int(stream.get("channels", 2)), int(
                stream.get("sample_rate", "44100")
            )
    return 2, 44100
