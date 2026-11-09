"""Convergencia: diodos de grampo suaves, opcoes do solver, timeout por caso em roda.py."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
g = root / "gera_netlist.py"; s = g.read_text(encoding="utf-8")
s = s.replace(".model DIDEAL D(Is=1e-12 n=0.5 Rs=1m)", ".model DIDEAL D(Is=1e-14 n=1 Rs=0.1 Cjo=10p)")
s = s.replace(".options reltol=0.003 abstol=1e-9 vntol=1e-6 method=gear", ".options reltol=0.005 abstol=1e-8 vntol=1e-5 method=gear itl4=50 gmin=1e-10")
# comparador e limiar com transicao suave (evita descontinuidade dura)
s = s.replace("B_cmp uc_rst 0 V=if(V(isns) > V(uc_th), 1, 0)", "B_cmp uc_rst 0 V=0.5+0.5*tanh((V(isns)-V(uc_th))*2000)")
g.write_text(s, encoding="utf-8")
r = root / "roda.py"; t = r.read_text(encoding="utf-8")
t = t.replace('    subprocess.run([LTSPICE, "-b", "-Run", f"{WIN_RUNS}\\\\{caso}.net"], check=False, timeout=7200)',
              '''    try:
        subprocess.run([LTSPICE, "-b", "-Run", f"{WIN_RUNS}\\\\{caso}.net"], check=False, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        subprocess.run(["/mnt/c/Windows/System32/taskkill.exe", "/F", "/IM", "LTspice.exe"], check=False, capture_output=True)
        print("   TIMEOUT -> LTspice morto", flush=True)''')
t = t.replace('WIN_RUNS = r"C:\\Users\\mateu\\OneDrive\\Documentos\\ELP2\\PROJETO\\03_Simulacao\\runs"',
              'WIN_RUNS = r"C:\\Users\\mateu\\OneDrive\\Documentos\\ELP2\\PROJETO\\03_Simulacao\\runs"\nTIMEOUT_S = 1500')
r.write_text(t, encoding="utf-8")
print("ok", "tanh" in s, "TIMEOUT_S" in t)
