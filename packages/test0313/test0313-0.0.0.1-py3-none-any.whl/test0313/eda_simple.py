import pandas as pd
from plot import plot
from process import process


class EDA:
    def __init__(self, df, target_column, drop_columns=None, mini=False, sample_fraction=0.1):
        self.df = df.copy()
        self.target_column = target_column
        self.mini = mini

        # Drop specified columns if any
        if drop_columns:
            self.df.drop(drop_columns, axis=1, inplace=True)

        if self.target_column not in self.df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in dataset")

        # 샘플링 옵션
        if self.mini:
            self.df = self.df.sample(frac=sample_fraction, random_state=42)

        self.plot = plot(df=self.df, target_column=self.target_column)
        self.process = process(df=self.df, target_column=self.target_column)

    def display_basic_info(self):
        print("Basic Information of the Dataset:")
        print("Shape:", self.df.shape)
        print("\nFirst 5 Rows:\n", self.df.head())
        print("\nData Types:\n", self.df.dtypes)
        print("\nSummary Statistics:\n", self.df.describe())
