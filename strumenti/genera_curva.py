"""
Genera il diagramma della curva del netto, con le sue discontinuita'.

E' il risultato piu' controintuitivo del progetto — in tre punti, guadagnare di
piu' fa guadagnare di meno — e in forma di tabella non si vede. Il diagramma
esiste per questo.

Due accorgimenti che la prima versione non aveva, entrambi emersi guardandola:

  * i gradini sono piccoli rispetto alla scala dell'asse, quindi la curva
    sembra continua. Serve un INGRANDIMENTO su uno di essi, altrimenti il
    disegno dice il contrario di cio' che dovrebbe dimostrare;

  * sei annotazioni sul tracciato si sovrappongono. Sul grafico restano i soli
    valori, con una linea che li collega al punto; le cause stanno in un elenco
    sotto, dove hanno lo spazio per essere lette.

    python3 strumenti/genera_curva.py
"""
import sys, pathlib
RADICE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE))
from motore import calcola
from motore.inverso import punti_di_salto

DA, A, PASSO = 5_000, 60_000, 25
W, H = 1260, 760
L, R, T, B = 96, 44, 78, 300

punti = [(r, calcola(float(r)).netto_annuo) for r in range(DA, A + 1, PASSO)]
salti = [s for s in punti_di_salto("2026", "MI") if DA < s < A]
# Le cause, nell'ordine crescente di RAL in cui i salti compaiono.
#
# Erano sei. Sono sette da quando i 75 euro di riduzione della capienza
# (L. 234/2021) hanno spostato la prima soglia da un imponibile di 8.500 a
# 8.173,91: prima cadeva esattamente dove finisce la prima fascia della somma
# esente, e le due discontinuita' si sovrapponevano in un punto solo.
CAUSE = ["scatta la capienza del trattamento integrativo",
         "la somma esente scende dal 7,1% al 5,3%",
         "finiscono la detrazione di fascia 1 e il trattamento pieno",
         "la somma esente lascia il posto alla detrazione del cuneo",
         "soglia di esenzione dell'addizionale comunale di Milano",
         "inizia l'ulteriore detrazione di 65 euro",
         "finisce l'ulteriore detrazione di 65 euro"]

# Un elenco scritto a mano accanto a soglie calcolate e' un disallineamento in
# attesa di succedere: se il registro cambia, la didascalia resta indietro e
# racconta una cosa per un'altra. Meglio fermarsi.
if len(CAUSE) != len(salti):
    raise SystemExit(
        f"Le cause sono {len(CAUSE)} ma le discontinuita' trovate sono "
        f"{len(salti)}. Aggiorna CAUSE in questo file prima di rigenerare."
    )

px, py = W - L - R, H - T - B
maxy = 40_000
X = lambda v: L + (v - DA) / (A - DA) * px
Y = lambda v: T + py - v / maxy * py
eu = lambda v: f"{v:,.0f}".replace(",", ".")
VERDE, ROSSO, LINEA, INK, TENUE, GRIGLIA = "#1a7a3c", "#a8341f", "#0a9184", "#11150a", "#4e5549", "#e1e0d9"

NORMALE = PASSO * 1.2
segmenti, corrente = [], [punti[0]]
for (r0, n0), (r1, n1) in zip(punti, punti[1:]):
    if abs(n1 - n0) > NORMALE:
        segmenti.append(corrente); corrente = []
    corrente.append((r1, n1))
segmenti = [s for s in (segmenti + [corrente]) if len(s) > 1]

o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
     f'font-family="system-ui,-apple-system,Segoe UI,sans-serif"><rect width="{W}" height="{H}" fill="#fff"/>']
o.append(f'<text x="{L}" y="34" font-size="21" font-weight="700" fill="{INK}">Il netto non cresce sempre col lordo</text>')
o.append(f'<text x="{L}" y="57" font-size="13.5" fill="{TENUE}">Sei discontinuita\'. In tre, un euro di lordo in piu\' fa scendere il netto. Milano, anno d\'imposta 2026.</text>')

for v in range(0, maxy + 1, 10_000):
    y = Y(v)
    o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+px}" y2="{y:.1f}" stroke="{GRIGLIA}"/>')
    o.append(f'<text x="{L-10}" y="{y+4:.1f}" font-size="11.5" fill="#898781" text-anchor="end">{eu(v)}</text>')
for v in range(10_000, A + 1, 10_000):
    o.append(f'<text x="{X(v):.1f}" y="{T+py+20}" font-size="11.5" fill="#898781" text-anchor="middle">{eu(v)}</text>')
o.append(f'<text x="{L+px}" y="{T+py+40}" font-size="11.5" fill="{TENUE}" text-anchor="end">RAL lorda annua &#8594;</text>')
o.append(f'<text x="{L-10}" y="{T-10}" font-size="11.5" fill="{TENUE}" text-anchor="end">netto annuo</text>')

for s in segmenti:
    d = " ".join(f"{'M' if i==0 else 'L'}{X(r):.1f},{Y(n):.1f}" for i,(r,n) in enumerate(s))
    o.append(f'<path d="{d}" fill="none" stroke="{LINEA}" stroke-width="2.5" stroke-linecap="round"/>')

# Solo i valori sul tracciato, alternati sopra e sotto per non toccarsi.
for i, s in enumerate(salti):
    x, prima, dopo = X(s), calcola(s-0.01).netto_annuo, calcola(s+0.01).netto_annuo
    delta = dopo - prima
    c = VERDE if delta > 0 else ROSSO
    ymed = (Y(prima) + Y(dopo)) / 2
    sopra = i % 2 == 0
    ye = ymed - 30 if sopra else ymed + 38
    o.append(f'<line x1="{x:.1f}" y1="{ymed:.1f}" x2="{x:.1f}" y2="{ye + (12 if sopra else -22):.1f}" stroke="{c}" stroke-width="1"/>')
    o.append(f'<circle cx="{x:.1f}" cy="{Y(prima):.1f}" r="4.5" fill="#fff" stroke="{c}" stroke-width="2.5"/>')
    o.append(f'<circle cx="{x:.1f}" cy="{Y(dopo):.1f}" r="4.5" fill="{c}"/>')
    o.append(f'<text x="{x:.1f}" y="{ye:.1f}" font-size="13" font-weight="700" fill="{c}" text-anchor="middle">{delta:+,.0f} €</text>'.replace(",", "."))
    o.append(f'<text x="{x:.1f}" y="{T+py+20 if not sopra else T+py+20}" font-size="0" fill="none">{i}</text>')
    o.append(f'<circle cx="{x:.1f}" cy="{T+py}" r="9" fill="{c}"/>')
    o.append(f'<text x="{x:.1f}" y="{T+py+4:.1f}" font-size="11" font-weight="700" fill="#fff" text-anchor="middle">{i+1}</text>')

# --- ingrandimento sul gradino comunale: senza, il salto non si vede ---
s = salti[3]
zx, zy, zw, zh = L, T + py + 62, 330, 132
lo, hi = s - 900, s + 900
zpunti = [(r, calcola(float(r)).netto_annuo) for r in range(int(lo), int(hi), 20)]
zmin, zmax = min(n for _, n in zpunti), max(n for _, n in zpunti)
mrg = (zmax - zmin) * 0.22
ZX = lambda v: zx + 54 + (v - lo) / (hi - lo) * (zw - 66)
ZY = lambda v: zy + 26 + (zh - 46) - (v - (zmin - mrg)) / ((zmax + mrg) - (zmin - mrg)) * (zh - 46)
o.append(f'<rect x="{zx}" y="{zy}" width="{zw}" height="{zh}" fill="#fbfbf9" stroke="{GRIGLIA}" rx="8"/>')
o.append(f'<text x="{zx+12}" y="{zy+18}" font-size="12" font-weight="700" fill="{INK}">Ingrandimento sul punto 4</text>')
zseg, zcur = [], [zpunti[0]]
for (r0,n0),(r1,n1) in zip(zpunti, zpunti[1:]):
    if abs(n1-n0) > 25: zseg.append(zcur); zcur = []
    zcur.append((r1,n1))
zseg = [x for x in (zseg+[zcur]) if len(x) > 1]
for sg in zseg:
    d = " ".join(f"{'M' if i==0 else 'L'}{ZX(r):.1f},{ZY(n):.1f}" for i,(r,n) in enumerate(sg))
    o.append(f'<path d="{d}" fill="none" stroke="{LINEA}" stroke-width="2.5"/>')
p0, p1 = calcola(s-0.01).netto_annuo, calcola(s+0.01).netto_annuo
o.append(f'<circle cx="{ZX(s):.1f}" cy="{ZY(p0):.1f}" r="4.5" fill="#fff" stroke="{ROSSO}" stroke-width="2.5"/>')
o.append(f'<circle cx="{ZX(s):.1f}" cy="{ZY(p1):.1f}" r="4.5" fill="{ROSSO}"/>')
o.append(f'<text x="{ZX(s)+10:.1f}" y="{(ZY(p0)+ZY(p1))/2+4:.1f}" font-size="12" font-weight="700" fill="{ROSSO}">-184 €</text>')
o.append(f'<text x="{zx+12}" y="{zy+zh-8}" font-size="11" fill="{TENUE}">un euro di lordo in piu\', 184 di netto in meno</text>')

# --- elenco delle sei discontinuita' ---
ex, ey = zx + zw + 34, zy + 6
o.append(f'<text x="{ex}" y="{ey+8}" font-size="12" font-weight="700" fill="{INK}">Le sei discontinuita\'</text>')
for i, sp in enumerate(salti):
    d = calcola(sp+0.01).netto_annuo - calcola(sp-0.01).netto_annuo
    c = VERDE if d > 0 else ROSSO
    y = ey + 30 + i * 19
    o.append(f'<circle cx="{ex+7}" cy="{y-4:.0f}" r="8" fill="{c}"/>')
    o.append(f'<text x="{ex+7}" y="{y:.0f}" font-size="10.5" font-weight="700" fill="#fff" text-anchor="middle">{i+1}</text>')
    o.append(f'<text x="{ex+24}" y="{y:.0f}" font-size="12" fill="{TENUE}">RAL {eu(sp)}</text>')
    o.append(f'<text x="{ex+186}" y="{y:.0f}" font-size="12" font-weight="700" fill="{c}" text-anchor="end">{d:+,.0f} €</text>'.replace(",", "."))
    o.append(f'<text x="{ex+200}" y="{y:.0f}" font-size="12" fill="{TENUE}">{CAUSE[i]}</text>')
o.append(f'<text x="{ex}" y="{ey+30+6*19+16:.0f}" font-size="11" fill="#898781">Cerchio vuoto: prima della soglia. Cerchio pieno: subito dopo.</text>')

o.append("</svg>")
(RADICE / "documenti/ux/design/diagrammi/curva-netto-discontinuita.svg").write_text("\n".join(o), encoding="utf-8")
print(f"  scritto: documenti/ux/design/diagrammi/curva-netto-discontinuita.svg   ({len(segmenti)} segmenti, {len(salti)} salti)")
