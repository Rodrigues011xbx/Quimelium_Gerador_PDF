     import streamlit as st
     from reportlab.lib.pagesizes import A4
     from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
     from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
     from reportlab.lib.units import inch
     from reportlab.lib import colors
     from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
     from datetime import datetime
     import io
     import base64

     # Função para gerar PDF (adaptada do código original)
     @st.cache_data
     def gerar_pdf(titulo, subtitulo, autor, data_atual, introducao, corpo_texto, conclusao, dados_tabela):
         buffer = io.BytesIO()
         doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
         story = []
         styles = getSampleStyleSheet()

         # Estilos personalizados (mesmos do código original)
         titulo_style = ParagraphStyle('CustomTitulo', parent=styles['Heading1'], fontSize=24, spaceAfter=30, alignment=TA_CENTER, textColor=colors.darkblue)
         subtitulo_style = ParagraphStyle('CustomSubtitulo', parent=styles['Heading2'], fontSize=16, spaceAfter=20, alignment=TA_CENTER, textColor=colors.black)
         corpo_style = ParagraphStyle('CustomCorpo', parent=styles['Normal'], fontSize=12, spaceAfter=12, leftIndent=0, alignment=TA_LEFT)
         info_style = ParagraphStyle('CustomInfo', parent=styles['Normal'], fontSize=10, spaceAfter=12, alignment=TA_RIGHT, textColor=colors.gray)
         rodape_style = ParagraphStyle('CustomRodape', parent=styles['Normal'], fontSize=9, spaceAfter=0, alignment=TA_CENTER, textColor=colors.gray)

         # Capa
         story.append(Paragraph(titulo, titulo_style))
         story.append(Spacer(1, 12))
         story.append(Paragraph(subtitulo, subtitulo_style))
         story.append(Spacer(1, 24))
         story.append(Paragraph(f"Autor: {autor}", info_style))
         story.append(Paragraph(f"Data: {data_atual}", info_style))
         story.append(PageBreak())

         # Seções
         story.append(Paragraph("1. Introdução", styles['Heading2']))
         story.append(Spacer(1, 12))
         story.append(Paragraph(introducao, corpo_style))
         story.append(Spacer(1, 24))

         story.append(Paragraph("2. Análise de Dados", styles['Heading2']))
         story.append(Spacer(1, 12))
         story.append(Paragraph(corpo_texto, corpo_style))
         story.append(Spacer(1, 18))

         # Tabela
         tabela = Table(dados_tabela, colWidths=[1.5*inch, 3*inch, 1*inch, 1.5*inch])
         tabela.setStyle(TableStyle([
             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
             ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
             ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
             ('FONTSIZE', (0, 0), (-1, 0), 12),
             ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
             ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
             ('GRID', (0, 0), (-1, -1), 1, colors.black),
             ('FONTSIZE', (0, 1), (-1, -1), 10),
         ]))
         story.append(tabela)
         story.append(Spacer(1, 24))

         story.append(Paragraph("3. Conclusão", styles['Heading2']))
         story.append(Spacer(1, 12))
         story.append(Paragraph(conclusao, corpo_style))
         story.append(Spacer(1, 24))

         story.append(Paragraph(f"Relatório gerado em {data_atual} por {autor}", rodape_style))

         # Construir PDF no buffer
         doc.build(story)
         buffer.seek(0)
         return buffer.getvalue()

     # Interface Streamlit
     st.set_page_config(page_title="Gerador de Relatórios PDF", page_icon="📊", layout="wide")

     st.title("📊 Gerador de Relatórios PDF")
     st.markdown("---")

     # Sidebar para configurações (responsiva)
     st.sidebar.header("⚙️ Configurações do Relatório")
     titulo = st.sidebar.text_input("Título do Relatório", value="Relatório de Projeto Exemplo")
     subtitulo = st.sidebar.text_input("Subtítulo", value="Análise e Resultados")
     autor = st.sidebar.text_input("Autor", value="Seu Nome ou Equipe")
     data_atual = st.sidebar.date_input("Data", value=datetime.now()).strftime("%d/%m/%Y")

     # Colunas principais para conteúdo
     col1, col2 = st.columns(2)

     with col1:
         st.subheader("1. Introdução")
         introducao = st.text_area("Texto da Introdução", value="""Este relatório apresenta os resultados preliminares do projeto em desenvolvimento. 
     O objetivo principal é analisar os dados coletados e propor melhorias para otimizar o processo.
     Foram utilizados métodos de análise quantitativa e qualitativa para garantir a precisão dos resultados.""" , height=150)

         st.subheader("2. Corpo/Análise")
         corpo_texto = st.text_area("Texto do Corpo", value="""No corpo do relatório, detalhamos os achados principais. 
     Por exemplo, a análise de dados revelou uma taxa de sucesso de 85% nas operações testadas. 
     Recomenda-se a implementação de novas ferramentas para elevar essa métrica para 95%.
     Adicionalmente, identificamos gargalos no fluxo de trabalho que serão abordados na próxima fase.""" , height=150)

     with col2:
         st.subheader("3. Conclusão")
         conclusao = st.text_area("Texto da Conclusão", value="""Em conclusão, o projeto demonstra viabilidade e potencial de impacto. 
     As próximas etapas incluem testes em escala maior e integração com sistemas existentes. 
     Agradecemos pela atenção e estamos abertos a feedbacks.""" , height=150)

         st.subheader("Tabela de Dados")
         st.markdown("Edite a tabela abaixo (adicione/remova linhas se necessário):")
         # Tabela editável simples (4 colunas fixas, até 5 linhas editáveis)
         num_linhas = st.number_input("Número de linhas na tabela (máx 10)", min_value=1, max_value=10, value=3)
         dados_tabela = [['Item', 'Descrição', 'Valor', 'Status']]  # Cabeçalho fixo
         for i in range(num_linhas):
             with st.expander(f"Linha {i+1}"):
                 item = st.text_input(f"Item {i+1}", value=f"Operação {i+1}" if i < 3 else "")
                 desc = st.text_input(f"Descrição {i+1}", value=f"Processamento de dados" if i==0 else f"Análise estatística" if i==1 else f"Relatório final" if i==2 else "")
                 valor = st.text_input(f"Valor {i+1}", value="R$ 1.500,00" if i==0 else "R$ 2.000,00" if i==1 else "R$ 800,00" if i==2 else "")
                 status = st.selectbox(f"Status {i+1}", ["Concluído", "Em Andamento", "Pendente"], index=0 if i==0 else 1 if i==1 else 2)
                 dados_tabela.append([item, desc, valor, status])

     # Botão para gerar PDF
     if st.button("🔥 Gerar e Baixar PDF", type="primary", use_container_width=True):
         with st.spinner("Gerando PDF..."):  # Mostra loading
             pdf_bytes = gerar_pdf(titulo, subtitulo, autor, data_atual, introducao, corpo_texto, conclusao, dados_tabela)
         
         st.success("PDF gerado com sucesso! 📄")
         st.markdown("### Visualização do PDF:")
         
         # Embed do PDF usando iframe com base64 (visualização inline)
         pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
         st.markdown(
             f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="600px" type="application/pdf" style="border: 1px solid #ccc; border-radius: 5px;"></iframe>',
             unsafe_allow_html=True
         )
         
         # Download
         b64 = base64.b64encode(pdf_bytes).decode()
         href = f'<a href="data:application/pdf;base64,{b64}" download="relatorio.pdf" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; font-weight: bold;">⬇️ Baixar PDF</a>'
         st.markdown(href, unsafe_allow_html=True)
         
         st.info("💡 Dica: Use o zoom do navegador para ver detalhes do PDF. Se o embed não carregar, o download sempre funciona!")

     # Rodapé
     st.markdown("---")
     st.markdown("*Desenvolvido com Streamlit e ReportLab. Hospedado no Streamlit Cloud.*")
     
