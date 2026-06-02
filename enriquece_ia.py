"""
enriquece_ia.py
Adiciona seção "analise_ia" ao dados_completos.json.

Lotes do Google Trends buscados SEPARADAMENTE para evitar
achatamento por normalização relativa:

  Lote A — IA como skill de trabalho (mercado profissional)
      "machine learning", "engenheiro de dados", "cientista de dados"

  Lote B — Ferramentas de IA no trabalho (adoção corporativa)
      "ChatGPT trabalho", "GitHub Copilot", "Gemini Google"

  Lote C — Demanda por vagas TI (proxy de mercado)
      "vaga analista de dados", "vaga desenvolvedor", "vaga engenheiro"

  Solo — Inteligência Artificial (buscado sozinho para não ser achatado)
      "Inteligência Artificial"
"""

import json
import time
import csv
from datetime import date
from pytrends.request import TrendReq

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_CAGED   = "data/serie_temporal.csv"
ARQUIVO_ENTRADA = "dados_completos.json"
ARQUIVO_SAIDA   = "dados_completos.json"

MARCO_CHATGPT = "2022-11"

# Lotes separados — cada um normalizado internamente pelo Trends
LOTES_TRENDS = {
    "skills_trabalho": [
        "machine learning",
        "engenheiro de dados",
        "cientista de dados",
    ],
    "ferramentas_ia": [
        "ChatGPT trabalho",
        "GitHub Copilot",
        "Gemini Google",
        "Claude AI",
    ],
    "demanda_vagas": [
        "vaga analista de dados",
        "vaga desenvolvedor",
        "vaga engenheiro",
    ],
    "ia_solo": [
        "Inteligência Artificial",
    ],
}

# Palavras-chave para detecção de IA nas vagas Adzuna
PALAVRAS_IA = [
    "inteligência artificial", "machine learning", "deep learning",
    "llm", "chatgpt", "gpt", "copilot", "ia generativa",
    "generative ai", "nlp", "computer vision", "mlops",
    "large language model", "transformers", "neural network",
    "prompt", "langchain", "hugging face",
]

# ============================================================
# FUNÇÕES
# ============================================================

def carregar_caged(caminho):
    series = []
    with open(caminho, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            series.append({
                "mes": row["ano_mes"].strip(),
                "saldo": int(row["saldo_liquido"].strip()),
            })
    series.sort(key=lambda x: x["mes"])
    return series


def buscar_lote(pytrends, termos, geo="BR", timeframe="today 5-y"):
    """Busca um lote e retorna dict {termo: [{mes, valor}]}."""
    resultado = {}
    for tentativa in range(5):
        try:
            pytrends.build_payload(termos, timeframe=timeframe, geo=geo)
            df = pytrends.interest_over_time()
            time.sleep(5)  # respeita rate limit

            if df.empty:
                print(f"    ⚠ Sem dados")
                for t in termos:
                    resultado[t] = []
                return resultado

            for termo in termos:
                if termo not in df.columns:
                    resultado[termo] = []
                    continue
                pontos = [
                    {"mes": idx.strftime("%Y-%m"), "valor": int(val)}
                    for idx, val in df[termo].items()
                ]
                resultado[termo] = pontos
                pico = max(p["valor"] for p in pontos) if pontos else 0
                print(f"    ✓ {termo}: {len(pontos)} pontos | pico={pico}")
            return resultado

        except Exception as e:
            print(f"    ⚠ Erro na tentativa {tentativa+1}: {e}")
            time.sleep(15 * (tentativa + 1))
            for t in termos:
                resultado[t] = []
    return resultado


def buscar_todos_trends():
    """Busca todos os lotes separadamente."""
    print("Conectando ao Google Trends...")
    pytrends = TrendReq(hl="pt-BR", tz=180)
    todos = {}

    for nome_lote, termos in LOTES_TRENDS.items():
        print(f"\n  Lote [{nome_lote}]: {termos}")
        resultado = buscar_lote(pytrends, termos)
        todos[nome_lote] = resultado
        time.sleep(4)  # pausa entre lotes

    return todos


def calcular_pct_ia(dados_json):
    """% vagas Adzuna que mencionam IA — usa titulos_vagas se disponível."""
    titulos = dados_json.get("titulos_vagas", [])

    if not titulos:
        total = dados_json["kpis"]["total_vagas"]
        skills_ia = ["Machine Learning", "Inteligência Artificial", "IA", "Deep Learning", "NLP"]
        vagas_ia = sum(s["vagas"] for s in dados_json["top_skills"] if s["skill"] in skills_ia)
        estimado = round((vagas_ia / (total * 2)) * 100, 1)
        return {"total_vagas": total, "vagas_com_ia": vagas_ia,
                "percentual": estimado, "metodo": "estimado_via_skills"}

    total = len(titulos)
    com_ia = sum(
        1 for item in titulos
        if any(p in (item.get("titulo", "") + " " + item.get("descricao", "")).lower()
               for p in PALAVRAS_IA)
    )
    return {
        "total_vagas": total,
        "vagas_com_ia": com_ia,
        "percentual": round(com_ia / total * 100, 1) if total > 0 else 0,
        "metodo": "exato_via_titulos",
    }


def gerar_insights(saldo_antes, saldo_depois, pct_ia, trends_todos):
    """
    Narrativa baseada no que os dados realmente suportam.
    Não atribui contração do mercado à IA — atribui ao ciclo econômico.
    """
    # Pico de interesse em IA solo
    ia_solo = trends_todos.get("ia_solo", {}).get("Inteligência Artificial", [])
    pico_ia = max((p["valor"] for p in ia_solo), default=0)

    # Copilot como proxy de adoção corporativa
    copilot = trends_todos.get("ferramentas_ia", {}).get("GitHub Copilot", [])
    pico_copilot = max((p["valor"] for p in copilot), default=0)

    return [
        f"• O mercado formal de TI contraiu após 2022 — reflexo do ciclo econômico, não destruição por IA",
        f"• Vagas líquidas pré-ChatGPT (jan/22–out/22): {saldo_antes:+,} | pós-ChatGPT (nov/22–hoje): {saldo_depois:+,}",
        f"• {pct_ia['percentual']}% das vagas abertas hoje exigem skills de IA — mercado encolheu, mas quem fica precisa saber IA",
        f"• Interesse em 'Inteligência Artificial' atingiu pico de {pico_ia}/100 no Google Trends BR",
        f"• GitHub Copilot (proxy de adoção corporativa) chegou a {pico_copilot}/100 — adoção real nas empresas",
        f"• A diferença salarial conta a história: Engenheiro de ML (R$13k) vs Analista de Dados (R$6k)",
    ]


# ============================================================
# EXECUÇÃO
# ============================================================

print("=" * 60)
print("ENRIQUECIMENTO IA — Mapa das Profissões")
print("=" * 60)

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
    dados = json.load(f)

# 1. CAGED
print("\n📂 Carregando série temporal CAGED...")
try:
    caged_series = carregar_caged(ARQUIVO_CAGED)
    print(f"   {len(caged_series)} meses ({caged_series[0]['mes']} → {caged_series[-1]['mes']})")
except FileNotFoundError:
    print(f"   ⚠ Não encontrado: {ARQUIVO_CAGED} — copie da pasta gold/ do CAGED")
    caged_series = []

# 2. Trends por lote
print("\n📈 Google Trends (lotes separados)...")
trends_todos = buscar_todos_trends()

# 3. % IA nas vagas
print("\n🤖 Calculando % vagas com IA...")
pct_ia = calcular_pct_ia(dados)
print(f"   {pct_ia['vagas_com_ia']}/{pct_ia['total_vagas']} vagas ({pct_ia['percentual']}%) [{pct_ia['metodo']}]")

# 4. Saldos antes/depois ChatGPT
saldo_antes  = sum(p["saldo"] for p in caged_series if p["mes"] <  MARCO_CHATGPT)
saldo_depois = sum(p["saldo"] for p in caged_series if p["mes"] >= MARCO_CHATGPT)

# 5. Insights narrativos
insights_ia = gerar_insights(saldo_antes, saldo_depois, pct_ia, trends_todos)

# 6. Monta seção
dados["analise_ia"] = {
    "data_atualizacao": date.today().isoformat(),
    "marco_chatgpt": MARCO_CHATGPT,
    "caged_serie": caged_series,
    "trends_lotes": trends_todos,          # estrutura nova por lote
    # compatibilidade com app.py — mantém trends_ia apontando para ia_solo
    "trends_ia": trends_todos.get("ia_solo", {}),
    "pct_vagas_ia": pct_ia,
    "saldo_antes_chatgpt": saldo_antes,
    "saldo_depois_chatgpt": saldo_depois,
    "insights": insights_ia,
}

dados["metadata"]["fontes"] = list(set(
    dados["metadata"].get("fontes", []) + ["CAGED/MTE (série 2022-2026)"]
))

with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

# ============================================================
# RELATÓRIO
# ============================================================

print("\n" + "=" * 60)
print("RESULTADO")
print("=" * 60)
print(f"\n✅ dados_completos.json atualizado")
print(f"   CAGED: {len(caged_series)} meses")
total_pts = sum(
    len(pontos)
    for lote in trends_todos.values()
    for pontos in lote.values()
)
print(f"   Trends: {total_pts} pontos em {len(LOTES_TRENDS)} lotes")
print(f"   % IA vagas: {pct_ia['percentual']}%")
print(f"   Saldo antes ChatGPT: {saldo_antes:+,}")
print(f"   Saldo depois ChatGPT: {saldo_depois:+,}")
print(f"\n💡 Insights gerados:")
for ins in insights_ia:
    print(f"   {ins}")
print(f"\nPróximo passo: python -m streamlit run app.py\n")
