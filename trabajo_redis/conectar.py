import redis

def conexion():
    conexion_redis = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)

    baseDatosRedis = redis.Redis(connection_pool=conexion_redis)

    return baseDatosRedis