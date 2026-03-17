# 🧪 Lab: Gemini 3 Flash + Agno (Phidata) Orchestration

Este repositório documenta o Experimento B do nosso laboratório de pesquisa autônoma. O objetivo foi testar a escalabilidade profunda da arquitetura **LLM-as-a-Judge**, fornecendo um budget de 50 iterações para o orquestrador **Gemini 3 Flash** (via Antigravity) para observar se ele descobriria heurísticas ótimas de extração de dados financeiros.

O resultado foi a escrita 100% autônoma de um agente (`agent.py`) de nível Sênior, culminando em uma pontuação de pico de **92/100** e uma estabilidade formidável.

---

## 🔬 Parâmetros do Experimento

* **Orquestrador:** Gemini 3 Flash (via Google Antigravity)
* **Juiz Avaliador:** Llama 3.2:3B (Local Edge / Ollama)
* **LLM do Agente (Target):** meta-llama/llama-3.1-8b-instruct (via OpenRouter)
* **Budget de Iterações:** 50
* **Iterações Utilizadas:** 35 (O Orquestrador identificou *diminishing returns* e encerrou a otimização após estabilizar o pico de 92 pontos).

---

## 🧠 Descobertas Arquiteturais do Orquestrador

O Gemini 3 Flash refatorou completamente a base de código durante as 35 iterações, convergindo para decisões de arquitetura de software modernas e incrivelmente robustas:

1. **Abandono do Vanilla e Adoção do Agno (Phidata):** O orquestrador identificou que tentar forçar um modelo de 8B (Llama 3.1) a gerar JSON via engenharia de prompt era suscetível a falhas. Ele importou o framework **Agno** (`from agno.agent import Agent`) para gerenciar as *tools* de busca nativamente.
2. **Type Safety com Pydantic (A Sacada de Mestre):** Para blindar o sistema contra quebras de formatação JSON (que diminuíam a nota do juiz), o agente criou uma classe estruturada `FinancialReport(BaseModel)`. Ao passar isso como `output_schema` para a LLM, ele garantiu matematicamente a geração do JSON perfeito em 100% das execuções, sem necessidade de Regex complexos.
3. **Expansão de *Due Diligence*:** Sem ser explicitamente instruído no prompt original, o Orquestrador alterou as próprias *system instructions* para mandar o agente caçar métricas avançadas (*"search for P/E Ratio, Debt-to-Equity, and Interest Coverage Ratio"*), demonstrando uma real adequação à persona de Senior Equity Analyst.

---

## 📊 Análise de Performance

A adoção da dupla **Agno + Pydantic** fez com que as taxas de falha crítica (Score 0 por erro de formatação) caíssem a praticamente zero nas iterações finais.

O agente estabilizou na faixa dos 87 a 92 pontos. A não-obtenção dos 100 pontos deve-se puramente à sensibilidade estocástica do buscador (DuckDuckGoTools) e ao rigor do Juiz local quanto a variações semânticas menores ("Metric not found" vs "Not publicly disclosed").

---

## 🚀 Como Reproduzir o Agente

### Pré-requisitos
* Python 3.10+
* Chave de API do OpenRouter

### Instalação

Clone o repositório e instale as dependências:

    pip install agno pydantic duckduckgo-search python-dotenv

Crie um arquivo `.env` na raiz e adicione sua chave:

    OPENROUTER_API_KEY="sk-or-v1-sua-chave"

### Execução

Execute no terminal passando o *ticker* desejado:

    python agent.py "Resultados Financeiros WEG (WEGE3) 2024"

A saída será o objeto JSON validado pelo Pydantic, pronto para consumo em pipelines de dados.