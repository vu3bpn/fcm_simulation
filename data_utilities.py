import os
import pandas as pd
from fuzzywuzzy import process

def merge_tables(filenames):
    """
    Merges multiple Excel files into a single DataFrame with standardized columns.
    
    Args:
        filenames (list): List of Excel file paths to merge.      
    
    Returns:
        pd.DataFrame: Merged DataFrame.
    """         
    all_columns = set()
    dfs = []    
    for file in filenames:
        df = pd.read_excel(file)
        df.columns = df.columns.str.strip()
        first_col = df.columns[0]
        sorted_cols = sorted(df.columns[1:])
        df = df[[first_col] + sorted_cols]
        dfs.append(df)
        all_columns.update(df.columns.str.strip())
    
    master_columns = list(all_columns)

    def match_columns(df, master_columns, threshold=80):
        new_columns = {}
        for col in df.columns:
            match, score = process.extractOne(col, master_columns)
            if score >= threshold:
                new_columns[col] = match
            else:
                new_columns[col] = col  # Keep original if no good match
        df = df.rename(columns=new_columns)
        for col in master_columns:
            if col not in df.columns:
                df[col] = None
        return df[master_columns]