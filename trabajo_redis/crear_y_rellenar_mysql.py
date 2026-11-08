from faker import Faker

import conectar

# Crea en MySQL (dono8do_mysql) las tablas que usan los ejercicios 21 y 22 y las rellena con Faker

fake = Faker('es_ES')

cnx = conectar.conexion_mysql()
cursor = cnx.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS Usuario (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), apellidos VARCHAR(150), dni VARCHAR(20), fecha_nacimiento DATE, grupo_sanguineo VARCHAR(5), email VARCHAR(150), telefono VARCHAR(20), fecha_registro DATETIME) ENGINE=InnoDB;")
cursor.execute("CREATE TABLE IF NOT EXISTS StockSangre (id_stock INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, grupo_sanguineo VARCHAR(5), cantidad_bolsas INT, fecha_actualizacion DATETIME) ENGINE=InnoDB;")
print("Tablas Usuario y StockSangre creadas")

for _ in range(10):
    cursor.execute("INSERT INTO Usuario (nombre, apellidos, dni, fecha_nacimiento, grupo_sanguineo, email, telefono, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (fake.first_name(), fake.last_name(), fake.bothify('########?'), fake.date_of_birth(minimum_age=18, maximum_age=65), fake.random_element(['A+', 'O-', 'B+']), fake.email(), fake.phone_number(), fake.date_time_this_year()))
cnx.commit()
print("10 usuarios insertados en Usuario")

cursor.close()
cnx.close()
