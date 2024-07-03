import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import numpy as np 
from datetime import datetime

# Code for ETL operations on Country-GDP data
url = 'https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29'
db_name = 'World_Economies.db'
table_name = 'Countries_by_GDP'
csv_path = r'C:\Users\ASUS\Documents\Personal_Learning_Courses\Python\Countries_by_GDP.csv'
# Importing the required libraries

def extract(url):
    df = pd.DataFrame(columns=['Country','GDP_USD_millions'])
    html = requests.get(url).text
    data = BeautifulSoup(html,'html.parser') 
    tables = data.find_all('tbody')
    rows = tables[2].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col)!=0:
            if col[0].find('a') is not None and '—' not in col[2]:
                data_dict = {"Country": col[0].a.contents[0],
                             "GDP_USD_millions": col[2].contents[0]}
                df1 = pd.DataFrame(data_dict,index=[0])
                df = pd.concat([df,df1],ignore_index = True)
    return df

def transform(df):
    GDP_list = []
    for line in df["GDP_USD_millions"]:
        GDP_list.append(line)
    i = []
    for x in GDP_list:
        GDP_list = float("".join(x.split(',')))
        GDP_list = np.round(GDP_list/1000,2)
        i.append(GDP_list)
    df["GDP_USD_millions"]=i
    df = df.rename(columns={'GDP_USD_millions':'GDP_USD_billions'})
    return df

def loading(transformed_data,csv_path):
    transformed_data.to_csv(csv_path)
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name, sql_connection, if_exists='replace', index=False)
#Run SQL
def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement, sql_connection)
    print(query_output)
#LOG
def log_progress(message):
    timestamp_format = '%Y-%b-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open("./etl_project_log.txt","a") as f: 
        f.write(timestamp + ' : ' + message + '\n')

#Function calls
#Execute time for extracted data
log_progress('Extract phase End')
log_progress('Extact phase Strated')
extracted_data = extract(url)
log_progress('Extract phase End')
#Execute time for transformation data
log_progress('Transform phase Started')
transformed_data = transform(extracted_data)
print('Transformed Data')
print(transformed_data)
log_progress("Transform phase Ended")
#Execute time for Loading Data
log_progress('Load phase Stated')
loading(transformed_data,csv_path)
log_progress('Load phase Ended')
#Statrt SQL
log_progress('Starting connect SQL database')
conn = sqlite3.connect(db_name)
log_progress('connected SQL database')
#Load data to database
load_to_db(transformed_data,conn,table_name)
log_progress('Data loaded to Database as table. Running the query')
#use SQL
log_progress('Use SQL command')
query_statement= f"SELECT * from {table_name} WHERE GDP_USD_billions >= 100"
run_query(query_statement, conn)
log_progress('Process Complete.')
conn.close()