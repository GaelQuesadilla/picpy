from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Tuple


@dataclass
class ImageMetadata:
    name: str = field(default="")
    path: Optional[Path] = field(default=None)
    size: Tuple[int, int] = field(default_factory=lambda: (0, 0))
