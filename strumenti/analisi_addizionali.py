"""
Analisi delle addizionali comunali IRPEF su tutti i comuni italiani.

A cosa serve
------------
A rispondere con dei numeri, invece che a intuito, alla domanda: quanto varia
davvero l'addizionale comunale da un comune all'altro? La risposta decide la
struttura del registro dei coefficienti (una tabella "comune -> aliquota" non
basta) e giustifica la scelta di Milano come territorio predefinito.

I risultati sono commentati in DIARIO_DI_BORDO.md, voci 17 e 18. Questo script
li rende riproducibili: chiunque puo' rilanciarlo e ottenere le stesse cifre.

Come si usa
-----------
1. Scaricare la tabella ufficiale delle aliquote dal sito dell'Agenzia delle
   Entrate (sezione addizionali comunali, elenco per modulistica).

   ATTENZIONE: le tabelle sono indicizzate per MODULISTICA, non per anno
   d'imposta. La tabella "modulistica 2026" contiene le aliquote dei redditi
   2025. Prendere quella con l'anno che si sta cercando produce aliquote
   sbagliate di un anno, con l'aspetto di una fonte ufficiale.

2. python3 strumenti/analisi_addizionali.py percorso/tabella.pdf

Dipendenze: PyPDF2.
"""

import collections
import re
import sys

try:
    from PyPDF2 import PdfReader
except ImportError:
    sys.exit("Serve PyPDF2:  pip install PyPDF2")

# Riga tipo:  "F205 MILANO MI 0.8 23000"
#             codice catastale, denominazione, provincia, valori numerici
RIGA = re.compile(r"^([A-Z]\d{3})\s+(.+?)\s+([A-Z]{2})\s+([\d\.\s]+)$")

# Codici catastali di alcuni capoluoghi, per il confronto finale
CAPOLUOGHI = {
    "F205": "Milano", "H501": "Roma", "L219": "Torino", "F839": "Napoli",
    "G273": "Palermo", "D612": "Firenze", "A944": "Bologna", "L736": "Venezia",
}


def leggi_comuni(percorso_pdf):
    """Estrae dalla tabella un dizionario codice -> {nome, provincia, aliquote, soglia}."""
    comuni = {}
    for pagina in PdfReader(percorso_pdf).pages:
        for riga in (pagina.extract_text() or "").splitlines():
            trovata = RIGA.match(riga.strip())
            if not trovata:
                continue
            codice, nome, provincia, numeri = trovata.groups()
            try:
                valori = [float(v) for v in numeri.split()]
            except ValueError:
                continue

            # Le soglie di esenzione sono importi in euro, le aliquote percentuali:
            # l'ordine di grandezza le separa senza ambiguita'.
            aliquote = [v for v in valori if v < 100]
            soglie = [v for v in valori if v >= 100]

            # Nei comuni a scaglioni l'ultimo valore piccolo e' il marcatore di
            # tipologia (1 o 2), non un'aliquota: va scartato.
            if len(aliquote) >= 2 and aliquote[-1] in (1.0, 2.0):
                aliquote = aliquote[:-1]

            if aliquote:
                comuni[codice] = {
                    "nome": nome.strip(),
                    "provincia": provincia,
                    "aliquote": aliquote,
                    "soglia": soglie[0] if soglie else None,
                }
    return comuni


def stampa_analisi(comuni):
    totale = len(comuni)
    if not totale:
        sys.exit("Nessun comune riconosciuto: il PDF non ha il formato atteso.")

    a_scaglioni = [c for c in comuni.values() if len(c["aliquote"]) > 1]
    con_soglia = [c for c in comuni.values() if c["soglia"] is not None]
    azzerata = [c for c in comuni.values() if max(c["aliquote"]) == 0]

    def quota(n):
        return f"{n:5d}  ({n / totale:5.1%})"

    print(f"Comuni nella tabella        : {totale}")
    print(f"  aliquota unica            : {quota(totale - len(a_scaglioni))}")
    print(f"  a scaglioni               : {quota(len(a_scaglioni))}")
    print(f"  con soglia di esenzione   : {quota(len(con_soglia))}")
    print(f"  senza alcuna soglia       : {quota(totale - len(con_soglia))}")
    print(f"  addizionale pari a zero   : {quota(len(azzerata))}")

    massime = [max(c["aliquote"]) for c in comuni.values()]
    print(f"\nAliquota massima applicata  : da {min(massime):.3f}% a {max(massime):.3f}%")

    print("\nAliquote piu' diffuse:")
    for valore, quanti in collections.Counter(round(m, 3) for m in massime).most_common(6):
        print(f"  {valore:6.3f}%   {quota(quanti)}")

    soglie = collections.Counter(int(c["soglia"]) for c in con_soglia)
    print(f"\nSoglie di esenzione distinte: {len(soglie)}"
          f"   (da {min(soglie):,} a {max(soglie):,} euro)")
    for valore, quanti in soglie.most_common(5):
        print(f"  {valore:8,d} euro   {quanti:5d} comuni")

    print("\nCapoluoghi a confronto:")
    for codice, atteso in CAPOLUOGHI.items():
        comune = comuni.get(codice)
        if not comune:
            continue
        aliquote = " / ".join(f"{a}%" for a in comune["aliquote"])
        soglia = (f"esente fino a {int(comune['soglia']):,} euro"
                  if comune["soglia"] else "nessuna esenzione")
        print(f"  {comune['nome']:12s} ({comune['provincia']})  {aliquote:30s}  {soglia}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Uso: python3 {sys.argv[0]} percorso/tabella_addizionali.pdf")
    stampa_analisi(leggi_comuni(sys.argv[1]))
