import pdfplumber
from typing import List


def extrair_texto_pdf(caminho_pdf: str) -> List[str]:
    """
    Lê um PDF e retorna uma lista de strings, uma por página.
    """
    paginas_texto = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                paginas_texto.append(texto)
    return paginas_texto


def extrair_texto_unico(caminho_pdf: str) -> str:
    """
    Lê todo o conteúdo do PDF e retorna como uma única string.
    """
    texto_completo = ""
    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_completo += texto + "\n"
    return texto_completo.strip()


def contar_ocorrencias(texto: str, padrao: str) -> int:
    """
    Conta quantas vezes um determinado padrão aparece no texto.
    """
    return texto.lower().count(padrao.lower())
