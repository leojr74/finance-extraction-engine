from collections import Counter

from engine.document_loader import DocumentLoader
from engine.orchestrator import ExtractionOrchestrator
from engine.classifier.financial_line_classifier import (
    FinancialLineClassifier,
    LineType
)

loader = DocumentLoader()
orchestrator = ExtractionOrchestrator()
classifier = FinancialLineClassifier()


def testar(path):

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    doc = loader.load_pdf(path)

    candidatos = orchestrator.extract_candidates(doc)

    tipos = [classifier.classify(c) for c in candidatos]
    contagem = Counter(tipos)

    print("Distribuição de tipos:")
    for k, v in contagem.items():
        print(k, "→", v)

    print("\nExemplos TRANSACTION:")
    for c in candidatos:
        if classifier.classify(c) == LineType.TRANSACTION:
            print("•", c.text)
            break


testar("tests/data/santander.pdf")
testar("tests/data/caixa.pdf")