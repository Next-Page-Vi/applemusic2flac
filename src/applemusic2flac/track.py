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
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Optional

from utils import parse_number


@dataclass
class TrackMetadata:
    """Class representing audio track metadata."""

    tracknumber: Optional[int] = None  # Track number
    discnumber: Optional[int] = None  # Disc number
    totaltracks: Optional[int] = None  # Total number of tracks
    totaldiscs: Optional[int] = None  # Total number of discs
    artist: Optional[str] = None  # Track artist
    title: Optional[str] = None  # Track title
    album: Optional[str] = None  # Album name
    performer: Optional[str] = None  # Performer
    copyright: Optional[str] = None  # Copyright information
    date: Optional[int] = None  # Release date
    isrc: Optional[str] = None  # International Standard Recording Code
    upc: Optional[str] = None  # Universal Product Code
    label: Optional[str] = None  # Record label
    albumartist: Optional[str] = None  # Album artist
    composer: Optional[str] = None  # Composer
    genre: Optional[str] = None  # Genre
    sample_rate: Optional[int] = None  # Sample rate (Hz)
    bit_depth: Optional[int] = None  # Bit depth

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
