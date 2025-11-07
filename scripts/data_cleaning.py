import pandas as pd
from datetime import datetime
timeStamp = datetime.now().strftime("%H%M%S")

filePath = '../data/movies_data_1.csv'

df = pd.read_csv(filePath)

allColumns = ['MOVIES','YEAR','GENRE','RATING','ONE-LINE','STARS','VOTES','RunTime','Gross']
df = df.dropna(subset=allColumns, axis=0, how='all')

nColumns = ['GENRE','ONE-LINE','STARS']
ownerColumn = ['owner_company']

for col in nColumns:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('\n', '', regex=False)
            .str.strip()
        )

for col in ownerColumn:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace('\t', '', regex=False)
            .str.strip()
        )

df['STARS'] = df['STARS'].fillna('')

has_pipe = df['STARS'].str.contains('|', regex=False)

df[['DIRECTOR','STARS-LIST']] = df.loc[has_pipe, 'STARS'].str.split('|', n=1, expand=True)
df.loc[~has_pipe, 'DIRECTOR'] = ''
df.loc[~has_pipe, 'STARS-LIST'] = df.loc[~has_pipe, 'STARS']
df['DIRECTOR'] = df['DIRECTOR'].str.strip()
df['STARS-LIST'] = df['STARS-LIST'].str.strip()

df.drop(columns=['STARS'], inplace=True)

df['Extract_date'] = pd.to_datetime(df['Extract_date'],errors='coerce')
df['extraction_date'] = df['Extract_date'].dt.date
df['extraction_time'] = df['Extract_date'].dt.time

df.drop(columns=['Extract_date'], inplace=True)

df.reset_index(drop=True, inplace=True)

df['YEAR'] = df['YEAR'].fillna('')
df['YEAR'] = df['YEAR'].str.replace(r'\(I\)', '', regex=True)
df['YEAR'] = df['YEAR'].str.replace(r'\(II\)', '', regex=True)
df['YEAR'] = df['YEAR'].str.replace(r'\(III\)', '', regex=True)
df['YEAR'] = df['YEAR'].str.replace(r'\(', '', regex=True)
df['YEAR'] = df['YEAR'].str.replace(r'\)', '', regex=True)
df['YEAR'] = df['YEAR'].str.replace('–', '-')
df['YEAR'] = df['YEAR'].str.replace(r'[^\d-]', '', regex=True)
df['YEAR'] = df['YEAR'].str.strip()
df['YEAR'] = df['YEAR'].replace('', '-')
df[['start_year','end_year']] = df['YEAR'].str.split('-',n=1, expand=True)
df['end_year'] = df['end_year'].fillna(df['start_year'])
df['end_year'] = df['end_year'].replace('', 'present')

durations = []

for i in range(len(df)):
    start = df.loc[i,'start_year']
    end = df.loc[i,'end_year']

    if end == 'present':
        durations.append(pd.NA)
    else:
        durations.append(int(end) - int(start) + 1)

df['duration_in_years'] = durations
df.drop(columns=['YEAR'], inplace=True)

unique_companies = df['owner_company'].dropna().unique()

DimCompan = pd.DataFrame(unique_companies, columns=['DimCompan'])

unique_directors = df['DIRECTOR'].dropna().unique()

DimDirector = pd.DataFrame(unique_directors, columns=['DimDirector'])

DimCompan.to_csv(f"../output/uniqueCompany.csv",index=False)
DimDirector.to_csv(f"../output/uniqueDirector.csv",index=False)
df.to_csv(f"../output/cleanedData.csv",index=False)
df.to_excel(f"../output/cleanedData.xlsx",index=False)