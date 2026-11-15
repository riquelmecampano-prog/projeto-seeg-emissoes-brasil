import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sqlalchemy import create_engine

# 1. Configurações de acesso ao MySQL
USUARIO = "root"
SENHA = "1234"
HOST = "localhost"
PORTA = "3306"
BANCO = "db_seeg"

conexao_str = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
engine = create_engine(conexao_str)

# 2. Consulta SQL na tabela normalizada
query = """
    SELECT ano, SUM(emissao) AS total_emissoes
    FROM tb_emissoes_longa
    GROUP BY ano
    ORDER BY ano ASC;
"""

print("Buscando dados agregados da tabela normalizada no MySQL...")
df_analise = pd.read_sql(query, con=engine)
df_analise = df_analise.dropna()

# 3. Preparando os dados para a Regressão Linear
X = df_analise[["ano"]]
Y = df_analise["total_emissoes"]

modelo = LinearRegression()
modelo.fit(X, Y)

coef_angular = modelo.coef_[0]
intercepto = modelo.intercept_

print(f"\n--- Resultados da Regressão Linear ---")
print(f"Tendência anual (Coeficiente): {coef_angular:.2f}")
print(f"Intercepto: {intercepto:.2f}")

# 4. Projeção para 2030
ano_futuro = pd.DataFrame({"ano": [2030]})
previsao_2030 = modelo.predict(ano_futuro)
print(
    f"\nPrevisão de emissões totais para 2030: {previsao_2030[0]:,.2f} toneladas"
)

# 5. Gerando o Gráfico Profissional com Matplotlib
plt.figure(figsize=(12, 6))

# Pontos reais do histórico
plt.scatter(
    X,
    Y,
    color="#3B82F6",
    alpha=0.7,
    label="Dados Reais (Histórico SEEG)",
    s=30,
)

# Linha da Regressão Linear
plt.plot(
    X,
    modelo.predict(X),
    color="#EF4444",
    linewidth=2.5,
    label="Linha de Tendência (Regressão Linear)",
)

# Ponto de previsão para 2030
plt.scatter(
    2030,
    previsao_2030[0],
    color="#10B981",
    s=150,
    zorder=5,
    label="Previsão 2030",
)
plt.annotate(
    f"2030: {previsao_2030[0]:,.0f}",
    (2030, previsao_2030[0]),
    textcoords="offset points",
    xytext=(0, 15),
    ha="center",
    fontweight="bold",
    color="#10B981",
)

plt.title(
    "Evolução e Projeção de Emissões de Gases de Efeito Estufa (Brasil)",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Ano", fontsize=12)
plt.ylabel("Total de Emissões", fontsize=12)
plt.legend(loc="upper left")
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()

print("\nAbrindo janela com o gráfico gerado...")
plt.show()