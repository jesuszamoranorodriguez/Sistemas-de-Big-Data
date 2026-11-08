import conectar

# EJERCICIO 21: Obtener datos de la BD MySQL de la tarea anterior mediante una SQL e incluirlos en Redis

db = conectar.conexion()
cnx = conectar.conexion_mysql()
cursor = cnx.cursor(dictionary=True)

print("#####21. Obtener datos de MySQL con una SQL e incluirlos en Redis#####")
sql = "SELECT id_usuario, nombre, apellidos, grupo_sanguineo FROM Usuario"
print(f"SQL ejecutada: {sql}")
cursor.execute(sql)

for fila in cursor.fetchall():
    clave = f"mysql:usuario:{fila['id_usuario']}"
    db.hset(clave, mapping={k: str(v) for k, v in fila.items()})
    print(f"Guardado en Redis: {clave} -> {db.hgetall(clave)}")

cursor.close()
cnx.close()
