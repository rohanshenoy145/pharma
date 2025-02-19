import pandas as pd
import numpy as np


def main():
    # Specify the path to the CSV file
    file_path = './dataset/drugbank_clean.csv'

    # Load the CSV into a DataFrame
    df = pd.read_csv(file_path)

    df_filtered = df[['drugbank-id','name','description' ,'drug-interactions']] 
    df_filtered.dropna(how='all', inplace=True)
    df_filtered['drug-interactions'].fillna('No interaction', inplace=True)

    # Display the first few rows to check
    print(df_filtered.head())

    

if __name__ == '__main__':
    main()

#Source of data: https://www.kaggle.com/datasets/devildev89/drug-bank-5110?select=drugbank_clean.csv

