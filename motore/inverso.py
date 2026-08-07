"""
Calcolo inverso: dal netto desiderato alla RAL da offrire.

    "Il candidato chiede 2.000 euro netti al mese: che RAL devo mettere
     nell'offerta?"

E' la domanda che un HR fa davvero, e non richiede alcuna logica fiscale nuova:
si cerca la RAL che produce quel netto, usando il motore diretto.

Perche' NON basta una bisezione
-------------------------------
La bisezione presuppone una funzione crescente. Il netto non lo e': ha sei punti
di discontinuita' (vedi DIARIO_DI_BORDO.md, voce 25), tre in salita e tre in
discesa. Provandola sul serio, su 5.400 andate-e-ritorni RAL -> netto -> RAL,
67 tornavano sbagliate, con errori fino a 309 euro.

I due modi in cui si rompe sono diversi e vanno trattati diversamente:

  * un salto IN SALITA lascia un buco: esistono netti che NESSUNA RAL produce.
    Il piu' ampio vale 1.047,78 euro — non e' possibile guadagnare fra 8.998,76
    e 10.046,54 euro netti l'anno. La bisezione cieca risponde comunque, con una
    RAL che vale tutt'altro.

  * un salto IN DISCESA rende il netto ambiguo: lo stesso importo si ottiene con
    PIU' RAL diverse. 20.600 euro netti si ottengono sia con RAL 25.050,43 sia
    con RAL 25.356,55. Rispondere con una sola delle due, in silenzio, e' un
    errore travestito da risposta.

Come lo risolviamo
------------------
Sappiamo dove sono i gradini: li ricaviamo dal registro. Fra un gradino e il
successivo la funzione cresce davvero, quindi:

  1. si divide l'intervallo delle RAL nei segmenti separati dai gradini;
  2. in ciascun segmento, se il netto cercato ci ricade, si biseca;
  3. ogni candidato viene VERIFICATO ricalcolando il netto: al punto di salto la
     bisezione converge su una RAL che non vale l'obiettivo, e va scartata.

Cosi' si trovano TUTTE le soluzioni, oppure si dichiara che non ne esistono —
indicando i due valori raggiungibili piu' vicini.
"""

from dataclasses import dataclass, field
from functools import lru_cache

from . import registro
from .calcolo import (GIORNI_ANNO, calcola, formatta_euro,
                      normalizza_importo, valida_giorni)

# Con 60 dimezzamenti su un intervallo di 500.000 euro si scende molto sotto il
# centesimo: la precisione non e' il problema di questo calcolo.
GIRI_BISEZIONE = 60
TOLLERANZA_NETTO = 0.01
RAL_MINIMA = 1.0
RAL_MASSIMA = 1_000_000.0


# ---------------------------------------------------------------------------
# Dove sono i gradini
# ---------------------------------------------------------------------------

def soglie_di_reddito(anno, territorio_codice: str) -> dict:
    """Le soglie di imponibile su cui il netto puo' saltare, lette dal registro.

    Restituisce `{valore: [motivi]}`, non `{valore: motivo}`.

    Perche' una lista di motivi
    ---------------------------
    Piu' norme diverse cadono sullo stesso reddito. A 15.000 euro finiscono
    insieme la detrazione di fascia 1, il trattamento integrativo pieno e la
    seconda fascia della somma esente: tre ragioni, un solo punto.

    La prima stesura usava un dizionario `{valore: motivo}` e le ragioni
    successive **sovrascrivevano** le precedenti in silenzio. Su otto motivi
    dichiarati ne sopravvivevano sette, e la didascalia a 15.000 raccontava
    mezza verita' — proprio quella che finisce nel diagramma delle
    discontinuita' e nei documenti.

    L'aritmetica non ne risentiva: il confine del segmento e' lo stesso valore
    comunque, quindi il calcolo inverso restava corretto. A perdersi era solo
    la spiegazione, che e' il motivo per cui il difetto e' sopravvissuto a
    tutti i test. Segnalato da una revisione esterna; e' l'errore 25.

    Le soglie non sono elencate a mano: se domani cambia un coefficiente, i
    punti di discontinuita' si spostano da soli.
    """
    naz = registro.nazionale(anno)
    terr = registro.territorio(territorio_codice, anno)

    # Prima si RACCOLGONO le coppie, poi si raggruppano. Accumulare
    # direttamente in un dizionario e' esattamente cio' che perdeva i motivi.
    coppie = []

    # La capienza del trattamento integrativo scatta dove l'IRPEF lorda supera
    # la detrazione di fascia 1 DIMINUITA DI 75 EURO (D.Lgs. 216/2023,
    # strutturali dalla L. 207/2024 art. 1 c. 3): la soglia e' quindi
    # (detrazione - 75) / prima aliquota, non detrazione / aliquota.
    #
    # Finche' i 75 euro mancavano, questa soglia cadeva a 8.500 — esattamente
    # dove finisce anche la prima fascia della somma esente. Due discontinuita'
    # diverse sovrapposte in un punto solo: una si vedeva, l'altra no.
    prima_aliquota = naz["irpef"]["scaglioni"][0][1]
    detrazioni = naz["detrazioni_lavoro_dipendente"]
    riduzione = naz["trattamento_integrativo"].get("riduzione_detrazione_capienza", 0.0)
    coppie.append(((detrazioni["fascia_1_importo"] - riduzione) / prima_aliquota,
                   "capienza del trattamento integrativo"))

    coppie.append((detrazioni["fascia_1_limite"],
                   "fine della detrazione di fascia 1 e del trattamento integrativo pieno"))

    # Ogni cambio di fascia della somma esente e' un gradino: l'aliquota cambia
    # di colpo e si applica all'INTERO imponibile, non allo scaglione.
    fasce = naz["cuneo_somma_esente"]["fasce"]
    for indice, (limite, aliquota) in enumerate(fasce[:-1]):
        successiva = fasce[indice + 1][1]
        coppie.append((limite, f"la somma esente scende dal {aliquota:.1%} al {successiva:.1%}"
                       .replace(".", ",")))

    coppie.append((naz["cuneo_somma_esente"]["limite_reddito_complessivo"],
                   "fine della somma esente, inizio dell'ulteriore detrazione"))
    coppie.append((naz["ulteriore_detrazione_65"]["reddito_minimo_escluso"],
                   "inizio dell'ulteriore detrazione di 65 euro"))
    coppie.append((naz["ulteriore_detrazione_65"]["reddito_massimo_incluso"],
                   "fine dell'ulteriore detrazione di 65 euro"))

    soglia_comunale = terr["comunale"].get("soglia_esenzione")
    if soglia_comunale is not None:
        coppie.append((soglia_comunale, "soglia di esenzione dell'addizionale comunale"))

    soglie: dict = {}
    for valore, motivo in coppie:
        soglie.setdefault(valore, []).append(motivo)
    return dict(sorted(soglie.items()))


def ral_per_imponibile(imponibile: float, anno, giorni: int = GIORNI_ANNO,
                       territorio_codice: str = None) -> float:
    """RAL che produce quell'imponibile fiscale.

    Qui la bisezione e' sicura: l'imponibile cresce sempre con la RAL, senza
    salti. Sono le detrazioni e i bonus a introdurre le discontinuita', e qui
    non c'entrano.
    """
    basso, alto = RAL_MINIMA, RAL_MASSIMA
    for _ in range(GIRI_BISEZIONE):
        medio = (basso + alto) / 2
        risultato = calcola(medio, anno=anno, giorni=giorni,
                            territorio_codice=territorio_codice)
        if risultato.imponibile_fiscale < imponibile:
            basso = medio
        else:
            alto = medio
    return (basso + alto) / 2


@lru_cache(maxsize=64)
def punti_di_salto(anno, territorio_codice: str, giorni: int = GIORNI_ANNO) -> tuple:
    """Le RAL in cui il netto salta, in ordine crescente.

    Dipendono solo da anno, territorio e giorni: si calcolano una volta sola.
    Senza cache ogni ricerca inversa le ricalcolerebbe da capo, raddoppiando
    inutilmente il lavoro.
    """
    soglie = soglie_di_reddito(anno, territorio_codice)
    return tuple(sorted(
        ral_per_imponibile(soglia, anno, giorni, territorio_codice)
        for soglia in soglie
    ))


# ---------------------------------------------------------------------------
# Il risultato
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RisultatoInverso:
    netto_richiesto: float
    raggiungibile: bool
    ral: float | None                  # la RAL piu' bassa che ottiene il netto
    alternative: list = field(default_factory=list)   # le altre soluzioni
    netto_raggiungibile_sotto: float | None = None
    netto_raggiungibile_sopra: float | None = None
    avvisi: list = field(default_factory=list)

    @property
    def ambiguo(self) -> bool:
        return len(self.alternative) > 0


# ---------------------------------------------------------------------------
# Il calcolo
# ---------------------------------------------------------------------------

def ral_per_netto(netto_desiderato, mensile: bool = False, anno=None,
                  territorio_codice: str = None, giorni: int = GIORNI_ANNO,
                  ccnl: str = None, mensilita: int = None) -> RisultatoInverso:
    """Dal netto desiderato alla RAL.

    Con `mensile=True` il valore e' inteso al mese e viene moltiplicato per le
    mensilita' del contratto: e' il modo in cui la domanda viene posta davvero
    ("2.000 euro netti al mese"), e passare per l'annuo a mente e' proprio il
    tipo di conversione che genera errori.
    """
    # La STESSA funzione del calcolo diretto, non `float()`.
    #
    # Con `float()` il campo accettava "2000" ma leggeva "2.000" come 2 euro:
    # una RAL da 29 euro invece di 40.101. E il messaggio d'errore prometteva
    # «Esempio: 1800 oppure 1.800,50» — cioe' proponeva un formato che poi
    # rifiutava. Lo stesso difetto dell'errore 12, sopravvissuto nel percorso
    # inverso perche' la correzione era stata applicata solo dove era stato
    # trovato. Segnalato da una revisione esterna.
    if netto_desiderato is None or (
            isinstance(netto_desiderato, str) and not netto_desiderato.strip()):
        raise ValueError("Inserisci il netto che vuoi ottenere.")
    try:
        netto_desiderato = normalizza_importo(netto_desiderato)
    except (TypeError, ValueError):
        raise ValueError(
            "Non riesco a leggere questo importo. Scrivilo come preferisci: "
            "1800, 1.800 oppure 1.800,50."
        )
    if netto_desiderato != netto_desiderato or netto_desiderato in (
            float("inf"), float("-inf")):
        raise ValueError("Il netto deve essere un numero valido.")
    if netto_desiderato <= 0:
        raise ValueError("Il netto desiderato deve essere maggiore di zero.")

    giorni = valida_giorni(giorni)
    anno = str(anno) if anno is not None else registro.anno_predefinito()
    territorio_codice = territorio_codice or registro.territorio_predefinito()
    ccnl = ccnl or registro.ccnl_predefinito()
    mensilita = int(mensilita) if mensilita is not None else registro.mensilita_di(ccnl)

    obiettivo = netto_desiderato * mensilita if mensile else netto_desiderato

    def netto_di(ral):
        return calcola(ral, anno=anno, territorio_codice=territorio_codice,
                       giorni=giorni, ccnl=ccnl, mensilita=mensilita).netto_annuo

    # I segmenti fra un gradino e l'altro: qui dentro il netto cresce davvero.
    salti = list(punti_di_salto(anno, territorio_codice, giorni))
    confini = [RAL_MINIMA] + salti + [RAL_MASSIMA]
    epsilon = 1e-6

    soluzioni = []
    for inizio, fine in zip(confini, confini[1:]):
        inizio_segmento = inizio + epsilon
        fine_segmento = fine - epsilon
        if fine_segmento <= inizio_segmento:
            continue
        netto_inizio = netto_di(inizio_segmento)
        netto_fine = netto_di(fine_segmento)
        if not (netto_inizio <= obiettivo <= netto_fine):
            continue

        basso, alto = inizio_segmento, fine_segmento
        for _ in range(GIRI_BISEZIONE):
            medio = (basso + alto) / 2
            if netto_di(medio) < obiettivo:
                basso = medio
            else:
                alto = medio
        candidato = (basso + alto) / 2

        # Verifica: al confine di un salto la bisezione converge su una RAL che
        # NON produce l'obiettivo. Senza questo controllo si restituirebbero
        # soluzioni fasulle — e' successo davvero, in fase di prova.
        if abs(netto_di(candidato) - obiettivo) <= TOLLERANZA_NETTO:
            soluzioni.append(candidato)

    if soluzioni:
        soluzioni.sort()
        avvisi = []
        if len(soluzioni) > 1:
            elenco = ", ".join(formatta_euro(s) for s in soluzioni)
            avvisi.append(
                f"Questo netto si ottiene con {len(soluzioni)} RAL diverse: {elenco}. "
                "Dipende da una soglia fiscale che fa scendere il netto quando "
                "viene superata. Viene proposta la più bassa, che è la più "
                "conveniente per il datore di lavoro."
            )
        return RisultatoInverso(
            netto_richiesto=obiettivo,
            raggiungibile=True,
            ral=soluzioni[0],
            alternative=soluzioni[1:],
            avvisi=avvisi,
        )

    # Nessuna soluzione: il netto cade in un buco lasciato da un salto in salita.
    sotto, sopra = _netti_vicini(obiettivo, salti, netto_di)
    avviso = ("Nessuna RAL produce esattamente questo netto: cade in un salto "
              "della curva, dovuto a una soglia fiscale.")
    if sotto is not None and sopra is not None:
        avviso += (f" I valori raggiungibili più vicini sono "
                   f"{formatta_euro(sotto, 2)} e {formatta_euro(sopra, 2)}.")
    return RisultatoInverso(
        netto_richiesto=obiettivo,
        raggiungibile=False,
        ral=None,
        netto_raggiungibile_sotto=sotto,
        netto_raggiungibile_sopra=sopra,
        avvisi=[avviso],
    )


def _netti_vicini(obiettivo: float, salti: list, netto_di) -> tuple:
    """I netti raggiungibili immediatamente sotto e sopra un valore impossibile.

    Stanno ai due lati di un salto: il netto appena prima e appena dopo il
    gradino che ha scavalcato l'obiettivo.
    """
    epsilon = 1e-6
    for salto in salti:
        prima = netto_di(salto - epsilon)
        dopo = netto_di(salto + epsilon)
        if prima < obiettivo < dopo:
            return prima, dopo
    return None, None
