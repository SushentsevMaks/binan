from fastapi import FastAPI
import mysql.connector

app = FastAPI()

mydb = mysql.connector.connect(
  host="localhost",
  user="banan_user",
  password="warlight123",
  database="banans"
)


@app.get("/")
def get_employees():
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM vision_orders")
    result = cursor.fetchall()
    return {"employees": result}

