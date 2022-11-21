import mysql.connector
from sqlalchemy import create_engine, engine_from_config
import configparser
import random
import numpy as np
import pandas as pd


##### Database Configuration ######
config = configparser.ConfigParser()
config.read('local_db.ini')
hostname = config['HOST_DATA']['hostname']
username = config['USER_DATA']['username']
password = config['USER_DATA']['password']
database = config['USER_DATA']['database']

config = {'db.url': f'mysql+pymysql://{username}:{password}@{hostname}/{database}'}
engine = engine_from_config(config, prefix='db.')


adds_lat = np.random.random(100)
adds_lon = np.random.random(100)

lat = np.random.randint(7, 12, 100)
lon = np.random.randint(3, 12, 100)
lat = lat + adds_lat
lon = lon + adds_lon
nin = np.random.randint(58234367482, 59362733627, 100, dtype=np.int64)
phone = np.random.randint(2348048372892, 2348098372892, 100, dtype=np.int64)

first = ['Yazid', 'Mustapha', 'Habib', 'Khalil', 'Jacob', 'Kingsley', 'Aminu', 'Sagir', 'Dahir', 'John', 'Wasiu', 'Ronald', 'Grace', 'Precious', 'Sunday']
last = ['Khalid', 'Chukwuma', 'Chinedu', 'Paul', 'Ahmad', 'Shettima', 'Atiku', 'Yusuf', 'Aliyu', 'Kamal', 'Abubakar', 'Olu', 'Pius', 'Nicholas', 'Charles']

names = []
for i in range(100):
    full_name=random.choice(first)+" "+random.choice(last)
    names.append(full_name)

# for i in names:
#     print(i)
id_no = [i for i in range(2,102)]
assets = [random.choice(list(range(10))) for i in range(100)]
address = ['Customer address' for i in range(100)]

df_list = [names, address, phone, nin, assets, lat, lon]

df = pd.DataFrame(df_list, ['name', 'address', 'phone', 'nin', 'asset_count', 'latitude', 'longitude'])
df = df.transpose()
df['phone']= df['phone'].apply(lambda x: str(x))
# print(type(df['phone'][0]))

# df.to_sql(name = 'customer_profile', con=engine, if_exists='append', index=False)


