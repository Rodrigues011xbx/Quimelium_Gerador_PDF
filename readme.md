# 📊 Gerador de Relatórios PDF

Este projeto é uma aplicação **Streamlit** integrada com a biblioteca **ReportLab** que permite gerar relatórios em **PDF** de forma simples, interativa e personalizável.

---

## ✨ Funcionalidades

- 📝 Edição de **título, subtítulo, autor e data**  
- 📄 Geração de **capa automática**  
- 📚 Estrutura de relatório com **introdução, análise e conclusão**  
- 📊 Inserção de **tabelas de dados editáveis**  
- 🎨 Estilização customizada (cores, fontes, alinhamentos)  
- 👀 **Visualização do PDF** em tela (embed com iframe)  
- ⬇️ **Download direto** do PDF gerado  

---

## 🚀 Como executar o projeto

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio


python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

pip install -r requirements.txt

streamlit run app.py

http://localhost:8501/


📁 seu-repositorio
 ┣ 📄 app.py              # Código principal da aplicação
 ┣ 📄 requirements.txt    # Lista de dependências
 ┣ 📄 README.md           # Documentação do projeto



---

### 📄 requirements.txt

```txt
## streamlit==1.39.0
## reportlab==4.2.2
