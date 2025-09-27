# app.py
# -*- coding: utf-8 -*-

from datetime import datetime
import io
import base64

import streamlit as st

# ReportLab imports (robustos)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# PageBreak pode variar entre versões do reportlab
try:
    from reportlab.platypus import PageBreak
except ImportError:
    from reportlab.platypus.flowables import PageBreak


def gerar_pdf(titulo, subtitulo, autor, data_atual_str, introducao, corpo_texto, conclusao, dados_tabela):
    """
    Gera um PDF e retorna bytes.
    Recebe dados_tabela como lista de listas (primeira linha header).
    """
    buffer = io.BytesIO()
    # Margens (em pontos). A4 em pontos ~ (595, 842)
    left_margin = right_margin = 72
    top_margin = 72
    bottom_margin = 18

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=right_margin,
        leftMargin=left_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
    )
    story = []
    styles = getSampleStyleSheet()

    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'CustomTitulo',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#0B3D91')
    )
    subtitulo_style = ParagraphStyle(
        'CustomSubtitulo',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.black
    )
    corpo_style = ParagraphStyle(
        'CustomCorpo',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leftIndent=0,
        alignment=TA_LEFT
    )
    info_style = ParagraphStyle(
        'CustomInfo',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        alignment=TA_RIGHT,
        textColor=colors.gray
    )
    rodape_style = ParagraphStyle(
        'CustomRodape',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=0,
        alignment=TA_CENTER,
        textColor=colors.gray
    )

    # Capa
    story.append(Paragraph(titulo, titulo_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(subtitulo, subtitulo_style))
    story.append(Spacer(1, 24))
    story.append(Paragraph(f"Autor: {autor}", info_style))
    story.append(Paragraph(f"Data: {data_atual_str}", info_style))
    story.append(PageBreak())

    # Seções
    story.append(Paragraph("1. Introdução", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(introducao.replace('\n', '<br/>'), corpo_style))
    story.append(Spacer(1, 24))

    story.append(Paragraph("2. Análise de Dados", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(corpo_texto.replace('\n', '<br/>'), corpo_style))
    story.append(Spacer(1, 18))

    # Tabela
    # Ajuste de colWidths para caber na página considerando as margens
    # Conteúdo útil = largura da página - left_margin - right_margin
    page_width = A4[0]
    content_width = page_width - left_margin - right_margin
    # escolha col widths que somem <= content_width
    col_widths = [1.2 * inch, 2.5 * inch, 1.0 * inch, 1.5 * inch]  # soma ~= 6.2 in
    # (em pontos) verificação opcional -- se exceder, ajusta proporcionalmente
    total_col = sum(col_widths)
    if total_col > content_width:
        scale = content_width / total_col
        col_widths = [w * scale for w in col_widths]

    tabela = Table(dados_tabela, colWidths=col_widths, hAlign='LEFT')
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 24))

    story.append(Paragraph("3. Conclusão", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(conclusao.replace('\n', '<br/>'), corpo_style))
    story.append(Spacer(1, 24))

    story.append(Paragraph(f"Relatório gerado em {data_atual_str} por {autor}", rodape_style))

    # Construir PDF no buffer
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


# -------- Streamlit UI --------
st.set_page_config(page_title="Interface Documents", page_icon="🧪", layout="wide")

st.title("📄 Docs")
st.markdown("---")

# Sidebar para configurações
st.sidebar.header("⚙️ Configuração")
titulo = st.sidebar.text_input("Título do Relatório", value="Relatório de Projeto Exemplo")
subtitulo = st.sidebar.text_input("Subtítulo", value="Análise e Resultados")
autor = st.sidebar.text_input("Autor", value="Seu Nome ou Equipe")
data_obj = st.sidebar.date_input("Data", value=datetime.now().date())
data_atual = data_obj.strftime("%d/%m/%Y")

# Colunas principais para conteúdo
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Introdução")
    introducao = st.text_area(
        "Texto da Introdução",
        value=(
            "Este relatório apresenta os resultados preliminares do projeto em desenvolvimento.\n"
            "O objetivo principal é analisar os dados coletados e propor melhorias para otimizar o processo.\n"
            "Foram utilizados métodos de análise quantitativa e qualitativa para garantir a precisão dos resultados."
        ),
        height=150
    )

    st.subheader("2. Corpo/Análise")
    corpo_texto = st.text_area(
        "Texto do Corpo",
        value=(
            "No corpo do relatório, detalhamos os achados principais.\n"
            "Por exemplo, a análise de dados revelou uma taxa de sucesso de 85% nas operações testadas.\n"
            "Recomenda-se a implementação de novas ferramentas para elevar essa métrica para 95%."
        ),
        height=150
    )

with col2:
    st.subheader("3. Conclusão")
    conclusao = st.text_area(
        "Texto da Conclusão",
        value=(
            "Em conclusão, o projeto demonstra viabilidade e potencial de impacto.\n"
            "As próximas etapas incluem testes em escala maior e integração com sistemas existentes."
        ),
        height=150
    )

    st.subheader("Tabela de Dados")
    st.markdown("Edite a tabela abaixo (adicione/remova linhas se necessário):")
    num_linhas = int(st.number_input("Número de linhas na tabela (máx 10)", min_value=1, max_value=10, value=3))
    dados_tabela = [['Item', 'Descrição', 'Valor', 'Status']]  # cabeçalho fixo
    for i in range(num_linhas):
        with st.expander(f"Linha {i+1}"):
            item_default = f"Operação {i+1}" if i < 3 else ""
            desc_default = ("Processamento de dados" if i == 0 else
                            "Análise estatística" if i == 1 else
                            "Relatório final" if i == 2 else "")
            valor_default = ("R$ 1.500,00" if i == 0 else
                             "R$ 2.000,00" if i == 1 else
                             "R$ 800,00" if i == 2 else "")
            item = st.text_input(f"Item {i+1}", value=item_default, key=f"item_{i}")
            desc = st.text_input(f"Descrição {i+1}", value=desc_default, key=f"desc_{i}")
            valor = st.text_input(f"Valor {i+1}", value=valor_default, key=f"valor_{i}")
            status_index = 0 if i == 0 else 1 if i == 1 else 2
            status = st.selectbox(f"Status {i+1}", ["Concluído", "Em Andamento", "Pendente"], index=status_index, key=f"status_{i}")
            dados_tabela.append([item, desc, valor, status])

# Botão para gerar PDF
if st.button("🔥 Gerar e Baixar PDF"):
    with st.spinner("Gerando PDF..."):
        pdf_bytes = gerar_pdf(titulo, subtitulo, autor, data_atual, introducao, corpo_texto, conclusao, dados_tabela)

    st.success("PDF gerado com sucesso! 📄")
    st.markdown("### Visualização do PDF:")

    # Embed do PDF usando iframe com base64 (visualização inline)
    pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
    st.markdown(
        f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px" type="application/pdf" style="border: 1px solid #ccc; border-radius: 5px;"></iframe>',
        unsafe_allow_html=True
    )

    # Botão de download nativo do Streamlit
    st.download_button(
        label="⬇️ Baixar PDF",
        data=pdf_bytes,
        file_name="relatorio.pdf",
        mime="application/pdf"
    )

st.markdown("---")
st.markdown("*Desenvolvido com Streamlit e ReportLab.*")
