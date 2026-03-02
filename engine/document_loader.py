# engine/document_loader.py

from dataclasses import dataclass, field
from typing import List, Tuple, Optional
import pdfplumber


# =========================================================
# MODELOS ESTRUTURAIS
# =========================================================

BBox = Tuple[float, float, float, float]  # x0, top, x1, bottom


@dataclass
class TextLine:
    text: str
    page: int
    bbox: Optional[BBox] = None


@dataclass
class TableCell:
    text: str
    row: int
    col: int


@dataclass
class TableBlock:
    page: int
    bbox: Optional[BBox]
    rows: List[List[TableCell]]


@dataclass
class PageLayout:
    page_number: int
    text_lines: List[TextLine] = field(default_factory=list)
    tables: List[TableBlock] = field(default_factory=list)


@dataclass
class StructuredDocument:
    pages: List[PageLayout]
    raw_text: str
    metadata: dict


# =========================================================
# DOCUMENT LOADER
# =========================================================

class DocumentLoader:

    def load_pdf(self, file_path: str) -> StructuredDocument:

        pages: List[PageLayout] = []
        full_text = []

        with pdfplumber.open(file_path) as pdf:

            for page_index, page in enumerate(pdf.pages):

                page_layout = PageLayout(page_number=page_index + 1)

                # -------------------------------------------------
                # EXTRAÇÃO DE TEXTO COM POSIÇÃO
                # -------------------------------------------------

                words = page.extract_words()

                # agrupar palavras por linha vertical
                lines = {}
                for w in words:
                    top = round(w["top"], 1)
                    lines.setdefault(top, []).append(w)

                for top, group in sorted(lines.items()):
                    group_sorted = sorted(group, key=lambda x: x["x0"])
                    text = " ".join(w["text"] for w in group_sorted)

                    x0 = min(w["x0"] for w in group_sorted)
                    x1 = max(w["x1"] for w in group_sorted)
                    bottom = max(w["bottom"] for w in group_sorted)

                    page_layout.text_lines.append(
                        TextLine(
                            text=text.strip(),
                            page=page_index + 1,
                            bbox=(x0, top, x1, bottom)
                        )
                    )

                # -------------------------------------------------
                # EXTRAÇÃO DE TABELAS REAIS
                # -------------------------------------------------

                table_settings = {
                    "vertical_strategy": "lines",
                    "horizontal_strategy": "lines",
                }

                tables = page.find_tables(table_settings)

                for table in tables:

                    extracted = table.extract()

                    if not extracted:
                        continue

                    rows = []
                    for r_idx, row in enumerate(extracted):
                        row_cells = []
                        for c_idx, cell in enumerate(row):
                            row_cells.append(
                                TableCell(
                                    text=(cell or "").strip(),
                                    row=r_idx,
                                    col=c_idx
                                )
                            )
                        rows.append(row_cells)

                    page_layout.tables.append(
                        TableBlock(
                            page=page_index + 1,
                            bbox=table.bbox,
                            rows=rows
                        )
                    )

                # -------------------------------------------------
                # TEXTO GLOBAL (para compatibilidade futura)
                # -------------------------------------------------

                txt = page.extract_text()
                if txt:
                    full_text.append(txt)

                pages.append(page_layout)

        return StructuredDocument(
            pages=pages,
            raw_text="\n".join(full_text),
            metadata={
                "page_count": len(pages),
                "source": file_path
            }
        )