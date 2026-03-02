from engine.document_loader import DocumentLoader
from engine.structure_detector import StructureDetector

def testar(path):

    loader = DocumentLoader()
    detector = StructureDetector()

    doc = loader.load_pdf(path)

    estrutura = detector.detect(doc, debug=True)

    print("Estrutura detectada:", estrutura)


print("\n===== SANTANDER =====")
testar("tests/data/santander.pdf")

print("\n===== CAIXA =====")
testar("tests/data/caixa.pdf")