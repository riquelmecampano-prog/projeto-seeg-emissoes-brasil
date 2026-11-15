# 🌍 SEEG Brasil - Pipeline de Dados e Painel Preditivo de GEE

> Pipeline completo de engenharia de dados, armazenamento relacional, modelagem preditiva de Machine Learning e visualização interativa das emissões de Gases de Efeito Estufa (GEE) no Brasil com base nos dados do SEEG (v14.0).

---

## 🛠️ Tecnologias e Ferramentas Utilizadas

* **Linguagem:** Python 3.x
* **Engenharia e Manipulação de Dados:** Pandas, NumPy, SQLAlchemy
* **Banco de Dados Relacional:** MySQL (com otimização de índices para alta performance)
* **Machine Learning:** Scikit-Learn (Regressão Linear para projeção temporal até 2050)
* **Visualização de Dados e UI:** Streamlit, Plotly, HTML/CSS personalizado
* **Versionamento:** Git & GitHub

---

## 📊 Arquitetura e Etapas do Projeto

1. **Ingestão e Limpeza (ETL):** Processamento de grandes volumes de dados brutos do SEEG, realizando a transformação do formato "largo" para o formato normalizado "longo" (`pd.melt`) otimizado para análise relacional.
2. **Armazenamento:** Persistência dos dados normalizados na tabela `tb_emissoes_longa` em um banco de dados local **MySQL** (`db_seeg`), com indexação na coluna `ano` para consultas instantâneas.
3. **Modelagem Preditiva:** Treinamento de um modelo estatístico de **Regressão Linear** utilizando Scikit-Learn sobre o histórico agregado de emissões, permitindo extrapolar tendências anuais e projetar cenários futuros até o ano de 2050.
4. **Dashboard Interativo (Web App):** Interface web desenvolvida em **Streamlit** com tema escuro (Eco-Dark), cartões de métricas executivas formatados em Bilhões/Milhões e gráficos dinâmicos construídos com **Plotly**.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Pré-requisitos
Certifique-se de ter o **Python** e o **MySQL Server** instalados em sua máquina, além das bibliotecas necessárias:
```bash
pip install pandas numpy scikit-learn streamlit plotly sqlalchemy pymysql matplotlib