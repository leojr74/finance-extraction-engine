from engine.document_loader import DocumentLoader
from engine.structure_detector import StructureDetector, DocumentStructure
from engine.extractors.table_extractor import TableExtractor

loader = DocumentLoader()
detector = StructureDetector()
extractor = TableExtractor()


def testar(path):

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    doc = loader.load_pdf(path)
    estrutura = detector.detect(doc)

    print("estrutura:", estrutura)

    if estrutura != DocumentStructure.TABULAR:
        print("Documento não é TABULAR")
        return

    candidatos = extractor.extract(doc)

    print("linhas detectadas:", len(candidatos))

    for c in candidatos[:10]:
        print("•", c.text)


testar("tests/data/caixa.pdf")