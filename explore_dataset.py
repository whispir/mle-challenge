"""
Run this file to explore the dataset to decide what
kinds of pre-processing are needed.
"""
import os
import pandas as pd


if __name__ == "__main__": 
    CUR_DIR = os.getcwd()
    file = os.path.join(CUR_DIR, "data/wind_power_generation.csv")
    df = pd.read_csv(file)
    
    df.info()

    for col in df.columns:
        print("\nStats for column {}: ".format(col))
        print(df[col].describe())
    
    # exploration findings:
    #   - The datatime column is unnamed
    #   - The value of 'ControlBoxTemperature' is either 0.0 or missing
    #   - Column 'WTG' has only one unique value: 'G01'

    print("\n\n", df['ControlBoxTemperature'].value_counts())
    print(df['WTG'].value_counts())