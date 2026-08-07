"""
Controllo di sensibilita' dei test.

A cosa serve
------------
Una suite di test che passa non dimostra che il codice sia giusto: dimostra
che i test non hanno trovato nulla. Puo' voler dire che il codice e' corretto,
oppure che i test non guardano dove serve.

Questo strumento risponde alla domanda: **se un coefficiente fosse sbagliato,
i test se ne accorgerebbero?** Guasta un valore alla volta nel registro,
rilancia la suite e riporta quanti test cadono. Un guasto che non fa fallire
nulla e' un buco nella copertura, e va chiuso.

E' cosi' che e' emerso che la soglia di esenzione comunale non era protetta:
i test ricavavano le proprie attese dal registro, quindi cambiando il dato si
spostavano insieme aspettativa e comportamento. La correzione e' stata
aggiungere valori fissati a mano (sezione 0 della suite) e un caso di
riferimento sotto la soglia.

Come si usa
-----------
    python3 strumenti/controllo_sensibilita.py

Il registro viene sempre ripristinato, anche in caso di interruzione.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

RADICE = pathlib.Path(__file__).resolve().parent.parent
REGISTRO = RADICE / "dati" / "coefficienti.json"
SUITE = RADICE / "test_motore.py"


def sostituisci(percorso, valore):
    """Restituisce una funzione che modifica il registro nel punto indicato.

    Il percorso e' una sequenza di chiavi, per esempio
    ("nazionale", "2026", "inps", "aliquota_dipendente").
    """
    def applica(dati):
        nodo = dati
        for chiave in percorso[:-1]:
            nodo = nodo[chiave]
        nodo[percorso[-1]] = valore
    return applica


GUASTI = [
    ("IRPEF 2026: seconda aliquota da 33% a 35%",
     sostituisci(("nazionale", "2026", "irpef", "scaglioni"),
                 [[28000.0, 0.23], [50000.0, 0.35], [None, 0.43]])),
    ("IRPEF 2026: soglia del secondo scaglione da 28.000 a 29.000",
     sostituisci(("nazionale", "2026", "irpef", "scaglioni"),
                 [[29000.0, 0.23], [50000.0, 0.33], [None, 0.43]])),
    ("INPS: aliquota da 9,19% a 9,20%",
     sostituisci(("nazionale", "2026", "inps", "aliquota_dipendente"), 0.092)),
    ("Detrazioni: quota di fascia 2 da 1.190 a 1.200",
     sostituisci(("nazionale", "2026", "detrazioni_lavoro_dipendente", "fascia_2_quota"), 1200.0)),
    ("Detrazioni: minimo di fascia 1 da 690 a 0",
     sostituisci(("nazionale", "2026", "detrazioni_lavoro_dipendente", "fascia_1_minimo"), 0.0)),
    ("Cuneo: detrazione piena da 1.000 a 900",
     sostituisci(("nazionale", "2026", "cuneo_ulteriore_detrazione", "importo_pieno"), 900.0)),
    ("Cuneo: la somma esente sparisce (percentuali a zero)",
     sostituisci(("nazionale", "2026", "cuneo_somma_esente", "fasce"),
                 [[8500.0, 0.0], [15000.0, 0.0], [20000.0, 0.0]])),
    ("Trattamento integrativo: da 1.200 a 1.000",
     sostituisci(("nazionale", "2026", "trattamento_integrativo", "importo"), 1000.0)),
    # I 75 euro della L. 234/2021 mancavano del tutto, e nessun test se ne
    # accorgeva: il test derivava la soglia dallo stesso registro incompleto.
    # Questo guasto verifica che adesso qualcuno se ne accorga.
    ("Trattamento integrativo: tolgo i 75 euro di riduzione della capienza",
     sostituisci(("nazionale", "2026", "trattamento_integrativo",
                  "riduzione_detrazione_capienza"), 0.0)),
    ("Ulteriore detrazione 65 euro: fascia da 25.000 a 28.000",
     sostituisci(("nazionale", "2026", "ulteriore_detrazione_65", "reddito_minimo_escluso"), 28000.0)),
    # I minimi contrattuali non entrano nel calcolo del netto: se i test che li
    # riguardano non fallissero, vorrebbe dire che nessuno li sta controllando.
    ("Commercio: minimo del livello 7 da 873,22 a 800,00",
     sostituisci(("ccnl", "contratti", 0, "minimi", "livelli", "7"), 800.0)),
    ("Commercio: rimuovo del tutto la tabella dei minimi",
     sostituisci(("ccnl", "contratti", 0, "minimi"), None)),
    ("Milano: rimuovo la soglia di esenzione comunale",
     sostituisci(("territori", "MI", "anni", "2026", "comunale", "soglia_esenzione"), None)),
    ("Milano: soglia di esenzione da 23.000 a 21.000",
     sostituisci(("territori", "MI", "anni", "2026", "comunale", "soglia_esenzione"), 21000.0)),
    ("Milano: aliquota comunale da 0,8% a 0,9%",
     sostituisci(("territori", "MI", "anni", "2026", "comunale", "aliquota"), 0.009)),
    ("Lombardia: aggiungo uno scaglione inventato",
     sostituisci(("territori", "MI", "anni", "2026", "regionale", "scaglioni"),
                 [[15000.0, 0.0123], [28000.0, 0.0158], [55000.0, 0.0172],
                  [75000.0, 0.0173], [None, 0.0174]])),
    ("Palermo: aliquota 2025 da 1,014% a 1,002% (l'anno d'imposta sbagliato)",
     sostituisci(("territori", "PA", "anni", "2025", "comunale", "aliquota"), 0.01002)),
]


def esegui_suite():
    """Lancia i test e riporta (esito_leggibile, ha_rilevato_il_guasto)."""
    esito = subprocess.run([sys.executable, str(SUITE)],
                           cwd=RADICE, capture_output=True, text=True)
    for riga in esito.stdout.splitlines():
        if "test FALLITI" in riga:
            quanti = riga.split()[1]
            return f"{quanti} test falliti", True
    if esito.returncode != 0:
        return "la suite si e' interrotta con un errore", True
    return "NESSUN TEST FALLITO", False


def main():
    originale = json.loads(REGISTRO.read_text(encoding="utf-8"))
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        copia = pathlib.Path(f.name)
    shutil.copy(REGISTRO, copia)

    print(f"Controllo di sensibilita': {len(GUASTI)} guasti, un test alla volta.\n")
    scoperti = 0
    try:
        for descrizione, guasta in GUASTI:
            dati = json.loads(copia.read_text(encoding="utf-8"))
            guasta(dati)
            REGISTRO.write_text(json.dumps(dati, indent=2, ensure_ascii=False) + "\n",
                                encoding="utf-8")
            risultato, rilevato = esegui_suite()
            scoperti += rilevato
            marcatore = "  " if rilevato else "<-"
            print(f"{marcatore} {descrizione:<58s} {risultato}")
    finally:
        shutil.copy(copia, REGISTRO)
        copia.unlink(missing_ok=True)
        ripristinato = json.loads(REGISTRO.read_text(encoding="utf-8"))
        assert ripristinato == originale, "IL REGISTRO NON E' STATO RIPRISTINATO"
        print("\nRegistro ripristinato e verificato identico all'originale.")

    print(f"\nGuasti rilevati dai test: {scoperti} su {len(GUASTI)}.")
    if scoperti < len(GUASTI):
        print("Le righe marcate con <- sono buchi nella copertura: vanno chiuse.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
