# applemusic2flac/__main__.py
"""Main entry point for the applemusic2flac conversion tool."""

import logging
import shutil
import sys
from pathlib import Path

from .album import get_album_matadata_sample
from .audio import convert_to_flac
from .framedepth import detect_true_bit_depth
from .metadata import (
    extract_tags_from_metadata,
    ffprobe_get_metadata,
    get_channels_and_samplerate,
)
from .utils import make_safe_filename

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def main(source_dir: str, dest_dir: str) -> None:
    """Convert Apple Music m4a files to FLAC format.

    Args:
        source_dir (str): Directory containing m4a files to convert
        dest_dir (str): Target directory for converted FLAC files

    Returns
    -------
        None
    """
    source_dir = Path(source_dir)
    m4a_files = list(source_dir.rglob("*.m4a"))
    if not m4a_files:
        logging.critical("未找到任何 .m4a 文件, 程序退出。")
        return

    logging.info("找到 %s 个 .m4a 文件。", len(m4a_files))
    matadata_sample = get_album_matadata_sample(m4a_files, 0)
    foldername_sample = make_safe_filename(
        f"{matadata_sample.artist} - {matadata_sample.album} - ({matadata_sample.date})"
    )
    target_dir = Path(dest_dir) / foldername_sample
    album_tags = []

    Path.mkdir(target_dir, exist_ok=True)

    for file_path in m4a_files:
        cover = False
        metadata = ffprobe_get_metadata(file_path)
        track_tags = extract_tags_from_metadata(metadata)
        album_tags.append(track_tags)
        channels, _ = get_channels_and_samplerate(metadata)
        true_depth = detect_true_bit_depth(file_path, channels)
        track_title = track_tags.get("title") or Path(file_path).stem
        dst_filename = make_safe_filename(
            f"{track_tags['discnumber']}.{track_tags['tracknumber']}.{track_title}.flac"
        )
        dst_file_path = Path(target_dir) / dst_filename

        logging.info(
            "正在处理: %s -> 有效比特深度: %s ,输出文件: %s",
            Path(file_path).name,
            true_depth,
            dst_file_path,
        )
        convert_to_flac(file_path, dst_file_path, true_depth, track_tags)

    cover_path = next(
        (
            f
            for f in Path(source_dir).rglob("*cover*")
            if f.suffix.lower() in {".jpg", ".jpeg", ".png"}
        ),
        None,
    )
    if cover_path:
        cover_suffix = cover_path.suffix.lower()
        shutil.copy(cover_path, Path(target_dir) / f"cover{cover_suffix}")
        logging.info("已复制封面到 %s", target_dir)
        cover = True
    if not cover:
        logging.info("未找到封面, 请手动复制。")
    for tracks in album_tags:
        logging.info(tracks.get("title"))


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        logging.info("用法: python -m src.applemusic2flac <source_dir> <dest_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
