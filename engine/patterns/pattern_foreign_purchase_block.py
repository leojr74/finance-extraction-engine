import re
from datetime import date


DATE_PATTERN = re.compile(r"(\d{2})/(\d{2})")
VALUE_PATTERN = re.compile(r"\d{1,3}(?:\.\d{3})*,\d{2}")
EXCHANGE_PATTERN = re.compile(r"\d+,\d+")

FOREIGN_LINE_PATTERN = re.compile(
    r"^\d{2}/\d{2} .+ \d{1,3}(?:\.\d{3})*,\d{2} \d{1,3}(?:\.\d{3})*,\d{2}"
)

COTACAO_PATTERN = re.compile(r"cotação", re.I)
IOF_PATTERN = re.compile(r"iof", re.I)


class ForeignPurchaseBlockPattern:

    def matches_block(self, lines, i):
        """
        Detecta bloco de 3 linhas:
        compra internacional + cotação + IOF
        """

        if i + 2 >= len(lines):
            return False

        l1 = lines[i].text.lower()
        l2 = lines[i + 1].text.lower()
        l3 = lines[i + 2].text.lower()

        return (
            FOREIGN_LINE_PATTERN.search(l1)
            and COTACAO_PATTERN.search(l2)
            and IOF_PATTERN.search(l3)
        )

    # -----------------------------------------------------

    def normalize_block(self, lines, i, reference_year, source_document):

        purchase_line = lines[i]
        exchange_line = lines[i + 1]
        iof_line = lines[i + 2]

        purchase_text = purchase_line.text
        exchange_text = exchange_line.text
        iof_text = iof_line.text

        # ----------------------------
        # DATA
        # ----------------------------
        d, m = DATE_PATTERN.search(purchase_text).groups()
        tx_date = date(reference_year, int(m), int(d))

        # ----------------------------
        # VALORES (R$ e moeda estrangeira)
        # ----------------------------
        values = VALUE_PATTERN.findall(purchase_text)
        amount_brl = float(values[-2].replace(".", "").replace(",", "."))
        amount_foreign = float(values[-1].replace(".", "").replace(",", "."))

        # ----------------------------
        # DESCRIÇÃO
        # ----------------------------
        desc = DATE_PATTERN.sub("", purchase_text)
        desc = VALUE_PATTERN.sub("", desc)
        desc = re.sub(r"\s+", " ", desc).strip()

        # ----------------------------
        # COTAÇÃO
        # ----------------------------
        rate = EXCHANGE_PATTERN.findall(exchange_text)[0]
        rate = float(rate.replace(",", "."))

        # ----------------------------
        # IOF
        # ----------------------------
        iof_value = VALUE_PATTERN.findall(iof_text)[0]
        iof_value = float(iof_value.replace(".", "").replace(",", "."))

        # ----------------------------
        # RETORNAR DUAS TRANSAÇÕES
        # ----------------------------
        return [
            dict(
                date=tx_date,
                description=desc,
                amount=amount_brl,
                transaction_type="debit",
                installment_info=None,
                source_document=source_document,
                raw_text=purchase_text,
                foreign_amount=amount_foreign,
                exchange_rate=rate,
            ),
            dict(
                date=tx_date,
                description=f"IOF {desc}",
                amount=iof_value,
                transaction_type="tax",
                installment_info=None,
                source_document=source_document,
                raw_text=iof_text,
            )
        ]