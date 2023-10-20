# PostgreSQL_to_ELK

The written python script is divided into two files: 
  “config.py” for all configuration variables.
  “Postgresql_Kibana.py” present the functions of the script.

Before starting, some main configurations must be verified in the config file:
  Under the Elasticsearch config comment, we have 
        CREDENTIALS (username and password: configured when installed), 
        CERTIFICATE_PATH (path of elasticsearch certificate in your machine), 
        IP_ADDR (usually localhost), 
        PORT (usually 9200).
  Under PostgreSQL database and data config comment, we have in the 
        DATABASE_CONFIG under “databasename” (database on PostgreSQL), 
        “username” (programmed user on PostgreSQL), 
        “password” (programmed password when installed must be “postgres”), 
        “host” (usually localhost), 
        “port” (usually 5432).

The python script is filled with docstrings and comments explaining how it works, its main function is an infinite while loop under the “send_data” function: that gets data from PostgreSQL and then sends it to Kibana. 
If needed, you can program a time to sleep since you may not want your script to work all day when you are not monitoring anything. 
The time to sleep is easily configured in the config file under UPDATE_TIME (= 0 by default for a total real-time experience).
Other possible modifications are offered in the config file under Kibana data config to add a new index file if needed in INDEX_NAME_LIST, then you must add a new mapping or use one of the preconfigured mappings in the main file LIST_MAPPINGS, also add the table's name in config file DATABASE_TABLES then add new table attributes list and register it in main file DATABASE_TABLES_ATTRIBUTES. 
In all these dictionary-type variables, you must use the same key.
If you want to reset the visuals, you can change the RESET_FLAGS in the main file to True, and increment DATA_INITIAL_OFFSET with the corresponding table's length.

