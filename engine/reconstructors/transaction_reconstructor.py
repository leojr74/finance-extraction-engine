# engine/reconstructors/transaction_reconstructor.py

import re
from typing import List
from engine.extractors.text_stream_extractor import FinancialLineCandidate


DATE_PATTERN = re.compile(r"\b\d{2}/\d{2}\b")
VALUE_PATTERN = re.compile(r"-?\d{1,3}(?:\.\d{3})*,\d{2}")


class TransactionReconstructor:

    def reconstruct(
        self,
        candidates: List[FinancialLineCandidate]
    ) -> List[FinancialLineCandidate]:

        if not candidates:
            return []

        # garantir ordem de leitura
        candidates = sorted(
            candidates,
            key=lambda c: (c.page, c.line_index)
        )

        reconstructed = []
        buffer = []

        current_page = None

        for c in candidates:

            text = c.text
            has_date = bool(DATE_PATTERN.search(text))
            has_value = bool(VALUE_PATTERN.search(text))

            is_transaction_anchor = has_date or has_value

            # nova página sempre fecha bloco
            if current_page is not None and c.page != current_page:
                self._flush_buffer(buffer, reconstructed)
                buffer = []

            current_page = c.page

            # se linha parece início de transação
            if is_transaction_anchor:

                # se já havia conteúdo → finalizar bloco anterior
                if buffer:
                    self._flush_buffer(buffer, reconstructed)
                    buffer = []

                buffer.append(c)

            else:
                # continuação textual
                if buffer:
                    buffer.append(c)

        # flush final
        self._flush_buffer(buffer, reconstructed)

        return reconstructed

    # -----------------------------------------------------

    def _flush_buffer(self, buffer, output):

        if not buffer:
            return

        combined_text = " ".join(c.text for c in buffer)
        combined_values = []

        for c in buffer:
            combined_values.extend(c.detected_values)

        first = buffer[0]

        output.append(
            FinancialLineCandidate(
                text=combined_text,
                page=first.page,
                bbox=first.bbox,
                detected_values=combined_values,
                line_index=first.line_index
            )
        )