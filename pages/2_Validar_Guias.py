import streamlit as st
from utils.leitor_pdf import extrair_texto_unico
import os
import re

st.set_page_config(page_title="Validação de Guias com Notas", layout="wide")
st.title("📄 Conferência de Guias com Notas Fiscais")

notas_pdf = st.file_uploader("📎 Envie o PDF das Notas Fiscais Agrupadas", type="pdf")
guias_upload = st.file_uploader("📎 Envie os PDFs das Guias (múltiplos)", type="pdf", accept_multiple_files=True)

if notas_pdf and guias_upload:
    with open("temp_notas.pdf", "wb") as f:
        f.write(notas_pdf.getbuffer())

    texto_notas = extrair_texto_unico("temp_notas.pdf")

    # Coletar todos os números de notas no PDF de notas
    notas_extraidas = re.findall(r"N[ºo]\s*([0-9]{5,})", texto_notas)
    notas_unicas = sorted(set(notas_extraidas))

    guias_encontradas = []
    guias_nao_encontradas = []
    guias_extraidas = []

    for guia in guias_upload:
        with open("temp_guia.pdf", "wb") as g:
            g.write(guia.getbuffer())
        texto_guia = extrair_texto_unico("temp_guia.pdf")

        match = re.search(r"N\.\s*FISCAIS DE NS[:\-]?\s*(\d{5,})", texto_guia, re.IGNORECASE)
        if match:
            numero_guia = match.group(1)
            guias_extraidas.append(numero_guia)
            if numero_guia in notas_unicas:
                guias_encontradas.append(numero_guia)
            else:
                guias_nao_encontradas.append(numero_guia)

        os.remove("temp_guia.pdf")

    os.remove("temp_notas.pdf")

    st.subheader("📊 Resultado da Conferência")
    col1, col2, col3 = st.columns(3)
    col1.metric("Notas no PDF", len(notas_unicas))
    col2.metric("Guias Recebidas", len(guias_extraidas))
    col3.metric("Guias Válidas", len(guias_encontradas))

    if guias_nao_encontradas:
        st.warning("⚠️ Algumas guias não foram localizadas nas notas:")
        st.code(", ".join(guias_nao_encontradas))
    else:
        if len(notas_unicas) == len(guias_encontradas):
            st.success("✅ Todas as guias correspondem às notas fiscais!")
        else:
            st.warning("⚠️ Nem todas as notas têm guias correspondentes!")
            notas_sem_guia = [n for n in notas_unicas if n not in guias_extraidas]
            st.info("Notas sem guia correspondente:")
            st.code(", ".join(notas_sem_guia))
else:
    st.info("Envie o PDF de notas fiscais e as guias para iniciar a conferência.")
