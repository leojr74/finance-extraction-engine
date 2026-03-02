# Finance Extraction Engine

Motor universal de extração, classificação e normalização de dados financeiros a partir de faturas de cartão de crédito e extratos bancários em PDF.

Projeto focado em **robustez estrutural**, **precisão contábil** e **escalabilidade multi-instituição**.

---

# 🎯 Objetivo do Projeto

Desenvolver um sistema capaz de:

* importar faturas de cartão de crédito em PDF
* extrair automaticamente transações financeiras
* classificar linhas financeiras semanticamente
* normalizar dados em modelo contábil único
* reconciliar totais da fatura
* persistir dados estruturados
* funcionar via API
* escalar para múltiplas instituições financeiras

---

# 🚀 Visão de Produto (Longo Prazo)

Este projeto evoluirá para:

* aplicativo de organização financeira pessoal
* sistema automático de categorização de gastos
* plataforma SaaS de ingestão financeira
* motor universal de leitura de documentos financeiros
* serviço comercial freemium + premium

Objetivo arquitetural principal:

👉 suportar múltiplos bancos com mínima customização

---

# 🧠 Filosofia de Engenharia

O sistema **não depende de parsers específicos por banco**.

A abordagem é baseada em estrutura documental.

O projeto utiliza:

✔ extração estrutural universal
✔ classificação semântica de linhas
✔ normalização contábil padronizada
✔ padrões reutilizáveis de transação
✔ adaptadores mínimos por instituição

---

# 🏗 Arquitetura do Sistema

Pipeline universal de processamento:

```
PDF
  ↓
Document Loader
  ↓
Structure Detector
  ↓
Structural Extractor
  ↓
Financial Line Classifier
  ↓
Transaction Pattern Engine
  ↓
Normalizer
  ↓
Reconciliation Engine
  ↓
Persistence / API
```

---

# 🧩 Componentes Principais

## Document Loader

Extrai estrutura física do PDF:

* texto bruto
* páginas
* linhas
* tabelas
* metadados estruturais

Não interpreta conteúdo financeiro.

---

## Structure Detector

Classifica o tipo estrutural do documento:

* TEXT_STREAM
* TABULAR
* HYBRID

Baseado em heurísticas estruturais.

---

## Structural Extractors

Extraem candidatos financeiros conforme estrutura:

* Text Stream Extractor
* Table Extractor
* Hybrid Reconstruction

---

## Financial Line Classifier

Classifica cada linha em:

* transaction
* credit
* interest
* tax
* fee
* total
* subtotal
* noise

---

## Transaction Pattern Engine

Sistema baseado em padrões reutilizáveis:

Cada padrão sabe:

* identificar formato de transação
* extrair dados estruturados
* normalizar representação contábil

Exemplos:

* compra parcelada
* compra internacional
* crédito estornado
* débito simples

---

## Normalizer

Converte dados extraídos em modelo único:

```
Transaction(
    date
    description
    amount
    transaction_type
    installment_info
    source_document
    page
    raw_text
)
```

---

## Reconciliation Engine

Validação contábil automática:

* identifica total da fatura
* soma transações
* detecta divergências
* auditoria financeira

---

# ✅ Estado Atual do Projeto

✔ Parser Santander completo e reconciliado
✔ Detecção estrutural universal funcional
✔ Extração text stream operacional
✔ Extração tabular funcional
✔ Classificador financeiro ativo
✔ Engine de padrões implementada
✔ Normalização multi-banco operacional
✔ Reconciliação contábil funcional
✔ Integração FastAPI
✔ Persistência SQLite

---

# 📊 Bancos Suportados (Atual)

* Santander
* Caixa Econômica Federal

Arquitetura preparada para expansão automática.

---

# 🧪 Como Executar o Projeto

### 1 — Clonar repositório

```
git clone https://github.com/leojr74/finance-extraction-engine.git
cd finance-extraction-engine
```

### 2 — Criar ambiente virtual

```
python -m venv venv
venv\\Scripts\\activate
```

### 3 — Instalar dependências

```
pip install -r requirements.txt
```

### 4 — Executar API

```
uvicorn main:app --reload
```

---

# 📡 Endpoint Principal

Upload de PDF financeiro:

```
POST /upload
```

Retorna transações estruturadas e auditadas.

---

# 🧭 Roadmap Técnico

## Extração

* detecção automática de ano da fatura
* reconstrução avançada de blocos multi-linha
* heurísticas híbridas aprimoradas

## Normalização

* expansão da biblioteca de padrões
* reconhecimento semântico de estabelecimentos
* padronização internacional de moedas

## Classificação

* categorização automática de gastos
* modelo ML supervisionado

## Plataforma

* dashboard web
* autenticação de usuários
* multi-contas
* análise histórica
* previsões financeiras

## SaaS

* API pública
* planos de assinatura
* integração bancária direta

---

# 🧪 Qualidade e Validação

O sistema é projetado para:

✔ reconciliação contábil obrigatória
✔ rastreabilidade completa da origem do dado
✔ tolerância a layouts inconsistentes
✔ auditabilidade financeira

---

# 📄 Licença

A definir.

---

# 👤 Autor

Leonardo Junior

Projeto independente de engenharia financeira aplicada.

---

# ⭐ Propósito Maior

Construir o primeiro motor universal brasileiro de leitura estruturada de documentos financeiros não padronizados.

Transformar PDFs bancários em dados financeiros confiáveis e auditáveis em escala.
