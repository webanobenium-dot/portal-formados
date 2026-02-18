import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Portal de Egressos ESMAC", page_icon="🎓")

st.title("🎓 Portal de Consulta de Formados")
st.write("Verifique a autenticidade de diplomas e certificações.")

# Link da sua planilha (já configurado para exportação)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jdrtajTIE3eoGEtpuGCgpcMqZSs4iHLnoIHRWYeM4JM/export?format=csv&gid=0"

@st.cache_data(ttl=300) 
def buscar_dados():
    return pd.read_csv(URL_PLANILHA)

try:
    df = buscar_dados()
    
    # Campo de busca
    termo_busca = st.text_input("Digite o Nome Completo ou CPF:")

    if termo_busca:
        # Busca o termo em todas as colunas
        resultado = df[df.apply(lambda row: termo_busca.lower() in row.astype(str).str.lower().values, axis=1)]
        
        if not resultado.empty:
            st.success(f"Encontrado(s) {len(resultado)} registro(s):")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("Nenhum registro encontrado.")
            
except Exception as e:
    st.error("Erro ao conectar com a planilha. Verifique se ela está pública.")

st.divider()
st.caption("Sistema de consulta pública - ESMAC")
