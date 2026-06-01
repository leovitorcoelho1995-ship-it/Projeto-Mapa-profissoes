import os
import requests
import re
from collections import Counter
from datetime import date, datetime, timedelta
import json
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# CONFIGURAÇÕES
# ============================================================

TERMOS_BUSCA = [
    "python",
    "dados",
    "inteligência artificial",
    "machine learning",
    "cloud",
    "aws",
    "azure",
    "devops",
    "full stack",
    "backend",
    "frontend",
    "mobile",
    "engenharia de software",
    "analista de dados",
    "cientista de dados",
    "engenheiro de dados",
    "business intelligence",
    "sql",
    "java",
    "javascript",
]

SKILLS_LIST = [
    "Python", "SQL", "Java", "JavaScript", "TypeScript", "C#", "Go", "Rust",
    "Scala", "R", "PHP", "Ruby", "Kotlin", "Swift",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Linux",
    "CI/CD", "Jenkins", "GitHub Actions", "Git",
    "Spark", "Databricks", "Airflow", "Kafka", "Snowflake", "dbt",
    "Machine Learning", "Deep Learning", "NLP", "Computer Vision",
    "Inteligência Artificial", "IA", "Data Science", "Big Data",
    "ETL", "Pipeline", "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
    "PyTorch", "Power BI", "Tableau", "Looker", "Excel",
    "Django", "Flask", "FastAPI", "Spring", "Node", "Express",
    ".NET", "REST", "GraphQL", "gRPC", "Microsserviços",
    "React", "Angular", "Vue", "Next.js", "HTML", "CSS",
    "React Native", "Flutter", "iOS", "Android",
    "Agile", "Scrum", "Kanban", "TDD",
]

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_API_KEY")
RESULTADOS_POR_BUSCA = 50
MAX_DIAS = 30

ARQUIVO_SAIDA = "dados_snapshot.json"

# ============================================================
# FUNÇÕES
# ============================================================

def buscar_vagas(termo):
    url = f"https://api.adzuna.com/v1/api/jobs/br/search/1"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": RESULTADOS_POR_BUSCA,
        "what": termo,
        "max_days_old": MAX_DIAS,
    }
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"  Erro ao buscar '{termo}': {e}")
        return []


def extrair_skills(descricao):
    desc = descricao.lower() if descricao else ""
    skills_encontradas = []
    for skill in SKILLS_LIST:
        if re.search(r'\b' + re.escape(skill.lower()) + r'\b', desc):
            skills_encontradas.append(skill)
    return skills_encontradas


def categorizar_profissao(titulo):
    t = titulo.lower()
    
    # Machine Learning / IA (checar antes de Python e Dados)
    if any(kw in t for kw in ["machine learning", "inteligência artificial", "inteligencia artificial", "ia ", " ia", "(ia)", "mlops", "ml engineer"]):
        if any(kw in t for kw in ["engenheiro", "engenharia", "engineer"]):
            return "Engenheiro de Machine Learning"
        if any(kw in t for kw in ["especialista", "cientista", "scientist", "pesquisador"]):
            return "Cientista de Dados"
        if any(kw in t for kw in ["analista", "analytics"]):
            return "Analista de Dados"
        return "Cientista de Dados"  # default para IA/ML
    
    # Engenharia de Dados
    if any(kw in t for kw in ["engenheiro de dados", "engenharia de dados", "data engineer"]):
        return "Engenheiro de Dados"
    
    # Cientista de Dados
    if any(kw in t for kw in ["cientista de dados", "data scientist", "data science"]):
        return "Cientista de Dados"
    
    # Analista de Dados / BI
    if any(kw in t for kw in ["analista de dados", "data analyst", "analytics", "analista de bi", "business intelligence", "power bi", "tableau", "looker"]):
        if any(kw in t for kw in ["power bi", "tableau", "looker", "bi", "business intelligence"]):
            return "BI Analyst"
        return "Analista de Dados"
    
    # Cloud / Infra / DevOps
    if any(kw in t for kw in ["cloud engineer", "cloud practitioner", "aws", "azure", "gcp", "cloud architect"]):
        if any(kw in t for kw in ["especialista", "tutor", "instrutor", "consultant"]):
            return "DevOps"
        return "DevOps"
    
    # DevOps / SRE
    if any(kw in t for kw in ["devops", "dev ops", "sre", "infraestrutura", "infrastructure", "infra"]):
        return "DevOps"
    
    # Backend (checar antes de linguagens específicas)
    if any(kw in t for kw in ["backend", "back-end", "back end"]):
        if "python" in t:
            return "Desenvolvedor Python"
        if "java" in t:
            return "Desenvolvedor Java"
        if any(kw in t for kw in ["javascript", "node", "typescript"]):
            return "Desenvolvedor JavaScript"
        return "Desenvolvedor JavaScript"  # default backend
    
    # Python
    if any(kw in t for kw in ["python", "django", "flask", "fastapi"]):
        return "Desenvolvedor Python"
    
    # Java
    if any(kw in t for kw in ["java ", "java developer", "spring"]):
        return "Desenvolvedor Java"
    
    # JavaScript / Frontend / Fullstack
    if any(kw in t for kw in ["javascript", "frontend", "front-end", "full stack", "fullstack", "node", "react", "angular", "vue", "typescript", "next.js"]):
        return "Desenvolvedor JavaScript"
    
    # Mobile
    if any(kw in t for kw in ["mobile", "android", "ios", "flutter", "react native", "videomaker mobile"]):
        return "Desenvolvedor Mobile"
    
    # Arquiteto / Tech Lead
    if any(kw in t for kw in ["arquiteto", "architect", "tech lead", "coordenador", "coordenador(a)"]):
        return "Arquiteto de Software"
    
    # Product
    if any(kw in t for kw in ["product manager", "product owner", "gerente de produto"]):
        return "Product Manager"
    
    # QA
    if any(kw in t for kw in ["qa", "quality assurance", "teste", "tester", "quality engineer"]):
        return "QA / Testes"
    
    # DBA
    if any(kw in t for kw in ["dba", "database administrator", "administrador de banco"]):
        return "DBA"
    
    # Segurança
    if any(kw in t for kw in ["segurança", "security", "cybersecurity", "infosec"]):
        return "Segurança da Informação"
    
    # Scrum
    if any(kw in t for kw in ["scrum master", "agile coach"]):
        return "Scrum Master"
    
    # UX/UI
    if any(kw in t for kw in ["ux", "ui", "user experience", "product designer"]):
        return "UX/UI Designer"
    
    # Salesforce
    if any(kw in t for kw in ["salesforce", "genesys"]):
        return "DevOps"
    
    # Analista de Sistemas / Suporte (genérico de TI)
    if any(kw in t for kw in ["analista de sistemas", "analista de suporte", "analista programador"]):
        return "Analista de Dados"
    
    return "Outros"


def classificar_modalidade(titulo, descricao=""):
    texto = (titulo + " " + descricao).lower()
    remoto = any(kw in texto for kw in ["remoto", "remote", "home office", "home-office", "trabalho remoto"])
    presencial = any(kw in texto for kw in ["presencial", "on-site", "onsite"])
    hibrido = any(kw in texto for kw in ["hibrido", "híbrido", "hybrid", "flexível", "flexivel"])
    if hibrido:
        return "Híbrido"
    elif remoto and not presencial:
        return "Remoto"
    elif presencial and not remoto:
        return "Presencial"
    elif remoto and presencial:
        return "Híbrido"
    else:
        return "Não especificado"


# ============================================================
# COLETA PRINCIPAL
# ============================================================

print("=" * 60)
print("MAPA DAS PROFISSÕES DO FUTURO - COLETA DE DADOS")
print("=" * 60)
print()

hoje = date.today().isoformat()
print(f"Data da coleta: {hoje}")
print(f"Termos de busca: {len(TERMOS_BUSCA)}")
print()

todas_vagas = {}
vagas_por_termo = {}
titulos_vagas = []  # NOVO: guarda títulos para análise de modalidade

for termo in TERMOS_BUSCA:
    print(f"Buscando: '{termo}'...")
    vagas = buscar_vagas(termo)
    vagas_por_termo[termo] = len(vagas)
    
    for vaga in vagas:
        vaga_id = vaga.get("id")
        if vaga_id and vaga_id not in todas_vagas:
            todas_vagas[vaga_id] = vaga
            titulos_vagas.append({
                "titulo": vaga.get("title", ""),
                "descricao": vaga.get("description", "")[:200]
            })
    
    print(f"  → {len(vagas)} vagas encontradas")

total_vagas = len(todas_vagas)
print(f"\nTotal de vagas únicas coletadas: {total_vagas}")

# ============================================================
# ANÁLISE DAS VAGAS
# ============================================================

print("\nAnalisando skills, profissões, salários e modalidade...")

skill_counter = Counter()
profissao_counter = Counter()
salarios = []
vagas_com_salario = 0
modalidades = {"Remoto": 0, "Presencial": 0, "Híbrido": 0, "Não especificado": 0}

for vaga_id, vaga in todas_vagas.items():
    titulo = vaga.get("title", "")
    descricao = vaga.get("description", "")
    salario_min = vaga.get("salary_min")
    
    skills = extrair_skills(descricao)
    skill_counter.update(skills)
    
    profissao = categorizar_profissao(titulo)
    profissao_counter[profissao] += 1
    
    if salario_min and salario_min > 0:
        salarios.append(salario_min)
        vagas_com_salario += 1
    
    # NOVO: classifica modalidade
    mod = classificar_modalidade(titulo, descricao)
    modalidades[mod] += 1

# ============================================================
# MÉTRICAS CONSOLIDADAS
# ============================================================

top_skills = skill_counter.most_common(30)
skills_dict = [{"skill": s, "vagas": c} for s, c in top_skills]
skills_unicas = len([s for s, c in skill_counter.items() if c > 0])

top_profissoes = profissao_counter.most_common(20)
profissoes_dict = [{"profissao": p, "vagas": c} for p, c in top_profissoes]
profissoes_unicas = len(profissao_counter)

salario_medio = sum(salarios) / len(salarios) if salarios else 0

# Modalidade em percentual
total_modalidades = sum(modalidades.values())
modalidade_percent = {}
for mod, count in modalidades.items():
    modalidade_percent[mod] = {
        "vagas": count,
        "percentual": round((count / total_modalidades * 100), 1) if total_modalidades > 0 else 0
    }

max_vagas_skill = top_skills[0][1] if top_skills else 1
opportunity_scores = []
for skill, vagas in top_skills[:15]:
    score_volume = (vagas / max_vagas_skill) * 100
    opportunity_scores.append({
        "skill": skill,
        "score": round(score_volume, 1),
        "vagas": vagas
    })

insights = []
if top_skills:
    insights.append(f"• {top_skills[0][0]} é a skill mais requisitada, presente em {top_skills[0][1]} vagas")
if len(top_skills) >= 3:
    insights.append(f"• {top_skills[1][0]} e {top_skills[2][0]} completam o top 3 de skills mais pedidas")
if top_profissoes:
    insights.append(f"• {top_profissoes[0][0]} lidera em volume de vagas abertas ({top_profissoes[0][1]} vagas)")
insights.append(f"• Foram identificadas {skills_unicas} skills técnicas diferentes nas descrições das vagas")
if vagas_com_salario > 10:
    insights.append(f"• Salário médio das vagas com valor informado: R${salario_medio:,.0f} (amostra de {vagas_com_salario} vagas)")
else:
    insights.append(f"• Apenas {vagas_com_salario} vagas informaram salário — a maioria das empresas não divulga valores")
if len(top_profissoes) >= 5:
    insights.append(f"• Profissões em destaque: {top_profissoes[0][0]}, {top_profissoes[1][0]} e {top_profissoes[2][0]}")
remoto_pct = modalidade_percent.get("Remoto", {}).get("percentual", 0)
if remoto_pct > 0:
    insights.append(f"• {remoto_pct}% das vagas mencionam trabalho remoto")

dados = {
    "metadata": {
        "data_coleta": hoje,
        "fonte": "Adzuna API",
        "total_vagas_coletadas": total_vagas,
        "periodo_dias": MAX_DIAS,
        "termos_busca": TERMOS_BUSCA,
    },
    "kpis": {
        "total_vagas": total_vagas,
        "skills_unicas": skills_unicas,
        "profissoes_unicas": profissoes_unicas,
        "salario_medio": round(salario_medio, 2),
        "vagas_com_salario": vagas_com_salario,
    },
    "top_skills": skills_dict,
    "top_profissoes": profissoes_dict,
    "opportunity_scores": opportunity_scores,
    "modalidade_trabalho": modalidade_percent,
    "insights": insights,
    "vagas_por_termo": vagas_por_termo,
    "titulos_vagas": titulos_vagas,
}

with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("\n" + "=" * 60)
print("RESULTADOS DA COLETA")
print("=" * 60)

print(f"\n📊 KPIs:")
print(f"   Vagas únicas: {total_vagas}")
print(f"   Skills distintas: {skills_unicas}")
print(f"   Profissões distintas: {profissoes_unicas}")
print(f"   Salário médio: R${salario_medio:,.0f} ({vagas_com_salario} vagas com salário)")

print(f"\n🔥 TOP 10 SKILLS:")
for i, (skill, count) in enumerate(top_skills[:10], 1):
    barra = "█" * (count // 5)
    print(f"   {i:2d}. {skill:25s} {barra} ({count})")

print(f"\n💼 TOP 10 PROFISSÕES:")
for i, (prof, count) in enumerate(top_profissoes[:10], 1):
    print(f"   {i:2d}. {prof:30s} {count} vagas")

print(f"\n🏢 MODALIDADE DE TRABALHO:")
for mod, dados_mod in modalidade_percent.items():
    print(f"   {mod:20s} {dados_mod['vagas']:4d} vagas ({dados_mod['percentual']:5.1f}%)")

print(f"\n✅ Dados salvos em: {ARQUIVO_SAIDA}\n")