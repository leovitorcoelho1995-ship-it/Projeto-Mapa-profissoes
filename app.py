import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mapa das Profissões do Futuro",
    page_icon="🧭",
    layout="wide"
)

# ============================================================
# CARREGAR DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    with open("dados_completos.json", "r", encoding="utf-8") as f:
        return json.load(f)

dados = carregar_dados()

# ============================================================
# CABEÇALHO
# ============================================================

st.title("🧭 Mapa das Profissões do Futuro")
st.caption(f"Última coleta: {dados['metadata']['data_coleta']} | Fontes: {', '.join(dados['metadata']['fontes'])}")

st.markdown("---")

# ============================================================
# KPIs
# ============================================================

kpi = dados["kpis"]

col1, col2, col3, col4 = st.columns(4)
col1.metric("📊 Vagas", f"{kpi['total_vagas']:,}")
col2.metric("🔧 Skills", kpi["skills_unicas"])
col3.metric("💼 Profissões", kpi["profissoes_unicas"])
col4.metric("💰 Salário Médio", f"R${kpi['salario_medio_estimado']:,.0f}")

st.markdown("---")

# ============================================================
# LINHA 1: TOP CRESCIMENTO + OPPORTUNITY SCORE
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Top Crescimento (5 anos)")
    
    # Pega top 8 skills por crescimento
    top_cresc = sorted(dados["top_skills"], key=lambda x: x["crescimento_5anos"], reverse=True)[:8]
    
    df_cresc = pd.DataFrame(top_cresc)
    df_cresc = df_cresc[df_cresc["skill"] != "IA"]  # IA distorce o gráfico
    
    fig = px.bar(
        df_cresc,
        x="skill",
        y="crescimento_5anos",
        color="crescimento_5anos",
        color_continuous_scale=["red", "yellow", "green"],
        labels={"crescimento_5anos": "Crescimento (%)", "skill": ""},
        text_auto="+.1f%"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🎯 Opportunity Score")
    
    df_score = pd.DataFrame(dados["opportunity_scores"][:8])
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_score["skill"][::-1],
        x=df_score["score"][::-1],
        orientation="h",
        marker=dict(
            color=df_score["score"][::-1],
            colorscale="blues",
            showscale=False
        ),
        text=df_score["score"][::-1].apply(lambda x: f"{x:.0f}"),
        textposition="outside"
    ))
    fig.update_layout(height=350, xaxis_title="Score (0-100)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# LINHA 2: TOP SKILLS + TOP PROFISSÕES
# ============================================================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Skills Mais Demandadas")
    
    df_skills = pd.DataFrame(dados["top_skills"][:10])
    
    fig = px.bar(
        df_skills,
        x="vagas",
        y="skill",
        orientation="h",
        color="vagas",
        color_continuous_scale="oranges",
        labels={"vagas": "Vagas", "skill": ""},
        text="vagas"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=False, height=350, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("💼 Profissões em Alta")
    
    df_prof = pd.DataFrame(dados["top_profissoes"][:10])
    
    fig = px.bar(
        df_prof,
        x="vagas",
        y="profissao",
        orientation="h",
        color="salario_medio_estimado",
        color_continuous_scale="greens",
        labels={"vagas": "Vagas", "profissao": "", "salario_medio_estimado": "Salário (R$)"},
        text="vagas"
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(showlegend=True, height=350, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# LINHA 3: EVOLUÇÃO DE SKILLS + MODALIDADE
# ============================================================

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📊 Salários por Profissão")
    
    df_sal = pd.DataFrame(dados["top_profissoes"][:10])
    df_sal["faixa_texto"] = df_sal["faixa"].apply(
        lambda f: f"Jr: R${f['junior']:,} | Pl: R${f['pleno']:,} | Sr: R${f['senior']:,}"
    )
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sal["profissao"][::-1],
        x=df_sal["salario_medio_estimado"][::-1],
        orientation="h",
        marker=dict(color=df_sal["salario_medio_estimado"][::-1], colorscale="viridis", showscale=False),
        text=df_sal["salario_medio_estimado"][::-1].apply(lambda x: f"R${x:,.0f}"),
        textposition="outside",
        hovertemplate=df_sal["faixa_texto"][::-1]
    ))
    fig.update_layout(height=350, xaxis_title="Salário Médio (Pleno)", yaxis_title="")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🏢 Modalidade")
    
    mod_data = dados["modalidade_trabalho"]
    df_mod = pd.DataFrame([
        {"Modalidade": k, "Vagas": v["vagas"], "%": v["percentual"]}
        for k, v in mod_data.items()
    ])
    
    fig = px.pie(
        df_mod,
        names="Modalidade",
        values="Vagas",
        color="Modalidade",
        color_discrete_map={
            "Remoto": "#2ecc71",
            "Presencial": "#e74c3c",
            "Híbrido": "#f39c12",
            "Não especificado": "#bdc3c7"
        },
        hole=0.5
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# LINHA 4: TABELA COMPLETA + INSIGHTS
# ============================================================

col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📋 Tabela Completa de Skills")
    
    df_tabela = pd.DataFrame(dados["top_skills"])
    df_tabela.columns = ["Skill", "Vagas", "Interesse", "Cresc. 5a", "Tendência"]
    df_tabela = df_tabela[["Skill", "Vagas", "Cresc. 5a", "Tendência"]]
    
    # Formata crescimento
    df_tabela["Cresc. 5a"] = df_tabela["Cresc. 5a"].apply(lambda x: f"{x:+.1f}%")
    
    st.dataframe(
        df_tabela,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Skill": st.column_config.TextColumn("Skill", width="medium"),
            "Vagas": st.column_config.NumberColumn("Vagas", width="small"),
            "Cresc. 5a": st.column_config.TextColumn("Cresc. 5 anos", width="small"),
            "Tendência": st.column_config.TextColumn("Tendência", width="small"),
        }
    )

with col2:
    st.subheader("💡 Insights")
    
    for insight in dados["insights"]:
        st.markdown(insight)
    
    st.markdown("---")
    st.subheader("ℹ️ Sobre")
    st.markdown(f"""
    **Fontes de dados:**
    - Vagas: Adzuna API (Brasil)
    - Tendências: Google Trends (5 anos)
    - Salários: Tabela de referência (Glassdoor/Catho)
    
    **Metodologia:**
    - {dados['metadata']['total_vagas_coletadas']} vagas analisadas
    - Skills extraídas das descrições
    - Opportunity Score = demanda + crescimento
    
    **Atualização:** Snapshot de {dados['metadata']['data_coleta']}
    """)

# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")
st.caption("🧭 Mapa das Profissões do Futuro — Projeto de análise de dados do mercado de TI brasileiro")