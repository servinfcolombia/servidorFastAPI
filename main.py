from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
import os
from fastapi.middleware.cors import CORSMiddleware

# Configuración de la base de datos
db_config = {
     'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 4000)),
    'database': os.getenv('DB_NAME')
}

# Modelo de datos para el login
class LoginRequest(BaseModel):
    email: str
    password: str

# Inicializar FastAPI
app = FastAPI()


# Función para obtener la conexión a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Ruta para el login
@app.post("/login")
def login(login_request: LoginRequest):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM loguin WHERE email = %s AND password = %s"
    cursor.execute(query, (login_request.email, login_request.password))
    user = cursor.fetchone()

    cursor.close()
    connection.close()

    if user:
        return {"message": "Login successful", "user": user}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI TiDB Gateway"}

@app.get("/test")
def read_test():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        
        # Ejecutar una consulta de prueba
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        return {
            "status": "success",
            "message": "Conexión exitosa a la base de datos",
            "database_result": result,
            "details": f"Conectado a {db_config['host']} (DB: {db_config['database']})"
        }

    except mysql.connector.Error as err:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Error al conectarse a la base de datos",
                "error_details": str(err)
            }
        )

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            
# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)