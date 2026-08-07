#!/usr/bin/env python3
"""
Costruisce documenti/ux/design/PRESENTAZIONE.md dai riquadri esportati da Figma.

## Perché esiste

Figma è un servizio in cloud: un file `.fig` in un repository è un blocco
binario che Git non sa confrontare e che nessuno può aprire senza un account.
Mettere solo il link, invece, significa che il giorno in cui quel link scade —
permessi cambiati, spazio di lavoro chiuso, piano scaduto — **la parte di
progettazione del lavoro sparisce.**

La soluzione è tenere entrambe le cose e non far dipendere la seconda dalla
prima: il link Figma per chi vuole vedere i livelli, e le immagini esportate
dentro il repository per chiunque altro. GitHub le mostra in pagina, senza
account e senza scaricare niente.

Questo script fa la seconda parte, così che rifarla dopo una modifica costi un
comando invece di mezz'ora di copia-incolla.

## Come si usa

1. In Figma: seleziona tutti i riquadri di una pagina, pannello di esportazione,
   **PNG a 2×**, esporta.
2. Metti i file in `documenti/ux/design/figma/riquadri/`. I nomi arrivano già giusti da
   Figma, nella forma `NN.M — titolo breve.png`.
3. `python3 strumenti/genera_presentazione.py`

Nessuna dipendenza, come il resto del progetto.
"""

import re
import sys
from pathlib import Path
from urllib.parse import quote

RADICE = Path(__file__).resolve().parent.parent
RIQUADRI = RADICE / "documenti" / "ux" / "design" / "figma" / "riquadri"
USCITA = RADICE / "documenti" / "ux" / "design" / "PRESENTAZIONE.md"

# Le pagine del racconto, nell'ordine in cui vanno guardate. Vengono da
# COSTRUZIONE_FIGMA.md: se lì cambiano, cambiano anche qui — sono due file, ma
# una sola decisione, ed è annotata in entrambi.
PAGINE = {
    "01": ("Il problema", "Che cosa non funziona oggi, e per chi."),
    "02": ("La ricerca", "Le fonti, i competitor, e cosa ne è venuto fuori."),
    "03": ("Il sistema di colore", "Le palette provate, quelle bocciate, e perché."),
    "04": ("Architettura e flussi", "Come è organizzata l'informazione e come ci si muove."),
    "05": ("Gli stati", "Cosa vede l'utente quando le cose non sono semplici."),
    "06": ("Evoluzione", "Come il progetto è cambiato mentre veniva verificato."),
    "07": ("Cosa costruirei dopo", "La direzione, e dove sono i soldi."),
}

# La pagina 00 contiene stili e componenti: serve a costruire, non a raccontare.
NON_SI_PRESENTA = {"00"}

NOME = re.compile(r"^(\d{2})\.(\d+)\s*[—–-]\s*(.+)$")


def riquadri_trovati() -> list[tuple[str, str, str, Path]]:
    """(pagina, numero, titolo, percorso), ordinati come vanno guardati."""
    trovati = []
    for file in sorted(RIQUADRI.glob("*.png")):
        corrisponde = NOME.match(file.stem)
        if not corrisponde:
            print(f"  ignorato (nome fuori schema): {file.name}", file=sys.stderr)
            continue
        pagina, numero, titolo = corrisponde.groups()
        if pagina in NON_SI_PRESENTA:
            continue
        trovati.append((pagina, numero, titolo.strip(), file))
    # Ordine numerico, non alfabetico: senza questo `03.10` finirebbe prima di
    # `03.2`, che è il genere di dettaglio che si nota solo in presentazione.
    return sorted(trovati, key=lambda r: (int(r[0]), int(r[1])))


def genera(trovati: list) -> str:
    righe = [
        "# Progettazione — la presentazione, riquadro per riquadro",
        "",
        "Le stesse pagine del file Figma, esportate qui perché **restino leggibili",
        "anche se il link al file smette di funzionare.** Un permesso cambiato o uno",
        "spazio di lavoro chiuso non devono portarsi via la parte di progettazione",
        "del lavoro.",
        "",
        "Chi vuole vedere i livelli, i componenti e come è costruito il file trova il",
        "link nel [README](../../../README.md). Chi vuole solo guardare, guarda qui.",
        "",
        "Il come e il perché di ogni scelta stanno in [GUIDA_FIGMA.md](GUIDA_FIGMA.md)",
        "(i contenuti) e [COSTRUZIONE_FIGMA.md](COSTRUZIONE_FIGMA.md) (il montaggio).",
        "",
        "> Generato da `strumenti/genera_presentazione.py`. Non modificare a mano:",
        "> riesportare i riquadri e rilanciare lo script.",
        "",
        "---",
        "",
    ]

    if not trovati:
        righe += [
            "*Nessun riquadro ancora esportato.* Esporta i riquadri da Figma in PNG a",
            "2× dentro `documenti/ux/design/figma/riquadri/` e rilancia lo script.",
            "",
        ]
        return "\n".join(righe)

    pagina_corrente = None
    for pagina, numero, titolo, file in trovati:
        if pagina != pagina_corrente:
            pagina_corrente = pagina
            nome, sottotitolo = PAGINE.get(pagina, (f"Pagina {pagina}", ""))
            righe += [f"## {pagina} · {nome}", "", sottotitolo, ""]
        # I nomi che arrivano da Figma contengono spazi e trattini lunghi.
        # Infilati grezzi fra le parentesi di un'immagine Markdown, il
        # collegamento si rompe allo spazio e in pagina resta il testo
        # alternativo — cioe' l'immagine non si vede, senza nessun errore.
        # Trovato eseguendo lo script, non leggendolo.
        percorso = quote(file.relative_to(RADICE / "documenti" / "ux" / "design").as_posix())
        righe += [
            f"### {pagina}.{numero} — {titolo}",
            "",
            f"![{titolo}]({percorso})",
            "",
        ]

    righe += [
        "---",
        "",
        f"**{len(trovati)} riquadri**, su {len({p for p, *_ in trovati})} pagine.",
        "",
    ]
    return "\n".join(righe)


if __name__ == "__main__":
    if not RIQUADRI.is_dir():
        RIQUADRI.mkdir(parents=True)
        print(f"Creata {RIQUADRI.relative_to(RADICE)} — mettici i PNG esportati da Figma.")
    trovati = riquadri_trovati()
    USCITA.write_text(genera(trovati), encoding="utf-8")
    print(f"Scritto {USCITA.relative_to(RADICE)} ({len(trovati)} riquadri).")
