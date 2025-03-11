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

from .framedepth import detect_true_bit_depth
from .utils import parse_number


@dataclass
class TrackMetadata:
    """Class representing audio track metadata."""

    tracknumber: Optional[str] = ""  # Track number
    discnumber: Optional[str] = ""  # Disc number
    totaltracks: Optional[str] = ""  # Total number of tracks
    totaldiscs: Optional[str] = ""  # Total number of discs
    artist: Optional[str] = ""  # Track artist
    title: Optional[str] = ""  # Track title
    album: Optional[str] = ""  # Album name
    performer: Optional[str] = ""  # Performer
    copyright: Optional[str] = ""  # Copyright information
    date: Optional[str] = ""  # Release date
    isrc: Optional[str] = ""  # International Standard Recording Code
    upc: Optional[str] = ""  # Universal Product Code
    label: Optional[str] = ""  # Record label
    albumartist: Optional[str] = ""  # Album artist
    composer: Optional[str] = ""  # Composer
    genre: Optional[str] = ""  # Genre
    sample_rate: Optional[str] = ""  # Sample rate (Hz)
    bit_depth: Optional[str] = ""  # Bit depth
    channels: Optional[str] = ""  # Number of audio channels

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


def get_track_metadata(file_path: str) -> TrackMetadata:
    """
    Extract audio tags from ffprobe metadata output.

    Args:
        metadata: Dictionary containing metadata from ffprobe.

    Returns
    -------
        A dictionary containing extracted audio tags.
    """
    track_metadata_dict = ffprobe_get_metadata(file_path)
    track_metadata = TrackMetadata()
    format_dict = track_metadata_dict.get("format", {})
    format_tags = format_dict.get("tags", {})


    track_metadata.tracknumber = parse_number(
        format_tags.get("track", format_tags.get("tracknumber", ""))
    )[0]
    track_metadata.discnumber = parse_number(
        format_tags.get("disc", format_tags.get("discnumber", ""))
    )[0]

    if parse_number(format_tags.get("totaltracks", ""))[1] == -1:
        track_metadata.totaltracks = ""
    else:
        track_metadata.totaltracks = parse_number(format_tags.get("totaltracks", ""))[1]

    if parse_number(format_tags.get("totaldiscs", ""))[1] == -1:
        track_metadata.totaldiscs = ""
    else:
        track_metadata.totaldiscs = parse_number(format_tags.get("totaldiscs", ""))[1]

    track_metadata.artist = format_tags.get("artist", "")
    track_metadata.title = format_tags.get("title", "")
    track_metadata.album = format_tags.get("album", "")

    track_metadata.performer = format_tags.get("performer", "")
    track_metadata.copyright = format_tags.get("copyright", "")
    track_metadata.date = format_tags.get("date", "")
    track_metadata.isrc = format_tags.get("isrc", "")
    track_metadata.upc = format_tags.get("upc", "")
    track_metadata.label = format_tags.get("label", "")
    track_metadata.albumartist = format_tags.get("albumartist", "")
    track_metadata.composer = format_tags.get("composer", "")
    track_metadata.genre = format_tags.get("genre", "")

    streams = track_metadata_dict.get("streams", [])
    for stream in streams:
        if stream.get("codec_type") == "audio":
            track_metadata.channels = stream.get("channels", "")
            track_metadata.sample_rate = stream.get("sample_rate", "")
            print(track_metadata.sample_rate)
            break
    # 判断真实比特深度
    track_metadata.bit_depth = detect_true_bit_depth(file_path, track_metadata.channels)
    return track_metadata
