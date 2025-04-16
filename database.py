import os
import pandas as pd
from dotenv import load_dotenv, dotenv_values
from sqlalchemy import create_engine
from sql import sql_p
import oracledb as odb

load_dotenv()
host = os.environ.get("HOST_DB")
port = os.environ.get('PORT_DB')
service_name = os.environ.get("SERVICE_NAME_DB")
user = os.environ.get("USER_DB")
password = os.environ.get("PASSWORD_DB")
engine = create_engine(f"oracle+oracledb://{user}:{password}@{host}:{port}/?service_name={service_name}")


def get_data(query,cd_grupo_material,ie_padronizado):
    try:
        with engine.connect() as connection:
            data = pd.read_sql(query, connection,params={'cd_grupo_material':cd_grupo_material,'ie_padronizado':ie_padronizado})
            return data
    except odb.Error as e:
        print(f'Error: {e}')
        return pd.DataFrame()

def get_data_fornecedor(query,cd_material):
    try:
        with engine.connect() as connection:
            data = pd.read_sql(query, connection,params={'cd_material':cd_material})
            return data
    except odb.Error as e:
        print(f'Error: {e}')
        return pd.DataFrame()
    
def get_data_oc(query,cd_material,cd_cgc_fornecedor):
    try:
        with engine.connect() as connection:
            data = pd.read_sql(query, connection,params={'cd_material':cd_material, 'cd_cgc_fornecedor':cd_cgc_fornecedor})
            return data
    except odb.Error as e:
        print(f'Error: {e}')
        return pd.DataFrame()
#data = get_data(sql_p)
#print(data)