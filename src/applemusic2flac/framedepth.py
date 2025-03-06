import logging
import subprocess
from typing import Optional


def detect_true_bit_depth(file_path: str, channels: int, max_frames: int = 100_000) -> int:
    """检测音频文件的真实比特深度(16位或24位)。

    Args:
        file_path: 音频文件路径
        channels: 声道数
        max_frames: 最大检查帧数, 默认100,000

    Returns
    -------
        int: 24 (真24位) 或16 (实际16位或检测失败)
    """
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", file_path,
        "-vn",
        "-acodec", "pcm_s24le",
        "-f", "s24le",
        "-hide_banner",
        "-loglevel", "error",  # 减少不必要输出
        "pipe:"
    ]
    frame_size = channels * 3  # 每帧字节数: 声道数 * 3字节 (24位)

    """分析音频数据的比特深度。"""
    process: Optional[subprocess.Popen] = None
    try:
        # 使用 subprocess.PIPE 替代 pipe:1, 避免平台差异
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = process.stdout
        if stdout is None:
            logging.warning("无法打开子进程的标准输出, 使用默认比特深度 16")
            return 16

        for _frames_checked in range(max_frames):
            frame_data = stdout.read(frame_size)
            # print(''.join(format(byte, '08b') for byte in frame_data))
            if not frame_data or len(frame_data) < frame_size:
                break
            if _check_frame_depth(frame_data):
                return 24
        else:
            return 16
    except (subprocess.SubprocessError, OSError) as e:
        logging.warning("比特深度检测出错, 使用默认比特深度: %s", e )
        return 16
    finally:
        if process and process.poll() is None:  # 仅在进程未结束时清理
            process.terminate()
            process.wait(timeout=1)  # 等待进程结束, 避免僵尸进程

def _check_frame_depth(frame_data: bytes) -> bool:
    """检查单帧数据是否使用超过16位深度。"""
    # 使用切片和 any() 提高性能
    return any(byte != 0 for byte in frame_data[::3])
