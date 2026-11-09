#!/usr/bin/env python3
"""Gerar PDF do relatório HTML"""

import subprocess
import sys
import os

print("🔄 Gerando PDF do relatório...")
print()

# Instalar weasyprint
print("📦 Instalando dependências (weasyprint)...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "weasyprint", "-q"])

from weasyprint import HTML

# Caminhos Windows
html_path = r"C:/Users/mateu/OneDrive/Documentos/ELP2/Tarefa_01_Calculo_Termico_Dissipador/RELATORIO_VISUAL.html"
pdf_path = r"C:/Users/mateu/OneDrive/Documentos/ELP2/Tarefa_01_Calculo_Termico_Dissipador/RELATORIO.pdf"

try:
    print(f"📄 Convertendo: RELATORIO_VISUAL.html → RELATORIO.pdf")
    print()
    HTML(filename=html_path).write_pdf(pdf_path)
    
    size = os.path.getsize(pdf_path) / (1024*1024)
    print()
    print("✅ PDF GERADO COM SUCESSO!")
    print(f"   📍 {pdf_path}")
    print(f"   📊 Tamanho: {size:.2f} MB")
    
except Exception as e:
    print(f"❌ Erro: {e}")
    sys.exit(1)
