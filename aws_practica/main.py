import os
import sys
import subprocess

sys.path.append("dono8do-dynamoDB")
import dynamoDB
import informe_unificado


print("\n===== 1. CREAR TABLAS =====")
print("Se crean 3 tablas: Usuarios (sin índices), Donaciones (índice local) y Eventos (índice global)")
dynamoDB.crear_tablas()

print("\n===== 2. CREAR REGISTROS =====")
print("Se insertan 3 registros en cada tabla con put_item")
dynamoDB.crear_registros()

print("\n===== 3. OBTENER UN REGISTRO =====")
print("Se obtiene un registro de cada tabla con get_item usando su clave")
dynamoDB.obtener_registro()

print("\n===== 4. ACTUALIZAR UN REGISTRO =====")
print("Se modifica un registro de cada tabla con update_item")
dynamoDB.actualizar_registro()

print("\n===== 5. ELIMINAR UN REGISTRO =====")
print("Se borra un registro de cada tabla con delete_item")
dynamoDB.eliminar_registro()

print("\n===== 6. OBTENER TODOS LOS REGISTROS =====")
print("Se obtienen todos los registros de cada tabla con scan")
dynamoDB.obtener_todos()

print("\n===== 7. FILTRAR CON SCAN =====")
print("Se filtran los registros con scan y FilterExpression")
dynamoDB.filtrar_scan()

print("\n===== 8. ELIMINACIÓN CONDICIONAL =====")
print("Se borra un registro solo si cumple una condición")
dynamoDB.eliminacion_condicional()

print("\n===== 9. VARIOS FILTROS =====")
print("Se obtienen registros aplicando varios filtros a la vez")
dynamoDB.varios_filtros()

print("\n===== 10. PARTIQL =====")
print("Se hacen consultas con PartiQL (SQL en DynamoDB)")
dynamoDB.partiql()

print("\n===== RDS =====")
print("Se crea la base de datos y las tablas en RDS y se hacen 3 consultas en JSON")
sys.stdout.flush()
subprocess.run([sys.executable, "gestionarBD.py"], cwd="dono8do-rds")

print("\n===== INFORME UNIFICADO =====")
print("Se juntan datos de DynamoDB y RDS en un archivo JSON")
informe_unificado.generar_informe()
