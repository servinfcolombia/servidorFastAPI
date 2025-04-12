import mysql.connector
import os

db_config = {
    'user': '2462m9QwrhhNgcv.root',
    'password': 'l2nwHbaiuEDMk3in',
    'host': 'gateway01.us-east-1.prod.aws.tidbcloud.com',
    'port': 4000,
    'database': 'test'
}

# Intentar conectarse a la base de datos
try:
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    # Ejecutar una consulta de prueba
    cursor.execute("SELECT 1")
    result = cursor.fetchone()

    print("Conexión exitosa a la base de datos. Resultado de la consulta:", result)

except mysql.connector.Error as err:
    print("Error al conectarse a la base de datos:", err)

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")