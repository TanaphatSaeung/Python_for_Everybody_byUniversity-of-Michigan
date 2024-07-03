import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import numpy as np 
from datetime import datetime
import glob

csv_path = r'C:\Users\ASUS\Downloads\exchange_rate1.csv'
output_path_csv = r'C:\Users\ASUS\Downloads\money.csv'
output_path_db = r'C:\Users\ASUS\Downloads\money.db'
table_name = 'Largest_banks'
table_attribs = ['Name','MC_USD_Billion']
log_file = './code_log.txt'
url = 'https://web.archive.org/web/20230908091635%20/https://en.wikipedia.org/wiki/List_of_largest_banks'

#Log progrogress
def log_progress(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S'
    now = datetime.now()
    timestamp = now.strftime(timestamp_format)
    with open(log_file,"a") as f: 
        f.write(timestamp + ' : ' + message + '\n')
#Extract Data
def extract(url, table_attribs):
    df = pd.DataFrame(columns=table_attribs)
    html = requests.get(url).text
    data = BeautifulSoup(html,'html.parser')
    table = data.find_all('tbody')
    rows = table[0].find_all('tr')
    for row in rows:
        col = row.find_all('td')
        if len(col) != 0:
            data_dict = {'Name':col[1].text.rstrip(),
                         'MC_USD_Billion': col[2].text.rstrip()}
            df1 = pd.DataFrame(data_dict,index = [0])
            df = pd.concat([df,df1],ignore_index=True)
    return df
#Transformation DATA
def transform(df, csv_path):
    csv_read = pd.read_csv(csv_path)
    money = []
    for line in df['MC_USD_Billion']:
        money.append(line)
    EUR =[]
    GBP = []
    INR = []
    for line in money:
        line = float(line)
        EUR_t = np.round(line*csv_read['Rate'][0],2)
        GBP_t = np.round(line*csv_read['Rate'][1],2)
        INR_t = np.round(line*csv_read['Rate'][2],2)
        EUR.append(EUR_t)
        GBP.append(GBP_t)
        INR.append(INR_t)
    df['MC_GBP_Billion'] = GBP
    df['MC_EUR_Billion'] = EUR
    df['MC_INR_Billion'] = INR
    return df
#Loading DATA
def load_to_csv(df, output_path):
    df.to_csv(output_path)
def load_to_db(df, sql_connection, table_name):
    df.to_sql(table_name,sql_connection, if_exists = 'replace',index=False)
#Run SQL
def run_query(query_statement, sql_connection):
    print(query_statement)
    query_output = pd.read_sql(query_statement,sql_connection)
    print(query_output)
#LOGGING
log_progress('Extract data Start')
extracted_data = extract(url, table_attribs)
log_progress('Extraxct data Ended')
log_progress('Transformation data Start')
transformed_data = transform(extracted_data,csv_path)
log_progress('Transformation data Endded')
log_progress('Loading data to CSV file Start')
load_to_csv(transformed_data,output_path_csv)
log_progress('Loading data to CSV file Ended')
conn = sqlite3.connect(output_path_db)
log_progress('Loading data to db file Start')
load_to_db(transformed_data,conn,table_name)
log_progress('Loading data to db file Ended')
log_progress('Runnig SQL command Start')
query_statement = f'SELECT AVG(MC_GBP_Billion) FROM {table_name}'
run_query(query_statement,conn)
log_progress('Process Complete.')
conn.close()