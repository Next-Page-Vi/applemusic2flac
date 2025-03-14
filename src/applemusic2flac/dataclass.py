from dataclasses import dataclass
from typing import Optional


@dataclass
class TrackMetadata:
    """Class representing audio track metadata."""

    #以下元数据存储为 int
    tracknumber: Optional[int] = None  # Track number
    discnumber: Optional[int] = None  # Disc number
    totaltracks: Optional[int] = None  # Total number of tracks
    totaldiscs: Optional[int] = None  # Total number of discs
    sample_rate: Optional[int] = None  # Sample rate (Hz)
    bit_depth: Optional[int] = None  # Bit depth
    channels: Optional[int] = None  # Number of audio channels

    #以下元数据存储为 str
    artist: Optional[str] = None  # Track artist
    title: Optional[str] = None  # Track title
    album: Optional[str] = None  # Album name
    performer: Optional[str] = None  # Performer
    copyright: Optional[str] = None  # Copyright information
    date: Optional[str] = None  # Release date
    isrc: Optional[str] = None  # International Standard Recording Code
    upc: Optional[str] = None  # Universal Product Code
    label: Optional[str] = None  # Record label
    albumartist: Optional[str] = None  # Album artist
    composer: Optional[str] = None  # Composer
    genre: Optional[str] = None  # Genre

@dataclass
class AlbumMetadata:
    """Album Metadata Class"""

    #以下元数据存储为 int
    year: Optional[int] = None # 年份
    sample_rate: Optional[int] = None # 采样率 (如 "44100")
    bit_depth: Optional[int] = None # 比特深度 (如 "16")

    #以下元数据存储为 str
    album: Optional[str] = None # 专辑名
    albumartist: Optional[str] = None # 专辑艺术家
    date: Optional[str] = None # 日期
    format: Optional[str] = "FLAC" # 音频格式
    source: Optional[str] = "WEB" # 来源
