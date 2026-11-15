import pandas as pd
from sqlalchemy import create_engine

# 1. Configurações de acesso ao MySQL
USUARIO = "root"
SENHA = "1234"
HOST = "localhost"
PORTA = "3306"
BANCO = "db_seeg"

conexao_str = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
engine = create_engine(conexao_str)

print("Lendo os dados da tabela atual do MySQL...")
df_largo = pd.read_sql("SELECT * FROM tb_emissoes_limpa;", con=engine)

# 2. Separar quais colunas são anos e quais são metadados (gás, setor, estado, etc.)
anos_colunas = [str(ano) for ano in range(1970, 2026)]
colunas_meta = [c for c in df_largo.columns if c not in anos_colunas]

print(
    "Transformando as colunas de anos em uma única coluna (Formato Longo)..."
)

# 3. A mágica do Unpivot (pd.melt): junta todas as colunas de anos em 'ano' e 'emissao'
df_longo = pd.melt(
    df_largo,
    id_vars=colunas_meta,
    value_vars=anos_colunas,
    var_name="ano",
    value_name="emissao",
)

# Converter a coluna 'ano' para número inteiro
df_longo["ano"] = df_longo["ano"].astype(int)

# Remover linhas onde a emissão é nula ou vazia para otimizar
df_longo = df_longo.dropna(subset=["emissao"])

print("\nAmostra dos dados normalizados:")
print(df_longo[["ano", "emissao", "gas", "estado"]].head(10))

# 4. Salvando essa nova tabela limpa e normalizada no MySQL
print(
    "\nSalvando a nova tabela otimizada 'tb_emissoes_longa' no MySQL (Isso pode"
    " levar alguns segundos)..."
)
df_longo.to_sql(
    "tb_emissoes_longa",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=10000,
)

print(
    "Sucesso! Agora você tem a tabela 'tb_emissoes_longa' com colunas unificadas"
    " de ano e emissão."
)