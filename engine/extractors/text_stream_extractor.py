from typing import List
from dataclasses import dataclass

from engine.patterns.pattern_foreign_purchase_block import (
    ForeignPurchaseBlockPattern,
)


# ---------------------------------------------------------
# MODELO DE LINHA
# ---------------------------------------------------------

@dataclass
class FinancialLineCandidate:
    text: str
    page: int = 0


# ---------------------------------------------------------
# EXTRACTOR
# ---------------------------------------------------------

class TextStreamExtractor:

    def __init__(self, reference_year: int, source_document: str):
        self.reference_year = reference_year
        self.source_document = source_document
        self.foreign_block_pattern = ForeignPurchaseBlockPattern()

    # -----------------------------------------------------

    def extract(self, document) -> List[FinancialLineCandidate]:

        candidates: List[FinancialLineCandidate] = []

        # -------------------------------------------------
        # GERAR LINHAS ESTRUTURADAS A PARTIR DO TEXTO
        # -------------------------------------------------
        raw_lines = document.raw_text.split("\n")

        structured_lines: List[FinancialLineCandidate] = []
        for raw in raw_lines:
            raw = raw.strip()
            if raw:
                structured_lines.append(
                    FinancialLineCandidate(
                        text=raw,
                        page=0
                    )
                )

        # -------------------------------------------------
        # PROCESSAR LINHAS
        # -------------------------------------------------
        i = 0

        while i < len(structured_lines):

            line = structured_lines[i]

            # ---------------------------------------------
            # BLOCO INTERNACIONAL (3 linhas)
            # ---------------------------------------------
            if self.foreign_block_pattern.matches_block(structured_lines, i):

                normalized_items = self.foreign_block_pattern.normalize_block(
                    structured_lines,
                    i,
                    reference_year=self.reference_year,
                    source_document=self.source_document
                )

                for item in normalized_items:
                    candidates.append(
                        FinancialLineCandidate(
                            text=item["raw_text"],
                            page=0
                        )
                    )

                i += 3
                continue

            # ---------------------------------------------
            # LINHA NORMAL
            # ---------------------------------------------
            candidates.append(line)
            i += 1

        return candidates