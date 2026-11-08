from datetime import datetime

import conectar

# EJERCICIO 22: Obtener datos de Redis (stock de sangre 'stock:*' creado por scriptDono8do.py)
# e incluirlos en la tabla StockSangre de MySQL

db = conectar.conexion()
cnx = conectar.conexion_mysql()
cursor = cnx.cursor()

print("#####22. Obtener datos de Redis e incluirlos en MySQL#####")
for clave in db.scan_iter("stock:*"):
    letra, signo = clave.split(":")[1].split("_")       # 'stock:A_positivo' -> 'A', 'positivo'
    grupo = letra + ("+" if signo == "positivo" else "-")  # -> 'A+'
    bolsas = int(db.get(clave))
    cursor.execute(
        "INSERT INTO StockSangre (grupo_sanguineo, cantidad_bolsas, fecha_actualizacion) VALUES (%s, %s, %s)",
        (grupo, bolsas, datetime.now()),
    )
    print(f"Redis {clave}={bolsas} -> insertado en StockSangre: grupo {grupo}, {bolsas} bolsas")
cnx.commit()

cursor.execute("SELECT * FROM StockSangre")
print("Contenido de StockSangre en MySQL:")
for fila in cursor.fetchall():
    print(fila)

cursor.close()
cnx.close()
