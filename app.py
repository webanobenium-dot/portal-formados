import streamlit as st
import pandas as pd

st.set_page_config(page_title="Portal de Egressos ESMAC", page_icon="🎓")

st.title("🎓 Portal de Consulta de Formados")
st.write("Verifique a conformidade de diplomas e certificações.")

# Link da sua planilha
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1jdrtajTIE3eoGEtpuGCgpcMqZSs4iHLnoIHRWYeM4JM/export?format=csv&gid=0"

@st.cache_data(ttl=60) # Diminuí o tempo para 1 minuto para atualizar mais rápido
def buscar_dados():
    # Lendo a planilha e forçando tudo para texto
    return pd.read_csv(URL_PLANILHA).astype(str)

try:
    df = buscar_dados()
    
    termo_busca = st.text_input("Digite o Nome Completo ou CPF:")

    if termo_busca:
        # Busca o nome ignorando se é maiúsculo ou minúsculo
        mask = df.apply(lambda row: row.str.contains(termo_busca, case=False, na=False)).any(axis=1)
        resultado = df[mask]
        
        if not resultado.empty:
            st.success(f"Registro encontrado!")
            st.table(resultado) # Formato de tabela fica mais bonito para consulta pública
        else:
            st.warning("Nenhum registro encontrado. Verifique se o nome está correto.")
            
except Exception as e:
    st.error("Erro ao carregar dados. Verifique a conexão com a planilha.")

st.divider()
st.caption("Sistema de consulta pública - ESMAC")
