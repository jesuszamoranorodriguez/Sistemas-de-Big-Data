import mysql.connector
import psycopg2
import json

def generar_reportes_json():
    # 1. CONSULTA EN MYSQL  -> donaciones_mysql.json
    # RAZÓN ANALÍTICA: Obtener el historial central de donaciones es vital para 
    # la trazabilidad. Une al donante, la campaña y el médico responsable para 
    # auditar quién donó, cuánto y bajo la supervisión de qué profesional.
    try:
        cnx_mysql = mysql.connector.connect(user="root", password="admin1234", host="127.0.0.1", port=3308, database="dono8do_mysql")
        cursor_mysql = cnx_mysql.cursor(dictionary=True)
        query_mysql = """
        SELECT d.id_donacion, CONCAT(u.nombre, ' ', u.apellidos) AS donante, u.grupo_sanguineo, 
               e.nombre_evento, CONCAT(m.nombre, ' ', m.apellidos) AS medico, d.volumen_ml, d.fecha_extraccion
        FROM Donacion d
        JOIN Usuario u ON d.id_usuario = u.id_usuario
        JOIN EventoDonacion e ON d.id_evento = e.id_evento
        JOIN Medico m ON d.id_medico = m.id_medico;
        """
        cursor_mysql.execute(query_mysql)
        res_mysql = cursor_mysql.fetchall()
        with open("donaciones_mysql.json", "w", encoding="utf-8") as f:
            json.dump(res_mysql, f, indent=4, ensure_ascii=False, default=str)
        print("-> [OK] MySQL: 'donaciones_mysql.json' generado.")
        cursor_mysql.close()
        cnx_mysql.close()
    except Exception as e:
        print(f"Error en MySQL: {e}")

    # 2. CONSULTA EN POSTGRESQL -> satisfaccion_postgres.json
    # RAZÓN ANALÍTICA: Analizar la calidad del servicio. Unir las encuestas de 
    # satisfacción con la donación y el usuario permite detectar si los donantes 
    # sufren dolor o tienen quejas, lo cual es clave para mejorar la retención.
    try:
        conn_pg = psycopg2.connect(user="postgres", password="admin1234", host="127.0.0.1", port=5432, dbname="dono8do_postgres")
        # RealDictCursor simula el dictionary=True de MySQL en Postgres
        from psycopg2.extras import RealDictCursor
        cursor_pg = conn_pg.cursor(cursor_factory=RealDictCursor)
        query_pg = """
        SELECT enc.id_encuesta, CONCAT(u.nombre, ' ', u.apellidos) AS donante, 
               enc.puntuacion_general, enc.dolor_experimentado, enc.comentario_texto, d.tipo_donacion
        FROM EncuestaSatisfaccion enc
        JOIN Donacion d ON enc.id_donacion = d.id_donacion
        JOIN Usuario u ON d.id_usuario = u.id_usuario;
        """
        cursor_pg.execute(query_pg)
        res_pg = cursor_pg.fetchall()
        with open("satisfaccion_postgres.json", "w", encoding="utf-8") as f:
            json.dump(res_pg, f, indent=4, ensure_ascii=False, default=str)
        print("-> [OK] PostgreSQL: 'satisfaccion_postgres.json' generado.")
        cursor_pg.close()
        conn_pg.close()
    except Exception as e:
        print(f"Error en PostgreSQL: {e}")

    # 3. CONSULTA EN MARIADB -> logistica_mariadb.json
    # RAZÓN ANALÍTICA: Control logístico y de recursos. Unir los eventos con 
    # los médicos y sus centros de origen permite a la directiva evaluar cómo 
    # se distribuye el personal de los hospitales en las campañas itinerantes.
    try:
        cnx_maria = mysql.connector.connect(user="root", password="admin1234", host="127.0.0.1", port=3309, database="dono8do_mariadb")
        cursor_maria = cnx_maria.cursor(dictionary=True)
        query_maria = """
        SELECT e.nombre_evento, e.municipio AS municipio_evento, e.objetivo_bolsas, 
               CONCAT(m.nombre, ' ', m.apellidos) AS medico_asignado, c.nombre_centro AS hospital_origen
        FROM EventoDonacion e
        JOIN Medico m ON e.id_medico_responsable = m.id_medico
        JOIN CentroMedico c ON m.id_centro = c.id_centro;
        """
        cursor_maria.execute(query_maria)
        res_maria = cursor_maria.fetchall()
        with open("logistica_mariadb.json", "w", encoding="utf-8") as f:
            json.dump(res_maria, f, indent=4, ensure_ascii=False, default=str)
        print("-> [OK] MariaDB: 'logistica_mariadb.json' generado.")
        cursor_maria.close()
        cnx_maria.close()
    except Exception as e:
        print(f"Error en MariaDB: {e}")

if __name__ == "__main__":
    print("Iniciando extracción de datos y generación de JSONs...")
    generar_reportes_json()
    print("¡Proceso completado con éxito!")