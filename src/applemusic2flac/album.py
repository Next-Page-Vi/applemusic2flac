# src/applemusic2flac/album.py
"""album level operations."""
import logging
from collections import Counter
from dataclasses import dataclass
from typing import Optional

from dateutil import parser

from .track import get_track_metadata


@dataclass
class AlbumMetadata:
    """Album Metadata Class"""

    album: Optional[str] = None # 专辑名
    albumartist: Optional[str] = None # 专辑艺术家
    date: Optional[str] = None # 日期
    year: Optional[int] = None # 年份
    format: Optional[str] = "FLAC" # 音频格式
    source: Optional[str] = "WEB" # 来源
    sample_rate: Optional[int] = 0 # 采样率 (如 "44100")
    bit_depth: Optional[int] = 0 # 比特深度 (如 "16")

def get_album_metadata_sample(m4a_files: list, sample_id: int = 0) -> AlbumMetadata:
    """Get album information from a list of m4a files."""
    album_metadata_sample = AlbumMetadata() #实例化类Albummetadata.sample
    sample_file_path = m4a_files[sample_id]
    track_metadata = get_track_metadata(sample_file_path)
    album_metadata_sample.album = track_metadata.album or "UnknownAlbum"
    album_metadata_sample.albumartist = track_metadata.artist or "UnknownArtist"
    try:
        year = parser.parse(track_metadata.date).year
        album_metadata_sample.date = year
    except ValueError:
        album_metadata_sample.date = "UnknownYear"

    return album_metadata_sample


def get_album_metadata(track_metadata_set: list) -> AlbumMetadata:
    """Get full album information from a list of m4a files."""
    album_metadata = AlbumMetadata() #实例化类Albummetadata.full
    # album
    album_values = Counter(
        [tag.album for tag in track_metadata_set if tag.album]
    )
    album_metadata.album = sorted(album_values.items(), key=lambda x: -x[1])

    # albumartist
    albumartist_values = Counter(
        [tag.albumartist for tag in track_metadata_set if tag.albumartist]
    )
    albumartist = sorted(albumartist_values.items(), key=lambda x: -x[1])
    artist_values = Counter(
        [tag.artist for tag in track_metadata_set if tag.artist]
    )
    artist = sorted(artist_values.items(), key=lambda x: -x[1])

     # 单一albumartist > 单一artist > 最多artist(WARNING) > 最多albumartist(WARNING)
    if len(albumartist) == 1:
        album_metadata.albumartist = albumartist[0][0]
    elif len(artist) == 1:
        album_metadata.albumartist = artist[0][0]
    elif len(artist) > 1:
        logging.warning(
            "Multiple artists found, using Various Artists as albumartist."
        )
        album_metadata.albumartist = "Various Artists"
    elif len(albumartist) > 1:
        logging.warning(
            "Multiple albumartist found, source folder might be a mix of multiple albums? "
            "Using Various Artists as albumartist."
        )
        album_metadata.albumartist = "Various Artists"
    # year
    date_values = Counter(
        [tag.date for tag in track_metadata_set if tag.date]
    )
    date = sorted(date_values.items(), key=lambda x: -x[1])
    album_metadata.date = date[0][0] if date else None
    if album_metadata.date:
        try:
            year = parser.parse(album_metadata.date).year
        except ValueError:
            year = "UnknownYear"
        album_metadata.year = year
