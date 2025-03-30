from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware


# Configuración de la base de datos
db_config = {
    'user': '2462m9QwrhhNgcv.root',
    'password': 'l2nwHbaiuEDMk3in',
    'host': 'gateway01.us-east-1.prod.aws.tidbcloud.com',
    'port': 4000,
    'database': 'test'
}

# Modelo de datos para el login
class LoginRequest(BaseModel):
    email: str
    password: str

# Modelo de datos para el Registro
class RegisterRequest(BaseModel):
    login_data: dict
    user_data: dict

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

@app.post("/register")
def register(register_request: RegisterRequest):
    try:
        # Insertar en tabla loguin
        login_query = "INSERT INTO loguin (email, password) VALUES (%s, %s)"
        login_values = (
            register_request.login_data['email'],
            register_request.login_data['password']
        )
        
        # Insertar en tabla usuarios
        user_query = """INSERT INTO usuarios 
                        (nombres, apellidos, tipo_documento, email, telefono, sexo, fecha_nacimiento) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        user_values = (
            register_request.user_data['nombres'],
            register_request.user_data['apellidos'],
            register_request.user_data['tipo_documento'],
            register_request.user_data['email'],
            register_request.user_data['telefono'],
            register_request.user_data['sexo'],
            register_request.user_data['fecha_nacimiento']
        )
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Ejecutar ambas inserciones en una transacción
        cursor.execute(login_query, login_values)
        cursor.execute(user_query, user_values)
        
        connection.commit()
        cursor.close()
        connection.close()
        
        return {"message": "Usuario registrado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI TiDB Gateway"}

# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)