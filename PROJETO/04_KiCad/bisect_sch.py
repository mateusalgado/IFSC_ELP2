"""Localiza o que o kicad-cli nao consegue ler: testa variantes do esquematico gerado."""
import subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gera_sch as g
from sexp import dumps, QStr

HERE = Path(__file__).resolve().parent
KC = "/mnt/c/Program Files/KiCad/10.0/bin/kicad-cli.exe"
WIN = r"C:\Users\mateu\OneDrive\Documentos\ELP2\PROJETO\04_KiCad\testes"
(HERE / "testes").mkdir(exist_ok=True)


def testa(nome, doc):
    (HERE / "testes" / f"{nome}.kicad_sch").write_text(dumps(doc), encoding="utf-8")
    r = subprocess.run([KC, "sch", "export", "netlist", "--format", "kicadsexpr", "--output", WIN + f"\\{nome}.net", WIN + f"\\{nome}.kicad_sch"],
                       capture_output=True, text=True)
    ok = "falha" not in (r.stdout + r.stderr).lower() and "fail" not in (r.stdout + r.stderr).lower()
    print(f"{'OK  ' if ok else 'FAIL'} {nome}")
    return ok


s = g.build()
head = ["kicad_sch", ["version", 20260101], ["generator", QStr("eeschema")], ["generator_version", QStr("10.0")], ["uuid", QStr(g.ROOT_UUID)], ["paper", QStr("A3")]]
tail = [["sheet_instances", ["path", QStr("/"), ["page", QStr("1")]]]]
# 1) so lib_symbols, um por vez
for lib_id, node in s.libs.items():
    testa("lib_" + lib_id.replace(":", "_").replace("+", "p").replace("-", "m"), head + [["lib_symbols", node]] + tail)
# 2) todas as libs + cada tipo de item
libs = ["lib_symbols"] + list(s.libs.values())
testa("libs_all", head + [libs] + tail)
for kind in ("wire", "junction", "label", "text", "no_connect", "symbol"):
    items = [i for i in s.items if i[0] == kind]
    testa(f"items_{kind}", head + [libs] + items + tail)
