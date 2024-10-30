from fastapi import FastAPI
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configurar CORS
origins = [
    "http://lb-prodpro-1434514222.us-east-1.elb.amazonaws.com:8084",
    "http://54.204.127.110:8084",
    "http://18.209.231.242:8084"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)


host_name = "100.28.85.79"
port_number = "8005"
user_name = "root"
password_db = "utec"
database_name = "bd_api_shared"
schema_name = "api_profesores"

class Item(BaseModel):
    name: str
    lastname: str
    email: str

# Get all professors
@app.get("/professors")
def get_professors():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {schema_name}.profesores")  # Utilizar el esquema específico
    result = cursor.fetchall()
    mydb.close()
    return {"professors": result}

# Get a professor by ID
@app.get("/professors/{id}")
def get_professor(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {schema_name}.profesores WHERE id = {id}")  # Utilizar el esquema específico
    result = cursor.fetchone()
    mydb.close()
    return {"professor": result}

# Add a new professor
@app.post("/professors")
def add_professor(item: Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = f"INSERT INTO {schema_name}.profesores (name, lastname, email) VALUES (%s, %s, %s)"  # Utilizar el esquema específico
    val = (item.name, item.lastname, item.email)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Professor added successfully"}

# Modify a professor
@app.put("/professors/{id}")
def update_professor(id: int, item: Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    sql = f"UPDATE {schema_name}.profesores SET name = %s, lastname = %s, email = %s WHERE id = %s"  # Utilizar el esquema específico
    val = (item.name, item.lastname, item.email, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Professor modified successfully"}

# Delete a professor by ID
@app.delete("/professors/{id}")
def delete_professor(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM {schema_name}.profesores WHERE id = {id}")  # Utilizar el esquema específico
    mydb.commit()
    mydb.close()
    return {"message": "Professor deleted successfully"}
