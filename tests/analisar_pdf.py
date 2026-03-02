from engine.document_loader import DocumentLoader
from collections import Counter


def analisar(path):

    loader = DocumentLoader()
    doc = loader.load_pdf(path)

    x_positions = []

    for page in doc.pages:
        for line in page.text_lines:
            if line.bbox:
                x_positions.append(round(line.bbox[0], 0))

    counts = Counter(x_positions)

    print("\n==============================")
    print("ARQUIVO:", path)
    print("==============================")

    print("total linhas:", len(x_positions))
    print("colunas distintas:", len(counts))

    print("\nTOP alinhamentos (coluna → frequência)")
    for pos, freq in counts.most_common(10):
        print(pos, "→", freq)


analisar("tests/data/santander.pdf")
analisar("tests/data/caixa.pdf")