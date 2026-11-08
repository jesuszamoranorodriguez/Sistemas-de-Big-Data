import conectar

# Vacia por completo Redis (FLUSHDB tambien elimina los indices de busqueda)

db = conectar.conexion()
print(f"Claves antes de vaciar: {db.dbsize()}")
db.flushdb()
print(f"Claves despues de vaciar: {db.dbsize()}")
