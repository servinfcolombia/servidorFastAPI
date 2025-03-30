import mysql.connector
import os

# Configuración de la base de datos
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 4000)),
    'database': os.getenv('DB_NAME')
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