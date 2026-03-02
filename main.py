from fastapi import FastAPI, UploadFile
from legacy.parser_santander import importar_pdf_bytes
from database.database import conn
import pandas as pd

app = FastAPI(title="Finance API")

@app.get("/")
def root():
    return {"status": "API online"}

@app.post("/upload")
async def upload(file: UploadFile):
    resultado = importar_pdf_bytes(file.file)
    return resultado

@app.get("/transacoes")
def listar():
    df = pd.read_sql_query(
        "SELECT data, descricao, categoria, valor FROM transactions",
        cursor.connection
    )
    return df.to_dict(orient="records")

@app.get("/resumo")
def resumo():
    df = pd.read_sql_query(
        "SELECT categoria, SUM(valor) as total FROM transactions GROUP BY categoria",
        cursor.connection
    )
    return df.to_dict(orient="records")