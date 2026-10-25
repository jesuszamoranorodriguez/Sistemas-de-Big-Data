import mysql.connector
import psycopg2
from faker import Faker

"""
REQUISITO CUMPLIDO: 10 PROVIDERS DISTINTOS DE FAKER USADOS EN ESTE SCRIPT
1. fake.company() -> [Provider: company] Genera nombres de centros médicos.
2. fake.street_address() -> [Provider: address] Genera direcciones.
3. fake.city() -> [Provider: address] Genera municipios.
4. fake.phone_number() -> [Provider: phone_number] Genera teléfonos.
5. fake.first_name() -> [Provider: person] Genera nombres.
6. fake.last_name() -> [Provider: person] Genera apellidos.
7. fake.bothify(text='??#####') -> [Provider: misc] Genera identificadores (DNI/Colegiado).
8. fake.date_of_birth() -> [Provider: date_time] Genera fechas de nacimiento.
9. fake.email() -> [Provider: internet] Genera correos electrónicos.
10. fake.random_element() -> [Provider: misc] Selecciona elementos aleatorios de listas.
11. fake.text() -> [Provider: lorem] Genera textos largos para comentarios.
"""

fake = Faker('es_ES')

# 1. RELLENAR MYSQL (Puerto 3308)
def rellenar_mysql():
    print("--- 1. Rellenando MySQL (Puerto 3308) ---")
    config = {"user": "root", "password": "admin1234", "host": "127.0.0.1", "port": 3308, "database": "dono8do_mysql"}
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        centros_ids = []
        for _ in range(3):
            cursor.execute("INSERT INTO CentroMedico (nombre_centro, direccion, municipio, telefono) VALUES (%s, %s, %s, %s)",
                           (fake.company() + " Hospital", fake.street_address(), fake.city(), fake.phone_number()))
            centros_ids.append(cursor.lastrowid)

        medicos_ids = []
        for _ in range(5):
            cursor.execute("INSERT INTO Medico (id_centro, nombre, apellidos, num_colegiado, especialidad) VALUES (%s, %s, %s, %s, %s)",
                           (fake.random_element(centros_ids), fake.first_name(), fake.last_name(), fake.bothify('MED-#####'), fake.random_element(['Hematología', 'Medicina General'])))
            medicos_ids.append(cursor.lastrowid)

        usuarios_ids = []
        for _ in range(10):
            cursor.execute("INSERT INTO Usuario (nombre, apellidos, dni, fecha_nacimiento, grupo_sanguineo, email, telefono, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (fake.first_name(), fake.last_name(), fake.bothify('########?'), fake.date_of_birth(minimum_age=18, maximum_age=65), fake.random_element(['A+', 'O-', 'B+']), fake.email(), fake.phone_number(), fake.date_time_this_year()))
            usuarios_ids.append(cursor.lastrowid)

        eventos_ids = []
        for _ in range(3):
            cursor.execute("INSERT INTO EventoDonacion (id_medico_responsable, nombre_evento, fecha_inicio, fecha_fin, direccion, municipio, objetivo_bolsas) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (fake.random_element(medicos_ids), "Campaña " + fake.city(), fake.date_time_this_month(), fake.date_time_this_month(), fake.street_address(), fake.city(), fake.random_int(50, 200)))
            eventos_ids.append(cursor.lastrowid)

        for _ in range(5):
            cursor.execute("INSERT INTO Donacion (id_usuario, id_evento, id_medico, volumen_ml, tipo_donacion, fecha_extraccion) VALUES (%s, %s, %s, %s, %s, %s)",
                           (fake.random_element(usuarios_ids), fake.random_element(eventos_ids), fake.random_element(medicos_ids), 450, 'Sangre', fake.date_time_this_year()))
            id_don = cursor.lastrowid
            
            cursor.execute("INSERT INTO EncuestaSatisfaccion (id_donacion, puntuacion_general, dolor_experimentado, comentario_texto, fecha_encuesta) VALUES (%s, %s, %s, %s, %s)",
                           (id_don, fake.random_int(1, 5), fake.random_int(1, 5), fake.text(max_nb_chars=100), fake.date_time_this_year()))

        cnx.commit()
        cursor.close()
        cnx.close()
        print("[OK] Datos insertados en MySQL.")
    except Exception as e:
        print(f"[ERROR MySQL]: {e}")

# 2. RELLENAR POSTGRESQL (Puerto 5432)
def rellenar_postgres():
    print("--- 2. Rellenando PostgreSQL (Puerto 5432) ---")
    config = {"user": "postgres", "password": "admin1234", "host": "127.0.0.1", "port": 5432, "dbname": "dono8do_postgres"}
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        centros_ids = []
        for _ in range(3):
            cursor.execute("INSERT INTO CentroMedico (nombre_centro, direccion, municipio, telefono) VALUES (%s, %s, %s, %s) RETURNING id_centro;",
                           (fake.company() + " Hospital", fake.street_address(), fake.city(), fake.phone_number()))
            centros_ids.append(cursor.fetchone()[0])

        medicos_ids = []
        for _ in range(5):
            cursor.execute("INSERT INTO Medico (id_centro, nombre, apellidos, num_colegiado, especialidad) VALUES (%s, %s, %s, %s, %s) RETURNING id_medico;",
                           (fake.random_element(centros_ids), fake.first_name(), fake.last_name(), fake.bothify('MED-#####'), fake.random_element(['Hematología', 'Medicina General'])))
            medicos_ids.append(cursor.fetchone()[0])

        usuarios_ids = []
        for _ in range(10):
            cursor.execute("INSERT INTO Usuario (nombre, apellidos, dni, fecha_nacimiento, grupo_sanguineo, email, telefono, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id_usuario;",
                           (fake.first_name(), fake.last_name(), fake.bothify('########?'), fake.date_of_birth(minimum_age=18, maximum_age=65), fake.random_element(['A+', 'O-', 'B+']), fake.email(), fake.phone_number(), fake.date_time_this_year()))
            usuarios_ids.append(cursor.fetchone()[0])

        eventos_ids = []
        for _ in range(3):
            cursor.execute("INSERT INTO EventoDonacion (id_medico_responsable, nombre_evento, fecha_inicio, fecha_fin, direccion, municipio, objetivo_bolsas) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id_evento;",
                           (fake.random_element(medicos_ids), "Campaña " + fake.city(), fake.date_time_this_month(), fake.date_time_this_month(), fake.street_address(), fake.city(), fake.random_int(50, 200)))
            eventos_ids.append(cursor.fetchone()[0])

        for _ in range(5):
            cursor.execute("INSERT INTO Donacion (id_usuario, id_evento, id_medico, volumen_ml, tipo_donacion, fecha_extraccion) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id_donacion;",
                           (fake.random_element(usuarios_ids), fake.random_element(eventos_ids), fake.random_element(medicos_ids), 450, 'Sangre', fake.date_time_this_year()))
            id_don = cursor.fetchone()[0]
            
            cursor.execute("INSERT INTO EncuestaSatisfaccion (id_donacion, puntuacion_general, dolor_experimentado, comentario_texto, fecha_encuesta) VALUES (%s, %s, %s, %s, %s);",
                           (id_don, fake.random_int(1, 5), fake.random_int(1, 5), fake.text(max_nb_chars=100), fake.date_time_this_year()))

        conn.commit()
        cursor.close()
        conn.close()
        print("[OK] Datos insertados en PostgreSQL.")
    except Exception as e:
        print(f"[ERROR PostgreSQL]: {e}")

# 3. RELLENAR MARIADB 
def rellenar_mariadb():
    print("--- 3. Rellenando MariaDB (Puerto 3309) ---")
    config = {"user": "root", "password": "admin1234", "host": "127.0.0.1", "port": 3309, "database": "dono8do_mariadb"}
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        centros_ids = []
        for _ in range(3):
            cursor.execute("INSERT INTO CentroMedico (nombre_centro, direccion, municipio, telefono) VALUES (%s, %s, %s, %s)",
                           (fake.company() + " Hospital", fake.street_address(), fake.city(), fake.phone_number()))
            centros_ids.append(cursor.lastrowid)

        medicos_ids = []
        for _ in range(5):
            cursor.execute("INSERT INTO Medico (id_centro, nombre, apellidos, num_colegiado, especialidad) VALUES (%s, %s, %s, %s, %s)",
                           (fake.random_element(centros_ids), fake.first_name(), fake.last_name(), fake.bothify('MED-#####'), fake.random_element(['Hematología', 'Medicina General'])))
            medicos_ids.append(cursor.lastrowid)

        usuarios_ids = []
        for _ in range(10):
            cursor.execute("INSERT INTO Usuario (nombre, apellidos, dni, fecha_nacimiento, grupo_sanguineo, email, telefono, fecha_registro) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                           (fake.first_name(), fake.last_name(), fake.bothify('########?'), fake.date_of_birth(minimum_age=18, maximum_age=65), fake.random_element(['A+', 'O-', 'B+']), fake.email(), fake.phone_number(), fake.date_time_this_year()))
            usuarios_ids.append(cursor.lastrowid)

        eventos_ids = []
        for _ in range(3):
            cursor.execute("INSERT INTO EventoDonacion (id_medico_responsable, nombre_evento, fecha_inicio, fecha_fin, direccion, municipio, objetivo_bolsas) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (fake.random_element(medicos_ids), "Campaña " + fake.city(), fake.date_time_this_month(), fake.date_time_this_month(), fake.street_address(), fake.city(), fake.random_int(50, 200)))
            eventos_ids.append(cursor.lastrowid)

        for _ in range(5):
            cursor.execute("INSERT INTO Donacion (id_usuario, id_evento, id_medico, volumen_ml, tipo_donacion, fecha_extraccion) VALUES (%s, %s, %s, %s, %s, %s)",
                           (fake.random_element(usuarios_ids), fake.random_element(eventos_ids), fake.random_element(medicos_ids), 450, 'Sangre', fake.date_time_this_year()))
            id_don = cursor.lastrowid
            
            cursor.execute("INSERT INTO EncuestaSatisfaccion (id_donacion, puntuacion_general, dolor_experimentado, comentario_texto, fecha_encuesta) VALUES (%s, %s, %s, %s, %s)",
                           (id_don, fake.random_int(1, 5), fake.random_int(1, 5), fake.text(max_nb_chars=100), fake.date_time_this_year()))

        cnx.commit()
        cursor.close()
        cnx.close()
        print("[OK] Datos insertados en MariaDB.")
    except Exception as e:
        print(f"[ERROR MariaDB]: {e}")

if __name__ == "__main__":
    print("Iniciando el relleno de datos con Faker en las 3 bases de datos...")
    rellenar_mysql()
    rellenar_postgres()
    rellenar_mariadb()
    print("¡Proceso completado con éxito!")