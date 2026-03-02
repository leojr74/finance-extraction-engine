from engine.document_loader import DocumentLoader
from engine.orchestrator import ExtractionOrchestrator

loader = DocumentLoader()
orchestrator = ExtractionOrchestrator()


def testar(path):

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    doc = loader.load_pdf(path)
    candidatos = orchestrator.extract_candidates(doc)
    print("\n--- Procurando CeA ---")

    for c in candidatos:
        if "CeA" in c.text:
            print("ENCONTRADO:", c.text)
    print("candidatos detectados:", len(candidatos))

    for c in candidatos[:10]:
        print("•", c.text)


testar("tests/data/santander.pdf")
testar("tests/data/caixa.pdf")