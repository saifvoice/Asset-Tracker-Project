import mysql.connector
from sqlalchemy import create_engine, engine_from_config
import configparser


##### Database Configuration ######
config = configparser.ConfigParser()
config.read('local_db.ini')
hostname = config['HOST_DATA']['hostname']
username = config['USER_DATA']['username']
password = config['USER_DATA']['password']
database = config['USER_DATA']['database']

# db = mysql.connector.connect(option_files='my.ini', database='tbcn_db')
config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
engine = engine_from_config(config, prefix='db.')
# cursor = db.cursor()
# db.close()

ret = engine.execute('Select * from customer_profile')
print(ret.rowcount)
engine.dispose()

