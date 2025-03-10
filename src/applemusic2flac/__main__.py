# applemusic2flac/__main__.py
"""Main entry point for the applemusic2flac conversion tool."""

import logging
import shutil
import sys
from pathlib import Path

from .album import get_album_metadata, get_album_metadata_sample
from .audio import convert_to_flac
from .framedepth import detect_true_bit_depth
from .track import get_track_metadata
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
    album_metadata_sample = get_album_metadata_sample(m4a_files, 0)
    foldername_sample = make_safe_filename(
        f"{album_metadata_sample.albumartist} - {album_metadata_sample.album} - ({album_metadata_sample.date})"
    )
    target_dir = Path(dest_dir) / foldername_sample
    track_metadata_set = []

    Path.mkdir(target_dir, exist_ok=True)

    # 逐个处理音轨
    for file_path in m4a_files: 
        cover = False
        # metadata = ffprobe_get_metadata(file_path)
        # track_tags = extract_tags_from_metadata(metadata)
        track_metadata = get_track_metadata(file_path)
        track_metadata_set.append(track_metadata) # 收集整张专辑的音轨信息用于判断专辑信息
        # channels, _ = get_channels_and_samplerate(metadata)
        # true_depth = detect_true_bit_depth(file_path, track_metadata.channels) # 获取真实比特深度
        track_title = track_metadata.title or Path(file_path).stem # 获取音轨标题

        dst_filename = make_safe_filename(
            f"{track_metadata.discnumber}.{track_metadata.tracknumber}.{track_title}.flac"
        )
        dst_file_path = Path(target_dir) / dst_filename

        logging.info(
            "正在处理: %s -> 有效比特深度: %s ,输出文件: %s",
            Path(file_path).name,
            track_metadata.bit_depth,
            dst_file_path,
        )
        convert_to_flac(file_path, dst_file_path, track_metadata.bit_depth, track_metadata)

    # 封面处理
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
    album_metadata = get_album_metadata(track_metadata_set)


if __name__ == "__main__":
    if len(sys.argv) < 3:  # noqa: PLR2004
        logging.info("用法: python -m src.applemusic2flac <source_dir> <dest_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
