import pandas as pd

from app.storage.csv_storage import CSVStorage


class CSVStorageImpl(CSVStorage):
    def read_csv(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path, encoding="utf-8-sig")
