from engine.document_loader import DocumentLoader
from engine.extractors.text_stream_extractor import TextStreamExtractor

loader = DocumentLoader()
extractor = TextStreamExtractor()

doc = loader.load_pdf("tests/data/caixa.pdf")

print("Total text lines:")

total = 0

for page in doc.pages:
    for line in page.text_lines:
        total += 1
        if "156,98" in line.text:
            print("Linha encontrada:", line.text)

print("Total linhas:", total)

candidatos = extractor.extract(doc)

print("\nCandidatos detectados:", len(candidatos))

for c in candidatos[:20]:
    print("•", c.text)