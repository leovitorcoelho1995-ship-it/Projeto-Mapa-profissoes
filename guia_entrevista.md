# Guia de Entrevista: Mapa das Profissões do Futuro

## 📌 Visão Geral do Projeto
Um painel analítico (Dashboard) focado no mercado de TI brasileiro. O objetivo é cruzar dados reais de vagas de emprego atuais (Adzuna) com tendências de interesse (Google Trends) e dados macroeconômicos (CAGED).

**Por que foi construído?**
Para responder a perguntas reais do mercado: "Quais skills estão em alta?", "A IA está roubando vagas ou o mercado apenas encolheu?" e "Qual área paga melhor?".

## 🏗️ Arquitetura e Pipeline de Dados (O "Como" e "Por que")
A arquitetura é propositalmente leve (Serverless / Flat Files). Optei por não usar bancos de dados caros, separando a extração da visualização para garantir velocidade e zero custo de infraestrutura.

- **`coleta.py` (Extração e Limpeza):**
  - Consome a **Adzuna API** para buscar centenas de vagas recentes.
  - Usa **Regex (NLP básico)** para varrer os títulos e descrições das vagas e extrair skills exigidas (ex: Python, AWS, Docker).
  - Gera agregações e salva um snapshot estático (`dados_snapshot.json`).
  - *Por que separado?* Chamadas de API demoram. Fazer isso em tempo real no dashboard arruinaria a experiência do usuário.

- **`enriquece_ia.py` (Enriquecimento e Tendências):**
  - Consome a API do **Google Trends** (`pytrends`) para pegar o histórico de 5 anos de buscas de skills e ferramentas (ex: ChatGPT, Copilot, Claude).
  - Cruza isso com a base histórica do **CAGED** (admissões/demissões no BR).
  - Possui um mecanismo de **Retentativa (Retry com Exponential Backoff)** para lidar de forma resiliente com bloqueios (Erro 429 - Too Many Requests) do Google.
  - Salva o arquivo final `dados_completos.json`.

- **`appi.py` (Frontend e Visualização):**
  - Desenvolvido em **Streamlit** (Python).
  - Lê o JSON consolidado instantaneamente.
  - Usa **Plotly** para gráficos interativos.
  - Possui **CSS customizado injetado** para fugir da "cara padrão" do Streamlit e garantir coesão visual com o resto do portfólio (Tipografia elegante, paleta de cores harmoniosa).

## 📊 Principais Insights da Análise
Se o recrutador perguntar "O que você descobriu com esses dados?", foque nestes pontos:

- **Efeito Macroeconômico vs IA:** A contração do mercado de TI após 2022 reflete o ciclo econômico (alta taxa de juros, fim do boom da pandemia) e não necessariamente a "destruição de empregos pela IA".
- **Adoção Corporativa de IA:** Mais de 10% das vagas já exigem conhecimento em IA. O mercado encolheu, mas quem fica precisa dominar as novas ferramentas (observado pelo pico do Gemini/Claude nas buscas).
- **Oportunidade (Demanda vs Salário):** DevOps e Engenharia de Dados apresentam o melhor equilíbrio de mercado. Engenharia de Machine Learning tem o maior teto salarial estimado (R$13k+), mas é um nicho com menos vagas brutas. Python é disparado a linguagem de programação mais exigida.
- **A Nuvem da Modalidade:** 83% das vagas não especificam se são remotas. A leitura crítica disso é: no Brasil, a omissão costuma indicar **contratação presencial (foco local)**.
- **Falta de Transparência Salarial:** Apenas uma fração mínima das empresas expõe o salário no anúncio. Por isso, a análise cruza os cargos coletados com tabelas salariais de referência para o nível Pleno, garantindo que o dashboard mostre uma realidade pé no chão.

## 💡 Dicas de Posicionamento (Como se vender)
- **Não foque só em código:** Diga que usou Python, mas destaque que seu maior valor foi **pensar no produto e no negócio**. Você construiu um "Data Product" ponta a ponta.
- **Defenda a engenharia pragmática:** Se perguntarem por que usou JSON e não SQL, responda: *"Para um dashboard analítico que funciona via snapshot, um JSON na memória custa R$0 e carrega em milissegundos. Não subo uma arquitetura complexa de banco de dados se o volume do problema não exige. Se o histórico crescesse para milhões de linhas, eu migraria para um PostgreSQL."*
- **Sinceridade sobre a IA (Vibe Coding):** Se perguntarem como você codou tudo, seja estratégico e transparente: *"Atuei como o Arquiteto e Tech Lead do projeto. Utilizei LLMs para acelerar a escrita do código pesado em Python/Streamlit, mas a modelagem de dados, a criação das métricas (Opportunity Score), a lógica de contornar os bloqueios de rede (Retry no Trends) e a interpretação humana dos dados (insight da vaga presencial) vieram do meu pensamento analítico."*
