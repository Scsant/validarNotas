import streamlit as st
from utils.leitor_pdf import extrair_texto_unico
import os
import re

st.set_page_config(page_title="Conferência de Guias", layout="wide")
st.title("📋 Conferência Isolada de Guias")

guias_upload = st.file_uploader("📎 Envie os PDFs das Guias (múltiplos)", type="pdf", accept_multiple_files=True)

if guias_upload:
    guias_ok = []
    guias_erro = []
    guias_total = []

    for guia in guias_upload:
        nome_arquivo = guia.name
        match_nome = re.search(r"(\d{3,})", nome_arquivo)
        numero_nome = match_nome.group(1) if match_nome else ""

        with open("temp_guia.pdf", "wb") as f:
            f.write(guia.getbuffer())
        texto = extrair_texto_unico("temp_guia.pdf")

        match_conteudo = re.search(r"N\.?\s*FISCAIS DE NS[:\-]?\s*(\d{5,})", texto, re.IGNORECASE)
        numero_extraido = match_conteudo.group(1) if match_conteudo else None

        if numero_extraido:
            if numero_extraido.endswith(numero_nome):
                guias_ok.append(numero_extraido)
            else:
                guias_erro.append((numero_nome, numero_extraido))
            guias_total.append(numero_extraido)

        os.remove("temp_guia.pdf")

    st.subheader("📊 Resultado da Conferência de Guias")
    st.metric("Guias Processadas", len(guias_total))
    st.metric("Guias Validadas com Sucesso", len(guias_ok))

    if guias_erro:
        st.error("❌ Guias com número divergente do nome do arquivo:")
        for esperado, encontrado in guias_erro:
            st.write(f"🟥 Arquivo: `{esperado}` → Conteúdo: `{encontrado}`")
    else:
        st.success("✅ Todas as guias estão consistentes com o nome do arquivo!")
else:
    st.info("Aguardando upload das guias para conferência.")
