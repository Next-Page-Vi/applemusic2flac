# applemusic2flac/utils.py
"""Utility functions for the applemusic2flac package."""
import re


def make_safe_filename(name: str) -> str:
    """Convert string to a safe filename by replacing special characters.

    Args:
        name (str): The original string to be converted

    Returns
    -------
        str: A string with special characters replaced by underscores
    """
    return re.sub(r'[\\/:*?"<>|]', "_", name)
