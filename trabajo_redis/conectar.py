import redis
import mysql.connector

def conexion():
    conexion_redis = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)

    baseDatosRedis = redis.Redis(connection_pool=conexion_redis)

    return baseDatosRedis


# Conexion a la BD MySQL de la tarea anterior (Dono8do). Mismos datos que en
# Dono8do/crear_todas_bd.py -> contenedor MySQL publicado en el puerto 3308
def conexion_mysql():
    config = {
        "user": "root", "password": "admin1234", "host": "127.0.0.1", "port": 3308, "database": "dono8do_mysql"
    }
    return mysql.connector.connect(**config)
