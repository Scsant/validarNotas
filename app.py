import streamlit as st

st.set_page_config(page_title="Validador Fiscal", layout="wide")

# Header visual com imagem da Bracell
st.markdown(
    """
    <style>
        .header-container {
            display: flex;
            justify-content: center;
            align-items: center;
            border-radius: 100px;
            background: linear-gradient(135deg,#F5F5DC, #A0522D);
            padding: 1rem;
            margin-bottom: 2rem;
        }
        .header-container img {
            max-width: 800px;
            opacity: 0.7;
        }
    </style>
    <div class="header-container">
        <img src="https://raw.githubusercontent.com/Scsant/bracc2/3361f72d7f1b83260bd325f41387d614f7b49ffd/bracell.jpg" alt="Logo Bracell">
    </div>
    """,
    unsafe_allow_html=True
)

# Título e descrição do app
st.title("📂 Sistema de Validação de Notas e Guias")

st.markdown("""
Bem-vindo ao sistema de validação. Use o menu lateral para:

- Validar Notas Fiscais
- Conferir Guias com as Notas
- Validar Guias para o Financeiro
""")
