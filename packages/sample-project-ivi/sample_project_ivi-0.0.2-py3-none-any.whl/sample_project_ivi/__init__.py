import os

from .src import calculate_mean, print_mean

__all__ = ["calculate_mean", "print_mean"]

# read the version from version.txt
with open(os.path.join(os.path.dirname(__file__), "version.txt"), encoding="utf-8") as file_handler:
    __version__ = file_handler.read().strip()
