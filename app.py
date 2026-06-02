import streamlit as st
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mapa das Profissões do Futuro",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Syne', system-ui, sans-serif !important; background-color: #f5f2ed !important; color: #0c0c0d !important; font-size: 1.1rem; font-weight: 500; }
.block-container { padding-top: 2rem !important; padding-bottom: 4rem !important; max-width: 95% !important; }
.hero-block { padding: 3rem 0 2rem 0; border-bottom: 1px solid #d9d4cc; margin-bottom: 2.5rem; }
.hero-eyebrow { font-family: 'DM Mono', monospace; font-size: 13px; color: #7a7570; letter-spacing: .1em; text-transform: uppercase; display: flex; align-items: center; gap: .6rem; margin-bottom: 1rem; }
.hero-eyebrow::before { content: ''; display: inline-block; width: 24px; height: 1px; background: #0d7a5f; }
.hero-title { font-family: 'DM Serif Display', Georgia, serif; font-size: clamp(2.4rem, 5vw, 3.8rem); line-height: 1.08; letter-spacing: -.01em; color: #0c0c0d; margin-bottom: .75rem; }
.hero-title em { font-style: italic; color: #0d7a5f; }
.hero-lead { font-size: 1.22rem; font-weight: 500; color: #5f5a55; line-height: 1.85; max-width: 680px; }
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; margin-bottom: 2.5rem; }
.kpi-card { background: #ede9e2; border: 1px solid #d9d4cc; border-radius: 8px; padding: 1.1rem 1.25rem; }
.kpi-val { font-family: 'DM Serif Display', serif; font-size: 2.3rem; line-height: 1; color: #0c0c0d; }
.kpi-money-number { font-family: 'Syne', sans-serif; font-size: 1.65rem; font-weight: 700; color: #0d7a5f; }
.kpi-label { font-family: 'DM Mono', monospace; font-size: 12px; color: #7a7570; text-transform: uppercase; letter-spacing: .07em; margin-top: .3rem; }
.section-header { display: flex; align-items: baseline; gap: .75rem; margin-bottom: 1.5rem; margin-top: 2.5rem; padding-bottom: .75rem; border-bottom: 1px solid #d9d4cc; }
.section-num { font-family: 'DM Mono', monospace; font-size: 13px; color: #7a7570; letter-spacing: .08em; }
.section-title { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #0c0c0d; }
.section-title em { font-style: italic; color: #0d7a5f; }
.ia-hero { background: #0c0c0d; border-radius: 12px; padding: 2.5rem; margin: 2rem 0; position: relative; overflow: hidden; }
.ia-hero::before { content: ''; position: absolute; top: -60px; right: -60px; width: 260px; height: 260px; border-radius: 50%; background: radial-gradient(circle, rgba(13,122,95,.35) 0%, transparent 70%); }
.ia-hero-eyebrow { font-family: 'DM Mono', monospace; font-size: 11px; color: #0d7a5f; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .75rem; }
.ia-hero-title { font-family: 'DM Serif Display', serif; font-size: clamp(1.8rem, 3.5vw, 2.8rem); color: #f5f2ed; line-height: 1.12; margin-bottom: 1rem; }
.ia-hero-title em { color: #4ade80; font-style: italic; }
.ia-hero-sub { font-family: 'Syne', sans-serif; font-size: .95rem; color: #7a7570; line-height: 1.7; max-width: 540px; }
.ia-stats-row { display: flex; gap: 1.5rem; margin-top: 1.75rem; flex-wrap: wrap; }
.ia-stat { background: rgba(245,242,237,.07); border: 1px solid rgba(245,242,237,.12); border-radius: 8px; padding: .9rem 1.25rem; min-width: 140px; }
.ia-stat-val { font-family: 'DM Serif Display', serif; font-size: 1.8rem; color: #4ade80; line-height: 1; }
.ia-stat-label { font-family: 'DM Mono', monospace; font-size: 10px; color: #7a7570; text-transform: uppercase; letter-spacing: .07em; margin-top: .25rem; }
.annotation { background: #ede9e2; border-left: 3px solid #0d7a5f; border-radius: 0 6px 6px 0; padding: 1.1rem 1.35rem; margin: 1.5rem 0; font-size: 1.08rem; font-weight: 500; color: #2f2d2a; line-height: 1.8; }
.insight-list { display: flex; flex-direction: column; gap: .5rem; }
.insight-item { background: #ede9e2; border: 1px solid #d9d4cc; border-radius: 6px; padding: .95rem 1.15rem; font-size: 1.04rem; font-weight: 500; color: #0c0c0d; line-height: 1.65; }
.divider { height: 1px; background: #d9d4cc; margin: 2.5rem 0; }
.footer-bar { border-top: 1px solid #d9d4cc; padding-top: 1.5rem; margin-top: 3rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: .5rem; }
.footer-name { font-family: 'DM Mono', monospace; font-size: 13px; color: #7a7570; }
.footer-tag { font-family: 'DM Mono', monospace; font-size: 12px; color: #0d7a5f; background: rgba(13,122,95,.1); border: 1px solid rgba(13,122,95,.2); padding: 3px 9px; border-radius: 3px; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# PALETA E HELPERS
# ============================================================

COR_PRINCIPAL  = "#0d7a5f"
COR_SECUNDARIA = "#4ade80"
COR_ACCENT     = "#c0392b"
COR_MUTED      = "#7a7570"
COR_INK        = "#0c0c0d"

LAYOUT_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Syne, system-ui", color=COR_INK, size=12),
    margin=dict(l=0, r=20, t=20, b=0),
)

TICK_FONT  = dict(family="DM Mono, monospace", size=13, color=COR_MUTED)
LABEL_FONT = dict(family="DM Mono, monospace", size=14, color=COR_MUTED)

def marca_chatgpt(fig):
    """Adiciona linha vertical e anotação do ChatGPT sem usar add_vline (incompatível com Python 3.14)."""
    fig.add_shape(
        type="line",
        x0="2022-11-01", x1="2022-11-01",
        y0=0, y1=1,
        xref="x", yref="paper",
        line=dict(color=COR_ACCENT, width=1.5, dash="dot"),
    )
    fig.add_annotation(
        x="2022-11-01", y=0.97,
        xref="x", yref="paper",
        text="ChatGPT ↑",
        showarrow=False,
        font=dict(family="DM Mono, monospace", size=11, color=COR_ACCENT),
        xanchor="left",
    )
    return fig

# ============================================================
# DADOS
# ============================================================

@st.cache_data
def carregar_dados():
    with open("dados_completos.json", "r", encoding="utf-8") as f:
        return json.load(f)

dados = carregar_dados()
tem_ia = "analise_ia" in dados

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero-block">
  <div class="hero-eyebrow">Análise de Mercado · Brasil · 2026</div>
  <div class="hero-title">Mapa das <em>Profissões</em><br>do Futuro</div>
  <div class="hero-lead">912 vagas reais analisadas. Google Trends de 5 anos. CAGED/MTE 2022-2025.<br>
  O que o mercado de TI brasileiro está pedindo - e para onde está indo.</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# KPIs
# ============================================================

kpi = dados["kpis"]
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card"><div class="kpi-val">{kpi['total_vagas']:,}</div><div class="kpi-label">Vagas analisadas</div></div>
  <div class="kpi-card"><div class="kpi-val">{kpi['skills_unicas']}</div><div class="kpi-label">Skills distintas</div></div>
  <div class="kpi-card"><div class="kpi-val">{kpi['profissoes_unicas']}</div><div class="kpi-label">Profissões mapeadas</div></div>
  <div class="kpi-card"><div class="kpi-val">R$<span class="kpi-money-number">{kpi['salario_medio_estimado']:,.0f}</span></div><div class="kpi-label">Salário médio estimado</div></div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# SECAO 1 - IMPACTO DA IA
# ============================================================

if tem_ia:
    ia = dados["analise_ia"]
    pct_ia      = ia["pct_vagas_ia"]["percentual"]
    saldo_antes  = ia["saldo_antes_chatgpt"]
    saldo_depois = ia["saldo_depois_chatgpt"]

    st.markdown(f"""
    <div class="ia-hero">
      <div class="ia-hero-eyebrow">01 - Impacto da IA no Mercado de TI</div>
      <div class="ia-hero-title">O mercado esfriou.<br>O interesse em <em>IA explodiu</em>.</div>
      <div class="ia-hero-sub">
        Desde o lançamento do ChatGPT em novembro de 2022, o número de vagas formais em TI
        entrou em contração - enquanto a demanda por skills de IA não para de crescer.
      </div>
      <div class="ia-stats-row">
        <div class="ia-stat"><div class="ia-stat-val">+2075%</div><div class="ia-stat-label">Interesse em IA (5 anos)</div></div>
        <div class="ia-stat"><div class="ia-stat-val">{pct_ia}%</div><div class="ia-stat-label">Vagas mencionam IA hoje</div></div>
        <div class="ia-stat"><div class="ia-stat-val">{saldo_depois:+,}</div><div class="ia-stat-label">Vagas líquidas pós-ChatGPT</div></div>
        <div class="ia-stat"><div class="ia-stat-val">{saldo_antes:+,}</div><div class="ia-stat-label">Vagas líquidas pré-ChatGPT</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # --- 01.1 Dual-axis CAGED + Trends ---
    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("""
        <div class="section-header">
          <span class="section-num">01.1</span>
          <span class="section-title">Vagas de TI x Interesse em <em>IA</em></span>
        </div>
        """, unsafe_allow_html=True)

        df_caged = pd.DataFrame(ia["caged_serie"])
        df_caged["mes_dt"] = pd.to_datetime(df_caged["mes"])

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_caged["mes_dt"],
            y=df_caged["saldo"],
            name="Vagas líquidas TI (CAGED)",
            line=dict(color=COR_PRINCIPAL, width=2.5),
            fill="tozeroy",
            fillcolor="rgba(13,122,95,0.08)",
            hovertemplate="<b>%{x|%b/%Y}</b><br>Vagas: %{y:+,}<extra></extra>",
        ))

        trends = ia.get("trends_ia", {})
        if "Inteligência Artificial" in trends and trends["Inteligência Artificial"]:
            df_tr = pd.DataFrame(trends["Inteligência Artificial"])
            df_tr["mes_dt"] = pd.to_datetime(df_tr["mes"])
            fig.add_trace(go.Scatter(
                x=df_tr["mes_dt"],
                y=df_tr["valor"],
                name="Interesse: IA (Google Trends)",
                line=dict(color=COR_SECUNDARIA, width=2, dash="dot"),
                yaxis="y2",
                hovertemplate="<b>%{x|%b/%Y}</b><br>Interesse: %{y}<extra></extra>",
            ))

        marca_chatgpt(fig)

        fig.update_layout(
            **LAYOUT_BASE,
            height=380,
            yaxis=dict(
                title=dict(text="Vagas líquidas por mês", font=LABEL_FONT),
                tickfont=TICK_FONT,
                gridcolor="#d9d4cc",
                zeroline=True, zerolinecolor="#d9d4cc",
            ),
            yaxis2=dict(
                title=dict(text="Interesse relativo (Google Trends)", font=dict(family="DM Mono, monospace", size=11, color=COR_SECUNDARIA)),
                tickfont=dict(family="DM Mono, monospace", size=10, color=COR_SECUNDARIA),
                overlaying="y", side="right",
                showgrid=False, range=[0, 120],
            ),
            xaxis=dict(gridcolor="#d9d4cc", tickfont=TICK_FONT),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        font=dict(family="DM Mono, monospace", size=11)),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("""
        <div class="section-header" style="margin-top:2.5rem">
          <span class="section-num">01.2</span>
          <span class="section-title" style="font-size:1.1rem">Insights</span>
        </div>
        """, unsafe_allow_html=True)
        html_ins = "".join(
            f'<div class="insight-item">{i.lstrip("• ")}</div>'
            for i in ia.get("insights", [])
        )
        st.markdown(f'<div class="insight-list">{html_ins}</div>', unsafe_allow_html=True)

    # --- 01.3 Trends por lote ---
    trends_lotes = ia.get("trends_lotes", {})

    CONFIGS_LOTES = [
        {
            "chave": "skills_trabalho",
            "titulo": "Skills de IA no <em>mercado de trabalho</em>",
            "subtitulo": "Demanda por perfis técnicos de IA - proxy de interesse profissional, não curiosidade geral",
            "cores": ["#064e3b", "#10b981", "#6ee7b7"],
        },
        {
            "chave": "ferramentas_ia",
            "titulo": "Ferramentas de IA no <em>ambiente corporativo</em>",
            "subtitulo": "Adoção real de ferramentas nas empresas - ChatGPT no trabalho, Copilot, Gemini, Claude",
            "cores": ["#fcd34d", "#f59e0b", "#b45309", "#78350f"],
        },
        {
            "chave": "demanda_vagas",
            "titulo": "Busca por <em>vagas de TI</em> (Google Trends)",
            "subtitulo": "Interesse em encontrar emprego em TI - reflete aquecimento/esfriamento do mercado",
            "cores": ["#4c1d95", "#7c3aed", "#c4b5fd"],
        },
    ]

    for cfg in CONFIGS_LOTES:
        lote_dados = trends_lotes.get(cfg["chave"], {})
        if not any(lote_dados.values()):
            continue

        st.markdown(f"""
        <div class="section-header">
          <span class="section-num">01.3</span>
          <span class="section-title">{cfg['titulo']}</span>
        </div>
        <div style="font-family:'DM Mono',monospace;font-size:12px;color:#7a7570;margin:-1rem 0 1rem 0;">
          {cfg['subtitulo']}
        </div>
        """, unsafe_allow_html=True)

        fig_lote = go.Figure()
        for i, (termo, pontos) in enumerate(lote_dados.items()):
            if not pontos:
                continue
            df_t = pd.DataFrame(pontos)
            df_t["mes_dt"] = pd.to_datetime(df_t["mes"])
            df_t = df_t[df_t["mes_dt"] >= "2022-07-01"]
            fig_lote.add_trace(go.Scatter(
                x=df_t["mes_dt"], y=df_t["valor"],
                name=termo,
                line=dict(color=cfg["cores"][i % len(cfg["cores"])], width=3.5),
                hovertemplate=f"<b>{termo}</b><br>%{{x|%b/%Y}}: %{{y}}<extra></extra>",
            ))

        marca_chatgpt(fig_lote)
        fig_lote.update_layout(
            **LAYOUT_BASE, height=420,
            xaxis=dict(gridcolor="#d9d4cc", tickfont=TICK_FONT),
            yaxis=dict(
                title=dict(text="Interesse relativo (0-100)", font=LABEL_FONT),
                tickfont=TICK_FONT, gridcolor="#d9d4cc",
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                        font=dict(family="DM Mono, monospace", size=11)),
            hovermode="x unified",
        )
        st.plotly_chart(fig_lote, use_container_width=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="annotation">
      <strong>Seção de IA não disponível.</strong>
      Execute <code>python enriquece_ia.py</code> para adicionar a análise de impacto da IA.
    </div>
    """, unsafe_allow_html=True)
# ============================================================
# SECAO 2 - CRESCIMENTO + OPPORTUNITY SCORE
# ============================================================

secnum = "02" if tem_ia else "01"
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum}.1</span>
      <span class="section-title">Top <em>Crescimento</em> (5 anos)</span>
    </div>
    """, unsafe_allow_html=True)

    SKILLS_EXCLUIR = {"IA", "R"}
    top_cresc = sorted(dados["top_skills"], key=lambda x: x["crescimento_5anos"], reverse=True)
    top_cresc = [s for s in top_cresc if s["skill"] not in SKILLS_EXCLUIR][:8]
    df_cresc = pd.DataFrame(top_cresc)

    fig = px.bar(
        df_cresc, x="skill", y="crescimento_5anos",
        color="crescimento_5anos",
        color_continuous_scale=[[0, "#c0392b"], [0.5, "#f59e0b"], [1, COR_PRINCIPAL]],
        text=df_cresc["crescimento_5anos"].apply(lambda x: f"{x:+.1f}%"),
    )
    fig.update_traces(textposition="outside", marker_line_width=0)
    fig.update_coloraxes(showscale=False)
    fig.update_layout(
        **LAYOUT_BASE, height=340,
        xaxis_title="", yaxis_title="Crescimento (%)",
        yaxis=dict(tickfont=TICK_FONT, gridcolor="#d9d4cc"),
        xaxis=dict(tickfont=dict(family="DM Mono, monospace", size=11, color=COR_INK)),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum}.2</span>
      <span class="section-title"><em>Opportunity</em> Score</span>
    </div>
    """, unsafe_allow_html=True)

    df_score = pd.DataFrame(dados["opportunity_scores"][:8])
    n_s = len(df_score)
    cores_score = [COR_PRINCIPAL if i == 0 else f"rgba(13,122,95,{0.9 - i*0.12:.2f})" for i in range(n_s)]

    fig = go.Figure(go.Bar(
        y=df_score["skill"][::-1],
        x=df_score["score"][::-1],
        orientation="h",
        marker_color=cores_score[::-1],
        text=df_score["score"][::-1].apply(lambda x: f"{x:.0f}"),
        textposition="outside",
        textfont=TICK_FONT,
    ))
    fig.update_layout(
        **LAYOUT_BASE, height=340,
        xaxis_title="Score (0-100)",
        xaxis=dict(tickfont=TICK_FONT, gridcolor="#d9d4cc"),
        yaxis=dict(tickfont=dict(family="DM Mono, monospace", size=13, color=COR_INK), automargin=True),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
# SECAO 3 - SKILLS + PROFISSOES
# ============================================================

secnum2 = "03" if tem_ia else "02"
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum2}.1</span>
      <span class="section-title">Skills mais <em>demandadas</em></span>
    </div>
    """, unsafe_allow_html=True)

    df_skills = pd.DataFrame(dados["top_skills"][:10])
    n_sk = len(df_skills)
    cores_skills = [f"rgba(13,122,95,{1.0 - i*(0.75/n_sk):.2f})" for i in range(n_sk)]

    fig = go.Figure(go.Bar(
        x=df_skills["vagas"], y=df_skills["skill"],
        orientation="h",
        marker_color=cores_skills,
        text=df_skills["vagas"],
        textposition="outside",
        textfont=TICK_FONT,
    ))
    fig.update_layout(
        **LAYOUT_BASE, height=360,
        xaxis_title="Vagas",
        xaxis=dict(tickfont=TICK_FONT, gridcolor="#d9d4cc"),
        yaxis=dict(autorange="reversed", tickfont=dict(family="DM Mono, monospace", size=13, color=COR_INK), automargin=True),
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum2}.2</span>
      <span class="section-title">Profissões em <em>alta</em></span>
    </div>
    """, unsafe_allow_html=True)

    df_prof = pd.DataFrame(dados["top_profissoes"][:10])
    fig = px.bar(
        df_prof, x="vagas", y="profissao",
        orientation="h",
        color="salario_medio_estimado",
        color_continuous_scale=[[0, "#ede9e2"], [0.5, COR_SECUNDARIA], [1, COR_PRINCIPAL]],
        text="vagas",
        labels={"salario_medio_estimado": "Salário (R$)", "vagas": "Vagas", "profissao": ""},
    )
    fig.update_traces(textposition="outside", textfont=TICK_FONT)
    fig.update_coloraxes(colorbar=dict(
        tickfont=TICK_FONT,
        title=dict(font=LABEL_FONT),
    ))
    fig.update_layout(
        **LAYOUT_BASE, height=360,
        xaxis_title="Vagas",
        xaxis=dict(tickfont=TICK_FONT, gridcolor="#d9d4cc"),
        yaxis=dict(autorange="reversed", tickfont=dict(family="DM Mono, monospace", size=13, color=COR_INK), automargin=True),
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
# SECAO 4 - SALÁRIOS + MODALIDADE
# ============================================================

secnum3 = "04" if tem_ia else "03"
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum3}.1</span>
      <span class="section-title">Salários por <em>profissão</em></span>
    </div>
    """, unsafe_allow_html=True)

    df_sal = pd.DataFrame(dados["top_profissoes"][:10])
    df_sal["faixa_hover"] = df_sal.apply(
        lambda r: f"Jr: R${r['faixa']['junior']:,} | Pl: R${r['faixa']['pleno']:,} | Sr: R${r['faixa']['senior']:,}",
        axis=1
    )
    sal_vals = df_sal["salario_medio_estimado"][::-1]
    cores_sal = [COR_PRINCIPAL if v == sal_vals.max() else f"rgba(13,122,95,{0.35 + v/sal_vals.max()*0.65:.2f})" for v in sal_vals]

    fig = go.Figure(go.Bar(
        y=df_sal["profissao"][::-1], x=sal_vals,
        orientation="h",
        marker_color=cores_sal,
        text=sal_vals.apply(lambda x: f"R${x:,.0f}"),
        textposition="outside",
        textfont=TICK_FONT,
        cliponaxis=False,
        hovertemplate=df_sal["faixa_hover"][::-1].values,
    ))
    fig.update_layout(
        **{**LAYOUT_BASE, "margin": dict(l=0, r=96, t=20, b=0)},
        height=360,
        xaxis_title="Salário Médio Pleno",
        xaxis=dict(tickfont=TICK_FONT, gridcolor="#d9d4cc", tickprefix="R$", range=[0, sal_vals.max() * 1.16]),
        yaxis=dict(tickfont=dict(family="DM Mono, monospace", size=13, color=COR_INK), automargin=True),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="annotation">
      <strong>Nota metodológica:</strong> Salários estimados a partir de tabelas de referência
      (Glassdoor/Catho) para o nível pleno - apenas 2 vagas da coleta informaram salário diretamente.
      A maioria das empresas brasileiras não divulga remuneração nas vagas publicadas.
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum3}.2</span>
      <span class="section-title">Transparência sobre <em>modalidade</em></span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="annotation">
      <strong>Leitura metodológica:</strong> modalidade não é um dado confiável nesta coleta.
      Das 912 vagas analisadas, 753 não declaram se são remotas, híbridas ou presenciais.
      Por isso, os 20 anúncios explicitamente presenciais não representam o tamanho real do
      presencial no mercado. Na prática, muitas vagas associadas a uma cidade e sem menção
      a remoto provavelmente são vagas locais, mas essa inferência não deve virar KPI.
      O dado mais importante aqui é a baixa transparência das publicações.
    </div>
    """, unsafe_allow_html=True)
    mod_data = dados["modalidade_trabalho"]
    vagas_sem_modalidade = next(
        (v["vagas"] for k, v in mod_data.items() if "especificado" in k.lower()),
        0,
    )
    total_modalidade = sum(v["vagas"] for v in mod_data.values())
    vagas_com_modalidade = total_modalidade - vagas_sem_modalidade
    df_transp = pd.DataFrame([
        {"Status": "Declara modalidade", "Vagas": vagas_com_modalidade},
        {"Status": "Não declara", "Vagas": vagas_sem_modalidade},
    ])
    df_transp["Percentual"] = df_transp["Vagas"] / total_modalidade * 100

    fig = go.Figure(go.Bar(
        y=df_transp["Status"][::-1],
        x=df_transp["Vagas"][::-1],
        orientation="h",
        marker_color=["#c8c1b7", COR_PRINCIPAL],
        text=df_transp.apply(lambda r: f"{r['Vagas']} ({r['Percentual']:.1f}%)", axis=1)[::-1],
        textposition="outside",
        textfont=TICK_FONT,
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>%{x} vagas<extra></extra>",
    ))
    fig.update_layout(
        **{**LAYOUT_BASE, "margin": dict(l=0, r=88, t=8, b=0)},
        height=220,
        xaxis=dict(tickfont=TICK_FONT, gridcolor="#d9d4cc", range=[0, total_modalidade * 1.15]),
        yaxis=dict(tickfont=dict(family="DM Mono, monospace", size=12, color=COR_INK), automargin=True),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ============================================================
# SECAO 5 - TABELA + INSIGHTS
# ============================================================

secnum4 = "05" if tem_ia else "04"
col1, col2 = st.columns([1.4, 1])

with col1:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum4}.1</span>
      <span class="section-title">Tabela de <em>skills</em></span>
    </div>
    """, unsafe_allow_html=True)

    df_tab = pd.DataFrame(dados["top_skills"])
    df_tab.columns = ["Skill", "Vagas", "Interesse", "Cresc. 5a", "Tendência"]
    df_tab = df_tab[["Skill", "Vagas", "Cresc. 5a", "Tendência"]]
    df_tab["Cresc. 5a"] = df_tab["Cresc. 5a"].apply(lambda x: f"{x:+.1f}%")

    st.dataframe(
        df_tab, use_container_width=True, hide_index=True, height=760,
        column_config={
            "Skill": st.column_config.TextColumn("Skill", width="medium"),
            "Vagas": st.column_config.NumberColumn("Vagas", width="small"),
            "Cresc. 5a": st.column_config.TextColumn("Cresc. 5 anos", width="small"),
            "Tendência": st.column_config.TextColumn("Tendência", width="small"),
        }
    )

with col2:
    st.markdown(f"""
    <div class="section-header">
      <span class="section-num">{secnum4}.2</span>
      <span class="section-title">Insights <em>gerais</em></span>
    </div>
    """, unsafe_allow_html=True)

    html_ins2 = "".join(
        f'<div class="insight-item">{i.lstrip("• ")}</div>'
        for i in dados.get("insights", [])
    )
    st.markdown(f'<div class="insight-list">{html_ins2}</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="annotation" style="margin-top:1.5rem">
      <strong>Fontes:</strong> Adzuna API · Google Trends · CAGED/MTE · Tabela salarial BR<br><br>
      <strong>Snapshot:</strong> {dados['metadata']['data_coleta']}
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer-bar">
  <div>
    <div class="footer-name">Leonardo Vitor Coelho · Tiradentes, MG · 2026</div>
    <div class="footer-name" style="margin-top:.2rem">
      <a href="https://github.com/leovitorcoelho1995-ship-it" style="color:#7a7570;text-decoration:none">GitHub</a>
      &nbsp;·&nbsp;
      <a href="https://wayto1.vercel.app" style="color:#7a7570;text-decoration:none">Wayto Tech</a>
    </div>
  </div>
  <div style="display:flex;gap:.4rem;flex-wrap:wrap">
    <span class="footer-tag">Python</span>
    <span class="footer-tag">Streamlit</span>
    <span class="footer-tag">CAGED/MTE</span>
    <span class="footer-tag">Adzuna API</span>
    <span class="footer-tag">Google Trends</span>
  </div>
</div>
""", unsafe_allow_html=True)

