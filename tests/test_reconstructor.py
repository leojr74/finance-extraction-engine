from engine.document_loader import DocumentLoader
from engine.orchestrator import ExtractionOrchestrator
from engine.reconstructors.transaction_reconstructor import TransactionReconstructor

loader = DocumentLoader()
orchestrator = ExtractionOrchestrator()
reconstructor = TransactionReconstructor()


def testar(path):

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    doc = loader.load_pdf(path)

    candidatos = orchestrator.extract_candidates(doc)
    print("candidatos brutos:", len(candidatos))

    reconstruidos = reconstructor.reconstruct(candidatos)
    print("candidatos reconstruídos:", len(reconstruidos))

    for r in reconstruidos[:10]:
        print("•", r.text)


testar("tests/data/santander.pdf")
testar("tests/data/caixa.pdf")