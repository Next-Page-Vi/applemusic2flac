# applemusic2flac/audio.py
"""
Module for audio file conversion operations, specifically for converting audio files to FLAC format

with specified bit depth and metadata tags using ffmpeg.
"""
import logging
import subprocess


def convert_to_flac(src_file: str, dst_file: str, bit_depth: int, track_tags:dict) -> None:
    """
    Convert audio file to FLAC format with specified bit depth and metadata tags.

    Args:
        src_file (str): Path to the source audio file
        dst_file (str): Path where the output FLAC file will be saved
        bit_depth (int): Bit depth for the output file (16 or 32)
        track_tags (dict): Dictionary containing metadata tags to be added to the FLAC file

    Returns
    -------
        None
    """
    sample_fmt = "s16" if bit_depth == 16 else "s32"  # noqa: PLR2004
    cmd = [
        "ffmpeg",
        "-y",
        "-i", src_file,
        "-vn",
        "-map_metadata", "-1",
        "-metadata", f"title={track_tags['title']}",
        "-metadata", f"album={track_tags['album']}",
        "-metadata", f"tracknumber={track_tags['tracknumber']}",
        "-metadata", f"discnumber={track_tags['discnumber']}",
        "-metadata", f"artist={track_tags['artist']}",
        "-metadata", f"performer={track_tags['performer']}",
        "-metadata", f"copyright={track_tags['copyright']}",
        "-metadata", f"date={track_tags['date']}",
        "-metadata", f"isrc={track_tags['isrc']}",
        "-metadata", f"upc={track_tags['upc']}",
        "-metadata", f"label={track_tags['label']}",
        "-metadata", f"albumartist={track_tags['albumartist']}",
        "-metadata", f"composer={track_tags['composer']}",
        "-metadata", f"totaldiscs={track_tags['totaldiscs']}",
        "-metadata", f"totaltracks={track_tags['totaltracks']}",
        "-metadata", f"genre={track_tags['genre']}",
        "-c:a", "flac",
        "-compression_level", "5",
        "-sample_fmt", sample_fmt,
        dst_file
    ]
    try:
        subprocess.run(cmd, check=True, stderr=subprocess.PIPE, text=True, encoding="utf-8")
    except subprocess.CalledProcessError:
        logging.exception("转码失败: ")
