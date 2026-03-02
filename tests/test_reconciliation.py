from engine.document_loader import DocumentLoader
from engine.orchestrator import ExtractionOrchestrator
from engine.classifier.financial_line_classifier import FinancialLineClassifier
from engine.normalizer import Normalizer
from engine.reconciliation.auditoria import extrair_total_fatura


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
    print("\n--- LINHAS CLASSIFICADAS COMO TOTAL ---")
    for c in candidates:
        if classifier.classify(c) == "total":
            print("TOTAL LINE:", c.text)
    print("---------------------------------------")

    transactions = []
    total_candidates = []

    # -----------------------------
    # separar transações e totais
    # -----------------------------
    for c in candidates:
        tipo = classifier.classify(c)

        if tipo == "transaction":
            t = normalizer.normalize(
                c,
                transaction_type="transaction",
                source_document=source_document
            )
            if t:
                transactions.append(t)

        elif tipo == "total":
            total_candidates.append(c)

    # -----------------------------
    # escolher total correto
    # -----------------------------
    total_line = None

    # prioridade 1 — pagamento total
    for c in total_candidates:
        if "pagamento total" in c.text.lower():
            total_line = c
            break

    # prioridade 2 — valor total da fatura
    if total_line is None:
        for c in total_candidates:
            texto = c.text.lower()
            if "valor total" in texto and "fatura" in texto:
                total_line = c
                break

    # fallback — último total
    if total_line is None and total_candidates:
        total_line = total_candidates[-1]

    # -----------------------------
    # validar
    # -----------------------------
    if total_line is None:
        print("Nenhum total encontrado.")
        return

    print("TOTAL ESCOLHIDO:", total_line.text)

    total_value = normalizer._extract_amount(total_line.text)

    # -----------------------------
    # calcular soma
    # -----------------------------
    soma = (
        sum(t.amount for t in transactions if t.transaction_type == "debit")
        - sum(t.amount for t in transactions if t.transaction_type == "credit")
    )

    print("Total da fatura:", total_value)
    print("Soma das transações:", soma)
    print("Diferença:", round(total_value - soma, 2))
    # extrair valor do total
    total_value = normalizer._extract_amount(total_line.text)
    print("Total da fatura:", total_value)

    soma = sum(t.amount for t in transactions if t.transaction_type == "debit") \
     - sum(t.amount for t in transactions if t.transaction_type == "credit")

    print("Soma das transações:", soma)

    print("Diferença:", round(total_value - soma, 2))


testar("tests/data/santander.pdf", "santander")
testar("tests/data/caixa.pdf", "caixa")