import streamlit as st

def aplicar_estilo():
    st.markdown("""
    <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .metric-container {
            background-color: #ffffff;
            padding: 1.2rem;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)
