import pandas as pd
from sqlalchemy import create_engine, text

# 1. Definição das variáveis de acesso (Devem vir sempre primeiro!)
USUARIO = "root"
SENHA = "1234"
HOST = "localhost"
PORTA = "3306"
BANCO = "db_seeg"

# 2. Conectar ao MySQL sem especificar o banco para poder criá-lo se não existir
conexao_str_temp = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/"
engine_temp = create_engine(conexao_str_temp)

with engine_temp.connect() as conexao:
    conexao.execute(text(f"CREATE DATABASE IF NOT EXISTS {BANCO};"))
    conexao.commit()

# 3. Conexão definitiva já apontando para o banco criado
conexao_str = f"mysql+pymysql://{USUARIO}:{SENHA}@{HOST}:{PORTA}/{BANCO}"
engine = create_engine(conexao_str)

# 4. Caminho do arquivo CSV limpo e parâmetros de carga
arquivo_csv = "seeg_dados_limpos.csv"
nome_tabela = "tb_emissoes_limpa"
chunksize = 10000

print("Iniciando a importação dos dados limpos para o MySQL...")

try:
    for i, chunk in enumerate(pd.read_csv(arquivo_csv, chunksize=chunksize, low_memory=False)):
        modo_gravacao = "replace" if i == 0 else "append"
        
        chunk.to_sql(
            name=nome_tabela,
            con=engine,
            if_exists=modo_gravacao,
            index=False,
            method="multi"
        )
        print(f"Lote {i + 1} inserido com sucesso (~{(i + 1) * chunksize} linhas processadas).")

    print("\nCarga concluída com sucesso! Seus dados limpos agora estão seguros no MySQL.")

except Exception as e:
    print(f"Ocorreu um erro durante a importação: {e}")