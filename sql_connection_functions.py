# -*- coding: utf-8 -*-
"""
@author: Ross Drucker
"""
import pandas as pd
import sqlalchemy

import os 
drive = os.path.dirname(os.path.realpath(__file__))[0]
import CommonFunctions as cf

def split_df_into_chunks(df, chunkSize = 2000):
    '''
    Takes in a big df and returns smaller dfs of the bigger df in chunks
    '''
    listOfDf = list()
    numberChunks = len(df) // chunkSize + 1
    for i in range(numberChunks):
        listOfDf.append(df[i*chunkSize:(i+1)*chunkSize])
    return listOfDf


def getLoginCredentials(file = ''):
    '''
    Gathers user and password from file
    '''
    
    temp = [1]
    while temp != []:
        try:
            with open(file) as f:
                lines = f.readlines()
                user = lines[0].strip()
                password = lines[1].strip()
            temp = []
        except:
            pass
        
    return user, password


def get_username_password(file):
    '''
    Takes in a file
    Reads in the lines of the file and returns the first two lines of the file as
    variables
    '''
    
    with open(file) as f:
        lines = f.readlines()
        user = lines[0].strip()
        password = lines[1].strip()
        
    return user, password

def getLoginCredentials2(file = os.path.join(SQLCF_dir, 'SQL_Password.txt'), max_count = 20):
    '''
    Gathers user and password from file
    '''
        
    # Define a base username and password
    user = ''
    password = ''
    

    i = 0
    
    # Attempt to get username and password
    while i < max_count:
        try:
            user, password = get_username_password(file)
            break
        except:
            pass
        
        i+=1

    return user, password

def dataframeToSql(df, table_name, server = '', database = '', driver = 'SQL+Server+Native+Client+11.0', ifexists = 'append'):
    '''
    Creates a SQL table from input dataframe. ifexists must be set to 'replace' (replace the data in the SQL table) or 'append' (add to the data in the SQL).
    '''
    import warnings
    import sqlalchemy
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=sqlalchemy.exc.SAWarning)
        user, password = getLoginCredentials()

        engine = sqlalchemy.create_engine(f'mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver}')
        try:
            df.to_sql(table_name, engine, if_exists=ifexists, index=False)
            return []
        except Exception as e:
            return [str(e)]
        
        
def chunked_sql_df_upload(df, table_name, database = '', ifexists = 'append', driver = 'SQL+Server+Native+Client+11.0', speak = True):
    '''
    Takes in a df, chunks it, and uploads the chunks individually to SQL
    helps to prevent the SQL TCP Connection errors
    '''
    chunked_df_list = split_df_into_chunks(df)
    counter = 0
    total_dfs = len(chunked_df_list)
    while chunked_df_list != []:
        if speak:
            print('Trying to Upload DF {} of {} ({}%)'.format(str(counter + 1), str(total_dfs), str(cf.truncate(100 * (counter + 1) / total_dfs))))
            
        small_df = chunked_df_list[0]
        val = dataframeToSql(small_df, table_name, database = database, ifexists = ifexists, driver = driver)
        if val == []:
            chunked_df_list.remove(small_df)
            counter+=1
        else:
            print('\n ERROR: {} \n Trying to Upload Again...'.format(str(val[0])))
        
        
def non_return_queries(query, server = '', database = '', driver = 'SQL+Server+Native+Client+11.0'):
    '''
    Performs queries which do not need/have a return statement for python
    '''
    

    user, password = getLoginCredentials()
    engine = sqlalchemy.create_engine('mssql+pyodbc://{0}:{1}@{2}/{3}?driver={4}'.format(user,password,server,database,driver))
    
    # Make connection
    conn = engine.connect()
    # Begin connection
    trans = conn.begin()
    # Execute query
    conn.execute(query)
    # Commit query
    trans.commit()
    # Close connection
    conn.close()
            


def sqlToDataframe(sql,server = '', database = '', driver = 'SQL+Server+Native+Client+11.0'):
    '''
    Returns a pandas dataframe from sql query results
    '''
    user, password = getLoginCredentials()


    engine = sqlalchemy.create_engine('mssql+pyodbc://{0}:{1}@{2}/{3}?driver={4}'.format(user,password,server,database,driver))

    df = pd.read_sql(sql,engine)
    return df