"""Roda todos os scripts de projeto na ordem correta e consolida as saidas em
resultados/RESULTADOS_TEORIA.md (fonte das tabelas do relatorio).
Uso (WSL): python3 run_all.py
"""
import subprocess, sys, os
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDEM = ["entrada.py", "flyback.py", "transformador.py", "flyback.py", "saida.py", "snubber.py",
         "uc3845.py", "semicondutores.py", "compensador.py", "emi.py"]
TITULOS = {"entrada.py": "Estágio de entrada", "flyback.py": "Projeto elétrico do flyback", "transformador.py": "Transformador",
           "saida.py": "Filtro de saída", "snubber.py": "Snubber", "uc3845.py": "UC3845", "semicondutores.py": "Semicondutores e térmico",
           "compensador.py": "Compensador", "emi.py": "Filtro de EMI"}
(HERE / "resultados" / "trafo.json").unlink(missing_ok=True)
out = ["# Resultados dos cálculos de projeto (gerado por run_all.py)\n"]
seen = set()
for s in ORDEM:
    r = subprocess.run([sys.executable, s], cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"ERRO em {s}:\n{r.stderr}"); sys.exit(1)
    if s == "flyback.py" and s not in seen:
        seen.add(s); continue            # guarda so a rodada final do flyback
    out.append(f"\n\n---\n\n<!-- {s} -->\n" + r.stdout)
    print(f"ok  {s}")
(HERE / "resultados" / "RESULTADOS_TEORIA.md").write_text("\n".join(out), encoding="utf-8")
print("-> resultados/RESULTADOS_TEORIA.md")
