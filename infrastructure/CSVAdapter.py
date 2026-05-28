from dataclasses import dataclass
import pandas as pd


@dataclass
class CSVAdapter:
    DATA_DIR = "data"

    def read(self, fileName: str):
        return pd.read_csv(f"{self.DATA_DIR}/{fileName}.csv")

    def write(self, data: list, fileName: str):
        df = pd.DataFrame(data)
        df.to_csv(f"{self.DATA_DIR}/{fileName}.csv", encoding="utf-8", index=False)
