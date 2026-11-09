"""Pedido de compra para UM protótipo (Possibilidade II) a partir da BOM B (05_BOM_Custo/BOM.csv).
Regras de sobressalentes: semicondutores, CI, opto, TL431 e fusível +1; resistores e cerâmicos +2 (minimos de loja);
eletroliticos +1; PCI = lote minimo de 5; transformador = 2 núcleos/carreteis (um para errar) + fio.
Saida: PEDIDO_COMPRA.csv e PEDIDO_COMPRA.md (quantidades, fornecedor sugerido, custo estimado da compra).
Uso: python pedido_compra.py
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BOM = HERE.parent / "05_BOM_Custo" / "BOM.csv"
rows = list(csv.DictReader(open(BOM, encoding="utf-8-sig"), delimiter=";"))
rows = [r for r in rows if r["Refs"] and not r["Refs"].startswith("TOTAL")]


def sobressalente(r):
    d = (r["Descricao"] + " " + r["Bloco"]).lower()
    ref = r["Refs"]
    if "pci" in d:
        return 5, "lote mínimo do fabricante (5 placas)"
    if ref.startswith("T1") or "transformador" in d or "núcleo" in d or "nucleo" in d or "carretel" in d:
        return 2, "um para errar o enrolamento"
    if "fio" in d:
        return 1, "rolo/metragem já cobre 2 trafos"
    if any(k in d for k in ("mosfet", "diodo", "schottky", "ponte", "uc3845", "tl431", "opto", "fusível", "fusivel", "varistor", "ntc")):
        return 1, "sobressalente (componente sensível a erro de montagem/ensaio)"
    if any(k in d for k in ("resistor", "cerâmic", "ceramic", "filme", "x2", "y1")):
        return 2, "mínimo de loja / reserva"
    if "eletrol" in d or "capacitor" in d:
        return 1, "reserva"
    return 0, ""


out = []
total = 0.0
for r in rows:
    try:
        q = int(float(r["Qtd"].replace(",", ".")))
    except ValueError:
        q = 1
    extra, motivo = sobressalente(r)
    if "pci" in (r["Descricao"] + r["Bloco"]).lower():
        qc = extra; preco = float(r["US$ unit. (1)"]) * 5  # lote de 5 = preco unit. rateado x 5
    else:
        qc = q + extra; preco = float(r["US$ unit. (1)"]) * qc
    total += preco
    out.append(dict(Refs=r["Refs"], Descricao=r["Descricao"], Valor=r["Valor / especificacao"], Fabricante=r["Fabricante"], PN=r["Part number"],
                    Fornecedor=r["Distribuidor / codigo"], Qtd_placa=q, Qtd_comprar=qc, Motivo=motivo, USD=round(preco, 2), Obs=r["Observacao"]))

with open(HERE / "PEDIDO_COMPRA.csv", "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys()), delimiter=";")
    w.writeheader(); w.writerows(out)
    w.writerow(dict(Refs="TOTAL", USD=round(total, 2)))

md = ["# Pedido de compra – 1 protótipo (Possibilidade II) – revisão B", "",
      f"Gerado de `05_BOM_Custo/BOM.csv` por `pedido_compra.py`. Quantidades = por placa + sobressalentes; preços de referência (orçamento de engenharia, out/nov 2026), sem frete nem impostos. "
      f"**Total estimado: US$ {total:.2f} (≈ R$ {total * 5.5:.0f} a R$ 5,50/US$)** — a PCI entra pelo lote mínimo de 5 placas (US$ 48 com frete).", "",
      "Prioridade de compra (prazo de chegada): 1) PCI (enviar `04_KiCad/gerbers/fonte_flyback_12V3A_B_gerbers.zip`); 2) importados de prazo longo (STF13N65M2, STPS20H100CT, choke Schaffner, Rubycon ZLH, UC3845, PC817); "
      "3) núcleo/carretel/fio (Thornton ou loja nacional); 4) passivos comuns e mecânica (loja nacional).", "",
      "| Refs | Descrição | Valor | Fabricante / PN | Fornecedor | por placa | comprar | motivo | US$ |", "|---|---|---|---|---|---|---|---|---|"]
for o in out:
    md.append(f"| {o['Refs']} | {o['Descricao']} | {o['Valor']} | {o['Fabricante']} {o['PN']} | {o['Fornecedor']} | {o['Qtd_placa']} | {o['Qtd_comprar']} | {o['Motivo']} | {o['USD']:.2f} |")
md.append(f"| **Total** | | | | | | | | **{total:.2f}** |")
md += ["", "## Itens fora da BOM (bancada e montagem)", "",
       "| Item | Para quê | Observação |",
       "|---|---|---|",
       "| Resistor de fio 4,7 kΩ / 10 W com cabos isolados | descarga de C1 (10 J) | obrigatório antes de tocar na placa |",
       "| Resistores de carga 4 Ω / 40 W e 8 Ω / 20 W (ou carga eletrônica) | 100 % e 50 % de carga | com dissipador |",
       "| Fita de poliéster (Mylar) 10 mm, verniz/esmalte | transformador | 3 camadas entre primário e secundário |",
       "| Soquete DIP-8 | U1 | já na BOM (mecânica) — conferir |",
       "| Estanho 0,8 mm, fluxo, isopropílico | montagem | |",
       "| Chave de curto com fio curto ≤ 50 mΩ | ensaio de curto (seção 5.4 do guia) | só após liberar os limites |",
       "| Termopar ou termômetro IR | térmico de Q1, D1, R5/R6, T1 | |",
       "| Transformador isolador, variac, sonda diferencial ≥ 700 V, multímetro CAT II 600 V, LCR, wattímetro | laboratório | confirmar disponibilidade com o professor antes de comprar |"]
(HERE / "PEDIDO_COMPRA.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"{len(out)} itens; total US$ {total:.2f} (R$ {total * 5.5:.0f})")
