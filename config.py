#Elasticsearch config
CREDENTIALS = ("elastic", "%%%%%%%%%%")
CERTIFICATE_PATH = "%%%%%%%%%%"
IP_ADDR = "localhost"
PORT = "9200"
UPDATE_TIME=0           # Time in seconds to update database

#Kibana data config
INDEX_NAME_LIST = {"bluetooth":"bluetooth_traffic", "zigbee":"zigbee_traffic", "other_flows":"other_traffic", "devices":"devices"}
DEVICES_MAPPING = {
            "properties": {
                "id": {"type" : "keyword"},
                "device_identifier": {"type" : "keyword"},
                "hostname": {"type" : "keyword",
                             "null_value": "NULL"},
                "ip": {"type" : "ip"},
                "oui": {"type" : "keyword"},
                "mac": {"type" : "keyword"},
                "network_chipset": {"type" : "keyword",
                                    "null_value": "NULL"},
                "monitor": {"type" : "boolean"},
                "user_id": {"type" : "keyword"},
                "inserted_at":{"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
                "updated_at": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"}
        }
    }
BLUETOOTH_MAPPING = {
    "properties":{
        "id": {"type" : "long"},
        "device_identifier": {"type" : "keyword"},
        "time": {"type" : "long"},
        "source": {"type" : "keyword"},
        "destination": {"type" : "keyword"},
        "protocol": {"type" : "keyword"},
        "packet_length": {"type" : "long"},
        "frame_length": {"type" : "long"},
        "rssi": {"type" : "keyword"},
        "channel": {"type" : "keyword"},
        "device_id": {"type" : "keyword"},
        "inserted_at":{"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
        "updated_at": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"}
    }
}
OTHERFLOWS_MAPPING = {
    "properties":{
        "id": {"type" : "long"},
        "device_port": {"type" : "keyword"},
        "remote_ip": {"type" : "ip"},
        "remote_ip_owner": {"type" : "keyword"},
        "remote_ip_city": {"type" : "keyword"},
        "remote_ip_country": {"type" : "keyword"},
        "remote_port": {"type" : "keyword"},
        "protocol": {"type" : "keyword"},
        "inbound_byte_count": {"type" : "long"},
        "outbound_byte_count": {"type" : "long"},
        "Device id": {"type" : "keyword"},
        "Inserted at":{"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"},
        "Updated at": {"type": "date", "format": "yyyy-MM-dd'T'HH:mm:ss"}
    }
}
#ZIGBEE_MAPPING = BLUETOOTH_MAPPING



#Postgresql database and data config
DATABASE_CONFIG = {"databasename":"net_snitch_dev", "username":"postgres", "password":"postgres", "host":"localhost", "port":"5432"}
DATABASE_TABLES = {"bluetooth":"bluetooth_flows", "other_flows":"flows", "zigbee":"zigbee_flows", "devices":"devices"}
BLUETOOTH_ATT=["id","device_identifier","time","source","destination","protocol","packet_length","frame_length","rssi","channel","device_id","inserted_at","updated_at"]
OTHERFLOWS_ATT=["id","device_port","remote_ip","remote_ip_owner","remote_ip_city","remote_ip_country","remote_port","protocol","inbound_byte_count","outbound_byte_count","device_id","inserted_at","updated_at"]
#ZIGBEE_ATT = BLUETOOTH_ATT
DEVICES_ATT=["id","device_identifier","hostname","ip","oui","mac","network_chipset","monitor","user_id","inserted_at","updated_at"]

DATA_INITIAL_OFFSET = {"bluetooth":0, "zigbee":0, "other_flows":0, "devices":0}
