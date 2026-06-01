# 🧭 Mapa das Profissões do Futuro

Dashboard interativo que analisa o mercado de tecnologia no Brasil, combinando dados reais de vagas, tendências de busca e salários.

---

## 📊 O que este projeto faz

- Coleta vagas reais de TI da API Adzuna (Brasil)
- Extrai skills técnicas das descrições usando NLP simples
- Mede tendências de busca de 5 anos no Google Trends
- Estima salários por profissão baseado em dados de mercado
- Calcula Opportunity Score (demanda + crescimento + interesse)
- Exibe tudo em dashboard visual interativo

---

## 🛠 Stack

| Tecnologia | Uso |
|------------|-----|
| Python | Coleta, processamento, dashboard |
| Adzuna API | Vagas reais do mercado brasileiro |
| Google Trends (pytrends) | Interesse de busca ao longo do tempo |
| Pandas | Manipulação e análise de dados |
| Streamlit | Dashboard interativo |
| Plotly | Gráficos e visualizações |

---

## 📁 Estrutura do projeto
mapa-profissoes/
├── coleta.py # Coleta vagas da Adzuna
├── coleta_complementar.py # Adiciona Trends 5 anos + salários
├── app.py # Dashboard Streamlit
├── ver_outros.py # Diagnóstico de categorização
├── .env # Chaves da API (não versionado)
├── dados_snapshot.json # Dados brutos da coleta
├── dados_completos.json # Dados enriquecidos finais
└── README.md # Este arquivo


---

## 🚀 Como rodar
```bash
1. Clone o repositório
git clone https://github.com/
cd mapa-profissoes

2. Crie o ambiente virtual
bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
3. Instale as dependências
bash
pip install -r requirements.txt
4. Configure a API Adzuna
Crie um arquivo .env com:

text
ADZUNA_APP_ID=seu_app_id
ADZUNA_API_KEY=sua_api_key
5. Execute a coleta
bash
python coleta.py
python coleta_complementar.py
6. Rode o dashboard
bash
streamlit run app.py
📈 Principais descobertas
IA cresceu +2075% em buscas nos últimos 5 anos

Python é a skill mais demandada (93 vagas)

JavaScript lidera em volume de vagas por profissão (184)

DevOps tem o melhor equilíbrio demanda/salário

83% das vagas não especificam modalidade de trabalho

📝 Licença
Projeto de portfólio pessoal. Dados públicos coletados via APIs oficiais.

text

## Passo 3: Criar requirements.txt

```bash
pip freeze > requirements.txt
Depois edite o arquivo e deixe apenas essas linhas:

text
pytrends==4.9.2
pandas
plotly
streamlit
requests
python-dotenv