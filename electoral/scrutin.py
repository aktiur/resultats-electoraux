from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List


@dataclass
class Scrutin:
    id: str
    url: str
    cleaner: Callable[[str, str], List[str]]

    def raw_filename(self):
        return Path("dist") / "raw" / (self.id + ".txt")

    def dist_filename(self, format, unit):
        return Path("dist") / "data" / f"{self.id}_par_{unit}_{format}.csv"
