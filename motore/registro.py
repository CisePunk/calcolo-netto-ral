"""
Accesso al registro dei coefficienti.

Unico punto del codice che sa dove stanno i numeri e come sono organizzati.
Il motore di calcolo (calcolo.py) chiede "i coefficienti IRPEF del 2026" e non
sa nulla di file, chiavi o formato: se domani i coefficienti arrivano da MySQL
invece che da un JSON, cambia solo questo modulo.

Le chiavi che iniziano con "_" nel registro sono metadati (fonte, stato di
verifica, note) e non servono al calcolo: restano leggibili per la pagina
/coefficienti e per chi apre il file.
"""

import json
from functools import lru_cache
from pathlib import Path

PERCORSO_REGISTRO = Path(__file__).resolve().parent.parent / "dati" / "coefficienti.json"


@lru_cache(maxsize=1)
def _registro() -> dict:
    with open(PERCORSO_REGISTRO, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Cosa è disponibile — serve all'interfaccia per costruire i menù senza
# duplicare da nessuna parte l'elenco degli anni o dei comuni.
# ---------------------------------------------------------------------------

def anni_disponibili() -> list[str]:
    return sorted(_registro()["nazionale"].keys())


def territori_disponibili() -> list[dict]:
    """Elenco dei territori, con il predefinito segnalato."""
    return [
        {
            "codice": codice,
            "comune": dati["comune"],
            "regione": dati["regione"],
            "predefinito": dati.get("predefinito", False),
            "anni": sorted(dati["anni"].keys()),
        }
        for codice, dati in _registro()["territori"].items()
    ]


def contratti_disponibili() -> list[dict]:
    return _registro()["ccnl"]["contratti"]


def territorio_predefinito() -> str:
    for codice, dati in _registro()["territori"].items():
        if dati.get("predefinito"):
            return codice
    raise ValueError("Nessun territorio predefinito nel registro.")


def anno_predefinito() -> str:
    """L'anno più recente: è quello su cui si fanno le proiezioni."""
    return anni_disponibili()[-1]


# ---------------------------------------------------------------------------
# Lettura dei coefficienti
# ---------------------------------------------------------------------------

def nazionale(anno) -> dict:
    """Coefficienti statali dell'anno: INPS, IRPEF, detrazioni, cuneo, bonus."""
    anno = str(anno)
    dati = _registro()["nazionale"].get(anno)
    if dati is None:
        raise ValueError(
            f"Anno d'imposta {anno} non presente nel registro. "
            f"Disponibili: {', '.join(anni_disponibili())}."
        )
    return dati


def _abbreviato(valore, massimo: int = 24) -> str:
    """Accorcia un valore prima di rimandarlo in un messaggio d'errore.

    Rispedire al mittente un input arbitrariamente lungo e' un modo gratuito di
    trasformare un errore di battitura in una risposta di dimensione scelta da
    chi chiama. Ventiquattro caratteri bastano a far capire cosa non e' stato
    riconosciuto.
    """
    testo = str(valore)
    return testo if len(testo) <= massimo else testo[:massimo] + "…"


def territorio(codice: str, anno) -> dict:
    """Addizionali regionale e comunale del territorio per quell'anno."""
    anno = str(anno)
    territori = _registro()["territori"]
    if codice not in territori:
        raise ValueError(
            f"Territorio '{_abbreviato(codice)}' non presente nel registro. "
            f"Disponibili: {', '.join(sorted(territori))}."
        )
    per_anno = territori[codice]["anni"].get(anno)
    if per_anno is None:
        disponibili = ", ".join(sorted(territori[codice]["anni"]))
        raise ValueError(
            f"Il territorio '{codice}' non ha coefficienti per il {anno}. "
            f"Anni disponibili: {disponibili}."
        )
    return per_anno


def anagrafica_territorio(codice: str) -> dict:
    territori = _registro()["territori"]
    if codice not in territori:
        raise ValueError(f"Territorio '{_abbreviato(codice)}' non presente nel registro.")
    dati = territori[codice]
    return {"codice": codice, "comune": dati["comune"], "regione": dati["regione"]}


def mensilita_di(codice_ccnl: str) -> int:
    """Mensilità previste dal CCNL. Non influenza il calcolo: solo il divisore."""
    for contratto in contratti_disponibili():
        if contratto["codice"] == codice_ccnl:
            return contratto["mensilita"]
    codici = ", ".join(c["codice"] for c in contratti_disponibili())
    raise ValueError(f"CCNL '{_abbreviato(codice_ccnl)}' sconosciuto. Disponibili: {codici}.")


def minimi_di(codice_ccnl: str) -> dict | None:
    """La tabella dei minimi tabellari del CCNL, se il registro ce l'ha.

    Restituisce None quando il contratto non ha minimi censiti: e' una
    risposta legittima, e chi chiama deve dire "non lo so" invece di
    calcolare un confronto con una tabella che non esiste.
    """
    for contratto in contratti_disponibili():
        if contratto["codice"] == codice_ccnl:
            return contratto.get("minimi")
    raise ValueError(f"CCNL '{_abbreviato(codice_ccnl)}' sconosciuto.")


def ccnl_predefinito() -> str:
    for contratto in contratti_disponibili():
        if contratto.get("predefinito"):
            return contratto["codice"]
    return contratti_disponibili()[0]["codice"]


def mensilita_ammesse() -> list[int]:
    return _registro()["ccnl"]["mensilita_ammesse"]


# ---------------------------------------------------------------------------
# Provenienza — quello che rende il registro diverso da un file di costanti
# ---------------------------------------------------------------------------

def provenienza(sezione: dict) -> dict:
    """Fonte, stato di verifica e nota di un gruppo di coefficienti."""
    return {
        "fonte": sezione.get("_fonte"),
        "stato": sezione.get("_stato"),
        "nota": sezione.get("_nota"),
    }


def elenco_provenienze(anno, codice_territorio: str) -> list[dict]:
    """Tutte le voci usate per un calcolo, con la loro fonte.

    È quello che alimenta la pagina /coefficienti e la modalità esperto: ogni
    numero mostrato all'utente può essere ricondotto a un atto e a una data.
    """
    voci = []
    for nome, sezione in nazionale(anno).items():
        if isinstance(sezione, dict) and "_fonte" in sezione:
            voci.append({"ambito": "nazionale", "voce": nome, **provenienza(sezione)})

    anagrafica = anagrafica_territorio(codice_territorio)
    for nome, sezione in territorio(codice_territorio, anno).items():
        if isinstance(sezione, dict) and "_fonte" in sezione:
            voci.append({
                "ambito": f"{anagrafica['comune']} / {anagrafica['regione']}",
                "voce": nome,
                **provenienza(sezione),
            })
    return voci


def riepilogo_verifiche(anno, codice_territorio: str) -> dict:
    """Quante voci sono su fonte primaria, quante no. Onestà in cifre."""
    conteggio = {"primaria": 0, "secondaria": 0, "da_verificare": 0}
    for voce in elenco_provenienze(anno, codice_territorio):
        stato = voce.get("stato")
        if stato in conteggio:
            conteggio[stato] += 1
    return conteggio
