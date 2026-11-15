import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

# 1. Configuração da Página (Tema Escuro / Layout Amplo)
st.set_page_config(
    page_title="Dashboard SEEG | Emissões de GEE",
    page_icon="🌍",
    layout="wide",
)

# Estilização CSS personalizada para os cards ficarem perfeitos
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0B1120;
        color: #D1D5DB;
    }
    .metric-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        color: #9CA3AF;
        font-size: 0.95rem;
        margin-bottom: 5px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 5px 0;
    }
    .metric-sub {
        color: #6B7280;
        font-size: 0.8rem;
        margin: 0;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("🌍 Painel de Inteligência de Emissões (SEEG)")
st.markdown(
    "Análise temporal, tendência estatística e modelo preditivo de gases de"
    " efeito estufa no Brasil."
)


# 2. Conexão Segura com o MySQL
@st.cache_resource
def carregar_dados():
  try:
    USUARIO = "root"
    SENHA = "1234"
    HOST = "localhost"
    PORTA = "3306"
    BANCO = "db_seeg"

    conexao_str = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
    engine = create_engine(conexao_str)

    query = """
            SELECT ano, SUM(emissao) AS total_emissoes
            FROM tb_emissoes_longa
            GROUP BY ano
            ORDER BY ano ASC;
        """
    df = pd.read_sql(query, con=engine)
    return df.dropna(), "Conectado ao MySQL com Sucesso! 🚀"
  except Exception as e:
    return None, f"Erro na conexão com o MySQL: {e}"


df_analise, status_msg = carregar_dados()

if df_analise is None or df_analise.empty:
  st.error(f"Não foi possível carregar os dados. Detalhe: {status_msg}")
  st.stop()

# 3. Treinamento do Modelo de Regressão Linear
X = df_analise[["ano"]]
Y = df_analise["total_emissoes"]

modelo = LinearRegression()
modelo.fit(X, Y)

coef_angular = modelo.coef_[0]

# 4. Barra Lateral (Sidebar) para Interatividade
st.sidebar.header("⚙️ Controles de Projeção")
ano_usuario = st.sidebar.slider(
    "Ano Alvo da Projeção",
    min_value=2026,
    max_value=2050,
    value=2030,
    step=1,
)

previsao_usuario = modelo.predict(pd.DataFrame({"ano": [ano_usuario]}))[0]
ano_recente = int(df_analise["ano"].max())
emissao_recente = df_analise[df_analise["ano"] == ano_recente][
    "total_emissoes"
].values[0]

# Conversão inteligente para Bilhões e Milhões para caber perfeitamente nos cards
bilhoes_recente = emissao_recente / 1e9
bilhoes_futuro = previsao_usuario / 1e9
milhoes_tendencia = coef_angular / 1e6

# 5. Cards de Métricas Estilizados (Sem cortes)
col1, col2, col3 = st.columns(3)

with col1:
  st.markdown(
      f"""
        <div class="metric-card">
            <div class="metric-title">Ano Base Recente ({ano_recente})</div>
            <div class="metric-value" style="color: #3B82F6;">{bilhoes_recente:.2f} Bilhões t</div>
            <div class="metric-sub">Total de Emissões</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

with col2:
  st.markdown(
      f"""
        <div class="metric-card">
            <div class="metric-title">Projeção para {ano_usuario}</div>
            <div class="metric-value" style="color: #10B981;">{bilhoes_futuro:.2f} Bilhões t</div>
            <div class="metric-sub">Estimativa (Regressão Linear)</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

with col3:
  st.markdown(
      f"""
        <div class="metric-card">
            <div class="metric-title">Tendência Anual Média</div>
            <div class="metric-value" style="color: #EF4444;">{milhoes_tendencia:+.2f} Milhões t/ano</div>
            <div class="metric-sub">Variação estatística anual</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

st.markdown("<br>", unsafe_allow_html=True)

# 6. Gráfico Interativo com Plotly
st.subheader("📈 Histórico e Linha de Tendência Preditiva")

df_analise["tendencia"] = modelo.predict(X)

fig = px.scatter(
    df_analise,
    x="ano",
    y="total_emissoes",
    labels={"ano": "Ano", "total_emissoes": "Total de Emissões (Toneladas)"},
    title="Evolução Histórica e Projeção de Emissões de GEE",
)

fig.update_traces(
    marker=dict(color="#3B82F6", size=8, opacity=0.8), name="Histórico SEEG"
)

fig.add_trace(
    go.Scatter(
        x=df_analise["ano"],
        y=df_analise["tendencia"],
        mode="lines",
        name="Linha de Regressão Linear",
        line=dict(color="#EF4444", width=3),
    )
)

fig.add_trace(
    go.Scatter(
        x=[ano_usuario],
        y=[previsao_usuario],
        mode="markers+text",
        name=f"Projeção {ano_usuario}",
        marker=dict(color="#10B981", size=16, symbol="star"),
        text=[f"  {ano_usuario}: {bilhoes_futuro:.2f} Bilhões t"],
        textposition="top right",
        textfont=dict(color="#10B981", size=12),
    )
)

fig.update_layout(
    plot_bgcolor="#0B1120",
    paper_bgcolor="#0B1120",
    font=dict(color="#D1D5DB"),
    xaxis=dict(showgrid=True, gridcolor="#1E293B"),
    yaxis=dict(showgrid=True, gridcolor="#1E293B"),
    margin=dict(l=20, r=20, t=40, b=20),
)

st.plotly_chart(fig, use_container_width=True)
