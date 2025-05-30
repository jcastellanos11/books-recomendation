# AIL_Library/utils.py
import pandas_profiling

def profile_data(df):
    return df.profile_report(title="Data Report")
