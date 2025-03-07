# src/applemusic2flac/album.py
"""album level operations."""
from .metadata import (
    extract_tags_from_metadata,
    ffprobe_get_metadata,
    get_channels_and_samplerate,
)
from .utils import make_safe_filename


def get_album_matadata_sample(m4a_files:list , sample_id:int = 0) -> str:
    """Get album information from a list of m4a files."""
    sample_file = m4a_files[sample_id]
    metadata = ffprobe_get_metadata(sample_file)
    metadata = ffprobe_get_metadata(sample_file)
    tags = extract_tags_from_metadata(metadata)
    artist = tags["artist"] or "UnknownArtist"
    album = tags["album"] or "UnknownAlbum"
    date = tags["date"] or "UnknownDate"
    return artist, album, date


def get_album_matadata(album_tags:list) -> str:
    """Get full album information from a list of m4a files."""
    values = set(tag.get(tag_name, '') for tag in tags_list if tag.get(tag_name))