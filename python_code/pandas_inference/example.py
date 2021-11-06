import numpy as np
import pandas as pd


def object_creation():
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print("Series: ", s)

    dates = pd.date_range("20130101", periods=6)
    print("dates: ", dates)
    df = pd.DataFrame(np.random.randn(6, 4), index=dates, columns=list("ABCD"))
    print(df)

    df2 = pd.DataFrame({
        "A": 1.0,
        "B": pd.Timestamp("20130102"),
        "C": pd.Series(1, index=list(range(5)), dtype="float32"),
        "D": np.array([3] * 5, dtype="int32"),
        "E": pd.Categorical(["test", "train", "test", "train", "train"]),
        "F": "foo",
    })
    print(df2)
    print(df2.dtypes)

    return df, df2


def viewing_data(df, df2):
    print(df.head(n=1))
    print(df.tail(n=2))

    print(df.index)
    print(df.columns)

    print(df.to_numpy())
    print(df2.to_numpy())

    print(df.describe())
    print(df2.describe())

    print(df.T)

    print(df.sort_index(axis=1, ascending=True))
    print(df.sort_values(by="A"))


if __name__ == '__main__':
    data_frame, data_frame2 = object_creation()
    viewing_data(data_frame, data_frame2)