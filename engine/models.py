# engine/models.py

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Transaction:

    # --- dados contábeis ---
    date: date
    description: str
    amount: float

    # --- classificação estrutural ---
    transaction_type: str   # debit / credit / fee / tax / etc

    # --- metadados ---
    installment_info: Optional[str]
    source_document: str
    page: int
    raw_text: str