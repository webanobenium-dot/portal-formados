import streamlit as st
import pandas as pd

# 1. Configuração da Página
st.set_page_config(page_title="Portal de Egressos ESMAC", page_icon="🎓")

# 2. Estilo Visual (CSS)
st.markdown("""
    <style>
    .stTextInput > div > div > input { border-radius: 10px; border: 2px solid #004a8d; }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 15px;
        border-left: 10px solid #004a8d;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Cabeçalho
st.title("🎓 Portal de Consulta de Formados")
st.markdown("Verificação de autenticidade de diplomas — **ESMAC**")
st.divider()

# 4. Dados da Planilha
URL = "https://docs.google.com/spreadsheets/d/1jdrtajTIE3eoGEtpuGCgpcMqZSs4iHLnoIHRWYeM4JM/export?format=csv&gid=0"

@st.cache_data(ttl=60)
def load_data():
    return pd.read_csv(URL).astype(str)

try:
    df = load_data()
    busca = st.text_input("🔍 Digite o Nome Completo para verificar:", placeholder="Ex: MARA DO SOCORRO...")

    if busca:
        # Busca ignorando maiúsculas/minúsculas
        resultado = df[df.apply(lambda row: row.str.contains(busca, case=False, na=False)).any(axis=1)]
        
        if not resultado.empty:
            st.success(f"✅ Encontramos {len(resultado)} registro(s) oficial(is):")
            for i, row in resultado.iterrows():
                # Exibição em formato de Card
                st.markdown(f"""
                <div class="card">
                    <h3 style='margin:0; color:#004a8d;'>👤 {row['Diplomado']}</h3>
                    <p style='margin:5px 0;'><b>📚 Curso:</b> {row['Curso']} — {row['Grau']}</p>
                    <p style='margin:0;'><b>📅 Conclusão:</b> {row['Data de Conclusão']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("❌ Nenhum registro encontrado. Verifique a grafia do nome.")

except Exception as e:
    st.error("Sincronizando base de dados... Recarregue a página em instantes.")

st.divider()
st.caption("© 2026 Escola Superior Madre Celeste - ESMAC | Secretaria Acadêmica")
