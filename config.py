import configparser

configer=configparser.ConfigParser()
configer.read('config.ini')
ogdbconfig=configer["RemoteDB"]

db=ogdbconfig["db"]
user=ogdbconfig["user"]
password=ogdbconfig["password"]
host=ogdbconfig["host"]
port=ogdbconfig["port"]
