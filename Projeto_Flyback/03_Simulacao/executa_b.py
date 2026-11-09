"""Executa a matriz B no LTspice Windows. Logs e amostras ficam em runs."""
import concurrent.futures, json, os, re, shutil, subprocess, sys
from pathlib import Path
from gera_netlist import CASOS, netlist, HERE, NET, C_BULK
from runs_dir import LOCAL, RUNS_ONEDRIVE
RUN=LOCAL                       # .raw fora do OneDrive (ver runs_dir.py); .log/.net/medidas.json copiados para runs/
RUN.mkdir(parents=True, exist_ok=True)
RUNS_ONEDRIVE.mkdir(exist_ok=True)
WORKERS=int(os.environ.get('ELP2_WORKERS','2'))
TIMEOUT=int(os.environ.get('ELP2_TIMEOUT','5400'))
EXE=Path(os.getenv('LOCALAPPDATA',''))/'Programs/ADI/LTspice/LTspice.exe'
def solve(p):
    work=RUN/p.name
    shutil.copyfile(p,work)
    log=work.with_suffix('.log')
    log.unlink(missing_ok=True)
    result=subprocess.run([str(EXE),'-b','-Run',str(work)],timeout=TIMEOUT,creationflags=subprocess.CREATE_NO_WINDOW)
    txt=log.read_text('utf8',errors='replace')
    for ext in ('.log','.net'):
        shutil.copyfile(work.with_suffix(ext), RUNS_ONEDRIVE/work.with_suffix(ext).name)
    if result.returncode or 'Total elapsed time:' not in txt or re.search(r'(?i)time step too small|simulation stopped|fatal error',txt):
        raise RuntimeError(p.name+': '+txt[-700:])
    return {m[1].lower():float(m[2]) for m in re.finditer(r'(?im)^([a-z0-9_]+):.*?=\s*([-+\d.eE]+)(?:\s|$)',txt)}
def charge(vac,fl):
    import math
    case=f'pre_carga_{vac}V'
    p=NET/(case+'.net')
    p.write_text(f'''* Revisao B. C1 e C5 descarregados, CI antes do UVLO; Istartup maximo 0.5 mA
Vac l n SINE(0 {vac*math.sqrt(2)} {fl})
Rntc l a 10
Cx1 a n 220n
Ldm a b 200u Rser=0.390
Cx2 b n 100n
D1 b bus db
D2 n bus db
D3 0 b db
D4 0 n db
.model db D(Is=1n n=1.5 Rs=0.03 bv=600 Cjo=50p tt=1u)
Rb bus bc 0.8
Cb bc 0 {C_BULK} ic=0
Rstart bus vcc 164k
Cvcc vcc 0 220u ic=0
Bicc vcc 0 I=0.5m*limit(V(vcc),0,1)
.tran 0 15 0 100u uic
.save V(vcc) V(bc) I(Vac)
.meas tran t_uv WHEN V(vcc)=8.4 rise=1
.meas tran b_uv FIND V(bc) WHEN V(vcc)=8.4 rise=1
.end
''','utf8')
    values=solve(p)
    if 't_uv' not in values or 'b_uv' not in values:
        raise RuntimeError(f'{case}: UVLO não alcançado em 15 s')
    values['t_uv'] = float(re.search(r'(?im)^t_uv:.*? AT ([+0-9.eE-]+)',p.with_suffix('.log').read_text('utf8') if p.with_suffix('.log').exists() else (RUN/(case+'.log')).read_text('utf8'))[1])
    return values
def run(case):
    params=CASOS[case].copy()
    pre={}
    if params.get('startup'):
        pre=charge(params['vac'],params['fline'])
        params.update(handoff=pre['b_uv'],phase=(360*params['fline']*pre['t_uv'])%360)
    p=netlist(case,**params)
    measures=solve(p)
    measures.update(pre)
    if not all(k in measures for k in ['vo_avg','ip_pk','vds_max','ripple_total']): raise RuntimeError(case+' medidas incompletas')
    print(case,measures['vo_avg'],measures['vds_max'],flush=True)
    return case,measures
if __name__=='__main__':
    jobs=sys.argv[1:] or ['partida_90V','partida_264V','curto_220V']+[k for k in CASOS if k not in ('partida_90V','partida_264V','curto_220V')]
    dest=RUNS_ONEDRIVE/'medidas.json'
    data=json.loads(dest.read_text()) if dest.exists() else {}
    errors=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for f in concurrent.futures.as_completed([pool.submit(run,k) for k in jobs]):
            try:
                k,v=f.result(); data[k]=v
                dest.write_text(json.dumps(data,indent=2,sort_keys=True),'utf8')
            except Exception as e: errors.append(str(e));print('FALHA',e,flush=True)
    if errors: sys.exit(1)

