import json
import time
from datetime import date, datetime, timedelta
from pytrends.request import TrendReq

# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_ENTRADA = "dados_snapshot.json"
ARQUIVO_SAIDA = "dados_completos.json"

SALARIOS_REFERENCIA = {
    "Cientista de Dados": {"junior": 6500, "pleno": 11000, "senior": 18000},
    "Engenheiro de Dados": {"junior": 7000, "pleno": 12000, "senior": 19000},
    "Analista de Dados": {"junior": 3500, "pleno": 6000, "senior": 9500},
    "Engenheiro de Machine Learning": {"junior": 7500, "pleno": 13000, "senior": 20000},
    "Desenvolvedor Python": {"junior": 4500, "pleno": 8500, "senior": 14000},
    "Desenvolvedor Java": {"junior": 4500, "pleno": 8500, "senior": 13500},
    "Desenvolvedor JavaScript": {"junior": 4000, "pleno": 7500, "senior": 12000},
    "Desenvolvedor Mobile": {"junior": 4500, "pleno": 8000, "senior": 13000},
    "DevOps": {"junior": 5500, "pleno": 10000, "senior": 16000},
    "Arquiteto de Software": {"junior": 9000, "pleno": 15000, "senior": 22000},
    "Product Manager": {"junior": 7000, "pleno": 12000, "senior": 18000},
    "BI Analyst": {"junior": 4000, "pleno": 7000, "senior": 11000},
    "DBA": {"junior": 4500, "pleno": 8000, "senior": 12000},
    "QA / Testes": {"junior": 3500, "pleno": 6000, "senior": 9500},
    "Segurança da Informação": {"junior": 5000, "pleno": 9000, "senior": 15000},
    "Scrum Master": {"junior": 6000, "pleno": 10000, "senior": 15000},
    "UX/UI Designer": {"junior": 3500, "pleno": 6000, "senior": 10000},
    "Outros": {"junior": 3500, "pleno": 6000, "senior": 10000},
}

# ============================================================
# FUNÇÕES
# ============================================================

def carregar_dados():
    with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
        return json.load(f)


def buscar_trends_5anos(skills, geo="BR"):
    """Busca 5 anos de Google Trends e calcula crescimento anual"""
    print("Conectando ao Google Trends...")
    pytrends = TrendReq(hl='pt-BR', tz=360)
    
    resultados = {}
    
    for i in range(0, len(skills), 5):
        lote = skills[i:i+5]
        print(f"  Buscando: {', '.join(lote)}")
        
        try:
            # 5 anos até hoje
            pytrends.build_payload(lote, timeframe='today 5-y', geo=geo)
            df = pytrends.interest_over_time()
            
            if df.empty:
                print(f"    ⚠ Sem dados")
                for skill in lote:
                    resultados[skill] = {"interesse_atual": 0, "crescimento_5anos": 0, "tendencia": "estável"}
                continue
            
            for skill in lote:
                if skill not in df.columns:
                    resultados[skill] = {"interesse_atual": 0, "crescimento_5anos": 0, "tendencia": "estável"}
                    continue
                
                # Pega o último valor (mês atual)
                valor_atual = int(df[skill].iloc[-1]) if not df.empty else 0
                
                # Pega a média do primeiro ano (primeiros 12 meses)
                primeiro_ano = df[skill].iloc[:12].mean() if len(df) >= 12 else df[skill].mean()
                
                # Calcula crescimento
                if primeiro_ano > 0:
                    crescimento = round(((valor_atual - primeiro_ano) / primeiro_ano) * 100, 1)
                else:
                    crescimento = 0
                
                # Tendência
                if crescimento > 10:
                    tendencia = "📈 Alta"
                elif crescimento < -10:
                    tendencia = "📉 Queda"
                else:
                    tendencia = "➡️ Estável"
                
                resultados[skill] = {
                    "interesse_atual": valor_atual,
                    "crescimento_5anos": crescimento,
                    "tendencia": tendencia
                }
            
            time.sleep(2)
            
        except Exception as e:
            print(f"    ⚠ Erro: {e}")
            for skill in lote:
                resultados[skill] = {"interesse_atual": 0, "crescimento_5anos": 0, "tendencia": "estável"}
    
    return resultados


def estimar_salario_medio(profissao):
    faixas = SALARIOS_REFERENCIA.get(profissao, SALARIOS_REFERENCIA["Outros"])
    return faixas["pleno"]


def recalcular_opportunity_score(skills_enriquecidas):
    if not skills_enriquecidas:
        return []
    
    max_vagas = max(s["vagas"] for s in skills_enriquecidas) if skills_enriquecidas else 1
    
    # Para normalizar crescimento: pega o maior valor absoluto
    max_cresc = max(abs(s["crescimento_5anos"]) for s in skills_enriquecidas) if skills_enriquecidas else 1
    
    scores = []
    for s in skills_enriquecidas:
        score_vagas = (s["vagas"] / max_vagas) * 50
        score_cresc = (s["crescimento_5anos"] / max_cresc) * 35 if max_cresc > 0 else 0
        score_interesse = (s.get("interesse_atual", 0) / 100) * 15
        
        score_total = round(score_vagas + score_cresc + score_interesse, 1)
        
        scores.append({
            "skill": s["skill"],
            "score": min(score_total, 100),
            "vagas": s["vagas"],
            "crescimento_5anos": s["crescimento_5anos"],
            "tendencia": s.get("tendencia", "estável"),
        })
    
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores


# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

print("=" * 60)
print("COLETA COMPLEMENTAR - Trends 5 anos, Salários")
print("=" * 60)
print()

# 1. Carrega dados
print("📂 Carregando dados da coleta anterior...")
dados = carregar_dados()
print(f"   {dados['kpis']['total_vagas']} vagas carregadas")

# 2. Google Trends 5 anos para top 20 skills
print(f"\n📈 Buscando tendências no Google Trends (5 anos)...")
top_skills_nomes = [s["skill"] for s in dados["top_skills"][:20]]
trends_data = buscar_trends_5anos(top_skills_nomes)
print(f"   {len(trends_data)} skills analisadas")

# 3. Enriquece skills
print(f"\n🔄 Combinando dados...")
skills_enriquecidas = []
for skill_item in dados["top_skills"]:
    nome = skill_item["skill"]
    trend = trends_data.get(nome, {"interesse_atual": 0, "crescimento_5anos": 0, "tendencia": "estável"})
    
    skills_enriquecidas.append({
        "skill": nome,
        "vagas": skill_item["vagas"],
        "interesse_atual": trend["interesse_atual"],
        "crescimento_5anos": trend["crescimento_5anos"],
        "tendencia": trend["tendencia"],
    })

# 4. Opportunity Score
print(f"\n🎯 Recalculando Opportunity Scores...")
opportunity_scores = recalcular_opportunity_score(skills_enriquecidas)

# 5. Salários
print(f"\n💰 Calculando salários estimados...")
profissoes_com_salario = []
for prof in dados["top_profissoes"]:
    salario_estimado = estimar_salario_medio(prof["profissao"])
    profissoes_com_salario.append({
        "profissao": prof["profissao"],
        "vagas": prof["vagas"],
        "salario_medio_estimado": salario_estimado,
        "faixa": SALARIOS_REFERENCIA.get(prof["profissao"], SALARIOS_REFERENCIA["Outros"]),
    })

total_vagas_salario = sum(p["vagas"] for p in profissoes_com_salario)
salario_medio_ponderado = 0
if total_vagas_salario > 0:
    salario_medio_ponderado = round(
        sum(p["salario_medio_estimado"] * p["vagas"] for p in profissoes_com_salario) / total_vagas_salario
    )

# 6. Insights
print(f"\n💡 Gerando insights...")
insights = dados.get("insights", [])

if opportunity_scores:
    maior_cresc = max(opportunity_scores, key=lambda x: x["crescimento_5anos"])
    insights.append(f"• {maior_cresc['skill']} é a skill com maior crescimento em 5 anos ({maior_cresc['crescimento_5anos']:+}%)")
    insights.append(f"• {opportunity_scores[0]['skill']} lidera o Opportunity Score combinando demanda atual + tendência de longo prazo")

insights.append(f"• Salário médio estimado do mercado: R${salario_medio_ponderado:,.0f} (baseado em faixas de referência)")

# 7. Arquivo final
print(f"\n📦 Consolidando...")

dados_completos = {
    "metadata": {
        "data_coleta": dados["metadata"]["data_coleta"],
        "data_complemento": date.today().isoformat(),
        "fontes": ["Adzuna API (vagas 30 dias)", "Google Trends (5 anos)", "Tabela de referência salarial BR"],
        "total_vagas_coletadas": dados["metadata"]["total_vagas_coletadas"],
    },
    "kpis": {
        "total_vagas": dados["kpis"]["total_vagas"],
        "skills_unicas": dados["kpis"]["skills_unicas"],
        "profissoes_unicas": dados["kpis"]["profissoes_unicas"],
        "salario_medio_estimado": salario_medio_ponderado,
    },
    "top_skills": skills_enriquecidas,
    "top_profissoes": profissoes_com_salario,
    "opportunity_scores": opportunity_scores,
    "modalidade_trabalho": dados["modalidade_trabalho"],
    "insights": insights,
}

with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados_completos, f, ensure_ascii=False, indent=2)

# ============================================================
# RELATÓRIO
# ============================================================

print("\n" + "=" * 60)
print("RESULTADOS - 5 ANOS DE TENDÊNCIAS")
print("=" * 60)

print(f"\n📈 TOP SKILLS COM TENDÊNCIA 5 ANOS:")
for s in skills_enriquecidas[:12]:
    print(f"   {s['tendencia']} {s['skill']:25s} Vagas: {s['vagas']:3d} | Cresc 5a: {s['crescimento_5anos']:+7.1f}%")

print(f"\n🎯 OPPORTUNITY SCORES:")
for s in opportunity_scores[:8]:
    print(f"   {s['skill']:25s} Score: {s['score']:5.1f} | Cresc 5a: {s['crescimento_5anos']:+7.1f}% | {s['tendencia']}")

print(f"\n💰 TOP SALÁRIOS ESTIMADOS:")
for p in profissoes_com_salario[:10]:
    print(f"   {p['profissao']:30s} R$ {p['salario_medio_estimado']:>6,.0f} (pleno) | {p['vagas']} vagas")

print(f"\n🏢 MODALIDADE:")
for mod, d in dados["modalidade_trabalho"].items():
    if d["vagas"] > 0:
        print(f"   {mod:20s} {d['vagas']:4d} vagas ({d['percentual']:5.1f}%)")

print(f"\n💡 INSIGHTS:")
for insight in insights:
    print(f"   {insight}")

print(f"\n✅ Dados completos salvos em: {ARQUIVO_SAIDA}\n")