import pandas as pd

LDF_AVERAGES = {
            # 'Geometric': 'geometric',
            # 'Medial': 'medial',
            'Regression': 'regression',
            'Straight': 'simple',
            'Volume': 'volume'
}

TEMP_LDF_LIST = pd.DataFrame(
    data=[
        [True, "All-year volume-weighted", "Volume", "9"],
        [False, "3-year volume-weighted", "Volume", "3"],
        [False, "5-year volume-weighted", "Volume", "5"],
    ],
    columns=["Selected", "Label", "Type", "Number of Years"]
)


