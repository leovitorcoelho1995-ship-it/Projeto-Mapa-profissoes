import os
import requests
import re
from collections import Counter
from dotenv import load_dotenv

load_dotenv()

# Lista de skills para monitorar
SKILLS_LIST = [
    "Python", "SQL", "AWS", "Azure", "GCP", "Java", "JavaScript", "TypeScript",
    "React", "Angular", "Vue", "Node", "Django", "Flask", "FastAPI",
    "Machine Learning", "Inteligência Artificial", "IA", "Data Science",
    "Databricks", "Spark", "Airflow", "Kafka", "Docker", "Kubernetes",
    "Power BI", "Tableau", "Excel", "ETL", "Pipeline", "Git",
    "CI/CD", "Linux", "Terraform", "Snowflake", "dbt", "Pandas",
]

url = "https://api.adzuna.com/v1/api/jobs/br/search/1"
params = {
    "app_id": os.getenv("ADZUNA_APP_ID"),
    "app_key": os.getenv("ADZUNA_API_KEY"),
    "results_per_page": 50,
    "what": "python",
    "max_days_old": 30,
}

print("Buscando vagas...")
response = requests.get(url, params=params)
data = response.json()
vagas = data["results"]

print(f"Analisando {len(vagas)} vagas...\n")

skill_counter = Counter()
total_com_salario = 0
soma_salarios = 0

for vaga in vagas:
    desc = vaga.get("description", "").lower()
    salario = vaga.get("salary_min")
    
    if salario:
        total_com_salario += 1
        soma_salarios += salario

    for skill in SKILLS_LIST:
        if skill.lower() in desc:
            skill_counter[skill] += 1

print("=== TOP SKILLS NAS VAGAS DE TI ===")
for skill, count in skill_counter.most_common(15):
    print(f"{skill:25s} {count} vagas")

if total_com_salario > 0:
    print(f"\nSalário médio (amostra com valores): R${soma_salarios/total_com_salario:,.0f}")