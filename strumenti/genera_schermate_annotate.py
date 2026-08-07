"""
Genera le due schermate annotate per la presentazione.

Sono wireframe VETTORIALI, non catture dello schermo: importati in Figma
restano modificabili elemento per elemento, e le annotazioni sono oggetti
separati dal disegno. Una cattura sarebbe un'immagine piatta, buona da
guardare e inutile da lavorare.

Le annotazioni seguono una regola: **una o due parole per il cosa, una riga
breve per il perche'**. Un richiamo che va a capo tre volte smette di essere un
richiamo e diventa un paragrafo con una freccia attaccata.

    python3 strumenti/genera_schermate_annotate.py
"""
import pathlib

RADICE = pathlib.Path(__file__).resolve().parent.parent
USCITA = RADICE / "documenti" / "ux" / "design" / "diagrammi"

INK, TENUE, MUTO = "#11150a", "#4e5549", "#8b9184"
LIME, SU_LIME = "#dfeb57", "#11150a"
CARTA, SFONDO, BORDO = "#ffffff", "#f4f7ee", "#dce0da"
AIUTO, EVID = "#f6f9cf", "#c3d13a"
RICHIAMO = "#0a9184"
FONT = "system-ui,-apple-system,Segoe UI,Helvetica,sans-serif"


class Tela:
    def __init__(self, larghezza, altezza, titolo, sottotitolo):
        self.w, self.h = larghezza, altezza
        self.p = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{larghezza}" height="{altezza}" '
            f'viewBox="0 0 {larghezza} {altezza}" font-family="{FONT}">',
            f'<rect width="{larghezza}" height="{altezza}" fill="#fbfcfa"/>',
            self.testo(56, 46, titolo, 24, INK, peso=700),
            self.testo(56, 72, sottotitolo, 13.5, TENUE),
        ]
        self.n = 0
        # y gia' occupate dalle etichette, per lato: due richiami troppo vicini
        # producono testi sovrapposti, che e' il difetto tipico di questi
        # disegni e li rende illeggibili proprio dove spiegano.
        self.occupate = {"destra": [], "sinistra": []}

    # --- primitive ---------------------------------------------------------
    def testo(self, x, y, t, dim=13, colore=INK, peso=400, ancora="start", corsivo=False):
        t = (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
        stile = ' font-style="italic"' if corsivo else ""
        return (f'<text x="{x}" y="{y}" font-size="{dim}" fill="{colore}" '
                f'font-weight="{peso}" text-anchor="{ancora}"{stile}>{t}</text>')

    def riquadro(self, x, y, w, h, riempi=CARTA, bordo=BORDO, raggio=8, spessore=1, tratteggio=None):
        d = f' stroke-dasharray="{tratteggio}"' if tratteggio else ""
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{raggio}" '
                      f'fill="{riempi}" stroke="{bordo}" stroke-width="{spessore}"{d}/>')

    def scritta(self, *a, **k):
        self.p.append(self.testo(*a, **k))

    def barra_finta(self, x, y, w, h=8, colore="#e6e9e2"):
        self.p.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{colore}"/>')

    # --- richiami ----------------------------------------------------------
    def richiamo(self, bersaglio, etichetta, perche, lato="destra", dy=0, gomito=None,
                 scarto=(0, 0)):
        """Un numero accanto all'elemento, una linea, due parole e un perche'.

        Il pallino NON si mette sopra il bersaglio: lo coprirebbe, e coprire
        cio' che si sta indicando e' peggio che non indicarlo. `scarto` lo
        allontana quel tanto che basta.

        Le etichette si distanziano da sole: se due cadono troppo vicine, la
        seconda scende finche' non c'e' spazio.
        """
        self.n += 1
        bx, by = bersaglio[0] + scarto[0], bersaglio[1] + scarto[1]
        fuori = self.w - 300 if lato == "destra" else 300
        ty = by + dy
        for usata in sorted(self.occupate[lato]):
            if abs(ty - usata) < 40:
                ty = usata + 40
        self.occupate[lato].append(ty)
        curva = gomito if gomito is not None else (bx + (60 if lato == "destra" else -60))

        self.p.append(f'<path d="M{bx},{by} L{curva},{ty} L{fuori},{ty}" fill="none" '
                      f'stroke="{RICHIAMO}" stroke-width="1.4" opacity="0.75"/>')
        self.p.append(f'<circle cx="{bx}" cy="{by}" r="10" fill="{RICHIAMO}"/>')
        self.p.append(self.testo(bx, by + 4, str(self.n), 11.5, "#fff", 700, "middle"))

        ax = fuori + (14 if lato == "destra" else -14)
        anc = "start" if lato == "destra" else "end"
        self.p.append(f'<circle cx="{fuori}" cy="{ty}" r="3" fill="{RICHIAMO}"/>')
        self.p.append(self.testo(ax, ty - 3, etichetta.upper(), 12.5, INK, 700, anc))
        self.p.append(self.testo(ax, ty + 14, perche, 11.5, TENUE, 400, anc))

    def salva(self, nome):
        self.p.append("</svg>")
        (USCITA / nome).write_text("\n".join(self.p), encoding="utf-8")
        print(f"  {nome}  ({self.n} richiami)")


def cornice_dispositivo(t, x, y, w, h, didascalia):
    t.p.append(f'<rect x="{x-10}" y="{y-10}" width="{w+20}" height="{h+20}" rx="18" '
               f'fill="{SFONDO}" stroke="{BORDO}" stroke-width="1.5"/>')
    t.scritta(x + w / 2, y + h + 34, didascalia, 12, MUTO, 500, "middle")


# ===========================================================================
# Schermata 1 — all'apertura
# ===========================================================================
def schermata_apertura():
    t = Tela(1560, 1080,
             "Schermata all'apertura — modalità «alle prime armi»",
             "Un solo campo obbligatorio. Tutto il resto ha un default dichiarato, e ogni voce spiega sé stessa prima che venga chiesto.")
    X, Y, W = 470, 130, 620
    cornice_dispositivo(t, X, Y, W, 830, "stato iniziale · nessun dato inserito")

    # intestazione
    t.scritta(X + 24, Y + 44, "Dalla RAL al netto", 22, INK, 700)
    t.scritta(X + 24, Y + 68, "Quanto resta davvero in tasca, e perché.", 12.5, TENUE)
    t.riquadro(X + W - 232, Y + 22, 208, 34, CARTA, BORDO, 8)
    t.riquadro(X + W - 228, Y + 26, 116, 26, INK, INK, 6)
    t.scritta(X + W - 170, Y + 43, "Alle prime armi", 11, "#fff", 600, "middle")
    t.scritta(X + W - 60, Y + 43, "Esperto", 11, TENUE, 400, "middle")
    t.richiamo((X + W - 170, Y + 26), "Due livelli", "commutabili senza perdere nulla", "destra", -46)

    # avviso indipendenza
    t.riquadro(X + 24, Y + 86, W - 48, 40, CARTA, BORDO, 8)
    t.p.append(f'<rect x="{X+24}" y="{Y+86}" width="5" height="40" fill="{LIME}"/>')
    t.scritta(X + 42, Y + 104, "Prototipo indipendente.", 11.5, INK, 700)
    t.scritta(X + 42, Y + 119, "Non è uno strumento ufficiale.", 11.5, TENUE)
    t.richiamo((X + 24, Y + 106), "Onestà", "chiarisce cosa non è", "sinistra", -8, scarto=(-16, 0))

    # leggibilità
    t.riquadro(X + 24, Y + 140, W - 48, 36, CARTA, BORDO, 8)
    t.scritta(X + 42, Y + 163, "◐  Leggibilità", 12.5, INK, 600)
    t.scritta(X + W - 42, Y + 163, "▸", 12.5, TENUE, 400, "end")
    t.richiamo((X + 24, Y + 158), "In alto", "serve prima di leggere", "sinistra", 8, scarto=(-16, 0))

    # schede
    t.riquadro(X + 24, Y + 194, 290, 40, CARTA, BORDO, 8)
    t.scritta(X + 40, Y + 219, "Ho il LORDO, voglio il netto", 12, INK, 600)
    t.riquadro(X + 322, Y + 194, 274, 40, SFONDO, BORDO, 8)
    t.scritta(X + 338, Y + 219, "Voglio garantire un NETTO", 12, TENUE)
    t.richiamo((X + W - 24, Y + 214), "Due domande", "l'HR le fa entrambe", "destra", -22, scarto=(14, 0))

    # campo principale
    t.scritta(X + 24, Y + 274, "RAL — Retribuzione Annua", 13, INK, 700)
    t.p.append(f'<rect x="{X+228}" y="{Y+261}" width="62" height="19" fill="{AIUTO}" stroke="{EVID}" stroke-width="2"/>')
    t.scritta(X + 232, Y + 275, "LORDA", 12.5, INK, 700)
    t.riquadro(X + 24, Y + 288, 200, 46, CARTA, MUTO, 8)
    t.scritta(X + 40, Y + 318, "35.000", 19, MUTO)
    t.scritta(X + 238, Y + 318, "€ all'anno", 12, TENUE)
    t.richiamo((X + 292, Y + 271), "Disambigua", "è l'errore più costoso", "destra", -34, scarto=(14, 0))

    # eco
    t.scritta(X + 24, Y + 356, "Ho letto  35.000 € lordi all'anno", 12, TENUE)
    t.p.append(f'<rect x="{X+70}" y="{Y+345}" width="146" height="16" fill="{AIUTO}" opacity="0.65"/>')
    t.scritta(X + 74, Y + 357, "35.000 € lordi all'anno", 12, INK, 700)
    t.richiamo((X + 220, Y + 353), "Eco viva", "mostra cosa ha capito", "destra", 12, scarto=(14, 0))

    # aiuto aperto
    t.riquadro(X + 24, Y + 372, W - 48, 84, AIUTO, EVID, 8)
    t.scritta(X + 40, Y + 394, "Che cos'è la RAL.", 12, INK, 700)
    t.scritta(X + 165, Y + 394, "È lo stipendio ANNUO e LORDO", 12, TENUE)
    t.scritta(X + 40, Y + 412, "scritto nel contratto, prima di tasse e contributi.", 12, TENUE)
    t.scritta(X + 40, Y + 436, "Se pensi a 1.800 € o 2.500 €, quello è un mensile.", 12, INK, 600)
    t.richiamo((X + 24, Y + 414), "Già aperta", "chi non sa, non chiede", "sinistra", 0, scarto=(-16, 0))

    # comune
    t.scritta(X + 24, Y + 490, "Comune di residenza", 13, INK, 600)
    t.riquadro(X + 24, Y + 502, W - 48, 42, CARTA, MUTO, 8)
    t.scritta(X + 42, Y + 528, "Milano (Lombardia) — predefinito", 12.5, INK)
    t.scritta(X + W - 44, Y + 528, "▾", 12, TENUE, 400, "end")
    t.richiamo((X + W - 24, Y + 523), "Mai implicito", "vale oltre 600 € l'anno", "destra", 0, scarto=(14, 0))

    # aiuto comune
    t.riquadro(X + 24, Y + 554, W - 48, 62, AIUTO, EVID, 8)
    t.scritta(X + 40, Y + 576, "Perché serve il comune.", 12, INK, 700)
    t.scritta(X + 40, Y + 596, "Le addizionali cambiano da un territorio all'altro.", 12, TENUE)

    # pulsante
    t.p.append(f'<rect x="{X+24}" y="{Y+646}" width="182" height="48" rx="8" fill="{LIME}" stroke="{INK}" stroke-width="1.5"/>')
    t.scritta(X + 115, Y + 676, "Calcola", 15, SU_LIME, 700, "middle")
    t.richiamo((X + 206, Y + 670), "Un'azione", "nessuna scelta da fare", "sinistra", 34, gomito=X - 60, scarto=(16, 0))

    # piede
    t.barra_finta(X + 24, Y + 726, W - 200, 7)
    t.barra_finta(X + 24, Y + 742, W - 300, 7)
    t.scritta(X + 24, Y + 782, "Versione del 2026-08-07 · prototipo indipendente", 11, MUTO)
    t.richiamo((X + 24, Y + 778), "Versione", "quale build stai guardando", "sinistra", 22, scarto=(-24, 0))

    t.salva("schermata-01-apertura.svg")


# ===========================================================================
# Schermata 2 — opzioni aperte
# ===========================================================================
def schermata_opzioni():
    t = Tela(1560, 1160,
             "Schermata con le opzioni aperte — modalità «esperto»",
             "Tutti i parametri in chiaro, gli aiuti richiudibili, e le quattro leve di leggibilità. Cambiare modalità non azzera nulla.")
    X, Y, W = 470, 130, 620
    cornice_dispositivo(t, X, Y, W, 900, "pannello leggibilità aperto · parametri avanzati visibili")

    # intestazione con esperto attivo
    t.scritta(X + 24, Y + 44, "Dalla RAL al netto", 22, INK, 700)
    t.riquadro(X + W - 232, Y + 22, 208, 34, CARTA, BORDO, 8)
    t.scritta(X + W - 170, Y + 43, "Alle prime armi", 11, TENUE, 400, "middle")
    t.riquadro(X + W - 116, Y + 26, 88, 26, INK, INK, 6)
    t.scritta(X + W - 72, Y + 43, "Esperto", 11, "#fff", 600, "middle")
    t.richiamo((X + W - 72, Y + 26), "Stesso stato", "gli input restano", "destra", -46)

    # pannello leggibilità aperto
    t.riquadro(X + 24, Y + 76, W - 48, 320, CARTA, BORDO, 10)
    t.scritta(X + 42, Y + 100, "◐  Leggibilità", 12.5, INK, 600)

    leve = [
        ("Tema", ["Chiaro", "Scuro", "Come il sistema"], 0, "Chiaro di default", "la materia chiede chiarezza"),
        ("Dimensione del testo", ["Normale", "Grande", "Molto grande"], 0, "Tre misure", "fino a +40%"),
        ("Contrasto", ["Normale", "Alto"], 0, "Bordi, non tinte", "la gerarchia sopravvive"),
    ]
    yy = Y + 124
    for etichetta, opzioni, attiva, cosa, perche in leve:
        t.scritta(X + 42, yy + 12, etichetta, 11.5, TENUE)
        xx = X + 42
        for i, o in enumerate(opzioni):
            larg = 22 + len(o) * 6.6
            attivo = i == attiva
            t.p.append(f'<rect x="{xx}" y="{yy+20}" width="{larg}" height="26" rx="13" '
                       f'fill="{LIME if attivo else CARTA}" stroke="{INK if attivo else MUTO}" stroke-width="1"/>')
            t.scritta(xx + larg / 2, yy + 37, o, 10.5, INK, 600 if attivo else 400, "middle")
            xx += larg + 7
        t.richiamo((X + 24, yy + 33), cosa, perche, "sinistra", 0, scarto=(-16, 0))
        yy += 62

    # anteprima colori
    t.scritta(X + 42, yy + 12, "Visione dei colori", 11.5, TENUE)
    for i, c in enumerate(["#0a9184", "#d0552a", "#3457c8", "#6f8f0a", "#9c3d8f"]):
        t.p.append(f'<rect x="{X+42+i*34}" y="{yy+20}" width="28" height="17" rx="4" fill="{c}" stroke="{BORDO}"/>')
    t.scritta(X + 224, yy + 33, "colori del grafico — standard", 10.5, TENUE)
    t.richiamo((X + W - 24, yy + 28), "Anteprima", "l'effetto si vede subito", "destra", -10, scarto=(14, 0))

    xx = X + 42
    for i, o in enumerate(["Standard", "Daltonismo rosso-verde", "Senza colore"]):
        larg = 22 + len(o) * 6.6
        attivo = i == 0
        t.p.append(f'<rect x="{xx}" y="{yy+48}" width="{larg}" height="26" rx="13" '
                   f'fill="{LIME if attivo else CARTA}" stroke="{INK if attivo else MUTO}" stroke-width="1"/>')
        t.scritta(xx + larg / 2, yy + 65, o, 10.5, INK, 600 if attivo else 400, "middle")
        xx += larg + 7
    t.richiamo((X + W - 66, yy + 61), "Tre modalità", "una per tipo di deficit", "destra", 10)

    # campo con aiuto CHIUSO
    ay = Y + 424
    t.scritta(X + 24, ay, "RAL — Retribuzione Annua", 13, INK, 700)
    t.p.append(f'<rect x="{X+228}" y="{ay-13}" width="62" height="19" fill="{AIUTO}" stroke="{EVID}" stroke-width="2"/>')
    t.scritta(X + 232, ay + 1, "LORDA", 12.5, INK, 700)
    t.scritta(X + W - 24, ay, "cosa vuol dire?", 11.5, "#44660a", 400, "end")
    t.richiamo((X + W - 24, ay - 5), "Su richiesta", "per l'esperto è rumore", "destra", -14, scarto=(14, 0))
    t.riquadro(X + 24, ay + 14, 200, 44, CARTA, MUTO, 8)
    t.scritta(X + 40, ay + 43, "35.000", 19, INK)
    t.scritta(X + 24, ay + 78, "Sto calcolando su 35.000 €", 12, TENUE)

    # comune
    t.scritta(X + 24, ay + 112, "Comune di residenza", 12.5, INK, 600)
    t.riquadro(X + 24, ay + 122, W - 48, 40, CARTA, MUTO, 8)
    t.scritta(X + 42, ay + 147, "Milano (Lombardia) — predefinito", 12.5, INK)
    t.richiamo((X + 24, ay + 142), "Resta visibile", "anche l'esperto sbaglia", "sinistra", 0, scarto=(-16, 0))

    # parametri avanzati
    py = ay + 182
    t.p.append(f'<line x1="{X+24}" y1="{py}" x2="{X+W-24}" y2="{py}" stroke="{BORDO}" stroke-dasharray="4 4"/>')
    parametri = [("Anno d'imposta", "2026 — corrente"), ("CCNL", "Commercio — 14 mensilità"),
                 ("Mensilità", "14"), ("Giorni di detrazione", "365  su 365")]
    for i, (etichetta, valore) in enumerate(parametri):
        yy2 = py + 22 + i * 46
        t.scritta(X + 24, yy2 + 14, etichetta, 12, INK, 600)
        t.riquadro(X + 232, yy2, 268, 32, CARTA, MUTO, 7)
        t.scritta(X + 248, yy2 + 21, valore, 11.5, INK)
    t.richiamo((X + W - 24, py + 68), "Tutto in chiaro", "niente è nascosto", "destra", -20, scarto=(14, 0))
    t.richiamo((X + 24, py + 160), "Giorni", "assunzione infrannuale", "sinistra", 6, scarto=(-16, 0))

    # pulsante
    t.p.append(f'<rect x="{X+24}" y="{py+218}" width="182" height="46" rx="8" fill="{LIME}" stroke="{INK}" stroke-width="1.5"/>')
    t.scritta(X + 115, py + 247, "Calcola", 15, SU_LIME, 700, "middle")

    t.salva("schermata-02-opzioni-aperte.svg")


if __name__ == "__main__":
    USCITA.mkdir(parents=True, exist_ok=True)
    print("Schermate annotate:")
    schermata_apertura()
    schermata_opzioni()
