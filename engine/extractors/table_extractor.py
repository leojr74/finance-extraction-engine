# engine/extractors/table_extractor.py

import re
from typing import List
from engine.document_loader import StructuredDocument
from engine.extractors.text_stream_extractor import FinancialLineCandidate


MONEY_PATTERN = re.compile(
    r"""
    (?:
        R\$?\s*
    )?
    -?
    \d{1,3}(?:\.\d{3})*
    ,\d{2}
    [DC]?              # ← aceita 156,98D ou 156,98C
    |
    -?\d+,\d{2}[DC]?
    """,
    re.VERBOSE
)

LETTER_PATTERN = re.compile(r"[a-zA-Z]{3,}")


class TableExtractor:

    def extract(self, doc: StructuredDocument) -> List[FinancialLineCandidate]:

        candidates = []
        global_line_index = 0

        for page in doc.pages:

            for table in page.tables:

                for row in table.rows:

                    # reconstruir texto da linha a partir das células
                    row_text_parts = []

                    for cell in row:
                        if cell.text and cell.text.strip():
                            row_text_parts.append(cell.text.strip())

                    if not row_text_parts:
                        continue

                    row_text = " ".join(row_text_parts)

                    matches = MONEY_PATTERN.findall(row_text)
                    has_letters = bool(LETTER_PATTERN.search(row_text))

                    institutional_words = [
                        "total",
                        "saldo",
                        "parceladas",
                        "final",
                        "compras",
                    ]

                    is_institutional = any(
                        word in row_text.lower()
                        for word in institutional_words
                    )

                    if matches and has_letters and not is_institutional:

                        candidates.append(
                            FinancialLineCandidate(
                                text=row_text,
                                page=page.page_number,
                                bbox=table.bbox,
                                detected_values=matches,
                                line_index=global_line_index
                            )
                        )

                    global_line_index += 1

        return candidates