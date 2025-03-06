# applemusic2flac/metadata.py
import json
import subprocess
from json import JSONDecodeError


def ffprobe_get_metadata(file_path: str) -> dict:
    cmd = [
        "ffprobe", "-v",
        "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, encoding='utf-8', errors='replace')
        if not result.stdout.strip():
            print(f"[ffprobe] 无输出，可能文件无法读取或不是音频: {file_path}")
            return {}
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, JSONDecodeError, Exception) as e:
        print(f"[ffprobe] 错误: {e}")
        return {}

def parse_number(disc_str: str) -> list[int]:
    # 如果不是字符串或字符串为空，返回默认值 [1, -1]
    if not isinstance(disc_str, str) or not disc_str.strip():
        return [1, -1]
    # 分割字符串并移除首尾空白
    parts = [part.strip() for part in disc_str.split("/")]
    # 默认值
    num = 1
    total = -1
    # 如果有第一个部分且是数字，转换为整数
    if parts[0] and parts[0].isdigit():
        num = int(parts[0])
    # 如果有第二个部分且是数字，转换为整数
    if len(parts) > 1 and parts[1] and parts[1].isdigit():
        total = int(parts[1])
    return [num, total]

def extract_tags_from_metadata(metadata: dict) -> dict:
    tags = {}
    fmt = metadata.get("format", {})
    format_tags = fmt.get("tags", {})

    tags["tracknumber"] = parse_number(format_tags.get("track", format_tags.get("tracknumber", "")))[0]
    tags["discnumber"] = parse_number(format_tags.get("disc", format_tags.get("discnumber", "")))[0]

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
    streams = metadata.get("streams", [])
    for stream in streams:
        if stream.get("codec_type") == "audio":
            return int(stream.get("channels", 2)), int(stream.get("sample_rate", "44100"))
    return 2, 44100

