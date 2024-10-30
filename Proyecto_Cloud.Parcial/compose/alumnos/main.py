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
schema_name = "api_alumnos"

class Item(BaseModel):
    name: str
    lastname: str
    degree: int

# Get all students
@app.get("/students")
def get_students():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {schema_name}.alumnos")  # Utilizar el esquema específico
    result = cursor.fetchall()
    mydb.close()
    return {"students": result}

# Get a student by ID
@app.get("/students/{id}")
def get_student(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {schema_name}.alumnos WHERE id = {id}")  # Utilizar el esquema específico
    result = cursor.fetchone()
    mydb.close()
    return {"student": result}

# Add a new student
@app.post("/students")
def add_student(item: Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    name = item.name
    lastname = item.lastname
    degree = item.degree
    cursor = mydb.cursor()
    sql = f"INSERT INTO {schema_name}.alumnos (name, lastname, degree) VALUES (%s, %s, %s)"  # Utilizar el esquema específico
    val = (name, lastname, degree)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Student added successfully"}

# Modify a student
@app.put("/students/{id}")
def update_student(id: int, item: Item):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    name = item.name
    lastname = item.lastname
    degree = item.degree
    cursor = mydb.cursor()
    sql = f"UPDATE {schema_name}.alumnos SET name = %s, lastname = %s, degree = %s WHERE id = %s"  # Utilizar el esquema específico
    val = (name, lastname, degree, id)
    cursor.execute(sql, val)
    mydb.commit()
    mydb.close()
    return {"message": "Student modified successfully"}

# Delete a student by ID
@app.delete("/students/{id}")
def delete_student(id: int):
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"DELETE FROM {schema_name}.alumnos WHERE id = {id}")  # Utilizar el esquema específico
    mydb.commit()
    mydb.close()
    return {"message": "Student deleted successfully"}
