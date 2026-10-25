import mysql.connector
import psycopg2

def crear_tablas_mysql():
    print("--- 1. Creando tablas en MySQL (dono8do_mysql) ---")
    config = {
        "user": "root", "password": "admin1234", "host": "127.0.0.1", "port": 3308, "database": "dono8do_mysql"
    }
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        tables = {
            'CentroMedico': "CREATE TABLE IF NOT EXISTS CentroMedico (id_centro INT AUTO_INCREMENT PRIMARY KEY, nombre_centro VARCHAR(150), direccion VARCHAR(200), municipio VARCHAR(100), telefono VARCHAR(20)) ENGINE=InnoDB;",
            'Medico': "CREATE TABLE IF NOT EXISTS Medico (id_medico INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, nombre VARCHAR(100), apellidos VARCHAR(150), num_colegiado VARCHAR(50), especialidad VARCHAR(100), FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE SET NULL) ENGINE=InnoDB;",
            'Usuario': "CREATE TABLE IF NOT EXISTS Usuario (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), apellidos VARCHAR(150), dni VARCHAR(20), fecha_nacimiento DATE, grupo_sanguineo VARCHAR(5), email VARCHAR(150), telefono VARCHAR(20), fecha_registro DATETIME) ENGINE=InnoDB;",
            'EventoDonacion': "CREATE TABLE IF NOT EXISTS EventoDonacion (id_evento INT AUTO_INCREMENT PRIMARY KEY, id_medico_responsable INT, nombre_evento VARCHAR(200), fecha_inicio DATETIME, fecha_fin DATETIME, direccion VARCHAR(200), municipio VARCHAR(100), objetivo_bolsas INT, FOREIGN KEY (id_medico_responsable) REFERENCES Medico(id_medico) ON DELETE SET NULL) ENGINE=InnoDB;",
            'Cita': "CREATE TABLE IF NOT EXISTS Cita (id_cita INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, id_evento INT, fecha_hora DATETIME, estado VARCHAR(50), FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE, FOREIGN KEY (id_evento) REFERENCES EventoDonacion(id_evento) ON DELETE CASCADE) ENGINE=InnoDB;",
            'CuestionarioSalud': "CREATE TABLE IF NOT EXISTS CuestionarioSalud (id_cuestionario INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, peso_actual DECIMAL(5,2), viaje_reciente_riesgo BOOLEAN, tatuaje_reciente BOOLEAN, enfermedad_infecciosa BOOLEAN, fecha_cuestionario DATETIME, FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE) ENGINE=InnoDB;",
            'ValidacionMedica': "CREATE TABLE IF NOT EXISTS ValidacionMedica (id_validacion INT AUTO_INCREMENT PRIMARY KEY, id_cuestionario INT, id_medico INT, apto_para_donar BOOLEAN, tension_arterial VARCHAR(20), motivo_rechazo VARCHAR(255), fecha_validacion DATETIME, FOREIGN KEY (id_cuestionario) REFERENCES CuestionarioSalud(id_cuestionario) ON DELETE CASCADE, FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE SET NULL) ENGINE=InnoDB;",
            'Donacion': "CREATE TABLE IF NOT EXISTS Donacion (id_donacion INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, id_evento INT, id_medico INT, volumen_ml INT, tipo_donacion VARCHAR(50), fecha_extraccion DATETIME, FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE, FOREIGN KEY (id_evento) REFERENCES EventoDonacion(id_evento) ON DELETE SET NULL, FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE SET NULL) ENGINE=InnoDB;",
            'StockSangre': "CREATE TABLE IF NOT EXISTS StockSangre (id_stock INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, grupo_sanguineo VARCHAR(5), cantidad_bolsas INT, fecha_actualizacion DATETIME, FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE CASCADE) ENGINE=InnoDB;",
            'EncuestaSatisfaccion': "CREATE TABLE IF NOT EXISTS EncuestaSatisfaccion (id_encuesta INT AUTO_INCREMENT PRIMARY KEY, id_donacion INT, puntuacion_general INT, dolor_experimentado INT, comentario_texto TEXT, fecha_encuesta DATETIME, FOREIGN KEY (id_donacion) REFERENCES Donacion(id_donacion) ON DELETE CASCADE) ENGINE=InnoDB;",
            'Reporte': "CREATE TABLE IF NOT EXISTS Reporte (id_reporte INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, tipo_analitica VARCHAR(100), titulo_reporte VARCHAR(200), ruta_archivo VARCHAR(255), fecha_generacion DATETIME, FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE CASCADE) ENGINE=InnoDB;"
        }
        for name, query in tables.items():
            cursor.execute(query)
        print("-> [OK] Tablas de MySQL creadas correctamente.\n")
        cursor.close()
        cnx.close()
    except Exception as e:
        print(f"-> [Error MySQL]: {e}\n")

def crear_tablas_postgres():
    print("--- 2. Creando tablas en PostgreSQL (dono8do_postgres) ---")
    config = {
        "user": "postgres", "password": "admin1234", "host": "127.0.0.1", "port": 5432, "dbname": "dono8do_postgres"
    }
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        tables = {
            'CentroMedico': "CREATE TABLE IF NOT EXISTS CentroMedico (id_centro SERIAL PRIMARY KEY, nombre_centro VARCHAR(150), direccion VARCHAR(200), municipio VARCHAR(100), telefono VARCHAR(20));",
            'Medico': "CREATE TABLE IF NOT EXISTS Medico (id_medico SERIAL PRIMARY KEY, id_centro INT, nombre VARCHAR(100), apellidos VARCHAR(150), num_colegiado VARCHAR(50), especialidad VARCHAR(100), FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE SET NULL);",
            'Usuario': "CREATE TABLE IF NOT EXISTS Usuario (id_usuario SERIAL PRIMARY KEY, nombre VARCHAR(100), apellidos VARCHAR(150), dni VARCHAR(20), fecha_nacimiento DATE, grupo_sanguineo VARCHAR(5), email VARCHAR(150), telefono VARCHAR(20), fecha_registro TIMESTAMP);",
            'EventoDonacion': "CREATE TABLE IF NOT EXISTS EventoDonacion (id_evento SERIAL PRIMARY KEY, id_medico_responsable INT, nombre_evento VARCHAR(200), fecha_inicio TIMESTAMP, fecha_fin TIMESTAMP, direccion VARCHAR(200), municipio VARCHAR(100), objetivo_bolsas INT, FOREIGN KEY (id_medico_responsable) REFERENCES Medico(id_medico) ON DELETE SET NULL);",
            'Cita': "CREATE TABLE IF NOT EXISTS Cita (id_cita SERIAL PRIMARY KEY, id_usuario INT, id_evento INT, fecha_hora TIMESTAMP, estado VARCHAR(50), FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE, FOREIGN KEY (id_evento) REFERENCES EventoDonacion(id_evento) ON DELETE CASCADE);",
            'CuestionarioSalud': "CREATE TABLE IF NOT EXISTS CuestionarioSalud (id_cuestionario SERIAL PRIMARY KEY, id_usuario INT, peso_actual DECIMAL(5,2), viaje_reciente_riesgo BOOLEAN, tatuaje_reciente BOOLEAN, enfermedad_infecciosa BOOLEAN, fecha_cuestionario TIMESTAMP, FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE);",
            'ValidacionMedica': "CREATE TABLE IF NOT EXISTS ValidacionMedica (id_validacion SERIAL PRIMARY KEY, id_cuestionario INT, id_medico INT, apto_para_donar BOOLEAN, tension_arterial VARCHAR(20), motivo_rechazo VARCHAR(255), fecha_validacion TIMESTAMP, FOREIGN KEY (id_cuestionario) REFERENCES CuestionarioSalud(id_cuestionario) ON DELETE CASCADE, FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE SET NULL);",
            'Donacion': "CREATE TABLE IF NOT EXISTS Donacion (id_donacion SERIAL PRIMARY KEY, id_usuario INT, id_evento INT, id_medico INT, volumen_ml INT, tipo_donacion VARCHAR(50), fecha_extraccion TIMESTAMP, FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE, FOREIGN KEY (id_evento) REFERENCES EventoDonacion(id_evento) ON DELETE SET NULL, FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE SET NULL);",
            'StockSangre': "CREATE TABLE IF NOT EXISTS StockSangre (id_stock SERIAL PRIMARY KEY, id_centro INT, grupo_sanguineo VARCHAR(5), cantidad_bolsas INT, fecha_actualizacion TIMESTAMP, FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE CASCADE);",
            'EncuestaSatisfaccion': "CREATE TABLE IF NOT EXISTS EncuestaSatisfaccion (id_encuesta SERIAL PRIMARY KEY, id_donacion INT, puntuacion_general INT, dolor_experimentado INT, comentario_texto TEXT, fecha_encuesta TIMESTAMP, FOREIGN KEY (id_donacion) REFERENCES Donacion(id_donacion) ON DELETE CASCADE);",
            'Reporte': "CREATE TABLE IF NOT EXISTS Reporte (id_reporte SERIAL PRIMARY KEY, id_centro INT, tipo_analitica VARCHAR(100), titulo_reporte VARCHAR(200), ruta_archivo VARCHAR(255), fecha_generacion TIMESTAMP, FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE CASCADE);"
        }
        for name, query in tables.items():
            cursor.execute(query)
        conn.commit()
        print("-> [OK] Tablas de PostgreSQL creadas correctamente.\n")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"-> [Error PostgreSQL]: {e}\n")

def crear_tablas_mariadb():
    print("--- 3. Creando tablas en MariaDB (dono8do_mariadb) ---")
    config = {
        "user": "root", "password": "admin1234", "host": "127.0.0.1", "port": 3309, "database": "dono8do_mariadb"
    }
    try:
        cnx = mysql.connector.connect(**config)
        cursor = cnx.cursor()
        
        tables = {
            'CentroMedico': "CREATE TABLE IF NOT EXISTS CentroMedico (id_centro INT AUTO_INCREMENT PRIMARY KEY, nombre_centro VARCHAR(150), direccion VARCHAR(200), municipio VARCHAR(100), telefono VARCHAR(20)) ENGINE=InnoDB;",
            'Medico': "CREATE TABLE IF NOT EXISTS Medico (id_medico INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, nombre VARCHAR(100), apellidos VARCHAR(150), num_colegiado VARCHAR(50), especialidad VARCHAR(100), FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE SET NULL) ENGINE=InnoDB;",
            'Usuario': "CREATE TABLE IF NOT EXISTS Usuario (id_usuario INT AUTO_INCREMENT PRIMARY KEY, nombre VARCHAR(100), apellidos VARCHAR(150), dni VARCHAR(20), fecha_nacimiento DATE, grupo_sanguineo VARCHAR(5), email VARCHAR(150), telefono VARCHAR(20), fecha_registro DATETIME) ENGINE=InnoDB;",
            'EventoDonacion': "CREATE TABLE IF NOT EXISTS EventoDonacion (id_evento INT AUTO_INCREMENT PRIMARY KEY, id_medico_responsable INT, nombre_evento VARCHAR(200), fecha_inicio DATETIME, fecha_fin DATETIME, direccion VARCHAR(200), municipio VARCHAR(100), objetivo_bolsas INT, FOREIGN KEY (id_medico_responsable) REFERENCES Medico(id_medico) ON DELETE SET NULL) ENGINE=InnoDB;",
            'Cita': "CREATE TABLE IF NOT EXISTS Cita (id_cita INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, id_evento INT, fecha_hora DATETIME, estado VARCHAR(50), FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE, FOREIGN KEY (id_evento) REFERENCES EventoDonacion(id_evento) ON DELETE CASCADE) ENGINE=InnoDB;",
            'CuestionarioSalud': "CREATE TABLE IF NOT EXISTS CuestionarioSalud (id_cuestionario INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, peso_actual DECIMAL(5,2), viaje_reciente_riesgo BOOLEAN, tatuaje_reciente BOOLEAN, enfermedad_infecciosa BOOLEAN, fecha_cuestionario DATETIME, FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE) ENGINE=InnoDB;",
            'ValidacionMedica': "CREATE TABLE IF NOT EXISTS ValidacionMedica (id_validacion INT AUTO_INCREMENT PRIMARY KEY, id_cuestionario INT, id_medico INT, apto_para_donar BOOLEAN, tension_arterial VARCHAR(20), motivo_rechazo VARCHAR(255), fecha_validacion DATETIME, FOREIGN KEY (id_cuestionario) REFERENCES CuestionarioSalud(id_cuestionario) ON DELETE CASCADE, FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE SET NULL) ENGINE=InnoDB;",
            'Donacion': "CREATE TABLE IF NOT EXISTS Donacion (id_donacion INT AUTO_INCREMENT PRIMARY KEY, id_usuario INT, id_evento INT, id_medico INT, volumen_ml INT, tipo_donacion VARCHAR(50), fecha_extraccion DATETIME, FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario) ON DELETE CASCADE, FOREIGN KEY (id_evento) REFERENCES EventoDonacion(id_evento) ON DELETE SET NULL, FOREIGN KEY (id_medico) REFERENCES Medico(id_medico) ON DELETE SET NULL) ENGINE=InnoDB;",
            'StockSangre': "CREATE TABLE IF NOT EXISTS StockSangre (id_stock INT AUTO_INCREMENT PRIMARY KEY, id_centro INT, grupo_sanguineo VARCHAR(5), cantidad_bolsas INT, fecha_actualizacion DATETIME, FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE CASCADE) ENGINE=InnoDB;",
            'EncuestaSatisfaccion': "CREATE TABLE IF NOT EXISTS EncuestaSatisfaccion (id_encuesta INT AUTO_INCREMENT PRIMARY KEY, id_donacion INT, puntuacion_general INT, dolor_experimentado INT, comentario_texto TEXT, fecha_encuesta DATETIME, FOREIGN KEY (id_donacion) REFERENCES Donacion(id_donacion) ON DELETE CASCADE) ENGINE=InnoDB;",
            'Reporte': "CREATE TABLE IF NOT EXISTS Reporte (id_reporte SERIAL PRIMARY KEY, id_centro INT, tipo_analitica VARCHAR(100), titulo_reporte VARCHAR(200), ruta_archivo VARCHAR(255), fecha_generacion DATETIME, FOREIGN KEY (id_centro) REFERENCES CentroMedico(id_centro) ON DELETE CASCADE) ENGINE=InnoDB;"
        }
        for name, query in tables.items():
            cursor.execute(query)
        print("-> [OK] Tablas de MariaDB creadas correctamente.\n")
        cursor.close()
        cnx.close()
    except Exception as e:
        print(f"-> [Error MariaDB]: {e}\n")

if __name__ == "__main__":
    print("=== INICIANDO CREACIÓN DE LAS 3 BASES DE DATOS (DONO8DO) ===\n")
    crear_tablas_mysql()
    crear_tablas_postgres()
    crear_tablas_mariadb()
    print("=== PROCESO FINALIZADO CON ÉXITO ===")