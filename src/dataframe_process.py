import numpy as np
import pandas as pd

from src.utils import time_convert


def add_timeinseconds_col(df):

    df["Datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"])
    df = df.set_index("Datetime")

    df["Year"] = [d.split("-")[0] for d in df.Date]
    df["Year"] = df.Year.astype(int)
    df["Month"] = [d.split("-")[1] for d in df.Date]
    df["Month"] = df.Month.astype(int)
    df["Day"] = [d.split("-")[2] for d in df.Date]
    df["Day"] = df.Day.astype(int)
    df["Hour"] = [d.split(":")[0] for d in df.Time]
    df["Hour"] = df.Hour.astype(int)
    df["Minute"] = [d.split(":")[1] for d in df.Time]
    df["Minute"] = df.Minute.astype(int)

    # Find the seconds since 1970-01-01 00:00:00
    df["tn"] = df.apply(
        lambda row: time_convert(
            row["Year"], row["Month"], row["Day"], row["Hour"], row["Minute"]
        ),
        axis=1,
    )
    df = df.drop(["Date", "Time", "Year", "Month", "Day", "Hour", "Minute"], axis=1)

    time_sec = df.tn
    df["prec"] = df.prec.astype(float)

    full_list = np.arange(time_sec[0], time_sec[len(time_sec) - 1], 900).tolist()
    print(df.isna().sum())
    df = df.set_index("tn").reindex(full_list).reset_index().reindex(columns=df.columns)

    return df, full_list
