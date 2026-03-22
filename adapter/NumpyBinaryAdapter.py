from dataclasses import dataclass
import numpy as np


@dataclass
class NumpyBinaryAdapter:
    def read(self, fileName: str):
        return np.load(f'{fileName}.npy')

    def write(self, data: list, fileName: str):
        np.save(f'{fileName}.npy', data)
