import re
from datetime import date
from engine.patterns.base import TransactionPattern


PATTERN = re.compile(
    r"""
    ^
    (\d{2}/\d{2})              # data
    \s+
    (.+?)                      # descrição
    \s+
    (\d{1,3}(?:\.\d{3})*,\d{2})([DC])   # valor + tipo
    $
    """,
    re.VERBOSE
)


class SignedAmountLinePattern(TransactionPattern):

    def matches(self, text: str) -> bool:
        return bool(PATTERN.match(text.strip()))

    def normalize(self, text: str, source_bank: str):

        m = PATTERN.match(text.strip())
        day_month, description, amount_str, sign = m.groups()

        # data (ano ainda simplificado)
        day, month = map(int, day_month.split("/"))
        transaction_date = date(2026, month, day)  # depois vamos inferir ano correto

        amount = float(amount_str.replace(".", "").replace(",", "."))

        transaction_type = "debit" if sign == "D" else "credit"

        return {
            "date": transaction_date,
            "description": description.strip(),
            "amount": amount,
            "transaction_type": transaction_type,
            "source_bank": source_bank,
            "raw_text": text,
        }