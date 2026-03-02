from engine.document_loader import DocumentLoader
from engine.orchestrator import ExtractionOrchestrator
from engine.classifier.financial_line_classifier import FinancialLineClassifier
from engine.normalizer import Normalizer


loader = DocumentLoader()
orchestrator = ExtractionOrchestrator()
classifier = FinancialLineClassifier()
normalizer = Normalizer(reference_year=2026)


def testar(path, source_document):

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    doc = loader.load_pdf(path)
    candidates = orchestrator.extract_candidates(doc)

    transactions = []

    for c in candidates:
        if classifier.classify(c) == "transaction":
            t = normalizer.normalize(
                c,
                transaction_type="transaction",
                source_document=source_document
            )
            if t:
                transactions.append(t)

    print("Transações normalizadas:", len(transactions))

    for t in transactions[:5]:
        print(t)


testar("tests/data/santander.pdf", "santander")
testar("tests/data/caixa.pdf", "caixa")