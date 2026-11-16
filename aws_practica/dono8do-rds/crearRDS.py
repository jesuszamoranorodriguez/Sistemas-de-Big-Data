import os

import boto3
from dotenv import load_dotenv

load_dotenv() 

session = boto3.session.Session(
   aws_access_key_id=os.getenv("ACCESS_KEY"),
   aws_secret_access_key=os.getenv("SECRET_KEY"),
   aws_session_token=os.getenv("SESSION_TOKEN"),
   region_name=os.getenv("REGION"))

rds = session.client('rds')

rds.create_db_instance(
    DBInstanceIdentifier="dono8do-db", #Nombre de la instancia del RDS (dono8do-db)
    AllocatedStorage= 20, #El tamaño del RDS
    DBInstanceClass="db.t4g.micro", #Tipo de clase de la base de datos
    Engine="mariadb", # motor de base de datos
    MasterUsername=os.getenv("DB_USER"), #usuario de la base de datos
    MasterUserPassword=os.getenv("DB_PASSWORD"), #password del usuario admin
    PubliclyAccessible=True #Publicar el RDS
 )


waiter = rds.get_waiter('db_instance_available') #Usaremos el waiter para continuar con el código cuando esté disponible el RDS
waiter.wait(DBInstanceIdentifier="dono8do-db")


info = rds.describe_db_instances(DBInstanceIdentifier="dono8do-db")
endpoint = info['DBInstances'][0]['Endpoint']['Address'] #IMPORTANTE, necesitamos el endpoint para conectarnos a la base de datos

print(endpoint)
