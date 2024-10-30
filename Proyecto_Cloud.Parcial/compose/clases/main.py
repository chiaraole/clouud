from fastapi import FastAPI, HTTPException
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
from mysql.connector import Error
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
schema_name = "api_clases"

class Item(BaseModel):
    name: str
    id_alumno: int
    id_profesor: int
    degree: int

# Get all classes
@app.get("/classes")
def get_classes():
    mydb = mysql.connector.connect(host=host_name, port=port_number, user=user_name, password=password_db, database=database_name)
    cursor = mydb.cursor()
    cursor.execute(f"SELECT * FROM {schema_name}.clases")  # Utilizar el esquema específico
    result = cursor.fetchall()
    mydb.close()
    return {"classes": result}

# Get a class by ID
@app.get("/classes/{id}")
def get_class(id: int):
    try:
        mydb = mysql.connector.connect(
            host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
        )
        cursor = mydb.cursor()
        cursor.execute(f"SELECT * FROM {schema_name}.clases WHERE id = %s", (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Class not found")
    finally:
        mydb.close()
    return {"class": result}

# Add a new class
@app.post("/classes")
def add_class(item: Item):
    try:
        mydb = mysql.connector.connect(
            host=host_name,
            port=port_number,
            user=user_name,
            password=password_db,
            database=database_name
        )
        cursor = mydb.cursor()

        # Verificar si el alumno existe
        cursor.execute(f"SELECT COUNT(*) FROM api_alumnos.alumnos WHERE id = %s", (item.id_alumno,))
        alumno_count = cursor.fetchone()[0]
        if alumno_count == 0:
            raise HTTPException(status_code=400, detail="Alumno no encontrado")

        # Verificar si el profesor existe
        cursor.execute(f"SELECT COUNT(*) FROM api_profesores.profesores WHERE id = %s", (item.id_profesor,))
        profesor_count = cursor.fetchone()[0]
        if profesor_count == 0:
            raise HTTPException(status_code=400, detail="Profesor no encontrado")

        # Insertar la nueva clase
        sql = f"INSERT INTO {schema_name}.clases (name, id_alumno, id_profesor, degree) VALUES (%s, %s, %s, %s)"
        val = (item.name, item.id_alumno, item.id_profesor, item.degree)
        cursor.execute(sql, val)
        mydb.commit()
        mydb.close()
        return {"message": "Class added successfully"}
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Modify a class
@app.put("/classes/{id}")
def update_class(id: int, item: Item):
    try:
        mydb = mysql.connector.connect(
            host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
        )
        cursor = mydb.cursor()

        # Verificar si la clase existe
        cursor.execute(f"SELECT COUNT(*) FROM {schema_name}.clases WHERE id = %s", (id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Class not found")

        sql = f"UPDATE {schema_name}.clases SET name = %s, id_alumno = %s, id_profesor = %s, degree = %s WHERE id = %s"
        val = (item.name, item.id_alumno, item.id_profesor, item.degree, id)
        cursor.execute(sql, val)
        mydb.commit()
    except mysql.connector.Error as e:
        mydb.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mydb.close()
    return {"message": "Class modified successfully"}

# Delete a class by ID
def delete_class(id: int):
    try:
        mydb = mysql.connector.connect(
            host=host_name, port=port_number, user=user_name, password=password_db, database=database_name
        )
        cursor = mydb.cursor()

        # Verificar si la clase existe
        cursor.execute(f"SELECT COUNT(*) FROM {schema_name}.clases WHERE id = %s", (id,))
        if cursor.fetchone()[0] == 0:
            raise HTTPException(status_code=404, detail="Class not found")

        cursor.execute(f"DELETE FROM {schema_name}.clases WHERE id = %s", (id,))
        mydb.commit()
    except mysql.connector.Error as e:
        mydb.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        mydb.close()
    return {"message": "Class deleted successfully"}
