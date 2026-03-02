from engine.document_loader import DocumentLoader

loader = DocumentLoader()
doc = loader.load_pdf("tests/data/santander.pdf")

print(type(doc))
print(dir(doc))