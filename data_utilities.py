import os
import pandas as pd
import numpy as np
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
    
    standardized_dfs = [match_columns(df, master_columns) for df in dfs]
    '''
    merged_df = pd.concat(standardized_dfs,
                          ignore_index=True
                         )
  
    merged_list = []
    
    df_row_list = [ merged_list.extend(x.to_dict()) for x in standardized_dfs]
    merged_df = pd.DataFrame(merged_list)
    '''
    merged_df = pd.concat(standardized_dfs,
                      ignore_index=True,
                     )
    sorted_df = merged_df.columns.to_list()
    sorted_df.insert(0, sorted_df.pop(sorted_df.index('Unnamed: 0')))
    merged_df = merged_df.loc[:, sorted_df]
    merged_df['Unnamed: 0'] = [x.strip() for x in merged_df['Unnamed: 0']]  
    first_col = merged_df.columns[0]
    sorted_cols = sorted(merged_df.columns[1:])
    merged_df = merged_df[[first_col] + sorted_cols]
    mean_df = merged_df.groupby('Unnamed: 0').mean()
    mean_df = mean_df.sort_values(by='Unnamed: 0')
    mean_df = mean_df.fillna(0)
    #mean_df  = np.nan_to_num(mean_df ,nan=0)
    return mean_df