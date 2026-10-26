import conectar

db = conectar.conexion()

def ejectuar_script_dono8do_redis():

    # ----------------------- 1 ---------------------
    print("#####1. Crear registros clave-valor#####")
    db.set("donante:1228", 'Celia Verdugo')
    db.set("donante:001", 'Pablo Rodriguez')
    db.set("donante:28", 'Jesus Zamorano')
    db.set("donante:002", 'Juan de Mesa')
    db.set("stock:A_positivo", "150")
    db.set("stock:0_negativo", "40")
    db.set("stock:B_positivo", "80")

    # ----------------------- 2 ----------------------
    print("#####2. Obtener y mostrar numeros de claves registradas#####")
    num_claves = len(db.keys())
    print(f"El total de claves registradas en BD es: {num_claves}\n")

    # ----------------------- 3 ----------------------
    print("#####3. Obtener un registro por clave (donante)#####")
    val_1228 = db.get("donante:1228")
    print(f"Valor de donante:1228: {val_1228}\n")

    # ------------------------ 4 ----------------------
    print("#####4. Actualizar el valor de una clave#####")
    db.set("stock:0_negativo", "10")
    print(f"Se ha actualizado el valor de 'stock:0_negativo': {db.get('stock:0_negativo')}")

    # ------------------------ 5 ------------------------
    print("#####5. Eliminar clave-valor#####")
    val_eliminar = db.get("donante:002")
    db.delete(val_eliminar)
    print(f"Clave eliminada: 'donante:002 | Valor eliminado: {val_eliminar}\n")

    # ----------------------- 6 -------------------------
    print("#####6. Obtener y mostrar todas las claves#####")
    todas_claves = db.keys()
    print(f"Claves: {todas_claves}\n")

    # ----------------------- 7 -------------------------
    print("#####7. Obtener y mostrar todos los valores guardados")
    for clave in db.keys():
        print(f"Clave: {clave} => Valor: {db.get(clave)}\n")

    # --------------------- 8 --------------------------
    print("#####8. Buscar patron usando * (donante)")
    for clave in db.scan_iter('donante*'):
        print(f"Encontrados con '*': {clave} -> {db.get(clave)}\n")

    # --------------------- 9 --------------------------
    print("#####9. Buscar patron '[]'#####")
    for clave in db.scan_iter('donante:00[12]'):
        print(f"Encontrados con el patrón '00[12]': {clave} -> {db.get(clave)}\n")

    # ------------------- 10 ---------------------------
    print("#####10. Buscar patrón '?'#####")
    for clave in db.scan_iter('stock:?_positivo'):
        print(f"Encontrados con '?_positivo': {clave} -> {db.get(clave)}\n")

    # -------------------- 11 ---------------------------
    print("#####11. Filtrar registros por valor concreto#####")
    for clave in db.scan_iter('stock:*'):
        if db.get(clave) == "150":
            print(f"Clave={clave}, Valor={db.get(clave)}\n")

    # -------------------- 12 -------------------------
    print("#####12. Actualizas registros filtrados#####")
    for clave in db.scan_iter('stock:*'):
        val = int(db.get(clave))
        if val < 100:
            nuevo_val = val + 10
            db.set(clave, nuevo_val)
            print(f"Clave {clave} actualizada de {val} a {nuevo_val}\n")

    # ------------------- 13 ---------------------------
    print("#####13. Eliminar registros filtrados#####")
    for clave in db.scan_iter('donante:00*'):
        val_borrado = db.get(clave)
        db.delete(clave)
        print(f"Eliminado por filtro: Clave={clave}, Valor={val_borrado}\n")

    # ------------------- 14 --------------------------
    print("#####14. crear estructura array en JSON#####")
    db.json().delete('donantes_array') # NO SIRVE DE NADA PQ NO LO ELIMINA PETA ANTES
    db.json().set("donantes_array", "$", [])
    db.json().arrappend("donantes_array", "$", {"nombre": "Laura", "grupo": "A+", "edad": 28, "donaciones": 5})
    db.json().arrappend("donantes_array", "$", {"nombre": "Manuel", "grupo": "O-", "edad": 45, "donaciones": 12})
    db.json().arrappend("donantes_array", "$", {"nombre": "Rocio", "grupo": "A+", "edad": 34, "donaciones": 3})
    print("Array de donantes en JSON creado con exito.\n")

    # ----------------------- 15 -------------------------
    print("#####15. Filtrar array JSON por atributo#####")
    res_nombre = db.json().get("donantes_array", "$[?(@.nombre=='Laura')]")
    res_grupo = db.json().get("donantes_array", "$[?(@.grupo=='A+')]")
    res_edad = db.json().get("donantes_array", "$[?(@.edad>30)]")
    res_donaciones = db.json().get("donantes_array", "$[?(@.donaciones>=5)]")
    print(f"Filtro Nombre ('Laura'): {res_nombre}")
    print(f"Filtro Grupo ('A+'): {res_grupo}")
    print(f"Filtro Edad (>30): {res_edad}")
    print(f"Filtro Donaciones (>=5): {res_donaciones}\n")
    # PETA SI YA SE HA EJECUTADO Y TIENES EL JSON DEL PUNTO 14 Y VUELVES A EJECUTAR, SE DEBE DE BORRAR ANTES DE VOLVER A EJECUTAR

    # ----------------------- 16 -------------------------------
    print("#####16. Crear lista en redis#####")
    db.delete("eventos_donacion") # NO SIRVE DE NADA PQ NO LO ELIMINA PETA ANTES
    db.lpush("eventos_donacion", "Sevilla_Centro:100")
    db.lpush("eventos_donacion", "Triana_Movil:50")
    db.lpush("eventos_donacion", "Nervion_Campana:80")
    print(f"Lista creada {db.lrange('eventos_donacion', 0, -1)}\n")


ejectuar_script_dono8do_redis()