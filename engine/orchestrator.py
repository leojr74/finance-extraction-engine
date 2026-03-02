# engine/orchestrator.py

from engine.structure_detector import StructureDetector, DocumentStructure
from engine.extractors.text_stream_extractor import TextStreamExtractor
from engine.extractors.table_extractor import TableExtractor


class ExtractionOrchestrator:

    def __init__(self):
        self.detector = StructureDetector()
        self.table_extractor = TableExtractor()

    # -----------------------------------------------------

    def extract_candidates(self, doc):

        structure = self.detector.detect(doc)
        text_extractor = TextStreamExtractor(
            reference_year=2026,
            source_document="santander"
        )

        # TEXT_STREAM direto
        if structure == DocumentStructure.TEXT_STREAM:
            return text_extractor.extract(doc)

        # TABULAR → tentar tabela primeiro
        if structure == DocumentStructure.TABULAR:

            table_candidates = self.table_extractor.extract(doc)

            # heurística: se extraiu pouco, tentar texto também
            if len(table_candidates) < 5:
                text_candidates = self.text_extractor.extract(doc)
                return text_candidates

            return table_candidates

        # HYBRID → combinar ambos
        if structure == DocumentStructure.HYBRID:

            table_candidates = self.table_extractor.extract(doc)
            text_candidates = self.text_extractor.extract(doc)

            return table_candidates + text_candidates