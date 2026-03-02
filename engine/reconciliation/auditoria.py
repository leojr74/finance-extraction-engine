import re

def extrair_total_fatura(texto):
    padrao_total = re.search(
        r"total\s+(?:da\s+)?fatura.*?(-?\d+[.,]\d{2})",
        texto,
        re.IGNORECASE
    )

    if padrao_total:
        return float(padrao_total.group(1).replace(".", "").replace(",", "."))
    
    return None