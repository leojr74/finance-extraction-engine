from engine.document_loader import DocumentLoader
from engine.structure_detector import StructureDetector, DocumentStructure
from engine.extractors.text_stream_extractor import TextStreamExtractor


loader = DocumentLoader()
detector = StructureDetector()
extractor = TextStreamExtractor()


def testar(path):

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    doc = loader.load_pdf(path)
    estrutura = detector.detect(doc)

    print("estrutura:", estrutura)

    if estrutura == DocumentStructure.TEXT_STREAM:
        candidatos = extractor.extract(doc)
        print("linhas financeiras detectadas:", len(candidatos))

        for c in candidatos[:10]:
            print("•", c.text)


testar("tests/data/santander.pdf")
testar("tests/data/caixa.pdf")