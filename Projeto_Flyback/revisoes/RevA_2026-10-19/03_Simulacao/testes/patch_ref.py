"""Referencia as medicoes do secundario ao no sgnd (terra do secundario flutua em relacao ao 0 do primario)
e adiciona figura da comutacao em plota.py."""
from pathlib import Path
root = Path(__file__).resolve().parent.parent
p = root / "gera_netlist.py"; s = p.read_text(encoding="utf-8")
s = s.replace("V(vcc)=15 V(vccc)=15 V(comp)=2.5\\n\"", "V(vcc)=15 V(vccc)=15 V(comp)=2.5 V(sgnd)=0\\n\"")
s = s.replace("V(vcc)=8.2 V(vccc)=8.2\\n\" if startup", "V(vcc)=8.2 V(vccc)=8.2 V(sgnd)=0\\n\" if startup")
for a, b in ((".meas TRAN Vo_avg AVG V(vo)", ".meas TRAN Vo_avg AVG V(vo,sgnd)"),
             (".meas TRAN Vo_pp PP V(vo)", ".meas TRAN Vo_pp PP V(vo,sgnd)"),
             (".meas TRAN Vo_min MIN V(vo)", ".meas TRAN Vo_min MIN V(vo,sgnd)"),
             (".meas TRAN Vo_max MAX V(vo)", ".meas TRAN Vo_max MAX V(vo,sgnd)"),
             (".meas TRAN Po AVG V(vo)*I(Rload)", ".meas TRAN Po AVG V(vo,sgnd)*I(Rload)")):
    assert a in s, a
    s = s.replace(a, b)
p.write_text(s, encoding="utf-8")

q = root / "plota.py"; t = q.read_text(encoding="utf-8")
t = t.replace('w["v(vo)"] - w["v(vo)"].mean()', '(w["v(vo)"] - w["v(sgnd)"]) - (w["v(vo)"] - w["v(sgnd)"]).mean()')
t = t.replace('w["v(vout)"] - w["v(vout)"].mean()', '(w["v(vout)"] - w["v(sgnd)"]) - (w["v(vout)"] - w["v(sgnd)"]).mean()')
t = t.replace('ax[1].plot(tt, w["v(vo)"], "C1")', 'ax[1].plot(tt, w["v(vo)"] - w["v(sgnd)"], "C1")')
fig_comut = '''

def fig_comut(caso, d, t_end=None):
    """zoom no desligamento e no ligamento do MOSFET (ultimo ciclo)"""
    t = d["time"]
    t1 = t[-1] if t_end is None else t_end
    w = janela(d, t1 - 1.2 / FS, t1)
    g = w["v(gate)"]; tw = w["time"]
    # instante de desligamento: ultima descida do gate abaixo de 5 V
    idx = np.where((g[:-1] > 5) & (g[1:] <= 5))[0]
    ion = np.where((g[:-1] < 5) & (g[1:] >= 5))[0]
    if len(idx) == 0 or len(ion) == 0:
        return
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    for a, i0, titulo in ((ax[0], ion[-1], "ligamento"), (ax[1], idx[-1], "desligamento")):
        t0 = tw[i0]
        z = janela(d, t0 - 150e-9, t0 + 250e-9)
        tz = (z["time"] - t0) * 1e9
        a.plot(tz, z["v(drain)"], "C3", label="v_DS (V)")
        a2 = a.twinx(); a2.plot(tz, z["id(m1)"], "C0", label="i_D (A)"); a2.plot(tz, z["v(gate)"], "C2", lw=.8, label="v_GS (V)")
        a.set_xlabel("tempo (ns)"); a.set_ylabel("v_DS (V)", color="C3"); a2.set_ylabel("i_D (A), v_GS (V)")
        a.set_title(f"{titulo}"); a.grid(alpha=.3)
        h1, l1 = a.get_legend_handles_labels(); h2, l2 = a2.get_legend_handles_labels(); a.legend(h1 + h2, l1 + l2, fontsize=8, loc="center right")
    fig.suptitle(f"{caso}: comutação do MOSFET"); fig.tight_layout()
    fig.savefig(OUT / f"{caso}_comut.png", dpi=140); plt.close(fig)
'''
t = t.replace('\n\nif __name__ == "__main__":', fig_comut + '\n\nif __name__ == "__main__":')
t = t.replace('        fig_rede(caso, d)\n', '        fig_rede(caso, d)\n        fig_comut(caso, d)\n')
q.write_text(t, encoding="utf-8")
print("ok")
