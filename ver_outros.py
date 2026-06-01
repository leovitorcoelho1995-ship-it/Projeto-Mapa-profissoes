import json

with open("dados_snapshot.json", "r", encoding="utf-8") as f:
    dados = json.load(f)

from collections import Counter
titulos_outros = []

for vaga in dados["titulos_vagas"]:
    titulo = vaga["titulo"].lower()
    
    # Mesma lógica do coleta.py
    categorias = {
        "Cientista de Dados": ["cientista de dados", "data scientist", "data science"],
        "Engenheiro de Dados": ["engenheiro de dados", "data engineer", "engenharia de dados"],
        "Analista de Dados": ["analista de dados", "data analyst", "analytics"],
        "Engenheiro de Machine Learning": ["machine learning engineer", "ml engineer", "mlops"],
        "Desenvolvedor Python": ["python developer", "desenvolvedor python"],
        "Desenvolvedor Java": ["java developer", "desenvolvedor java"],
        "Desenvolvedor JavaScript": ["javascript developer", "desenvolvedor javascript", "frontend", "front-end", "full stack", "fullstack"],
        "Desenvolvedor Mobile": ["mobile developer", "desenvolvedor mobile", "android", "ios", "flutter", "react native"],
        "DevOps": ["devops", "dev ops", "infraestrutura", "infrastructure", "sre", "cloud engineer"],
        "Arquiteto de Software": ["arquiteto de software", "software architect", "tech lead"],
        "Product Manager": ["product manager", "gerente de produto", "product owner"],
        "BI Analyst": ["bi analyst", "analista de bi", "business intelligence", "power bi", "tableau"],
        "DBA": ["dba", "database administrator", "administrador de banco"],
        "QA / Testes": ["qa", "quality assurance", "teste", "tester", "quality engineer"],
        "Segurança da Informação": ["segurança da informação", "security", "cybersecurity", "infosec"],
        "Scrum Master": ["scrum master", "agile coach"],
        "UX/UI Designer": ["ux", "ui", "user experience", "designer", "product designer"],
    }
    
    encontrado = False
    for categoria, keywords in categorias.items():
        for kw in keywords:
            if kw in titulo:
                encontrado = True
                break
        if encontrado:
            break
    
    if not encontrado:
        titulos_outros.append(vaga["titulo"])

# Mostra os 30 títulos mais comuns em "Outros"
contagem = Counter(titulos_outros)
print("Títulos classificados como 'Outros':\n")
for titulo, qtd in contagem.most_common(30):
    print(f"  {qtd}x - {titulo}")