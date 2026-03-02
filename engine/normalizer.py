# engine/normalizer.py

import re
from datetime import date
from typing import Optional
from engine.models import Transaction
from engine.extractors.text_stream_extractor import FinancialLineCandidate
from engine.patterns.registry import REGISTERED_PATTERNS


DATE_PATTERN = re.compile(r"\b(\d{2})/(\d{2})\b")
VALUE_PATTERN = re.compile(r"-?\d{1,3}(?:\.\d{3})*,\d{2}")
INSTALLMENT_PATTERN = re.compile(r"\b\d{2}/\d{2}\b")


class Normalizer:

    def __init__(self, reference_year: int):
        """
        reference_year:
        ano base da fatura (ex: 2026)
        futuramente será detectado automaticamente.
        """
        self.reference_year = reference_year

    # -----------------------------------------------------

    def _extract_date(self, text: str) -> date:

        match = DATE_PATTERN.search(text)
        if not match:
            raise ValueError("Data não encontrada")

        day = int(match.group(1))
        month = int(match.group(2))

        return date(self.reference_year, month, day)

    # -----------------------------------------------------

    def _extract_amount(self, text: str) -> float:

        values = VALUE_PATTERN.findall(text)
        if not values:
            raise ValueError("Valor não encontrado")

        value = values[-1]  # normalmente último valor é o relevante

        value = value.replace("D", "").replace("C", "")
        return float(value.replace(".", "").replace(",", "."))

    # -----------------------------------------------------

    def _extract_installment(self, text: str) -> Optional[str]:

        matches = INSTALLMENT_PATTERN.findall(text)

        # se houver duas datas pequenas, segunda pode ser parcela
        if len(matches) >= 2:
            return matches[1]

        return None

    # -----------------------------------------------------

    def _clean_description(self, text: str) -> str:

        # remove datas
        text = DATE_PATTERN.sub("", text)

        # remove valores
        text = VALUE_PATTERN.sub("", text)

        # remove espaços extras
        return re.sub(r"\s+", " ", text).strip()

    # -----------------------------------------------------

    def normalize(
        self,
        candidate: FinancialLineCandidate,
        transaction_type: str,
        source_document: str
    ) -> Transaction:

        text = candidate.text

        for pattern in REGISTERED_PATTERNS:
            if pattern.matches(text):

                data = pattern.normalize(text, source_document)

                return Transaction(
                    date=data["date"],
                    description=data["description"],
                    amount=data["amount"],
                    transaction_type=data["transaction_type"],
                    installment_info=data.get("installment_info"),
                    source_document=data["source_bank"],
                    page=candidate.page,
                    raw_text=data["raw_text"],
                )

        return None