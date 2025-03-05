# applemusic2flac/utils.py
import re

def make_safe_filename(name: str) -> str:
    return re.sub(r'[\\/:*?"<>|]', '_', name)