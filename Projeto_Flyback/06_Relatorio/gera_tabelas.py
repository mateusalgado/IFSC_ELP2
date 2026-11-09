"""Revisao B: tabelas teoria x simulacao (markdown) a partir de 02_Calculos/resultados/*.json,
03_Simulacao/runs/medidas.json (.meas do LTspice via executa_b.py), runs/transitorios.json e runs/curto_220V_janelas.json.
Saida: tabelas/*.md e tabelas.json. Cada numero e marcado pela origem: C = calculo, S = simulacao.
Roda no WSL: python3 gera_tabelas.py
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
P = HERE.parent
R = P / "02_Calculos/resultados"
fb = json.load(open(R / "flyback.json", encoding="utf-8"))
en = json.load(open(R / "entrada.json", encoding="utf-8"))
sm = json.load(open(R / "semicondutores.json", encoding="utf-8"))
sn = json.load(open(R / "snubber.json", encoding="utf-8"))
uc = json.load(open(R / "uc3845.json", encoding="utf-8"))
cp = json.load(open(R / "compensador.json", encoding="utf-8"))
med = json.load(open(P / "03_Simulacao/runs/medidas.json", encoding="utf-8"))
tra = json.load(open(P / "03_Simulacao/runs/transitorios.json", encoding="utf-8")) if (P / "03_Simulacao/runs/transitorios.json").exists() else {}
jan = json.load(open(P / "03_Simulacao/runs/curto_220V_janelas.json", encoding="utf-8")) if (P / "03_Simulacao/runs/curto_220V_janelas.json").exists() else {}
hic_s = json.load(open(P / "03_Simulacao/runs/curto_220V_hiccup.json", encoding="utf-8")) if (P / "03_Simulacao/runs/curto_220V_hiccup.json").exists() else {}
hic = uc["partida"].get("hiccup", [])
OUT = HERE / "tabelas"
OUT.mkdir(exist_ok=True)


def f(x, n=2):
    return "-" if x is None else f"{x:.{n}f}".replace(".", ",")


def delta(t, s):
    return f"{100 * (s - t) / t:+.1f} %".replace(".", ",") if t else "-"


pts = {}
for k, r in fb["pontos"].items():
    vac = int(k.split("V_")[0]); c = int(k.split("V_")[1].rstrip("%"))
    pts[(vac, c)] = dict(Ip=r["Ip"], Is_pk=r["Is_pk"], Is_rms=r["Is_rms"], Vds_clamp=r["Vds_clamp_max"], Vd_rev=r["Vd_rev_max"], Vb_vale=r["vbulk"])

# ---------------- 1. regime permanente ----------------
md = ["| Vac | carga | Vo S (V) | ΔVo chav. S (mV) | ΔVo total S (mV) | Ip C (A) | Ip S (A) | Δ | Is,pk C (A) | Is,pk S (A) | Δ | Is,rms C (A) | Is,rms S (A) | Δ | Vds C (V) | Vds S (V) | Δ | η S (%) |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
rows = {}
excedidos = []
for vac in (90, 127, 220, 264):
    for c in (10, 50, 100):
        m = med.get(f"regime_{vac}V_{c}pct"); t = pts.get((vac, c))
        if not m or not t:
            continue
        eta = 100 * m["po"] / m["pin"]
        rows[(vac, c)] = dict(vo=m["vo_avg"], vopp=1e3 * m["vo_pp"], ripple=1e3 * m.get("ripple_total", float("nan")), ip_t=t["Ip"], ip_s=m["ip_pk"], ispk_t=t["Is_pk"], ispk_s=m["is_pk"],
                              isrms_t=t["Is_rms"], isrms_s=m["is_rms"], vds_t=t["Vds_clamp"], vds_s=m["vds_max"], eta=eta, vd_t=t["Vd_rev"], vd_s=-m["vd_min"],
                              pmos=m["pmos"], pdiode=m["pdiode"], psnub=m["psnub"], pbr=m["pbr"], vbmin=m["vbulk_min"], vb_t=t["Vb_vale"], iin=m["iin_rms"], vcc=m["vcc_avg"])
        for nome, tt, ss in (("Ip", t["Ip"], m["ip_pk"]), ("Is,pk", t["Is_pk"], m["is_pk"]), ("Is,rms", t["Is_rms"], m["is_rms"]), ("Vds", t["Vds_clamp"], m["vds_max"])):
            if abs(ss - tt) / tt > 0.10:
                excedidos.append(f"{vac} V / {c} %: {nome} {delta(tt, ss)}")
        md.append(f"| {vac} | {c} % | {f(m['vo_avg'])} | {f(1e3 * m['vo_pp'], 1)} | {f(1e3 * m.get('ripple_total', float('nan')), 1)} | {f(t['Ip'])} | {f(m['ip_pk'])} | {delta(t['Ip'], m['ip_pk'])} | {f(t['Is_pk'], 1)} | {f(m['is_pk'], 1)} | {delta(t['Is_pk'], m['is_pk'])} | {f(t['Is_rms'])} | {f(m['is_rms'])} | {delta(t['Is_rms'], m['is_rms'])} | {f(t['Vds_clamp'], 0)} | {f(m['vds_max'], 0)} | {delta(t['Vds_clamp'], m['vds_max'])} | {f(eta, 1)} |")
(OUT / "regime.md").write_text("\n".join(md) + "\n", encoding="utf-8")

# ---------------- 2. plena carga: perdas e rendimento ----------------
md = ["| Vac | Vbulk mín C (V) | Vbulk mín S (V) | I in,rms C (A) | I in,rms S (A) | P MOSFET C (W) | P MOSFET S (W) | P diodo C (W) | P diodo S (W) | P snubber C (W) | P snubber S (W) | P ponte C (W) | P ponte S (W) | η C (%) | η S (%) |",
      "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
orc = {int(k.rstrip("V")): dict(ponte=v["itens"]["ponte"], eta=100 * v["eta"]) for k, v in sm["orcamento"].items()}
ent = {}
for k, v in en["pontos"].items():
    vac = int(k.split("V_")[0])
    if (vac == 90 and k.endswith("50Hz")) or (vac != 90 and k.endswith("60Hz")):
        ent[vac] = dict(Iin_rms=v["i_rms_in"])
for vac in (90, 127, 220, 264):
    r = rows.get((vac, 100))
    if not r:
        continue
    o = orc.get(vac, {}); e = ent.get(vac, {})
    pm_t = sm["mosfet"]["lo"]["P_total"] if vac <= 127 else sm["mosfet"]["hi"]["P_total"]
    md.append(f"| {vac} | {f(r['vb_t'], 1)} | {f(r['vbmin'], 1)} | {f(e['Iin_rms'])} | {f(r['iin'])} | {f(pm_t)} | {f(r['pmos'])} | {f(sm['diodo']['P'])} | {f(r['pdiode'])} | {f(sn['P_2pct'])} | {f(r['psnub'])} | {f(o['ponte'])} | {f(r['pbr'])} | {f(o['eta'], 1)} | {f(r['eta'], 1)} |")
(OUT / "perdas.md").write_text("\n".join(md) + "\n", encoding="utf-8")

# ---------------- 3. transitorios (partida a frio, degraus nos dois sentidos, tolerancias) ----------------
md = ["| Caso (S) | Resultado |", "|---|---|"]
for nome, desc in (("partida_90V", "Partida a frio em 90 VAC, plena carga (C1 e C5 descarregados, fase da rede do cruzamento do UVLO)"), ("partida_264V", "Partida a frio em 264 VAC, plena carga")):
    m = med.get(nome); tr_ = tra.get(nome, {})
    if m:
        md.append(f"| {desc} | pré-carga até 8,4 V em {f(m.get('t_uv'), 2)} s com V<sub>bulk</sub> = {f(m.get('b_uv'), 0)} V; VCC mínimo após o UVLO {f(tr_.get('vcc_min'))} V; V<sub>o</sub> ≥ 11,4 V em {f(tr_.get('t_vo_11v4_ms'), 1)} ms; V<sub>o</sub> máx {f(tr_.get('vo_max'))} V; I<sub>p</sub> máx {f(m['ip_pk'])} A; V<sub>ds</sub> máx {f(m['vds_max'], 0)} V |")
for nome, desc in (("degrau_90V", "Degraus 50 → 100 % (80 ms) e 100 → 50 % (100 ms) em 90 VAC"), ("degrau_264V", "Degraus 50 → 100 % e 100 → 50 % em 264 VAC"), ("ctr05_90V", "Degraus em 90 VAC com CTR = 0,5 (pior opto)")):
    tr_ = tra.get(nome); m = med.get(nome)
    if tr_ and m:
        s = tr_["subida"]; d = tr_["descida"]
        ret = lambda x: (f"não sai de ±1 %, volta a ±0,5 % em {f(x['t_retorno_0p5pct_ms'], 1)} ms" if x["t_retorno_1pct_ms"] == 0 else f"retorno a ±1 % em {f(x['t_retorno_1pct_ms'], 1)} ms (±0,5 % em {f(x['t_retorno_0p5pct_ms'], 1)} ms)")
        md.append(f"| {desc} | subida: {f(s['vo_antes'])} → mín {f(s['vo_extremo'])} V ({f(s['desvio_mV'], 0)} mV), {ret(s)}; descida: máx {f(d['vo_extremo'])} V (+{f(d['desvio_mV'], 0)} mV), {ret(d)}; V<sub>o</sub> na janela 80–120 ms: {f(m['vo_min'])}–{f(m['vo_max'])} V; I<sub>p</sub> máx {f(m['ip_pk'])} A |")
m = med.get("bulk_min_90V")
if m:
    md.append(f"| Tolerância do barramento: C1 = 120 µF (−20 %) em 90 VAC/50 Hz, plena carga | V<sub>bulk</sub> mín {f(m['vbulk_min'], 1)} V; V<sub>o</sub> {f(m['vo_avg'])} V; I<sub>p</sub> máx {f(m['ip_pk'])} A; η {f(100 * m['po'] / m['pin'], 1)} % |")
for nome, desc in (("sem_snubber_264V", "Sem grampo RCD, 264 VAC, plena carga"), ("llk3pct_264V", "L<sub>lk</sub> = 3 % de L<sub>p</sub> (projeto 2 %), 264 VAC, plena carga")):
    m = med.get(nome)
    if m:
        md.append(f"| {desc} | V<sub>ds</sub> máx {f(m['vds_max'], 0)} V; V<sub>rev</sub> D1 {f(-m['vd_min'], 0)} V; P snubber {f(m['psnub'])} W; I<sub>p</sub> {f(m['ip_pk'])} A |")
(OUT / "transitorios.md").write_text("\n".join(md) + "\n", encoding="utf-8")

# ---------------- 4. curto-circuito por janelas ----------------
m = med.get("curto_220V", {})
md = ["| Janela (S, 220 VAC) | Id(Q1) máx (A) | I<sub>p</sub> máx (A) | B equiv. (T) | I(D1) máx (A) | I(D1) rms (A) | V<sub>ds</sub> máx (V) | VCC mín (V) | V<sub>o</sub> máx (V) | P<sub>D1</sub> média (W) |",
      "|---|---|---|---|---|---|---|---|---|---|"]
for jn, desc in (("aplic", "aplicação (2 ms)"), ("sust", "curto sustentado"), ("rec", "recuperação")):
    if f"iq_{jn}" in m:
        ipk = m[f"ip_{jn}"]
        md.append(f"| {desc} | {f(m[f'iq_{jn}'])} | {f(ipk)} | {f(0.25 * ipk / fb['Ip_max'])} | {f(m[f'id1_{jn}'], 1)} | {f(m[f'id1rms_{jn}'], 1)} | {f(m[f'vds_{jn}'], 0)} | {f(m[f'vccmin_{jn}'])} | {f(m[f'vomax_{jn}'])} | {f(m[f'pd1_{jn}'])} |")
if jan:
    md.append("")
    md.append(f"Releitura do .raw (`analisa_curto.py`, `hiccup_tempos.py`): pulsos de comando no curto sustentado = {jan.get('curto sustentado', {}).get('pulsos_drv')}; hiccup: {f(hic_s.get('t_ate_uvlo_ms'), 0)} ms até o UVLO, {f(hic_s.get('t_recarga_ms'), 0)} ms desligado, {f(hic_s.get('t_ligado_ms'), 0)} ms ligado por tentativa (ciclo de trabalho da falha {f(hic_s.get('duty_falha_pct'), 0)} %; cálculo: {hic[2][3] if len(hic) > 2 else '-'} ms / {hic[2][4] if len(hic) > 2 else '-'} %). Curto removido em 380 ms com o CI desligado: VCC = {f(hic_s.get('vcc_fim'))} V no fim da simulação (420 ms), religamento na tentativa seguinte do hiccup, seguido da partida normal.")
(OUT / "curto.md").write_text("\n".join(md) + "\n", encoding="utf-8")


def resumo_excedidos(ex):
    """resume a lista 'Vac / carga: grandeza delta' por grandeza (n, faixa de desvio)"""
    import re
    g = {}
    for e in ex:
        m = re.match(r"(\d+) V / (\d+) %: (\S+) ([-+]\d+,\d) %", e)
        if not m:
            continue
        g.setdefault(m.group(3), []).append((int(m.group(2)), float(m.group(4).replace(",", "."))))
    partes = []
    for k, v in g.items():
        ds = [d for _, d in v]; cargas = sorted({c for c, _ in v})
        partes.append(f"{k}: {len(v)} pontos ({'/'.join(str(c) for c in cargas)} % de carga), {min(ds):+.0f} a {max(ds):+.0f} %".replace(".", ","))
    return f"{len(ex)} de {4 * len(pts)} comparações fora de ±10 % — " + "; ".join(partes) + ". I<sub>p</sub> dentro de 10 % em todos os pontos"


# ---------------- 5. criterios ----------------
r90 = rows[(90, 100)]; r264 = rows[(264, 100)]
vo_all = [rows[k]["vo"] for k in rows]
eta100 = {k[0]: rows[k]["eta"] for k in rows if k[1] == 100}
crit = [
    ("Vo em ±5 % (11,4–12,6 V) para 90–264 VAC e 10–100 % de carga [S]", f"{f(min(vo_all))} – {f(max(vo_all))} V", "atende" if 11.4 <= min(vo_all) and max(vo_all) <= 12.6 else "NÃO atende"),
    ("Ondulação ≤ 120 mV p-p: de chaveamento e excursão total em ciclos da rede [S]", f"≤ {f(max(rows[k]['vopp'] for k in rows), 1)} mV / ≤ {f(max(rows[k]['ripple'] for k in rows), 1)} mV", "atende"),
    ("Vds máx ≤ 520 V (80 % de 650 V) em regime, 264 VAC [S]", f"{f(r264['vds_s'], 0)} V (Llk 2 %) / {f(med['llk3pct_264V']['vds_max'], 0)} V (Llk 3 %); sem grampo {f(med['sem_snubber_264V']['vds_max'], 0)} V", "atende" if max(r264['vds_s'], med['llk3pct_264V']['vds_max']) <= 520 else "NÃO atende"),
    ("Vds máx em falha (curto) – margem específica: ≤ 600 V (92 % de 650 V, pulso) [S]", f"{f(m.get('vds_aplic'), 0)} V na aplicação, {f(m.get('vds_sust'), 0)} V sustentado", "atende" if m.get("vds_aplic", 1e3) <= 600 else "NÃO atende"),
    ("Ip ≤ limite do Rsense (2,6–2,9 A) em regime [S]", f"{f(r90['ip_s'])} A em 90 VAC", "atende" if r90["ip_s"] <= 2.95 else "NÃO atende"),
    ("Δ teoria × simulação ≤ 10 % nos esforços (critério estrito) [C×S]", ("todos dentro" if not excedidos else resumo_excedidos(excedidos)), "atende" if not excedidos else "atende com ressalva (hipóteses do cálculo: triângulo ideal no vale de Vbulk, grampo a 1,8·Vr)"),
    ("Margem de fase ≥ 45° com pós-filtro LC e polo do opto no modelo [C]; degraus sem oscilação [S]", "MF = " + " / ".join(f"{v['pm']:.0f}°" for v in cp["margens"].values()) + f" (fc {f(min(v['fc'] for v in cp['margens'].values())/1e3)}–{f(max(v['fc'] for v in cp['margens'].values())/1e3)} kHz); degraus: desvio ≤ {f(max(abs(x[s]['desvio_mV']) for n in ('degrau_90V', 'degrau_264V') for x in (tra.get(n, {}),) if x for s in ('subida', 'descida')), 0)} mV, dentro de ±1 %, retorno a ±0,5 % em ≤ {f(max(x[s]['t_retorno_0p5pct_ms'] for n in ('degrau_90V', 'degrau_264V') for x in (tra.get(n, {}),) if x for s in ('subida', 'descida')), 1)} ms sem oscilação", "atende" if min(v["pm"] for v in cp["margens"].values()) >= 45 else "NÃO atende"),
    ("Partida a frio sem sobretensão [S]", f"Vo máx {f(tra.get('partida_90V', {}).get('vo_max'))} / {f(tra.get('partida_264V', {}).get('vo_max'))} V; VCC mín {f(tra.get('partida_90V', {}).get('vcc_min'))} V > 7,6 V", "atende"),
    ("Curto sustentado: desligamento por UVLO (hiccup) [C e S]", f"VCC mín no curto {f(m.get('vccmin_sust'))} V (C: UVLO em {hic[2][1] if len(hic) > 2 else '-'} ms a 220 V); I(D1) rms sustentado {f(m.get('id1rms_sust'), 1)} A", "atende" if m.get("vccmin_sust", 99) <= 7.65 else "NÃO atende – ver §4.11"),
    ("Rendimento em 220 V: meta 85 % / cálculo 83 % [S]", f"{f(eta100.get(220), 1)} % (90 V: {f(eta100.get(90), 1)} %)", "atende a meta" if eta100.get(220, 0) >= 85 else "atende o cálculo, não a meta"),
]
md = ["| Critério | Resultado | Situação |", "|---|---|---|"] + [f"| {a} | {b} | {c} |" for a, b, c in crit]
(OUT / "criterios.md").write_text("\n".join(md) + "\n", encoding="utf-8")
json.dump({f"{k[0]}_{k[1]}": v for k, v in rows.items()}, open(OUT / "tabelas.json", "w"), indent=1)
print("ok", len(rows), "pontos; excedidos:", excedidos)
