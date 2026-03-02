import re
import unicodedata
from database import cursor, conn

def normalizar(txt):
    txt = txt.lower()
    txt = unicodedata.normalize("NFKD", txt)
    txt = txt.encode("ASCII", "ignore").decode("ASCII")
    txt = re.sub(r"[^\w\s]", " ", txt)
    return re.sub(r"\s+", " ", txt).strip()

def classificar(desc):
    desc_n = normalizar(desc)
    for palavra, cat in cursor.execute("SELECT palavra,categoria FROM regras"):
        if palavra in desc_n:
            return cat
    return "Outros"