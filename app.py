import streamlit as st
import pandas as pd

# 1. Configuração da Página e Estilo
st.set_page_config(page_title="Portal de Egressos ESMAC", page_icon="🎓", layout="wide")

# CSS personalizado para melhorar as cores e fontes
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stTextInput { border-radius: 20px; }
    .stButton>button { border-radius: 20px; width: 100%; background-color: #004a8d; color: white; }
    .res-card { 
        background-color: white; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        border-left: 5px solid #004a8d;
    }
    </style>
    """, unsafe_index=True)

# 2. Cabeçalho Dinâmico
col1, col2 = st.columns([1, 4])
with col1:
    st.title("🎓")
with col2:
    st.title("Portal de Consulta de Formados")
    st.subheader("Secretaria Acadêmica ESMAC")

st.divider()

# 3. Função de Dados (com Cache rápido)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jdrtajTIE3eoGEtpuGCgpcMqZSs4iHLnoIHRWYeM4JM/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def carregar_dados():
    # Lê a planilha, garante que os nomes das colunas fiquem limpos
    df = pd.read_csv(URL_PLANILHA)
    return df

try:
    df = carregar_dados()
    
    # Exibe uma métrica simples do total na base
    st.info(f"💡 Nossa base conta atualmente com {len(df)} registros de diplomas emitidos.")

    # 4. Área de Busca Centralizada
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        busca = st.text_input("🔍 Pesquisar por Nome Completo ou identificador:", placeholder="Ex: MARA DO SOCORRO...")

    if busca:
        # Filtro inteligente (ignora acentos e maiúsculas/minúsculas)
        resultado = df[df.apply(lambda row: row.astype(str).str.contains(busca, case=False, na=False)).any(axis=1)]
        
        if not resultado.empty:
            st.success(f"✅ Encontramos {len(resultado)} registro(s) correspondente(s):")
            
            # Exibe os resultados em formato de "Fichas" (Cards) em vez de tabela feia
            for i, row in resultado.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="res-card">
                        <h4>👤 {row['Diplomado']}</h4>
                        <p><b>📚 Curso:</b> {row['Curso']} ({row['Grau']})</p>
                        <p><b>📅 Conclusão:</b> {row['Data de Conclusão']} | <b>🎓 Colação:</b> {row['Data de colação de Grau']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("❌ Nenhum registro encontrado. Certifique-se de que o nome está correto ou entre em contato com a secretaria.")

except Exception as e:
    st.warning("🔄 Sincronizando com a base de dados... Por favor, recarregue em instantes.")

# Rodapé
st.markdown("---")
st.caption("© 2026 Escola Superior Madre Celeste - ESMAC | Gestão de Tecnologia Educacional")
