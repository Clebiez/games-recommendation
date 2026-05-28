from dataclasses import dataclass
from pathlib import Path
import pandas as pd


@dataclass
class CSVAdapter:
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"

    def read(self, fileName: str):
        return pd.read_csv(self.DATA_DIR / f"{fileName}.csv")

    def write(self, data: list, fileName: str):
        df = pd.DataFrame(data)
        df.to_csv(f"{self.DATA_DIR}/{fileName}.csv", encoding="utf-8", index=False)
