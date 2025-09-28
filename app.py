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
        textColor=colors.HexColor("#141414")
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
    page_width = A4[0]
    content_width = page_width - left_margin - right_margin
    col_widths = [1.2 * inch, 2.5 * inch, 1.0 * inch, 1.5 * inch]
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


# -------- Estilização CSS Moderna e Responsiva --------
css = """
<style>
    /* Tema Geral: Moderno, Clean, Azul Escuro como Primário */
    :root {
        --primary-color:#000; /* Azul corporativo */
        --secondary-color: #000; /* Azul claro para botões */
        --accent-color: #FF9800; /* Laranja para destaques */
        --bg-color: #F8FAFC; /* Fundo claro */
        --card-bg: #FFF; /* Cards brancos */
        --text-primary: #000000; /* Texto preto forte */
        --text-secondary: #718096; /* Texto cinza */
        --border-color: #E2E8F0; /* Bordas suaves */
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }

    /* Configurações Globais */
    body {
        background-color: var(--bg-color);
        color: var(--text-primary);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .stApp {
        background-color: var(--bg-color);
    }

    /* Título Principal */
    h1 {
        color: var(--primary-color) !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        text-align: center;
        margin-bottom: 0.5rem !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Subtítulos e Headers */
    .stMarkdown h2, .stSubheader {
        color: var(--primary-color) !important;
        font-size: 1.5rem !important;
        font-weight: 600 !important;
        border-bottom: 2px solid var(--border-color);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem !important;
    }

    /* Sidebar Estilizada */
    .css-1d391kg { /* Sidebar container */
        background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%);
        border-right: 1px solid var(--border-color);
        box-shadow: var(--shadow);
    }

    .css-1d391kg .stTextInput > label, .css-1d391kg .stDateInput > label {
        color: var(--text-primary) !important;
        font-weight: 600;
    }

    .css-1d391kg input, .css-1d391kg .stDateInput input {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        background-color: #FFFFFF !important;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    /* Colunas e Cards */
    .stColumns > div {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        margin: 0.5rem;
        border: 1px solid var(--border-color);
    }

    /* Text Areas e Inputs */
    .stTextArea > label, .stNumberInput > label, .stSelectbox > label {
        color: var(--text-primary) !important;
        font-weight: 600;
        font-size: 1rem;
    }

    .stTextArea textarea, .stNumberInput input, .stSelectbox select {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
        background-color: #FFFFFF !important;
        box-shadow: var(--shadow);
        font-family: inherit;
    }

    .stTextArea textarea {
        min-height: 120px !important;
        resize: vertical;
    }

    /* Expanders para Tabela */
    .stExpander {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        box-shadow: var(--shadow) !important;
        margin: 0.5rem 0 !important;
    }

    .stExpander > div > label {
        color: var(--primary-color) !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
    }

    /* Botões */
    .stButton > button {
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
        background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%) !important;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--accent-color) 0%, #F57C00 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    /* Mensagens de Status */
    .stSuccess {
        background-color: #D4EDDA !important;
        border: 1px solid #C3E6CB !important;
        border-radius: 8px !important;
        color: #155724 !important;
        padding: 1rem !important;
        box-shadow: var(--shadow);
    }

    .stInfo {
        background-color: #CCE5FF !important;
        border: 1px solid #B3D9FF !important;
        border-radius: 8px !important;
        color: #004085 !important;
        padding: 1rem !important;
        box-shadow: var(--shadow);
    }

    /* Preview Section */
    .preview-container {
        background-color: var(--card-bg) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        box-shadow: var(--shadow-lg) !important;
        margin: 1rem 0 !important;
        border: 1px solid var(--border-color) !important;
    }

    .preview-header {
        text-align: center;
        margin-bottom: 1rem;
        color: var(--primary-color);
        font-size: 1.2rem;
        font-weight: 600;
    }

    /* PDF.js Container Responsivo */
    #pdf-viewer {
        width: 100%;
        height: 600px;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Botão de Preview em Nova Aba */
    .preview-btn {
        background: linear-gradient(135deg, var(--secondary-color) 0%, var(--primary-color) 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: var(--shadow) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-bottom: 1rem;
    }

    .preview-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-lg) !important;
    }

    /* Responsividade */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem !important;
        }
        
        .stColumns > div {
            margin: 0.25rem !important;
            padding: 1rem !important;
        }
        
        #pdf-viewer {
            height: 400px !important;
        }
        
        .stTextArea textarea {
            min-height: 100px !important;
        }
    }

    /* Spinner Customizado */
    .stSpinner > div {
        border-color: var(--secondary-color) !important;
    }
    
    
</style>
"""

# Injeta o CSS
st.markdown(css, unsafe_allow_html=True)

# -------- Streamlit UI --------
st.set_page_config(page_title="Interface Documents", page_icon="🧪", layout="wide")

st.title("📄 Docs Technora")
st.markdown("---")

# Inicializa session_state para persistir PDF
if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None
if 'pdf_nome' not in st.session_state:
    st.session_state.pdf_nome = "relatorio.pdf"

# Sidebar para configurações
with st.sidebar:
    st.header("⚙️ Configurações")
    st.markdown("---")
    titulo = st.text_input("Título do Relatório", value="Relatório de Projeto Exemplo")
    subtitulo = st.text_input("Subtítulo", value="Análise e Resultados")
    autor = st.text_input("Autor", value="Seu Nome ou Equipe")
    nome_arquivo = st.text_input("Nome do Arquivo PDF", value="relatorio.pdf")
    # Adiciona .pdf se não tiver
    if not nome_arquivo.lower().endswith('.pdf'):
        nome_arquivo += '.pdf'
    data_obj = st.date_input("Data", value=datetime.now().date())
    data_atual = data_obj.strftime("%d/%m/%Y")

# Colunas principais para conteúdo (responsivas)
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

# Botão para gerar PDF (limpa anterior se necessário)
col_gen, col_limpar = st.columns(2)
with col_gen:
    if st.button("🔥 Gerar PDF", type="primary"):
        with st.spinner("Gerando PDF..."):
            pdf_bytes = gerar_pdf(
                titulo, subtitulo, autor, data_atual,
                introducao, corpo_texto, conclusao, dados_tabela
            )
            st.session_state.pdf_bytes = pdf_bytes
            st.session_state.pdf_nome = nome_arquivo
        st.success("PDF gerado com sucesso! 📄 Agora persiste na página.")
with col_limpar:
    if st.button("🗑️ Limpar PDF Anterior"):
        st.session_state.pdf_bytes = None
        st.session_state.pdf_nome = "relatorio.pdf"
        st.rerun()

# Seção de Preview/Download (persiste com session_state)
if st.session_state.pdf_bytes is not None:
    with st.expander("📋 Preview e Download (Clique para Expandir)", expanded=True):
        st.success(f"PDF pronto: {st.session_state.pdf_nome}")
        
        # Gera base64 para o JS (uma vez só)
        pdf_base64 = base64.b64encode(st.session_state.pdf_bytes).decode('utf-8')
        
        # Botão para Preview em Nova Aba (apenas este, sem fallback)
        preview_html_btn = f"""
        <div style="text-align: center; margin-bottom: 1rem;">
            <button id="previewBtn" onclick="openPDFInNewTab('{pdf_base64.replace("'", "\\'")}')" 
                    class="preview-btn" style="width: auto !important; display: inline-block;">
                👁️ Preview em Nova Aba (Carregamento Automático)
            </button>
        </div>
        <script>
        function openPDFInNewTab(base64Data) {{
            try {{
                console.log('Iniciando preview em nova aba...');
                const byteCharacters = atob(base64Data);
                const byteNumbers = new Array(byteCharacters.length);
                for (let i = 0; i < byteCharacters.length; i++) {{
                    byteNumbers[i] = byteCharacters.charCodeAt(i);
                }}
                const byteArray = new Uint8Array(byteNumbers);
                const blob = new Blob([byteArray], {{ type: 'application/pdf' }});
                const blobUrl = URL.createObjectURL(blob);
                const newTab = window.open(blobUrl, '_blank');
                if (!newTab) {{
                    alert('Popup bloqueado! Permita popups para este site.');
                    return;
                }}
                setTimeout(() => URL.revokeObjectURL(blobUrl), 60000);
                console.log('Preview em nova aba aberto com sucesso!');
            }} catch (error) {{
                console.error('Erro no preview:', error);
                alert('Erro no preview: ' + error.message + '. Tente baixar o PDF.');
            }}
        }}
        </script>
        """
        st.components.v1.html(preview_html_btn, height=100, scrolling=False)
        
        # Preview Inline com PDF.js (carrega todas as páginas, renderização fiel e responsiva)
        st.markdown("### Preview Inline do PDF")
        pdf_viewer_html = f"""
        <div class="preview-container">
            <div class="preview-header">Visualização Completa do Documento (Todas as Páginas)</div>
            <div id="pdf-viewer"></div>
        </div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
        <script>
        // Configura PDF.js worker (essencial para renderização fiel)
        pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
        
        async function loadPDF(base64Data) {{
            try {{
                console.log('Carregando PDF inline...');
                const loadingTask = pdfjsLib.getDocument({{
                    data: atob(base64Data),
                    cMapUrl: 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/cmaps/',
                    cMapPacked: true
                }});
                const pdf = await loadingTask.promise;
                
                const container = document.getElementById('pdf-viewer');
                container.innerHTML = ''; // Limpa container
                
                // Renderiza todas as páginas sequencialmente para visualização completa
                for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {{
                    const page = await pdf.getPage(pageNum);
                    const scale = 1.5; // Escala para renderização fiel (ajustável para responsividade)
                    const viewport = page.getViewport({{ scale: scale }});
                    
                    // Cria canvas para cada página
                    const canvas = document.createElement('canvas');
                    const context = canvas.getContext('2d');
                    canvas.height = viewport.height;
                    canvas.width = viewport.width;
                    canvas.style.width = '100%';
                    canvas.style.height = 'auto';
                    canvas.style.borderBottom = '1px solid #E2E8F0';
                    canvas.style.display = 'block';
                    canvas.style.marginBottom = '10px';
                    
                    await page.render({{
                        canvasContext: context,
                        viewport: viewport
                    }}).promise;
                    
                    container.appendChild(canvas);
                    
                    // Adiciona numeração da página para clareza
                    const pageLabel = document.createElement('div');
                    pageLabel.style.textAlign = 'center';
                    pageLabel.style.color = '#718096';
                    pageLabel.style.fontSize = '0.9rem';
                    pageLabel.style.marginTop = '5px';
                    pageLabel.textContent = `Página ${{pageNum}} de ${{pdf.numPages}}`;
                    container.appendChild(pageLabel);
                }}
                
                console.log('PDF inline renderizado com sucesso! Todas as páginas carregadas.');
            }} catch (error) {{
                console.error('Erro no PDF.js:', error);
                document.getElementById('pdf-viewer').innerHTML = '<p style="color: red; text-align: center;">Erro ao carregar preview: ' + error.message + '. Use o botão de nova aba ou download.</p>';
            }}
        }}
        
        // Carrega o PDF assim que o script roda (carregamento automático)
        loadPDF('{pdf_base64.replace("'", "\\'") }');
        
        // Responsividade: Ajusta escala em telas menores
        function adjustScale() {{
            const viewer = document.getElementById('pdf-viewer');
            const canvases = viewer.querySelectorAll('canvas');
            if (window.innerWidth < 768) {{
                canvases.forEach(canvas => {{
                    canvas.style.transform = 'scale(0.8)';
                    canvas.style.transformOrigin = 'top left';
                }});
            }} else {{
                canvases.forEach(canvas => canvas.style.transform = 'none');
            }}
        }}
        window.addEventListener('resize', adjustScale);
        adjustScale(); // Chama inicial
        </script>
        """
        st.components.v1.html(pdf_viewer_html, height=700, scrolling=True)
        
        # Download nativo
        st.download_button(
            label="⬇️ Baixar PDF",
            data=st.session_state.pdf_bytes,
            file_name=st.session_state.pdf_nome,
            mime="application/pdf",
            use_container_width=True
        )

else:
    st.info("💡 Gere um PDF primeiro para ver preview inline, preview em nova aba e download aqui. Persiste na aba atual!")

    st.markdown("---")
    st.markdown("*Desenvolvido com Streamlit e ReportLab. Preview inline com PDF.js (todas páginas, renderização fiel) e botão para nova aba. Totalmente responsivo e moderno.*")


