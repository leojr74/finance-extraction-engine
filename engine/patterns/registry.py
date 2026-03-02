from engine.patterns.pattern_signed_amount import SignedAmountLinePattern
from engine.patterns.pattern_installment_inline import InstallmentInlinePattern
from engine.patterns.pattern_simple_amount import SimpleAmountLinePattern

REGISTERED_PATTERNS = [
    SignedAmountLinePattern(),
    InstallmentInlinePattern(),
    SimpleAmountLinePattern(),   # ← ADICIONAR AQUI
]