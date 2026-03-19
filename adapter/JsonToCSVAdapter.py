from dataclasses import dataclass
import pandas as pd


@dataclass
class JsonToCSVAdapter:
    def write(self, data: list, fileName: str):
        df = pd.DataFrame(data)
        df.to_csv(f"{fileName}.csv", encoding="utf-8", index=False)
