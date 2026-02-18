import streamlit as st
import pandas as pd

# Configuração básica
st.set_page_config(page_title="Portal de Egressos ESMAC", page_icon="🎓")

st.title("🎓 Portal de Consulta de Formados")
st.markdown("### Secretaria Acadêmica - ESMAC")
st.write("Verifique a autenticidade de diplomas e certificações.")

# Link da sua planilha (Já testado e funcionando)
URL = "https://docs.google.com/spreadsheets/d/1jdrtajTIE3eoGEtpuGCgpcMqZSs4iHLnoIHRWYeM4JM/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def carregar_dados():
    # Lê a planilha e força tudo para texto para evitar erros
    df = pd.read_csv(URL)
    return df.astype(str)

try:
    df = carregar_dados()
    
    busca = st.text_input("🔍 Digite o Nome Completo ou CPF para consulta:")

    if busca:
        # Busca em todas as colunas ignorando maiúsculas/minúsculas
        resultado = df[df.apply(lambda row: row.str.contains(busca, case=False, na=False)).any(axis=1)]
        
        if not resultado.empty:
            st.success(f"✅ Registro encontrado com sucesso!")
            # Exibe os dados em uma tabela limpa
            st.dataframe(resultado, use_container_width=True, hide_index=True)
        else:
            st.warning("❌ Nenhum registro encontrado. Verifique a grafia do nome.")

except Exception as e:
    st.error("Erro ao carregar a base de dados. Verifique se a planilha está pública.")

st.divider()
st.caption("© 2026 ESMAC - Sistema Acadêmico de Consulta Pública")
