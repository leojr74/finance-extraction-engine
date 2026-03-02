import pdfplumber
import re
import io
from datetime import datetime, date
import sqlite3
import pandas as pd
import calendar


# =====================================================
# DATABASE
# =====================================================
conn = sqlite3.connect("finance.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    descricao TEXT,
    categoria TEXT,
    valor REAL
)
""")

conn.commit()


# =====================================================
# UTILITÁRIOS
# =====================================================

def ultimo_dia_mes(ano, mes):
    return calendar.monthrange(ano, mes)[1]


def detectar_periodo_fatura(texto):
    """
    Detecta o período contábil da fatura baseado nas datas presentes.
    Não depende da palavra 'Vencimento'.
    """

    datas_completas = re.findall(r"\d{2}/\d{2}/\d{4}", texto)
    if not datas_completas:
        raise Exception("Nenhuma data completa encontrada na fatura")

    anos = [int(d.split("/")[2]) for d in datas_completas]
    ano_base = max(anos)

    datas = re.findall(r"\b(\d{2})/(\d{2})\b", texto)
    meses = sorted({int(m) for _, m in datas})

    if not meses:
        raise Exception("Não encontrou meses nas transações")

    menor_mes = min(meses)
    maior_mes = max(meses)

    if 12 in meses and 1 in meses:
        inicio = date(ano_base - 1, 12, 1)
        fim = date(ano_base, 1, 31)
    else:
        inicio = date(ano_base, menor_mes, 1)
        fim = date(ano_base, maior_mes, ultimo_dia_mes(ano_base, maior_mes))

    return inicio, fim


def resolver_data(dia, mes, inicio, fim):
    for ano in [inicio.year, fim.year]:
        try:
            d = date(ano, mes, dia)
        except:
            d = date(ano, mes, min(dia, ultimo_dia_mes(ano, mes)))

        if inicio <= d <= fim:
            return d

    return date(inicio.year, mes, dia)


# =====================================================
# EXTRAÇÃO DE TRANSAÇÕES POR BLOCO
# =====================================================

PADRAO_LINHA = re.compile(
    r"^(?:\d+\s+)?"
    r"(\d{2}/\d{2})\s+"
    r"(.+?)\s+"
    r"(?:(\d{2}/\d{2})\s+)?"
    r"(-?\d+[.,]\d{2})$"
)


def extrair_transacoes(texto, inicio, fim):

    texto_unico = texto.replace("\n", " ")

    PADRAO = re.compile(
        r"(?:\d+\s+)?"
        r"(\d{2}/\d{2})\s+"
        r"(.+?)\s+"
        r"(?:(\d{2}/\d{2})\s+)?"
        r"(-?\d{1,3}(?:\.\d{3})*,\d{2})"
    )

    transacoes = []
    ultima_data = None
    ultima_desc = None

    for m in PADRAO.finditer(texto_unico):

        data_str, desc, parcela, valor = m.groups()
        desc_upper = desc.upper()

        # bloquear lançamentos financeiros que não são despesas reais
        bloquear = [
            "JUROS",
            "ENCARGO",
            "FINANCIAMENTO",
            "SALDO ANTERIOR",
            "ROTATIVO",
            "CET",
            "MULTA",
            "MORA",
            "PAGAMENTO",
            "TOTAL",
            "RESUMO"
        ]

        if any(p in desc_upper for p in bloquear):
            continue

        dia, mes = map(int, data_str.split("/"))
        data_real = resolver_data(dia, mes, inicio, fim)

        valor_float = float(valor.replace(".", "").replace(",", "."))

        if parcela:
            desc = f"{desc.strip()} ({parcela})"

        data_sql = data_real.strftime("%Y-%m-%d")

        transacoes.append(
            (data_sql, desc.strip(), valor_float)
        )

        ultima_data = data_sql
        ultima_desc = desc.strip()

    # -------------------------------------------------
    # CAPTURAR IOF SEM DATA (TRANSACAO SEPARADA)
    # -------------------------------------------------

    PADRAO_IOF = re.compile(
        r"IOF(?:\s+DESPESA\s+NO\s+EXTERIOR)?\s+(-?\d{1,3}(?:\.\d{3})*,\d{2})",
        re.IGNORECASE
    )

    for m in PADRAO_IOF.finditer(texto_unico):

        valor = m.group(1)
        valor_float = float(valor.replace(".", "").replace(",", "."))

        if ultima_data:
            transacoes.append(
                (
                    ultima_data,
                    f"IOF sobre {ultima_desc}",
                    valor_float
                )
            )

    return transacoes


# =====================================================
# TOTAL DA FATURA
# =====================================================

def extrair_total_fatura(texto):

    m = re.search(r"Total desta Fatura R\$\s*([\d.,]+)", texto)

    if m:
        return float(m.group(1).replace(".", "").replace(",", "."))

    return None


# =====================================================
# FUNÇÃO PRINCIPAL
# =====================================================

def importar_pdf_bytes(file_obj):

    file_obj.seek(0)
    pdf_bytes = file_obj.read()

    texto_total = ""

    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for pg in pdf.pages:
            txt = pg.extract_text()
            if txt:
                texto_total += txt + "\n"

    inicio, fim = detectar_periodo_fatura(texto_total)

    transacoes = extrair_transacoes(texto_total, inicio, fim)

    # limpa tabela antes de importar nova fatura
    cursor.execute("DELETE FROM transactions")

    soma = 0
    for data_sql, desc, valor in transacoes:
        cursor.execute(
            "INSERT INTO transactions(data,descricao,categoria,valor) VALUES(?,?,?,?)",
            (data_sql, desc, "Outros", valor),
        )
        soma += valor

    conn.commit()

    total_fatura = extrair_total_fatura(texto_total)

    diferenca = None
    if total_fatura:
        diferenca = round(total_fatura - soma, 2)

    # =====================================================
    # CSV DEBUG
    # =====================================================
    df = pd.read_sql_query(
        "SELECT data, descricao, valor FROM transactions ORDER BY data",
        conn
    )
    df.to_csv("debug_transacoes_extraidas.csv", index=False, encoding="utf-8-sig")

    return {
        "transacoes_importadas": len(transacoes),
        "total_extraido": round(soma, 2),
        "total_fatura_pdf": total_fatura,
        "diferenca": diferenca,
    }