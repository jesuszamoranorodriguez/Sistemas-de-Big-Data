import os
import json

import boto3
from boto3.dynamodb.conditions import Key, Attr
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

session = boto3.session.Session(
    aws_access_key_id=os.getenv("ACCESS_KEY"),
    aws_secret_access_key=os.getenv("SECRET_KEY"),
    aws_session_token=os.getenv("SESSION_TOKEN"),
    region_name=os.getenv("REGION"))

dynamodb = session.client('dynamodb')
dynamodb_res = session.resource('dynamodb')

tabla_usuarios = dynamodb_res.Table('Dono8do_Usuarios')
tabla_donaciones = dynamodb_res.Table('Dono8do_Donaciones')
tabla_eventos = dynamodb_res.Table('Dono8do_EventosDonacion')


def mostrar(datos):
    print(json.dumps(datos, indent=2, ensure_ascii=False, default=str))


def mostrar_tabla(tabla):
    elementos = tabla.scan()['Items']
    print(f"Registros en {tabla.name}: {len(elementos)}")
    for elemento in elementos:
        print(json.dumps(elemento, ensure_ascii=False, default=str))


# 1. Crear las tablas con sus índices
def crear_tablas():
    # Si ya existen se borran para poder ejecutar el script varias veces
    for nombre in ['Dono8do_Usuarios', 'Dono8do_Donaciones', 'Dono8do_EventosDonacion']:
        try:
            dynamodb.delete_table(TableName=nombre)
            dynamodb.get_waiter('table_not_exists').wait(TableName=nombre)
        except dynamodb.exceptions.ResourceNotFoundException:
            pass

    # Tabla sin índices
    dynamodb.create_table(
        TableName='Dono8do_Usuarios',
        AttributeDefinitions=[
            {'AttributeName': 'email', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'email', 'KeyType': 'HASH'}  # Partition Key
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Tabla con índice local
    dynamodb.create_table(
        TableName='Dono8do_Donaciones',
        AttributeDefinitions=[
            {'AttributeName': 'email', 'AttributeType': 'S'},           # Partition Key
            {'AttributeName': 'fecha_donacion', 'AttributeType': 'S'},  # Sort Key
            {'AttributeName': 'volumen_ml', 'AttributeType': 'N'}       # Sort Key del LSI
        ],
        KeySchema=[
            {'AttributeName': 'email', 'KeyType': 'HASH'},
            {'AttributeName': 'fecha_donacion', 'KeyType': 'RANGE'}
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': 'VolumenIndex',
                'KeySchema': [
                    {'AttributeName': 'email', 'KeyType': 'HASH'},
                    {'AttributeName': 'volumen_ml', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'}
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Tabla con índice global
    dynamodb.create_table(
        TableName='Dono8do_EventosDonacion',
        AttributeDefinitions=[
            {'AttributeName': 'id_evento', 'AttributeType': 'S'},
            {'AttributeName': 'municipio', 'AttributeType': 'S'},
            {'AttributeName': 'fecha_inicio', 'AttributeType': 'S'}
        ],
        KeySchema=[
            {'AttributeName': 'id_evento', 'KeyType': 'HASH'}
        ],
        GlobalSecondaryIndexes=[
            {
                'IndexName': 'MunicipioIndex',
                'KeySchema': [
                    {'AttributeName': 'municipio', 'KeyType': 'HASH'},
                    {'AttributeName': 'fecha_inicio', 'KeyType': 'RANGE'}
                ],
                'Projection': {'ProjectionType': 'ALL'},
                'ProvisionedThroughput': {'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
            }
        ],
        ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
    )

    # Las tablas deberian estar creadas
    for nombre in ['Dono8do_Usuarios', 'Dono8do_Donaciones', 'Dono8do_EventosDonacion']:
        dynamodb.get_waiter('table_exists').wait(TableName=nombre)
        print("Tabla creada:", nombre)


# 2. Crear tres registros en cada tabla
def crear_registros():
    usuarios = [
        {'email': 'jose@mail.com', 'nombre': 'Jose', 'grupo_sanguineo': 'A+', 'municipio': 'Sevilla', 'num_donaciones': 4, 'apto': True},
        {'email': 'celia@mail.com', 'nombre': 'Celia', 'grupo_sanguineo': 'O-', 'municipio': 'Dos Hermanas', 'num_donaciones': 2, 'apto': True},
        {'email': 'lucia@mail.com', 'nombre': 'Lucia', 'grupo_sanguineo': 'AB-', 'municipio': 'Écija', 'num_donaciones': 0, 'apto': False},
    ]
    donaciones = [
        {'email': 'jose@mail.com', 'fecha_donacion': '2026-04-14', 'tipo': 'Sangre total', 'volumen_ml': 450, 'estado': 'completada'},
        {'email': 'jose@mail.com', 'fecha_donacion': '2026-06-03', 'tipo': 'Plasma', 'volumen_ml': 600, 'estado': 'completada'},
        {'email': 'celia@mail.com', 'fecha_donacion': '2026-10-20', 'tipo': 'Sangre total', 'volumen_ml': 120, 'estado': 'anulada'},
    ]
    eventos = [
        {'id_evento': 'EV-1', 'nombre': 'Campaña Universitaria', 'municipio': 'Sevilla', 'fecha_inicio': '2026-11-25', 'plazas': 80, 'inscritos': 35, 'estado': 'programado'},
        {'id_evento': 'EV-2', 'nombre': 'Maratón de Navidad', 'municipio': 'Sevilla', 'fecha_inicio': '2026-12-22', 'plazas': 150, 'inscritos': 20, 'estado': 'programado'},
        {'id_evento': 'EV-3', 'nombre': 'Unidad móvil Écija', 'municipio': 'Écija', 'fecha_inicio': '2026-08-15', 'plazas': 40, 'inscritos': 0, 'estado': 'cancelado'},
    ]

    print("ANTES:")
    mostrar_tabla(tabla_usuarios)
    for usuario in usuarios:
        tabla_usuarios.put_item(Item=usuario)
    print("DESPUÉS:")
    mostrar_tabla(tabla_usuarios)

    print("\nANTES:")
    mostrar_tabla(tabla_donaciones)
    for donacion in donaciones:
        tabla_donaciones.put_item(Item=donacion)
    print("DESPUÉS:")
    mostrar_tabla(tabla_donaciones)

    print("\nANTES:")
    mostrar_tabla(tabla_eventos)
    for evento in eventos:
        tabla_eventos.put_item(Item=evento)
    print("DESPUÉS:")
    mostrar_tabla(tabla_eventos)


# 3. Obtener un registro de cada tabla
def obtener_registro():
    respuesta = tabla_usuarios.get_item(Key={'email': 'jose@mail.com'})
    mostrar(respuesta['Item'])

    respuesta = tabla_donaciones.get_item(Key={'email': 'jose@mail.com', 'fecha_donacion': '2026-04-14'})
    mostrar(respuesta['Item'])

    respuesta = tabla_eventos.get_item(Key={'id_evento': 'EV-1'}, ProjectionExpression="id_evento, municipio, fecha_inicio")
    mostrar(respuesta['Item'])


# 4. Actualizar un registro de cada tabla
def actualizar_registro():
    print("Jose hace una donación más: num_donaciones de 4 a 5")
    print("ANTES:")
    mostrar(tabla_usuarios.get_item(Key={'email': 'jose@mail.com'})['Item'])
    tabla_usuarios.update_item(
        Key={'email': 'jose@mail.com'},
        UpdateExpression="SET num_donaciones = :n",
        ExpressionAttributeValues={':n': 5})
    print("DESPUÉS:")
    mostrar(tabla_usuarios.get_item(Key={'email': 'jose@mail.com'})['Item'])

    print("\nLa donación de Jose del 2026-04-14 se envía a un hospital")
    print("ANTES:")
    mostrar(tabla_donaciones.get_item(Key={'email': 'jose@mail.com', 'fecha_donacion': '2026-04-14'})['Item'])
    tabla_donaciones.update_item(
        Key={'email': 'jose@mail.com', 'fecha_donacion': '2026-04-14'},
        UpdateExpression="SET hospital = :h",
        ExpressionAttributeValues={':h': 'Hospital Virgen Macarena'})
    print("DESPUÉS:")
    mostrar(tabla_donaciones.get_item(Key={'email': 'jose@mail.com', 'fecha_donacion': '2026-04-14'})['Item'])

    print("\nSe apunta una persona más al evento EV-1: inscritos de 35 a 36")
    print("ANTES:")
    mostrar(tabla_eventos.get_item(Key={'id_evento': 'EV-1'})['Item'])
    tabla_eventos.update_item(
        Key={'id_evento': 'EV-1'},
        UpdateExpression="SET inscritos = :i",
        ExpressionAttributeValues={':i': 36})
    print("DESPUÉS:")
    mostrar(tabla_eventos.get_item(Key={'id_evento': 'EV-1'})['Item'])


# 5. Eliminar un registro de cada tabla
def eliminar_registro():
    print("Borramos a celia@mail.com")
    print("ANTES:")
    mostrar_tabla(tabla_usuarios)
    tabla_usuarios.delete_item(Key={'email': 'celia@mail.com'})
    print("DESPUÉS:")
    mostrar_tabla(tabla_usuarios)

    print("\nBorramos la donación de jose del 2026-06-03")
    print("ANTES:")
    mostrar_tabla(tabla_donaciones)
    tabla_donaciones.delete_item(Key={'email': 'jose@mail.com', 'fecha_donacion': '2026-06-03'})
    print("DESPUÉS:")
    mostrar_tabla(tabla_donaciones)

    print("\nBorramos el evento EV-2")
    print("ANTES:")
    mostrar_tabla(tabla_eventos)
    tabla_eventos.delete_item(Key={'id_evento': 'EV-2'})
    print("DESPUÉS:")
    mostrar_tabla(tabla_eventos)


# 6. Obtener todos los registros de cada tabla
def obtener_todos():
    mostrar(tabla_usuarios.scan()['Items'])
    mostrar(tabla_donaciones.scan()['Items'])
    mostrar(tabla_eventos.scan()['Items'])


# 7. Filtrar con scan 
def filtrar_scan():
    print("Usuarios del grupo A+:")
    respuesta = tabla_usuarios.scan(FilterExpression=Attr('grupo_sanguineo').eq('A+'))
    mostrar(respuesta['Items'])

    print("Donaciones de tipo Sangre total:")
    respuesta = tabla_donaciones.scan(FilterExpression=Attr('tipo').eq('Sangre total'))
    mostrar(respuesta['Items'])

    print("Eventos programados (usando el índice global):")
    respuesta = tabla_eventos.scan(IndexName='MunicipioIndex', FilterExpression=Attr('estado').eq('programado'))
    mostrar(respuesta['Items'])


# 8. Eliminación condicional 
def eliminacion_condicional():
    print("Borramos a lucia solo si no es apta para donar")
    print("ANTES:")
    mostrar_tabla(tabla_usuarios)
    tabla_usuarios.delete_item(
        Key={'email': 'lucia@mail.com'},
        ConditionExpression=Attr('apto').eq(False))
    print("DESPUÉS:")
    mostrar_tabla(tabla_usuarios)

    print("\nBorramos la donación de celia solo si está anulada")
    print("ANTES:")
    mostrar_tabla(tabla_donaciones)
    tabla_donaciones.delete_item(
        Key={'email': 'celia@mail.com', 'fecha_donacion': '2026-10-20'},
        ConditionExpression=Attr('estado').eq('anulada'))
    print("DESPUÉS:")
    mostrar_tabla(tabla_donaciones)

    print("\nBuscamos con el índice global los eventos de Écija y los borramos solo si están cancelados")
    print("ANTES:")
    mostrar_tabla(tabla_eventos)
    respuesta = tabla_eventos.query(IndexName='MunicipioIndex', KeyConditionExpression=Key('municipio').eq('Écija'))
    for evento in respuesta['Items']:
        tabla_eventos.delete_item(
            Key={'id_evento': evento['id_evento']},
            ConditionExpression=Attr('estado').eq('cancelado'))
    print("DESPUÉS:")
    mostrar_tabla(tabla_eventos)


# 9. Obtener datos con varios filtros
def varios_filtros():
    print("Usuarios de Sevilla, aptos y con más de 2 donaciones:")
    respuesta = tabla_usuarios.scan(
        FilterExpression=Attr('municipio').eq('Sevilla') & Attr('apto').eq(True) & Attr('num_donaciones').gt(2))
    mostrar(respuesta['Items'])

    print("Donaciones de jose de 400 ml o más y completadas (usando el índice local):")
    respuesta = tabla_donaciones.query(
        IndexName='VolumenIndex',
        KeyConditionExpression=Key('email').eq('jose@mail.com') & Key('volumen_ml').gte(400),
        FilterExpression=Attr('estado').eq('completada'))
    mostrar(respuesta['Items'])

    print("Eventos programados en Sevilla en noviembre y diciembre (usando el índice global):")
    respuesta = tabla_eventos.query(
        IndexName='MunicipioIndex',
        KeyConditionExpression=Key('municipio').eq('Sevilla') & Key('fecha_inicio').between('2026-11-01', '2026-12-31'),
        FilterExpression=Attr('estado').eq('programado'))
    mostrar(respuesta['Items'])


# 10. PartiQL en cada tabla
def partiql():
    consulta = 'SELECT * FROM "Dono8do_Usuarios" WHERE municipio = \'Sevilla\''
    print(consulta)
    respuesta = dynamodb.execute_statement(Statement=consulta)
    mostrar(respuesta['Items'])

    consulta = 'SELECT * FROM "Dono8do_Donaciones" WHERE email = \'jose@mail.com\''
    print(consulta)
    respuesta = dynamodb.execute_statement(Statement=consulta)
    mostrar(respuesta['Items'])

    consulta = 'SELECT * FROM "Dono8do_EventosDonacion" WHERE estado = \'programado\''
    print(consulta)
    respuesta = dynamodb.execute_statement(Statement=consulta)
    mostrar(respuesta['Items'])
