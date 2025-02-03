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

DB_HOST = os.environ.get('DB_HOST', 'mypostgres123.postgres.database.azure.com')
DB_PORT = urllib.parse.quote_plus(str(os.environ.get('DB_PORT', '5432')))
DB_NAME = os.environ.get('DB_NAME', 'postgres')
DB_USER = urllib.parse.quote_plus(str(os.environ.get('DB_USER', 'postgresql')))
DB_PASSWORD = urllib.parse.quote_plus(str(os.environ.get('DB_PASSWORD', 'Sql12345')))
ssl_mode = urllib.parse.quote_plus(str(os.environ.get('ssl_mode','prefer')))
DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}?sslmode={}'.format(DB_NAME,DB_PASSWORD, DB_HOST, DB_PORT,DB_NAME, ssl_mode)


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
    


# Database connection
# conn = psycopg2.connect(
#     dbname=DB_NAME,
#     user=DB_USER,
#     password=DB_PASSWORD,
#     host=DB_HOST,
#     port=DB_PORT
# )


# @app.get("/customers/{customer_id}")
# def get_customer(customer_id: int):
#     try:
#         with conn.cursor(cursor_factory=RealDictCursor) as cur:
#             cur.execute("SELECT * FROM customer WHERE id = %s;", (customer_id,))
#             customer = cur.fetchone()
#             if not customer:
#                 raise HTTPException(status_code=404, detail="Customer not found")
#         return customer
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))



def get_connection():
    return psycopg2.connect(DATABASE_URL)

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



