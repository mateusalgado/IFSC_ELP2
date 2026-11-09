"""Renderiza as equacoes do relatorio como imagens PNG (matplotlib mathtext),
para uso no RELATORIO_VISUAL.html sem depender de LaTeX/pandoc instalado.

Uso: python3 gerar_equacoes.py
"""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).parent / "assets" / "eq"
OUT.mkdir(parents=True, exist_ok=True)

FONTSIZE = 20

EQUATIONS = {
    "eq_D_Ts_Ro": r"$D=\dfrac{V_o}{V_{in}}=\dfrac{12}{36}=0,3333 \quad\quad "
                  r"T_s=\dfrac{1}{f_s}=20\,\mu s \quad\quad "
                  r"R_o=\dfrac{V_o^2}{P_o}=1,44\,\Omega$",
    "eq_Io": r"$I_o=I_{L,med}=\dfrac{P_o}{V_o}=8,333\,A$",
    "eq_diL": r"$\Delta i_L=\dfrac{(V_{in}-V_o)\,D}{L\,f_s}"
              r"=\dfrac{24\times0,3333}{100\times10^{-6}\times50\times10^3}=1,600\,A$",
    "eq_ILminmax": r"$I_{L,min}=7,533\,A \quad\quad I_{L,max}=9,133\,A$",
    "eq_Pcond": r"$P_{cond}=R_{DS(on),25}\cdot k_T\cdot I_{T,rms}^{\,2}$",
    "eq_Psw": r"$P_{sw}=\dfrac{f_s}{2}\,(t_r+t_f)\,V_{in}\,I_{L,max}$",
    "eq_Pg": r"$P_g=Q_g\,V_{GS}\,f_s$",
    "eq_Cmin": r"$C_{min}=\dfrac{\Delta i_L}{8\,f_s\,\Delta V_o}"
               r"=\dfrac{1,6}{8\times50\times10^3\times0,12}=33,3\,\mu F$",
    "eq_RSEmax": r"$RSE_{max}=k\cdot\dfrac{\Delta V_o}{\Delta i_L}=0,2\times\dfrac{0,12}{1,6}=15\,m\Omega$",
    "eq_ICrms": r"$I_{C,rms}=\dfrac{\Delta i_L}{\sqrt{12}}=0,462\,A$",
    "eq_RthSAmax_geral": r"$R_{\theta SA,max}=\dfrac{T_{j,proj}-T_a}{P}-R_{\theta JC}-R_{\theta CS}$",
    "eq_RthJA_transistor": r"$R_{\theta JA,\,\mathrm{transistor}}=\dfrac{125-40}{0,50}=170\,^{\circ}C/W$",
    "eq_RthSA_diodo": r"$R_{\theta SA,max,\,\mathrm{diodo}}=\dfrac{125-40}{3,01}-0,45-0,5=27,3\,^{\circ}C/W$",
}


def render(name: str, tex: str) -> None:
    fig = plt.figure(figsize=(0.01, 0.01))
    text = fig.text(0, 0, tex, fontsize=FONTSIZE, color="black")
    fig.canvas.draw()
    bbox = text.get_window_extent()
    width_in = bbox.width / fig.dpi + 0.15
    height_in = bbox.height / fig.dpi + 0.15
    fig.set_size_inches(width_in, height_in)
    text.set_position((0.5, 0.5))
    text.set_horizontalalignment("center")
    text.set_verticalalignment("center")
    out_path = OUT / f"{name}.png"
    fig.savefig(out_path, dpi=220, transparent=True)
    plt.close(fig)
    print(f"OK  {out_path.name}  ({width_in:.2f}in x {height_in:.2f}in)")


if __name__ == "__main__":
    for name, tex in EQUATIONS.items():
        render(name, tex)
    print(f"\n{len(EQUATIONS)} equacoes renderizadas em {OUT}")
