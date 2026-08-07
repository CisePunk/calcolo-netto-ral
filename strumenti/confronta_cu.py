"""
Confronto del motore con una Certificazione Unica reale.

Perche' esiste
--------------
Confrontare un calcolatore con un altro calcolatore dimostra solo che due
prototipi sbagliano allo stesso modo. Una CU e' emessa da un sostituto d'imposta:
se i nostri numeri coincidono con i suoi, il motore regge contro un conteggio
fatto davvero, non contro un'altra approssimazione.

Il problema: la CU non contiene una RAL
---------------------------------------
Noi lavoriamo sulla RAL, cioe' sul LORDO. La CU dichiara l'IMPONIBILE FISCALE,
che e' gia' al netto dei contributi. Non sono la stessa cosa, e la differenza
non e' un dettaglio: e' proprio il primo passo della catena.

Una prima versione di questo strumento ricostruiva una "RAL equivalente"
sommando i contributi all'imponibile. Era un errore di metodo: la riga
"imponibile fiscale" tornava quasi per costruzione, perche' era stata usata per
costruire l'ingresso. Un test che si fabbrica la propria risposta non prova
niente — lo stesso difetto trovato nei test del motore (DIARIO_DI_BORDO.md,
voce 28).

Le due modalita'
----------------
CONFRONTO COMPLETO — se la CU dichiara l'**imponibile previdenziale** (sezione
dati previdenziali INPS). Quello e' il LORDO del periodo: da li' la catena si
verifica per intero, contributi compresi, senza ricostruire nulla.

SOLO FISCALE — se c'e' solo l'imponibile fiscale. Si parte da quello e si
verificano IRPEF, detrazioni, addizionali e bonus, cioe' tutta la macchina
tributaria. Il passo LORDO -> imponibile resta NON verificato, e lo strumento
lo dice invece di far finta di averlo controllato.

Privacy
-------
Nessun dato qui dentro: si leggono da dati_privati/cu.json, che il .gitignore di
quella cartella tiene fuori dal repository. Chi lancia lo strumento vede i propri
numeri; chi legge il repository vede il metodo, mai gli importi.

Uso
---
    cp dati_privati/cu_modello.json dati_privati/cu.json
    (riempire cu.json)
    python3 strumenti/confronta_cu.py
"""

import json
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE))

from motore import calcola, registro                              # noqa: E402
from motore.calcolo import GIORNI_ANNO, imposte_su_imponibile     # noqa: E402

DATI = RADICE / "dati_privati" / "cu.json"

# Un euro di scarto su base annua e' arrotondamento, non un errore di regola.
TOLLERANZA = 1.00

# (chiave nella CU, chiave nel risultato, etichetta, dipende_dai_giorni)
VOCI_FISCALI = [
    ("irpef_lorda", "irpef_lorda", "IRPEF lorda", False),
    ("detrazioni_lavoro_dipendente", "detrazione_lavoro_dipendente",
     "Detrazione lavoro dipendente", True),
    ("irpef_netta", "irpef_netta", "IRPEF netta", True),
    ("addizionale_regionale", "addizionale_regionale", "Addizionale regionale", False),
    ("addizionale_comunale", "addizionale_comunale", "Addizionale comunale", False),
    ("trattamento_integrativo", "trattamento_integrativo", "Trattamento integrativo", True),
    ("somma_esente_cuneo", "somma_esente_cuneo", "Somma esente cuneo fiscale", True),
]

VOCI_CONTRIBUTIVE = [
    ("contributi_previdenziali", "contributi_inps", "Contributi a carico del dipendente", False),
    ("imponibile_fiscale", "imponibile_fiscale", "Imponibile fiscale", False),
]


def carica():
    if not DATI.exists():
        print(f"Manca il file {DATI.relative_to(RADICE)}.\n")
        print("Per crearlo:")
        print("  cp dati_privati/cu_modello.json dati_privati/cu.json")
        print("  (poi riempi i valori presi dalla Certificazione Unica)\n")
        print("Il file non entrera' nel repository: la cartella e' esclusa dal .gitignore.")
        raise SystemExit(1)
    with open(DATI, encoding="utf-8") as f:
        return {k: v for k, v in json.load(f).items() if not k.startswith("_")}


def confronta(voci, cu, ottenuti, giorni_noti):
    """Restituisce (righe_stampabili, scarti, saltate)."""
    righe, scarti, saltate = [], [], []
    for chiave, attributo, etichetta, serve_giorni in voci:
        atteso = cu.get(chiave)
        if atteso is None:
            saltate.append(f"{etichetta} — non dichiarata")
            continue
        if serve_giorni and not giorni_noti:
            saltate.append(f"{etichetta} — servono i giorni di detrazione")
            continue
        ottenuto = ottenuti[attributo]
        scarto = ottenuto - atteso
        marcatore = " " if abs(scarto) <= TOLLERANZA else "!"
        righe.append(f"{marcatore} {etichetta:<34s}{atteso:>13,.2f}{ottenuto:>13,.2f}{scarto:>+11,.2f}")
        if abs(scarto) > TOLLERANZA:
            scarti.append((etichetta, scarto))
    return righe, scarti, saltate


def main():
    cu = carica()

    anno = str(cu.get("anno_imposta") or registro.anno_predefinito())
    territorio = cu.get("territorio") or registro.territorio_predefinito()
    giorni_dichiarati = cu.get("giorni_detrazione")
    giorni = giorni_dichiarati or GIORNI_ANNO
    quota_anno = giorni / GIORNI_ANNO

    imponibile = cu.get("imponibile_fiscale")
    lordo_periodo = cu.get("imponibile_previdenziale")

    if imponibile is None and lordo_periodo is None:
        raise SystemExit("Serve almeno 'imponibile_fiscale' oppure "
                         "'imponibile_previdenziale' per fare il confronto.")

    anagrafica = registro.anagrafica_territorio(territorio)
    completo = lordo_periodo is not None

    print("=" * 74)
    print("CONFRONTO CON LA CERTIFICAZIONE UNICA")
    print("=" * 74)
    print(f"  anno d'imposta : {anno}")
    print(f"  territorio     : {anagrafica['comune']} / {anagrafica['regione']}")
    print(f"  giorni         : {giorni}"
          f"{'' if giorni_dichiarati else '  (non dichiarati: assunto anno intero)'}")
    print()

    if completo:
        # L'imponibile previdenziale E' il lordo del periodo: nessuna
        # ricostruzione, la catena si verifica dall'inizio.
        ral_equivalente = lordo_periodo * GIORNI_ANNO / giorni
        risultato = calcola(ral_equivalente, anno=anno,
                            territorio_codice=territorio, giorni=giorni)
        ottenuti = risultato.come_dizionario()
        voci = VOCI_CONTRIBUTIVE + VOCI_FISCALI
        print(f"  MODALITA': confronto COMPLETO")
        print(f"  Il lordo del periodo e' dichiarato ({lordo_periodo:,.2f}): si verifica")
        print(f"  l'intera catena, contributi compresi. RAL annua equivalente:")
        print(f"  {ral_equivalente:,.2f}")
    else:
        # Si parte dall'imponibile dichiarato dalla CU: il passo lordo ->
        # imponibile non e' verificabile e non viene simulato.
        ottenuti = imposte_su_imponibile(
            imponibile, quota_anno,
            registro.nazionale(anno), registro.territorio(territorio, anno))
        voci = VOCI_FISCALI
        print(f"  MODALITA': SOLO FISCALE")
        print(f"  La CU dichiara l'imponibile ({imponibile:,.2f}) ma non il lordo.")
        print(f"  Si verifica la macchina tributaria a partire dall'imponibile.")
        print(f"  Il passo LORDO -> IMPONIBILE (i contributi) NON e' verificato.")

    print()
    print(f"  {'Voce':<34s}{'CU':>13s}{'Motore':>13s}{'Scarto':>11s}")
    print("  " + "-" * 70)

    righe, scarti, saltate = confronta(voci, cu, ottenuti, bool(giorni_dichiarati))
    for riga in righe:
        print(riga)

    print()
    if saltate:
        print("  Non confrontate:")
        for voce in saltate:
            print(f"    - {voce}")
        print()

    print("=" * 74)
    if not righe:
        print("Nessuna voce confrontata: il file e' vuoto.")
        return 1
    if not scarti:
        print(f"Le {len(righe)} voci confrontate coincidono tutte "
              f"(tolleranza {TOLLERANZA:.2f} euro).")
        if not completo:
            print("Resta fuori il passo lordo -> imponibile: per verificarlo serve")
            print("l'imponibile previdenziale, nella sezione INPS della CU.")
        return 0

    print(f"{len(scarti)} voci su {len(righe)} NON coincidono:")
    for etichetta, scarto in scarti:
        print(f"  - {etichetta}: scarto {scarto:+,.2f}")
    print()
    print("Prima di sospettare il motore, controllare in quest'ordine:")
    print("  1. l'ANNO. Una CU emessa nel 2026 riguarda i redditi 2025, dove la")
    print("     seconda aliquota IRPEF e' 35% e non 33%.")
    print("  2. il TERRITORIO. Le addizionali cambiano per comune e regione, e")
    print("     l'aliquota di Palermo e' cambiata in ognuno degli ultimi tre anni.")
    print("  3. i GIORNI. Detrazioni e bonus sono rapportati al periodo di lavoro.")
    print("  4. eventuali carichi di famiglia o altre detrazioni, che questo")
    print("     prototipo non tratta (vedi ASSUNZIONI).")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
