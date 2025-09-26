from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime

# =====================================
# CONFIGURAÇÕES EDITÁVEIS - ALTERE AQUI
# =====================================
TITULO_RELATORIO = "Relatório de Projeto Exemplo"
SUBTITULO = "Análise e Resultados"
AUTOR = "Seu Nome ou Equipe"
DATA_ATUAL = datetime.now().strftime("%d/%m/%Y")  # Data automática, ou altere manualmente

# Conteúdo das seções (texto editável)
INTRODUCAO = """
Este relatório apresenta os resultados preliminares do projeto em desenvolvimento. 
O objetivo principal é analisar os dados coletados e propor melhorias para otimizar o processo.
Foram utilizados métodos de análise quantitativa e qualitativa para garantir a precisão dos resultados.
"""

CORPO_TEXTO = """
No corpo do relatório, detalhamos os achados principais. 
Por exemplo, a análise de dados revelou uma taxa de sucesso de 85% nas operações testadas. 
Recomenda-se a implementação de novas ferramentas para elevar essa métrica para 95%.
Adicionalmente, identificamos gargalos no fluxo de trabalho que serão abordados na próxima fase.
"""

CONCLUSAO = """
Em conclusão, o projeto demonstra viabilidade e potencial de impacto. 
As próximas etapas incluem testes em escala maior e integração com sistemas existentes. 
Agradecemos pela atenção e estamos abertos a feedbacks.
"""

# Dados da tabela de exemplo (adicione/remova linhas conforme necessário)
DADOS_TABELA = [
    ['Item', 'Descrição', 'Valor', 'Status'],
    ['Operação 1', 'Processamento de dados', 'R$ 1.500,00', 'Concluído'],
    ['Operação 2', 'Análise estatística', 'R$ 2.000,00', 'Em Andamento'],
    ['Operação 3', 'Relatório final', 'R$ 800,00', 'Pendente']
]

# Nome do arquivo de saída (altere se quiser)
NOME_ARQUIVO_PDF = "relatorio.pdf"

# =====================================
# CÓDIGO PRINCIPAL - NÃO ALTERE ABAIXO
# =====================================
def gerar_relatorio_pdf():
    # Configurações do documento
    doc = SimpleDocTemplate(NOME_ARQUIVO_PDF, pagesize=A4, rightMargin=72, leftMargin=72,
                            topMargin=72, bottomMargin=18)
    story = []  # Lista de elementos do PDF
    styles = getSampleStyleSheet()  # Estilos padrão do ReportLab

    # Estilo personalizado para título centralizado e grande
    titulo_style = ParagraphStyle(
        'CustomTitulo',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkgreen
    )

    # Estilo para subtítulo
    subtitulo_style = ParagraphStyle(
        'CustomSubtitulo',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.black
    )

    # Estilo para parágrafos normais
    corpo_style = ParagraphStyle(
        'CustomCorpo',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=12,
        leftIndent=0,
        alignment=TA_LEFT
    )

    # Adicionar título
    story.append(Paragraph(TITULO_RELATORIO, titulo_style))
    story.append(Spacer(1, 12))  # Espaçador
    story.append(Paragraph(SUBTITULO, subtitulo_style))
    story.append(Spacer(1, 24))  # Espaçador maior

    # Informações da capa (autor e data)
    info_style = ParagraphStyle(
        'CustomInfo',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=12,
        alignment=TA_RIGHT,
        textColor=colors.gray
    )
    story.append(Paragraph(f"Autor: {AUTOR}", info_style))
    story.append(Paragraph(f"Data: {DATA_ATUAL}", info_style))
    story.append(PageBreak())  # Nova página para o conteúdo

    # Seção de Introdução
    story.append(Paragraph("1. Introdução", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(INTRODUCAO, corpo_style))
    story.append(Spacer(1, 24))

    # Seção do Corpo com Tabela
    story.append(Paragraph("2. Análise de Dados", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(CORPO_TEXTO, corpo_style))
    story.append(Spacer(1, 18))

    # Criar tabela
    tabela = Table(DADOS_TABELA, colWidths=[1.5*inch, 3*inch, 1*inch, 1.5*inch])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Cabeçalho cinza
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Linhas alternadas
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Bordas
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    story.append(tabela)
    story.append(Spacer(1, 24))

    # Seção de Conclusão
    story.append(Paragraph("3. Conclusão", styles['Heading2']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(CONCLUSAO, corpo_style))
    story.append(Spacer(1, 24))

    # Rodapé simples (pode ser expandido com canvas)
    rodape_style = ParagraphStyle(
        'CustomRodape',
        parent=styles['Normal'],
        fontSize=9,
        spaceAfter=0,
        alignment=TA_CENTER,
        textColor=colors.gray
    )
    story.append(Paragraph(f"Relatório gerado em {DATA_ATUAL} por {AUTOR}", rodape_style))

    # Construir o PDF
    doc.build(story)
    print(f"PDF gerado com sucesso: {NOME_ARQUIVO_PDF}")

# Executar a função principal
if __name__ == "__main__":
    gerar_relatorio_pdf()
