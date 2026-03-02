# engine/structure_detector.py

from enum import Enum
from dataclasses import dataclass
from typing import Dict
from engine.document_loader import StructuredDocument


class DocumentStructure(Enum):
    TEXT_STREAM = "text_stream"
    TABULAR = "tabular"
    HYBRID = "hybrid"


@dataclass
class StructureMetrics:
    total_pages: int
    total_lines: int
    total_tables: int
    lines_per_page: float
    tables_per_page: float
    table_line_ratio: float
    avg_columns_per_table: float


class StructureDetector:

    def analyze(self, doc: StructuredDocument) -> StructureMetrics:

        total_pages = len(doc.pages)
        total_lines = 0
        total_tables = 0
        table_columns = []

        for page in doc.pages:
            total_lines += len(page.text_lines)
            total_tables += len(page.tables)

            for table in page.tables:
                if table.rows:
                    table_columns.append(len(table.rows[0]))

        lines_per_page = total_lines / total_pages if total_pages else 0
        tables_per_page = total_tables / total_pages if total_pages else 0
        table_line_ratio = (
            total_tables / total_lines if total_lines else 0
        )
        avg_columns = (
            sum(table_columns) / len(table_columns)
            if table_columns else 0
        )

        return StructureMetrics(
            total_pages=total_pages,
            total_lines=total_lines,
            total_tables=total_tables,
            lines_per_page=lines_per_page,
            tables_per_page=tables_per_page,
            table_line_ratio=table_line_ratio,
            avg_columns_per_table=avg_columns
        )

    # -----------------------------------------------------

    def detect(self, doc: StructuredDocument, debug: bool = False) -> DocumentStructure:

        metrics = self.analyze(doc)

        if debug:
            print("\n===== STRUCTURE METRICS =====")
            for field, value in metrics.__dict__.items():
                print(f"{field}: {value}")
            print("=============================\n")

        # -------------------------------------------------
        # HEURÍSTICA V1 (CALIBRADA COM SEUS DADOS)
        # -------------------------------------------------

        # Caso claramente tabular
        if metrics.tables_per_page >= 1.2:
            return DocumentStructure.TABULAR

        # Caso claramente textual denso
        if metrics.lines_per_page >= 120 and metrics.tables_per_page < 1:
            return DocumentStructure.TEXT_STREAM

        # Caso intermediário
        return DocumentStructure.HYBRID