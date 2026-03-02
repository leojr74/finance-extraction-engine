# engine/financial_line_classifier.py
import re
import unicodedata
from dataclasses import dataclass
from typing import List
from engine.extractors.text_stream_extractor import FinancialLineCandidate


FULL_DATE_PATTERN = re.compile(r"\b\d{2}/\d{2}/\d{4}\b")
LETTER_PATTERN = re.compile(r"[a-zA-Z]{3,}")
DATE_PATTERN = re.compile(r"\b\d{2}/\d{2}\b")
CAIXA_TRANSACTION_PATTERN = re.compile(
    r"""
    ^\d{2}/\d{2}          # data no início
    .+                    # descrição
    \d{1,3}(?:\.\d{3})*,\d{2}[DC]$   # valor no final com D ou C
    """,
    re.VERBOSE
)


# ---------------------------------------------------------
# ENUM SIMPLES DE TIPOS
# ---------------------------------------------------------

class LineType:
    TRANSACTION = "transaction"
    CREDIT = "credit"
    INTEREST = "interest"
    FEE = "fee"
    TAX = "tax"
    TOTAL = "total"
    SUBTOTAL = "subtotal"
    NOISE = "noise"


# ---------------------------------------------------------
# UTIL
# ---------------------------------------------------------

def normalize(text: str) -> str:
    text = text.lower()
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ASCII", "ignore").decode("ASCII")
    return text


DATE_PATTERN = re.compile(r"\b\d{2}/\d{2}\b")


# ---------------------------------------------------------
# CLASSIFICADOR
# ---------------------------------------------------------

class FinancialLineClassifier:

    def classify(self, candidate: FinancialLineCandidate) -> str:

        text = normalize(candidate.text)

        has_date = bool(DATE_PATTERN.search(text))
        has_value = len(candidate.detected_values) > 0

        if CAIXA_TRANSACTION_PATTERN.match(text.strip()):
            return LineType.TRANSACTION
        
        # -------------------------------------------------
        # TOTAL / SUBTOTAL
        # -------------------------------------------------
        if "total" in text:
            return LineType.TOTAL

        if "subtotal" in text:
            return LineType.SUBTOTAL

        # -------------------------------------------------
        # CREDIT
        # -------------------------------------------------
        if any(word in text for word in [
            "pagamento",
            "credito",
            "estorno"
        ]):
            return LineType.CREDIT

        # -------------------------------------------------
        # INTEREST / FEE / TAX
        # -------------------------------------------------
        if any(word in text for word in [
            "juros",
            "encargo",
            "multa"
        ]):
            return LineType.INTEREST

        if "iof" in text:
            return LineType.TAX

        if "taxa" in text:
            return LineType.FEE

        # -------------------------------------------------
        # TRANSACTION (regra estrutural refinada)
        # -------------------------------------------------

        full_dates = FULL_DATE_PATTERN.findall(text)
        has_letters = bool(LETTER_PATTERN.search(text))

        institutional_words = [
            "fatura",
            "vencimento",
            "limite",
            "disponivel",
            "saldo",
            "pagamento total",
            "resumo",
        ]

        is_institutional = any(word in text for word in institutional_words)

        if (
            has_date
            and has_value
            and has_letters
            and len(full_dates) <= 1
            and not is_institutional
        ):
            return LineType.TRANSACTION

        # fallback
        return LineType.NOISE