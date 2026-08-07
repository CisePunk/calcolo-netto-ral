"""
API del calcolatore RAL -> netto.

Il ruolo di questo strato e' sottile ma preciso: **non calcola niente**.
Traduce richieste HTTP in chiamate al motore e risposte del motore in JSON,
e converte gli errori di validazione in messaggi che l'interfaccia possa
mostrare cosi' come sono.

Tutta la logica fiscale vive in motore/, che non sa nulla del web. E' la
condizione perche' il calcolo resti verificabile con `python3 test_motore.py`
senza avviare un server, e perche' un errore nel routing non possa mai
diventare un errore in una busta paga.
"""

from pathlib import Path

import time
from collections import deque

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from motore import calcola, registro                     # noqa: E402
from motore.calcolo import GIORNI_ANNO                   # noqa: E402
from motore.inverso import ral_per_netto                 # noqa: E402

RADICE = Path(__file__).resolve().parent.parent
FRONTEND = RADICE / "web" / "dist"

app = FastAPI(
    title="Calcolatore RAL → netto",
    description=(
        "Calcolo della retribuzione netta a partire dalla RAL. "
        "Ogni coefficiente usato è consultabile con la sua fonte su /api/coefficienti."
    ),
    version="1.0.0",
)

# In sviluppo il frontend gira su una porta diversa (Vite, 5173). In produzione
# viene servito da qui, quindi l'origine e' la stessa e CORS non entra in gioco.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Intestazioni di sicurezza
# ---------------------------------------------------------------------------

# La pagina non carica NULLA da domini esterni: nessun carattere tipografico
# remoto, nessuna libreria da CDN, nessuna immagine di terze parti. Questo
# permette una politica dei contenuti molto stretta, che e' la differenza fra
# "probabilmente non c'e' modo di iniettare uno script" e "il browser lo
# impedisce".
POLITICA_CONTENUTI = "; ".join([
    "default-src 'self'",
    # Vite mette lo stile del pacchetto in un foglio esterno, ma alcuni stili
    # calcolati (le larghezze dei segmenti del grafico) sono in linea.
    "style-src 'self' 'unsafe-inline'",
    "script-src 'self'",
    "img-src 'self' data:",
    "font-src 'self'",
    "connect-src 'self'",
    "form-action 'none'",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "object-src 'none'",
])

INTESTAZIONI_SICUREZZA = {
    "Content-Security-Policy": POLITICA_CONTENUTI,
    # Impedisce al browser di indovinare il tipo di un file servito: senza,
    # un file interpretato come script diventa un vettore.
    "X-Content-Type-Options": "nosniff",
    # Nessuno puo' incorniciare la pagina: toglie di mezzo il clickjacking,
    # che su uno strumento con un pulsante di conferma non e' teorico.
    "X-Frame-Options": "DENY",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=(), payment=()",
}


# ---------------------------------------------------------------------------
# Limite di frequenza
# ---------------------------------------------------------------------------

# Il calcolo inverso costa circa quindici millisecondi: non e' pesante, ma e'
# ottanta volte il calcolo diretto, e senza alcun limite un solo client puo'
# occupare il servizio a costo quasi nullo per se'.
#
# Questo e' un limite volutamente elementare, in memoria: basta per un
# prototipo pubblicato su un piano gratuito, e non pretende di essere altro.
# Dietro a piu' processi o piu' macchine servirebbe uno stato condiviso, ed e'
# scritto qui perche' chi lo legge non lo scambi per una difesa completa.
FINESTRA_SECONDI = 60
RICHIESTE_PER_FINESTRA = 120
_visite: dict[str, deque] = {}


@app.middleware("http")
async def limite_di_frequenza(richiesta: Request, prosegui):
    if not richiesta.url.path.startswith("/api/"):
        return await prosegui(richiesta)

    chiave = richiesta.client.host if richiesta.client else "sconosciuto"
    adesso = time.monotonic()
    coda = _visite.setdefault(chiave, deque())
    while coda and adesso - coda[0] > FINESTRA_SECONDI:
        coda.popleft()

    if len(coda) >= RICHIESTE_PER_FINESTRA:
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=429,
            content={"detail": "Troppe richieste ravvicinate. Riprova fra un minuto."},
            headers={"Retry-After": str(FINESTRA_SECONDI)},
        )

    coda.append(adesso)
    # Senza questa potatura la mappa cresce con il numero di indirizzi visti.
    if len(_visite) > 5_000:
        for k in [k for k, v in _visite.items() if not v or adesso - v[-1] > FINESTRA_SECONDI]:
            _visite.pop(k, None)
    return await prosegui(richiesta)


# Registrato per ultimo, quindi eseguito per primo: Starlette costruisce la pila
# al contrario, e l'ultimo middleware aggiunto e' il piu' esterno. Con l'ordine
# opposto la risposta 429 del limite di frequenza usciva senza intestazioni,
# perche' non attraversava mai questo strato. Verificato con una richiesta vera,
# non dedotto dalla documentazione.
@app.middleware("http")
async def intestazioni_di_sicurezza(richiesta: Request, prosegui):
    risposta = await prosegui(richiesta)
    for nome, valore in INTESTAZIONI_SICUREZZA.items():
        risposta.headers.setdefault(nome, valore)
    return risposta


# ---------------------------------------------------------------------------
# Modelli di richiesta
# ---------------------------------------------------------------------------

class RichiestaCalcolo(BaseModel):
    # La RAL arriva come stringa perche' l'utente puo' scriverla in molti modi
    # ("35000", "35.000", "35.000,50"): la normalizzazione e la validazione
    # stanno nel motore, in un posto solo, non sparse fra interfaccia e API.
    ral: str | float = Field(description="Retribuzione annua lorda")
    anno: int | None = None
    territorio: str | None = None
    ccnl: str | None = None
    mensilita: int | None = None
    giorni: int = Field(default=GIORNI_ANNO, description="Giorni di detrazione")


class RichiestaInversa(BaseModel):
    netto: str | float = Field(description="Netto desiderato")
    mensile: bool = Field(default=True, description="Se il netto è mensile o annuo")
    anno: int | None = None
    territorio: str | None = None
    ccnl: str | None = None
    mensilita: int | None = None
    giorni: int = GIORNI_ANNO


# ---------------------------------------------------------------------------
# Opzioni: l'interfaccia non deve conoscere nessun elenco
# ---------------------------------------------------------------------------

@app.get("/api/opzioni", tags=["riferimenti"])
def opzioni():
    """Anni, territori, contratti e mensilità disponibili.

    L'interfaccia costruisce i menù da qui e non contiene nessun elenco
    codificato: aggiungere un comune al registro lo fa comparire in pagina
    senza toccare il frontend.
    """
    return {
        "anni": [int(a) for a in registro.anni_disponibili()],
        "anno_predefinito": int(registro.anno_predefinito()),
        "territori": registro.territori_disponibili(),
        "territorio_predefinito": registro.territorio_predefinito(),
        "ccnl": registro.contratti_disponibili(),
        "ccnl_predefinito": registro.ccnl_predefinito(),
        "mensilita_ammesse": registro.mensilita_ammesse(),
        "giorni_anno": GIORNI_ANNO,
    }


# ---------------------------------------------------------------------------
# Calcolo diretto
# ---------------------------------------------------------------------------

@app.post("/api/calcolo", tags=["calcolo"])
def calcolo(richiesta: RichiestaCalcolo):
    """Dalla RAL al netto, con il dettaglio di ogni trattenuta."""
    try:
        risultato = calcola(
            richiesta.ral,
            anno=richiesta.anno,
            territorio_codice=richiesta.territorio,
            giorni=richiesta.giorni,
            ccnl=richiesta.ccnl,
            mensilita=richiesta.mensilita,
        )
    except ValueError as errore:
        # I messaggi del motore sono gia' scritti per essere letti da una
        # persona: non vanno riformulati qui, o si finisce con due versioni
        # dello stesso testo che divergono.
        raise HTTPException(status_code=400, detail=str(errore))

    dati = risultato.come_dizionario()
    dati["voci"] = [
        {
            "etichetta": voce.etichetta,
            "importo": round(voce.importo, 2),
            "segno": voce.segno,
            "provenienza": voce.provenienza,
        }
        for voce in risultato.voci
    ]
    dati["verifiche"] = registro.riepilogo_verifiche(
        risultato.anno, risultato.territorio)
    return dati


# ---------------------------------------------------------------------------
# Calcolo inverso
# ---------------------------------------------------------------------------

@app.post("/api/inverso", tags=["calcolo"])
def inverso(richiesta: RichiestaInversa):
    """Dal netto desiderato alla RAL da offrire.

    Puo' restituire piu' soluzioni, o nessuna: il netto non cresce in modo
    continuo con il lordo, e la risposta lo dice invece di sceglierne una in
    silenzio.
    """
    try:
        esito = ral_per_netto(
            richiesta.netto,
            mensile=richiesta.mensile,
            anno=richiesta.anno,
            territorio_codice=richiesta.territorio,
            giorni=richiesta.giorni,
            ccnl=richiesta.ccnl,
            mensilita=richiesta.mensilita,
        )
    except ValueError as errore:
        raise HTTPException(status_code=400, detail=str(errore))

    risposta = {
        "netto_richiesto": round(esito.netto_richiesto, 2),
        "raggiungibile": esito.raggiungibile,
        "ral": round(esito.ral, 2) if esito.ral is not None else None,
        "alternative": [round(a, 2) for a in esito.alternative],
        "ambiguo": esito.ambiguo,
        "avvisi": esito.avvisi,
        "netto_raggiungibile_sotto": (
            round(esito.netto_raggiungibile_sotto, 2)
            if esito.netto_raggiungibile_sotto is not None else None),
        "netto_raggiungibile_sopra": (
            round(esito.netto_raggiungibile_sopra, 2)
            if esito.netto_raggiungibile_sopra is not None else None),
    }

    # Se una RAL c'e', la si ricalcola in avanti e si allega il dettaglio: cosi'
    # chi legge vede il risultato completo e puo' controllare che il netto
    # trovato sia davvero quello chiesto.
    if esito.raggiungibile:
        verifica = calcola(
            esito.ral, anno=richiesta.anno, territorio_codice=richiesta.territorio,
            giorni=richiesta.giorni, ccnl=richiesta.ccnl, mensilita=richiesta.mensilita)
        risposta["dettaglio"] = calcolo(RichiestaCalcolo(
            ral=verifica.ral, anno=richiesta.anno, territorio=richiesta.territorio,
            giorni=richiesta.giorni, ccnl=richiesta.ccnl, mensilita=richiesta.mensilita))
    return risposta


# ---------------------------------------------------------------------------
# Coefficienti: la parte che rende il calcolo ispezionabile
# ---------------------------------------------------------------------------

@app.get("/api/coefficienti", tags=["riferimenti"])
def coefficienti(
    anno: int | None = Query(default=None),
    territorio: str | None = Query(default=None),
):
    """Ogni coefficiente usato, con la norma che lo fissa e il suo stato.

    E' l'endpoint che distingue questo strumento da una scatola chiusa: il
    numero non arriva mai senza la sua provenienza.
    """
    anno = str(anno) if anno is not None else registro.anno_predefinito()
    territorio = territorio or registro.territorio_predefinito()
    try:
        voci = registro.elenco_provenienze(anno, territorio)
        riepilogo = registro.riepilogo_verifiche(anno, territorio)
    except ValueError as errore:
        raise HTTPException(status_code=400, detail=str(errore))
    return {
        "anno": int(anno),
        "territorio": registro.anagrafica_territorio(territorio),
        "riepilogo": riepilogo,
        "voci": voci,
    }


@app.get("/api/salute", tags=["servizio"])
def salute():
    """Controllo di vita, e insieme prova che il motore risponde davvero.

    Un servizio che risponde "sto bene" senza aver provato a calcolare nulla
    dice poco: qui si esegue un caso noto e si verifica che il numero sia
    quello atteso.
    """
    prova = calcola(35_000, anno=2026, territorio_codice="MI")
    atteso = 26_032.22
    return {
        "stato": "ok" if abs(prova.netto_annuo - atteso) < 0.01 else "coefficienti alterati",
        "caso_di_prova": {
            "ral": 35_000, "anno": 2026, "territorio": "MI",
            "netto_atteso": atteso,
            "netto_calcolato": round(prova.netto_annuo, 2),
        },
    }


# ---------------------------------------------------------------------------
# Frontend
# ---------------------------------------------------------------------------

if FRONTEND.is_dir():
    app.mount("/assets", StaticFiles(directory=FRONTEND / "assets"), name="assets")

    # I file in /assets hanno il contenuto nel nome (index-a1b2c3.js): se cambia
    # il contenuto cambia il nome, quindi possono essere tenuti in cache per
    # sempre senza rischio.
    #
    # index.html e' l'opposto: il nome resta uguale e il contenuto cambia a ogni
    # compilazione, perche' e' lui a dire quali pacchetti caricare. Se il
    # browser lo tiene in cache continua a chiedere i pacchetti VECCHI, e chi
    # usa l'applicazione vede una versione precedente senza avere alcun modo di
    # accorgersene: le modifiche semplicemente "non funzionano".
    #
    # E' successo davvero durante lo sviluppo, ed e' costato un giro di verifiche
    # su codice che era gia' corretto.
    SENZA_CACHE = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0",
    }

    def _dentro_al_frontend(percorso: str) -> Path | None:
        """Risolve il percorso richiesto e lo restituisce solo se sta dentro
        la cartella dell'applicazione compilata.

        Senza questo controllo, `FRONTEND / "../../api/main.py"` e' un file che
        esiste, e verrebbe servito. Oggi non succede perche' lo strato ASGI
        normalizza il percorso prima di consegnarlo — ma quella e' una
        protezione di qualcun altro, che sparisce mettendo davanti un proxy o
        cambiando server. Una difesa che dipende da un componente che non
        controlliamo non e' una difesa: e' una coincidenza.

        `resolve()` scioglie anche i collegamenti simbolici, quindi un link
        dentro dist che punta fuori non aggira il controllo.
        """
        if not percorso:
            return None
        try:
            candidato = (FRONTEND / percorso).resolve()
        except (OSError, RuntimeError):
            return None
        radice = FRONTEND.resolve()
        if candidato == radice or radice in candidato.parents:
            return candidato if candidato.is_file() else None
        return None

    @app.get("/{percorso:path}", include_in_schema=False)
    def pagina(percorso: str):
        """Serve l'applicazione compilata. Un solo indirizzo per tutto.

        Qualunque percorso che non corrisponda a un file dentro la cartella
        compilata restituisce l'applicazione: e' il comportamento richiesto da
        un'interfaccia a pagina unica, e insieme evita di rivelare quali file
        esistono e quali no.
        """
        file = _dentro_al_frontend(percorso)
        if file is not None:
            return FileResponse(file)
        return FileResponse(FRONTEND / "index.html", headers=SENZA_CACHE)
