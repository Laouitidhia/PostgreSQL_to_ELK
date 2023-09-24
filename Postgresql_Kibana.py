from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import psycopg2
import pandas as pd
import time
import copy

import config


LIST_MAPPINGS = {"bluetooth":config.BLUETOOTH_MAPPING, "zigbee":config.BLUETOOTH_MAPPING,
                 "other_flows":config.OTHERFLOWS_MAPPING, "devices":config.DEVICES_MAPPING}
DATABASE_TABLES_ATTRIBUTES = {"bluetooth":config.BLUETOOTH_ATT, "other_flows":config.OTHERFLOWS_ATT,
                              "zigbee":config.BLUETOOTH_ATT, "devices":config.DEVICES_ATT}
RESET_FLAG = {"bluetooth":False, "zigbee":False, "other_flows":False, "devices":False}

def elasticsearch_connect(ip_addr, port, auth, path_to_certif):
    '''
        Connect to the elastic search web application to create a session
        
        :ip_addr: IP of the elasticsearch web app
        :port: port of the elasticsearch web app
        :auth: credentials of the connecting user on the web app
        :path_to_certif: certificate of the elasticsearch web app

        :return: a session id
    '''
    es = Elasticsearch(f"https://{ip_addr}:{port}",
                       ca_certs=f"{path_to_certif}/http_ca.crt",
                       basic_auth=auth)
    return es

def create_mapping(mapping, es, index_name, flag_index):
    '''
        create structure of the index in elastic search
        assign each feature its type

        :mapping: format of index
        :es: elastic search client id
        :index_name: chosen index name on the web app
        :flag_index: reset flag of database true if database has been reset
    '''
    if flag_index == True:
        delete_mappings(index_name)
        flag_index = False
    try: 
        es.search(index=index_name)
    except:
        rk=es.indices.create(index=index_name, mappings=mapping)
        return rk

def send_by_line(dataframe, es, index_name):
    '''
        Add logs line by line from the chosen database to the web app

        :dataframe: the data extracted from the database
        :es: elastic search client id
        :index_name: chosen index name on the web app
    '''

    for i, row in dataframe.iterrows():
        doc={}
        
        for column in range(len(dataframe.keys())):
            doc.update({
                dataframe.keys().values[column]:row[column]
                })
              
        es.index(index=index_name, id=i, document=doc)
        time.sleep(1)

#bulk to be modified
def send_bulk(df, es, indexname):
    """
        append all detected rows in database and send them together

        :df: dataframe of the database's table
        :es: session object to connect to Kibana
        :indexname: defined index name on Kibana
    """
    bulk_data = []
    doc={}
    for i,row in df.iterrows():
        for column in range(len(df.keys())):
            doc.update({
                df.keys().values[column]:row[column]
                })
        bulk_data.append(
            {
                "_index": indexname,
                "_id": i,
                "_source": copy.deepcopy(doc)
            }
        )
    bulk(es, bulk_data)

def postgresql_connect(config):
    """
        Establish session between python script and Postresql database

        :config: database configuration

        :return: cursor object used to send SQL requests to database
    """
    conn = psycopg2.connect(database=config["databasename"], user=config["username"],
                            password=config["password"], host=config["host"],
                            port=config["port"])
    return conn.cursor()

def send_data(tables, Attributes, cursor, listindex,
              time_to_sleep, data_row_number):
    """
        Send data to Kibana dashboard by line if database has increased by 1 row   
            or by bulk(all detected data) if there is more than one line or pass 
            if there is no change detected

        :tables: Dictionary of the names of the tables in postgresql
        :Attributes: Dictionary of the database column names of each table
        :cursor: used to send SQL requests to the database
        :listindex: lists of Kibana's index names
    """
    while 1:
        for key in tables.keys():
            cursor.execute(f'''SELECT * FROM {tables[key]} 
                                OFFSET {data_row_number[key]}''')
            result = cursor.fetchall()
            df = pd.DataFrame(result, columns=Attributes[key])
            data_row_number[key] += df.shape[0]
            if df.shape[0] == 0:
                continue
            elif df.shape[0] == 1:
                send_by_line(df,es,listindex[key])
            else:
                send_bulk(df,es,listindex[key])
        time.sleep(time_to_sleep)

def delete_mappings(index_name):
    """
        delete mapping of an index from elasticsearch
        any created dashboard with that mapping won't be deleted
        any visuals in the dashboard will stay with same configuration
        new data of the same mapping will be visualized in the same dashboard

        :index_name: name of the index in elasticsearch
    """
    es.indices.delete(index=index_name)


if __name__== "__main__":

    #Connect to elasticsearch and create a session
    es = elasticsearch_connect(config.IP_ADDR, config.PORT, 
                               config.CREDENTIALS, config.CERTIFICATE_PATH)

    #Connect to postgresql and create a cursor
    cur = postgresql_connect(config.DATABASE_CONFIG)

    #assign structure to the web app
    for key in config.INDEX_NAME_LIST.keys():
        create_mapping(LIST_MAPPINGS[key], es, config.INDEX_NAME_LIST[key], RESET_FLAG[key])
    
    #send data
    send_data(config.DATABASE_TABLES, DATABASE_TABLES_ATTRIBUTES, cur, 
              config.INDEX_NAME_LIST, config.UPDATE_TIME, config.DATA_INITIAL_OFFSET)
