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

# Inicializar FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes desde cualquier origen; para producción, especifica los orígenes permitidos.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Función para obtener la conexión a la base de datos
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

# Ruta para el login
@app.post("/login")
def login(login_request: LoginRequest):
    print(f"Received email: {login_request.email}")
    print(f"Received password: {login_request.password}")

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

# Ejecutar la aplicación
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)