#!/usr/bin/env python3
"""Converter markdown para PDF (estilo simples, sem customizações)"""

import subprocess
import sys

print("🔄 Gerando PDF simples do markdown...")
print()

# Verificar se pandoc está disponível no WSL
result = subprocess.run(
    ["wsl", "which", "pandoc"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print("✅ Pandoc encontrado no WSL")
    print()
    print("🔨 Convertendo RELATORIO.md → RELATORIO.pdf...")
    
    # Usar pandoc via WSL
    md_path = r"C:\Users\mateu\OneDrive\Documentos\ELP2\Tarefa_01_Calculo_Termico_Dissipador\RELATORIO.md"
    pdf_path = r"C:\Users\mateu\OneDrive\Documentos\ELP2\Tarefa_01_Calculo_Termico_Dissipador\RELATORIO.pdf"
    
    # Converter com pandoc (saída padrão)
    result = subprocess.run([
        "wsl", "pandoc",
        "/mnt/c/Users/mateu/OneDrive/Documentos/ELP2/Tarefa_01_Calculo_Termico_Dissipador/RELATORIO.md",
        "-o", "/mnt/c/Users/mateu/OneDrive/Documentos/ELP2/Tarefa_01_Calculo_Termico_Dissipador/RELATORIO.pdf",
        "-V", "geometry:margin=2cm"
    ])
    
    if result.returncode == 0:
        print("✅ PDF gerado com sucesso!")
        print(f"📍 {pdf_path}")
    else:
        print("❌ Erro ao gerar PDF")
        sys.exit(1)
else:
    print("❌ Pandoc não encontrado no WSL")
    print()
    print("Para instalar no WSL, execute:")
    print("   wsl sudo apt update && sudo apt install -y pandoc")
    sys.exit(1)

