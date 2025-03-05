# applemusic2flac/__main__.py
# -*- coding: utf-8 -*-
import os
import sys
import shutil
from .metadata import ffprobe_get_metadata, extract_tags_from_metadata,parse_number, get_channels_and_samplerate
from .audio import convert_to_flac
from .framedepth import detect_true_bit_depth
from .utils import make_safe_filename

def main(source_dir: str, dest_dir: str):
    m4a_files = [os.path.join(root, f) for root, _, files in os.walk(source_dir) 
                 for f in files if f.lower().endswith(".m4a")]
    if not m4a_files:
        print("未找到任何 .m4a 文件，程序退出。")
        return
    else :
        print(f"找到 {len(m4a_files)} 个 .m4a 文件。")

    sample_file = m4a_files[0]
    metadata = ffprobe_get_metadata(sample_file)
    tags = extract_tags_from_metadata(metadata)
    artist = tags["artist"] or "UnknownArtist"
    album = tags["album"] or "UnknownAlbum"
    date = tags["date"] or "UnknownDate"
    target_dir = os.path.join(dest_dir, make_safe_filename(f"{artist} - {album} - ({date})"))
    os.makedirs(target_dir, exist_ok=True)

    for file_path in m4a_files:
        meta = ffprobe_get_metadata(file_path)
        track_tags = extract_tags_from_metadata(meta)
        channels, _ = get_channels_and_samplerate(meta)
        true_depth = detect_true_bit_depth(file_path, channels)
        '''
        tracknumber = parse_number(track_tags["tracknumber"])[0]
        discnumber = parse_number(track_tags["discnumber"])[0]
        print(parse_number(track_tags["discnumber"])[1])
        print(track_tags["totaldiscs"])
        '''

        track_title = track_tags["title"] or os.path.splitext(os.path.basename(file_path))[0]
        dst_filename = make_safe_filename(f"{track_tags["discnumber"]}.{track_tags["tracknumber"]}.{track_title}.flac")
        dst_file_path = os.path.join(target_dir, dst_filename)

        print(f"正在处理：{file_path}\n  -> 有效比特深度: {true_depth}, 输出文件: {dst_file_path}")
        convert_to_flac(file_path, dst_file_path, true_depth, track_tags)

    cover_jpg_path = next((os.path.join(root, f) for root, _, files in os.walk(source_dir) 
                           for f in files if f.lower() == "cover.jpg"), None)
    if cover_jpg_path:
        shutil.copy(cover_jpg_path, os.path.join(target_dir, "cover.jpg"))
        print(f"已复制封面到 {target_dir}")
    else:
        print("未找到 cover.jpg，不进行复制。")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python -m applemusic2flac <source_dir> <dest_dir>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])