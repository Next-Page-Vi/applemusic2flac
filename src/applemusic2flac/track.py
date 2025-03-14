# applemusic2flac/metadata.py
"""
Metadata handling module for Apple Music to FLAC conversion.

This module provides utilities for extracting and processing audio metadata
using ffprobe, including functions to parse track numbers, extract tags,
and retrieve audio format information like channels and sample rate.
"""
from .dataclass import TrackMetadata
from .ffmpeg_tools import ffmpeg_get_metadata
from .framedepth import detect_true_bit_depth
from .utils import parse_number


def get_track_metadata(file_path: str) -> TrackMetadata:
    """
    Extract audio tags from ffprobe metadata output.

    Args:
        metadata: Dictionary containing metadata from ffprobe.

    Returns
    -------
        A dictionary containing extracted audio tags.
    """
    # track_metadata_dict = ffprobe_get_metadata(file_path)
    track_metadata_dict = ffmpeg_get_metadata(file_path)
    track_metadata = TrackMetadata()
    format_dict = track_metadata_dict.get("format", {})
    format_tags = format_dict.get("tags", {})

    track_metadata.tracknumber = parse_number(format_tags.get("track", format_tags.get("tracknumber", "")))[0]
    track_metadata.discnumber = parse_number(format_tags.get("disc", format_tags.get("discnumber", "")))[0]

    track_metadata.totaltracks = parse_number(format_tags.get("totaltracks", ""))[1]
    track_metadata.totaldiscs = parse_number(format_tags.get("totaldiscs", ""))[1]

    track_metadata.artist = format_tags.get("artist", None)
    track_metadata.title = format_tags.get("title", None)
    track_metadata.album = format_tags.get("album", None)

    track_metadata.performer = format_tags.get("performer", None)
    track_metadata.copyright = format_tags.get("copyright", None)
    track_metadata.date = format_tags.get("date", None)
    track_metadata.isrc = format_tags.get("isrc", None)
    track_metadata.upc = format_tags.get("upc", None)
    track_metadata.label = format_tags.get("label", None)
    track_metadata.albumartist = format_tags.get("albumartist", None)
    track_metadata.composer = format_tags.get("composer", None)
    track_metadata.genre = format_tags.get("genre", None)

    streams = track_metadata_dict.get("streams", [])
    for stream in streams:
        if stream.get("codec_type") == "audio":
            track_metadata.channels = stream.get("channels", "")
            track_metadata.sample_rate = stream.get("sample_rate", "")
            break
    # 判断真实比特深度
    track_metadata.bit_depth = detect_true_bit_depth(file_path, track_metadata.channels)
    return track_metadata
