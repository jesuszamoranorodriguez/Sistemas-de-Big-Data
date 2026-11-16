import os
import json

from dotenv import load_dotenv
import mysql.connector

load_dotenv()

config = {
       "user": os.getenv("DB_USER"),
       "password": os.getenv("DB_PASSWORD"),
       "host": os.getenv("ENDPOINT"),
   }
DB_NAME = os.getenv("DB_NAME")

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor(dictionary=True)

cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
cursor.execute(f"USE {DB_NAME}")

cursor.execute("CREATE TABLE IF NOT EXISTS Centro (id_centro INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), ciudad VARCHAR(100)) ENGINE=InnoDB;")
cursor.execute("CREATE TABLE IF NOT EXISTS Usuario (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), apellidos VARCHAR(150), grupo_sanguineo VARCHAR(5), email VARCHAR(150), fecha_registro DATE) ENGINE=InnoDB;")
cursor.execute("CREATE TABLE IF NOT EXISTS StockSangre (id_stock INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, grupo_sanguineo VARCHAR(5), cantidad_bolsas INT, FOREIGN KEY (id_centro) REFERENCES Centro(id_centro)) ENGINE=InnoDB;")

cursor.execute("SELECT COUNT(*) AS total FROM Centro")
if cursor.fetchone()["total"] == 0:
    cursor.executemany("INSERT INTO Centro (nombre, ciudad) VALUES (%s, %s)", [
        ("Hospital Virgen del Rocío", "Sevilla"),
        ("Centro de Transfusión", "Málaga"),
    ])
    cursor.executemany("INSERT INTO Usuario (nombre, apellidos, grupo_sanguineo, email, fecha_registro) VALUES (%s, %s, %s, %s, %s)", [
        ("Jose", "Cortes", "A+", "jose@mail.com", "2026-01-15"),
        ("Celia", "Verdugo", "O-", "celia@mail.com", "2026-03-02"),
        ("Jesus", "Zamorano", "A+", "jesus@mail.com", "2026-05-20"),
        ("Pablo", "Rodriguez", "B+", "pablo@mail.com", "2026-07-11"),
    ])
    cursor.executemany("INSERT INTO StockSangre (id_centro, grupo_sanguineo, cantidad_bolsas) VALUES (%s, %s, %s)", [
        (1, "A+", 40), (1, "O-", 8), (1, "B+", 15),
        (2, "A+", 25), (2, "O-", 5), (2, "B+", 12),
    ])
    cnx.commit()
    print("Datos insertados")

consultas = {
    "usuarios": "SELECT * FROM Usuario",
    "donantes_por_grupo": "SELECT grupo_sanguineo, COUNT(*) AS total FROM Usuario GROUP BY grupo_sanguineo",
    "stock_bajo": "SELECT c.nombre AS centro, c.ciudad, s.grupo_sanguineo, s.cantidad_bolsas FROM StockSangre s JOIN Centro c ON s.id_centro = c.id_centro WHERE s.cantidad_bolsas < 10",
}

for nombre, sql in consultas.items():
    cursor.execute(sql)
    resultado = cursor.fetchall()
    print(f"\n--- {nombre} ---")
    print(json.dumps(resultado, indent=4, ensure_ascii=False, default=str))

cursor.close()
cnx.close()
