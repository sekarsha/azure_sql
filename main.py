from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
import urllib
load_dotenv()

app=FastAPI()


import urllib.parse



@app.get("/", response_class=HTMLResponse)
async def welcome():
    """
    Welcome page that serves as the entry point for the application.
    """
    return """
    <html>
        <head>
            <title>Welcome Page</title>
        </head>
        <body>
            <h1>Welcome to the API!</h1>
            <p>This is the welcome page.</p>
        </body>
    </html>
    """
    

conn = psycopg2.connect(
    dbname='postgres',
    user='postgresql',
    password='Sql12345',
    host='mypostgres123.postgres.database.azure.com',
    port='5432'
)

DATABASE_URL = os.getenv('DATABASE_URL')

@app.get("/customers/{customer_id}")
def get_customer(customer_id: int):
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM customer WHERE id = %s;", (customer_id,))
            customer = cur.fetchone()
            if not customer:
                raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require") 

@app.get("/customerss/{customer_id}")
def get_customer(customer_id: int):
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT * FROM customer WHERE id = %s;", (customer_id,))
                customer = cur.fetchone()
                if not customer:
                    raise HTTPException(status_code=404, detail="Customer not found")
        return customer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



