import sys
from pathlib import Path


def file_path(*, day: int) -> Path:
    return Path(f"../{"test-" if "-t" in sys.argv else ""}data/d{day:02d}.txt")
