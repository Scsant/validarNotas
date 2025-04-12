import streamlit as st
from utils.leitor_pdf import extrair_texto_unico, contar_ocorrencias
import os
import re

st.set_page_config(page_title="Validação de Notas", layout="wide")
st.title("🔍 Validação de Notas Fiscais")

uploaded_file = st.file_uploader("📎 Envie o PDF das Notas Fiscais Agrupadas", type="pdf")

if uploaded_file is not None:
    caminho_temporario = os.path.join("temp.pdf")
    with open(caminho_temporario, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("Arquivo carregado com sucesso!")

    texto = extrair_texto_unico(caminho_temporario)

    # Entradas do usuário
    with st.form("form_validacao"):
        nome_fazenda = st.text_input("🧾 Nome esperado da Fazenda")
        nome_transportadora = st.text_input("🚛 Nome esperado da Transportadora")
        data_emissao = st.text_input("📅 Data esperada de Emissão (ex: 11.04.2025)")
        submitted = st.form_submit_button("✅ Validar")

    if submitted:
        # Contagens
        total_datas = contar_ocorrencias(texto, data_emissao)
        total_fazenda = contar_ocorrencias(texto, nome_fazenda)
        total_transportadora = contar_ocorrencias(texto, nome_transportadora)

        # Extração dinâmica de número de notas com regex
        padrao_nota = re.findall(r"N[ºo]\s*(\d{5,})", texto)
        total_notas = len(padrao_nota)

        st.subheader("📊 Resultados da Validação")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Notas Encontradas", total_notas)
        col2.metric(f"{data_emissao} Encontrada(s)", total_datas)
        col3.metric(f"{nome_fazenda} Encontrada(s)", total_fazenda)
        col4.metric(f"{nome_transportadora} Encontrada(s)", total_transportadora)

        # Validação final
        if (
            total_notas > 0 and
            total_datas == total_notas * 2 and
            total_fazenda == total_notas and
            total_transportadora == total_notas
        ):
            st.success("✅ Todas as validações foram concluídas com sucesso!")
        else:
            st.error("❌ Algumas validações falharam. Verifique as contagens e os nomes informados.")

        with st.expander("📄 Visualizar conteúdo do PDF"):
            st.text_area("Texto Extraído", texto, height=400)

    os.remove(caminho_temporario)
else:
    st.info("Aguardando upload do arquivo PDF...")
