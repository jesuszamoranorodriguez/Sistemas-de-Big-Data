import sys
import json

import mysql.connector
from dotenv import dotenv_values
from boto3.dynamodb.conditions import Key, Attr

sys.path.append("dono8do-dynamoDB")
import dynamoDB


def generar_informe():
    # Datos de RDS
    env = dotenv_values("dono8do-rds/.env")
    cnx = mysql.connector.connect(user=env["DB_USER"], password=env["DB_PASSWORD"],
                                  host=env["ENDPOINT"], database=env["DB_NAME"])
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("SELECT nombre, apellidos, email, grupo_sanguineo FROM Usuario WHERE grupo_sanguineo = 'A+'")
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM StockSangre WHERE cantidad_bolsas < 10")
    stock_bajo = cursor.fetchall()

    cnx.close()

    for usuario in usuarios:
        respuesta = dynamoDB.tabla_donaciones.query(
            KeyConditionExpression=Key('email').eq(usuario['email']),
            FilterExpression=Attr('estado').eq('completada'))
        usuario['donaciones'] = respuesta['Items']

    respuesta = dynamoDB.tabla_eventos.scan(FilterExpression=Attr('estado').eq('programado'))
    eventos = respuesta['Items']

    informe = {
        'usuarios_A+_con_sus_donaciones': usuarios,
        'stock_bajo': stock_bajo,
        'eventos_programados': eventos
    }

    with open("informe_unificado.json", "w", encoding="utf-8") as f:
        json.dump(informe, f, indent=2, ensure_ascii=False, default=str)

    dynamoDB.mostrar(informe)
    print("Informe guardado en informe_unificado.json")


if __name__ == "__main__":
    generar_informe()
