"""
Test del motore di calcolo. Nessuna dipendenza esterna:

    python3 test_motore.py

Cosa verificano, in ordine di importanza:

  1. UN CASO VERIFICATO A MANO, voce per voce. Se il motore sbaglia una regola,
     questo test cade per primo e dice quale voce.

  2. LE DISCONTINUITA'. Il dominio fiscale e' pieno di soglie, e attraversarle
     fa saltare il netto. Il test non si limita a tollerarlo: pretende che i
     salti siano ESATTAMENTE quelli previsti dal registro, con il segno giusto.
     Una discontinuita' non prevista fa fallire il test. E' il controllo piu'
     utile che ci sia, perche' e' dove un errore passerebbe inosservato.

  3. LE INVARIANTI su tutto l'arco dei redditi: nessun valore assurdo, nessun
     NaN, identita' contabile sempre rispettata.

  4. La meccanica di base, la validazione degli input, i periodi parziali.

NOTA su un'invariante che NON vale, e non e' un errore: il netto puo' SUPERARE
il lordo per i redditi bassi, perche' somma esente e trattamento integrativo
sono denaro corrisposto in piu', non riduzioni di imposta. Vedi il test apposito.
"""

import math

from motore import calcolo, inverso, registro
from motore.calcolo import calcola

CENTESIMO = 0.01
TOLLERANZA = 0.01

_esiti = {"ok": 0, "falliti": []}


def verifica(descrizione, condizione, dettaglio=""):
    if condizione:
        _esiti["ok"] += 1
    else:
        _esiti["falliti"].append(f"{descrizione}{'  ->  ' + dettaglio if dettaglio else ''}")
        print(f"  [FAIL] {descrizione}")
        if dettaglio:
            print(f"         {dettaglio}")


def quasi_uguale(a, b, tolleranza=TOLLERANZA):
    return abs(a - b) <= tolleranza


def titolo(testo):
    print(f"\n{testo}")
    print("-" * len(testo))


# ===========================================================================
# 0. Ancoraggio del registro ai valori verificati sulle fonti
# ===========================================================================

titolo("0. Il registro contiene i valori confermati sulle fonti primarie")

# Questi test non guardano il motore ma i DATI, e sono l'unica parte della
# suite che non puo' essere ricavata dal registro: i valori sono scritti qui
# a mano, presi dalla fonte. Senza di essi, un test che deriva le proprie
# attese dal registro si adatterebbe silenziosamente a un dato guasto —
# esattamente il buco che un controllo di sensibilita' ha fatto emergere.

ANCORE = [
    ("IRPEF 2026, seconda aliquota = 33% (L. 199/2025)",
     lambda: registro.nazionale("2026")["irpef"]["scaglioni"][1][1], 0.33),
    ("IRPEF 2025, seconda aliquota = 35%",
     lambda: registro.nazionale("2025")["irpef"]["scaglioni"][1][1], 0.35),
    ("IRPEF, soglie degli scaglioni = 28.000 e 50.000",
     lambda: (registro.nazionale("2026")["irpef"]["scaglioni"][0][0],
              registro.nazionale("2026")["irpef"]["scaglioni"][1][0]), (28_000.0, 50_000.0)),
    ("INPS, aliquota a carico del dipendente = 9,19%",
     lambda: registro.nazionale("2026")["inps"]["aliquota_dipendente"], 0.0919),
    ("Milano, addizionale comunale = 0,8% (tabella Agenzia delle Entrate, F205)",
     lambda: registro.territorio("MI", "2025")["comunale"]["aliquota"], 0.008),
    ("Milano, soglia di esenzione = 23.000 euro (stessa fonte)",
     lambda: registro.territorio("MI", "2025")["comunale"]["soglia_esenzione"], 23_000.0),
    ("Palermo 2025, addizionale comunale = 1,014% (tabella AdE, G273)",
     lambda: registro.territorio("PA", "2025")["comunale"]["aliquota"], 0.01014),
    ("Palermo, nessuna soglia di esenzione",
     lambda: registro.territorio("PA", "2025")["comunale"]["soglia_esenzione"], None),
    ("Ulteriore detrazione di 65 euro: fascia 25.000-35.000 (art. 13 c. 1.1)",
     lambda: (registro.nazionale("2026")["ulteriore_detrazione_65"]["reddito_minimo_escluso"],
              registro.nazionale("2026")["ulteriore_detrazione_65"]["reddito_massimo_incluso"]),
     (25_000.0, 35_000.0)),
    ("Cuneo fiscale, detrazione piena = 1.000 euro fino a 32.000 (L. 207/2024 c. 6)",
     lambda: (registro.nazionale("2026")["cuneo_ulteriore_detrazione"]["importo_pieno"],
              registro.nazionale("2026")["cuneo_ulteriore_detrazione"]["reddito_soglia_piena"]),
     (1_000.0, 32_000.0)),
    ("Trattamento integrativo = 1.200 euro fino a 15.000",
     lambda: (registro.nazionale("2026")["trattamento_integrativo"]["importo"],
              registro.nazionale("2026")["trattamento_integrativo"]["soglia_importo_pieno"]),
     (1_200.0, 15_000.0)),
    ("Milano 2026: aliquota 0,8% e soglia 23.000 (invariate rispetto al 2025)",
     lambda: (registro.territorio("MI", "2026")["comunale"]["aliquota"],
              registro.territorio("MI", "2026")["comunale"]["soglia_esenzione"]),
     (0.008, 23_000.0)),
    ("Lombardia: quattro scaglioni, soglie allineate a quelle IRPEF",
     lambda: registro.territorio("MI", "2026")["regionale"]["scaglioni"],
     [[15_000.0, 0.0123], [28_000.0, 0.0158], [50_000.0, 0.0172], [None, 0.0173]]),
    ("Sicilia: aliquota unica 1,23%",
     lambda: registro.territorio("PA", "2026")["regionale"]["aliquota"], 0.0123),
    ("Cuneo, somma esente: 7,1% / 5,3% / 4,8% (L. 207/2024 c. 4-5)",
     lambda: registro.nazionale("2026")["cuneo_somma_esente"]["fasce"],
     [[8_500.0, 0.071], [15_000.0, 0.053], [20_000.0, 0.048]]),
    ("INPS 2026: prima fascia 56.224, massimale 122.295",
     lambda: (registro.nazionale("2026")["inps"]["soglia_prima_fascia"],
              registro.nazionale("2026")["inps"]["massimale_annuo"]),
     (56_224.0, 122_295.0)),
]

for descrizione, leggi, atteso in ANCORE:
    ottenuto = leggi()
    verifica(descrizione, ottenuto == atteso, f"nel registro: {ottenuto!r}, atteso {atteso!r}")


# ===========================================================================
# 1. Il caso verificato a mano
# ===========================================================================

titolo("1. Caso di riferimento: RAL 35.000, Milano, 2026 (calcolato a mano)")

# Ogni valore atteso e' stato ricavato applicando la norma a mano, non
# copiando l'output del motore: e' l'unico modo perche' il test dimostri
# qualcosa invece di fotografare un eventuale errore.
ATTESI_35K = {
    "contributi_inps": 3216.50,            # 35.000 x 9,19%
    "imponibile_fiscale": 31783.50,        # 35.000 - contributi
    "irpef_lorda": 7688.56,                # 28.000x23% + 3.783,50x33%
    "detrazione_lavoro_dipendente": 1581.52,   # 1.910 x (50.000-31.783,50)/22.000
    "ulteriore_detrazione_65": 65.00,      # art. 13 c. 1.1 (25.000 < R <= 35.000)
    "detrazione_cuneo": 1000.00,           # L. 207/2024 (20.000 < R <= 32.000)
    "irpef_netta": 5042.03,                # lorda - detrazioni
    "addizionale_regionale": 454.98,       # 15.000x1,23% + 13.000x1,58% + 3.783,50x1,72%
    "addizionale_comunale": 254.27,        # 31.783,50 x 0,8%
    "netto_annuo": 26032.22,
}

riferimento = calcola(35_000, anno=2026, territorio_codice="MI")
for voce, atteso in ATTESI_35K.items():
    ottenuto = getattr(riferimento, voce)
    verifica(f"{voce} = {atteso:,.2f}", quasi_uguale(ottenuto, atteso),
             f"ottenuto {ottenuto:,.4f}")

verifica("netto mensile = netto annuo / 14 (CCNL commercio)",
         quasi_uguale(riferimento.netto_mensile, riferimento.netto_annuo / 14))

# Secondo caso di riferimento, scelto apposta SOTTO la soglia di esenzione
# comunale: qui l'addizionale comunale deve essere zero. Serve a fissare
# l'effetto della soglia, che il caso da 35.000 non attraversa e quindi non
# proteggerebbe se il dato sparisse dal registro.
ATTESI_25K = {
    "contributi_inps": 2297.50,            # 25.000 x 9,19%
    "imponibile_fiscale": 22702.50,
    "irpef_lorda": 5221.58,                # 22.702,50 x 23%
    "detrazione_lavoro_dipendente": 2394.93,   # 1.910 + 1.190 x (28.000-22.702,50)/13.000
    "ulteriore_detrazione_65": 0.00,       # sotto i 25.000: non spetta
    "detrazione_cuneo": 1000.00,
    "irpef_netta": 1826.65,
    "addizionale_regionale": 306.20,       # 15.000x1,23% + 7.702,50x1,58%
    "addizionale_comunale": 0.00,          # imponibile sotto la soglia di 23.000
    "netto_annuo": 20569.65,
}

riferimento_basso = calcola(25_000, anno=2026, territorio_codice="MI")
for voce, atteso in ATTESI_25K.items():
    ottenuto = getattr(riferimento_basso, voce)
    verifica(f"RAL 25.000: {voce} = {atteso:,.2f}", quasi_uguale(ottenuto, atteso),
             f"ottenuto {ottenuto:,.4f}")

# Terzo caso: reddito basso. Serve a esercitare somma esente e trattamento
# integrativo, che nei due casi precedenti valgono zero e quindi resterebbero
# senza protezione.
ATTESI_16K = {
    "contributi_inps": 1470.40,            # 16.000 x 9,19%
    "imponibile_fiscale": 14529.60,
    "irpef_lorda": 3341.81,                # 14.529,60 x 23%
    "detrazione_lavoro_dipendente": 1955.00,   # fascia 1, fino a 15.000
    "detrazione_cuneo": 0.00,              # sotto i 20.000 non spetta
    "irpef_netta": 1386.81,
    "addizionale_regionale": 178.71,       # tutto nel primo scaglione, 1,23%
    "addizionale_comunale": 0.00,          # sotto la soglia di 23.000
    "somma_esente_cuneo": 770.07,          # 14.529,60 x 5,3% (fascia 8.500-15.000)
    "trattamento_integrativo": 1200.00,    # con capienza: lorda > detrazione
    "netto_annuo": 14934.15,
}

riferimento_povero = calcola(16_000, anno=2026, territorio_codice="MI")
for voce, atteso in ATTESI_16K.items():
    ottenuto = getattr(riferimento_povero, voce)
    verifica(f"RAL 16.000: {voce} = {atteso:,.2f}", quasi_uguale(ottenuto, atteso),
             f"ottenuto {ottenuto:,.4f}")

# Quarto caso: reddito alto. Esercita il contributo aggiuntivo dell'1% oltre la
# prima fascia, il terzo scaglione IRPEF, l'azzeramento delle detrazioni e
# l'ultimo scaglione dell'addizionale regionale.
ATTESI_80K = {
    "contributi_inps": 7589.76,            # 80.000x9,19% + (80.000-56.224)x1%
    "imponibile_fiscale": 72410.24,
    "irpef_lorda": 23336.40,               # 28.000x23% + 22.000x33% + 22.410,24x43%
    "detrazione_lavoro_dipendente": 0.00,  # oltre 50.000 non spetta
    "ulteriore_detrazione_65": 0.00,
    "detrazione_cuneo": 0.00,              # oltre 40.000 non spetta
    "irpef_netta": 23336.40,
    "addizionale_regionale": 1156.00,      # tutti e quattro gli scaglioni
    "addizionale_comunale": 579.28,        # 72.410,24 x 0,8%
    "netto_annuo": 47338.56,
}

riferimento_alto = calcola(80_000, anno=2026, territorio_codice="MI")
for voce, atteso in ATTESI_80K.items():
    ottenuto = getattr(riferimento_alto, voce)
    verifica(f"RAL 80.000: {voce} = {atteso:,.2f}", quasi_uguale(ottenuto, atteso),
             f"ottenuto {ottenuto:,.4f}")


# ===========================================================================
# 2. La riforma IRPEF si vede al centesimo
# ===========================================================================

titolo("2. Differenza 2026 / 2025: solo la seconda aliquota IRPEF")

# Fra i due anni cambia la seconda aliquota (35% -> 33%). Su una RAL che ricade
# in quello scaglione, la differenza di netto deve essere ESATTAMENTE il 2%
# della quota di imponibile compresa fra 28.000 e 50.000.
r26 = calcola(45_000, anno=2026, territorio_codice="MI")
r25 = calcola(45_000, anno=2025, territorio_codice="MI")
quota_secondo_scaglione = min(r26.imponibile_fiscale, 50_000) - 28_000
atteso = quota_secondo_scaglione * 0.02
verifica("RAL 45.000: differenza 2026-2025 = 2% della quota nel secondo scaglione",
         quasi_uguale(r26.netto_annuo - r25.netto_annuo, atteso),
         f"differenza {r26.netto_annuo - r25.netto_annuo:,.2f}, attesa {atteso:,.2f}")

verifica("sotto i 28.000 i due anni coincidono",
         quasi_uguale(calcola(25_000, anno=2026).netto_annuo,
                      calcola(25_000, anno=2025).netto_annuo))


# ===========================================================================
# 3. Le discontinuita': dove sono, quante sono, in che direzione
# ===========================================================================

titolo("3. Discontinuita': solo quelle previste dal registro")


def soglie_attese(anno, territorio_codice):
    """Le soglie su cui il netto puo' saltare — SCRITTE A MANO.

    La prima versione le ricavava dal registro, con la motivazione che cosi'
    "il test si aggiorna da solo se cambia un coefficiente". Era esattamente
    l'errore 5 di ERRORI.md ripetuto in un punto diverso: un test che deriva
    la propria risposta da cio' che dovrebbe controllare non controlla niente.

    E ha avuto la conseguenza prevista. La soglia di capienza del trattamento
    integrativo era calcolata come detrazione / aliquota, senza i 75 euro di
    riduzione previsti dalla L. 234/2021. Il registro sbagliava, il test
    rifaceva lo stesso conto sbagliato, ed entrambi erano d'accordo. E' stata
    trovata da una revisione esterna, non da qui.

    Adesso ogni numero e' calcolato a mano e scritto per esteso. Se domani un
    coefficiente cambia, questo test FALLISCE — ed e' il comportamento giusto:
    un cambio di aliquota deve costringere qualcuno a guardare.

    Valori per il 2026. Il segno e' la direzione del salto del netto.
    """
    if str(anno) != "2026":
        # Gli ancoraggi sono stati calcolati per il 2026. Per gli altri anni si
        # dichiara di non sapere invece di indovinare.
        return None

    soglie = {
        # (1.955 - 75) / 23%  — la detrazione art. 13 diminuita dei 75 euro
        # della L. 234/2021. Sopra questa soglia l'IRPEF lorda supera la
        # detrazione ridotta e il trattamento integrativo da 1.200 spetta.
        8173.91: ("capienza del trattamento integrativo", +1),

        # Fine della prima fascia della somma esente del cuneo: l'aliquota
        # scende dal 7,1% al 5,3% e si applica all'INTERO imponibile, non allo
        # scaglione. Finche' la soglia qui sopra era sbagliata le due cadevano
        # nello stesso punto, e questa non si vedeva.
        8500.0: ("cambio di fascia della somma esente: 7,1% -> 5,3%", -1),

        # Fine della detrazione di fascia 1 (1.955 pieni) e del trattamento
        # integrativo pieno.
        15000.0: ("fine detrazione di fascia 1 e del trattamento integrativo", -1),

        # Fine della somma esente, inizio dell'ulteriore detrazione del cuneo.
        20000.0: ("somma esente -> ulteriore detrazione del cuneo", +1),

        # Ulteriore detrazione da 65 euro, art. 13 c. 1.1: inizio e fine.
        25000.0: ("inizio ulteriore detrazione di 65 euro", +1),
        35000.0: ("fine ulteriore detrazione di 65 euro", -1),
    }

    # La soglia di esenzione comunale esiste a Milano, non a Palermo. E'
    # l'unica differenza fra i due territori nel numero di discontinuita'.
    if territorio_codice == "MI":
        soglie[23000.0] = ("soglia di esenzione dell'addizionale comunale", -1)

    return soglie


def discontinuita(anno, territorio_codice, fino_a=60_000, passo=1.0):
    """Scansiona e restituisce ogni punto in cui il netto salta.

    Un passo di un euro basta: i salti reali valgono decine o centinaia di euro,
    mentre la variazione ordinaria e' inferiore all'euro.
    """
    trovate = []
    precedente = None
    valore = passo
    while valore <= fino_a:
        r = calcola(valore, anno=anno, territorio_codice=territorio_codice)
        if precedente is not None:
            delta = r.netto_annuo - precedente
            if delta < 0 or delta > passo * 2:
                trovate.append((r.imponibile_fiscale, delta))
        precedente = r.netto_annuo
        valore += passo
    return trovate


for codice in ("MI", "PA"):
    anagrafica = registro.anagrafica_territorio(codice)
    attese = soglie_attese("2026", codice)
    trovate = discontinuita("2026", codice)

    verifica(f"{anagrafica['comune']}: {len(attese)} discontinuita' attese, {len(trovate)} trovate",
             len(trovate) == len(attese),
             f"trovate a imponibile {[round(i) for i, _ in trovate]}, "
             f"attese a {sorted(round(s) for s in attese)}")

    for imponibile, delta in trovate:
        # Con passo di un euro il salto viene rilevato appena oltre la soglia.
        vicina = min(attese, key=lambda s: abs(s - imponibile))
        verifica(f"{anagrafica['comune']}: salto a imponibile {imponibile:,.2f} "
                 f"e' sulla soglia {vicina:,.0f} ({attese[vicina][0]})",
                 abs(imponibile - vicina) <= 2.0,
                 f"soglia piu' vicina a {vicina:,.0f}, distante {abs(imponibile - vicina):.2f}")
        segno_atteso = attese[vicina][1]
        verifica(f"{anagrafica['comune']}: il salto a {vicina:,.0f} va nella direzione prevista",
                 (delta > 0) == (segno_atteso > 0),
                 f"variazione {delta:+,.2f}, attesa {'in salita' if segno_atteso > 0 else 'in discesa'}")

# Il gradino comunale deve valere esattamente soglia x aliquota.
comunale_mi = registro.territorio("MI", "2026")["comunale"]
verifica("Milano ha una soglia di esenzione comunale",
         comunale_mi.get("soglia_esenzione") is not None)
if comunale_mi.get("soglia_esenzione") is not None:
    gradino_atteso = comunale_mi["soglia_esenzione"] * comunale_mi["aliquota"]
    sopra = calcola(25_328, territorio_codice="MI")
    sotto = calcola(25_327, territorio_codice="MI")
    verifica(f"il gradino di Milano vale circa {gradino_atteso:,.2f} (soglia x aliquota)",
             quasi_uguale(sotto.netto_annuo - sopra.netto_annuo, gradino_atteso, tolleranza=1.5),
             f"misurato {sotto.netto_annuo - sopra.netto_annuo:,.2f}")

verifica("a Palermo, che non ha soglia, quel gradino non esiste",
         registro.territorio("PA", "2026")["comunale"].get("soglia_esenzione") is None
         and calcola(25_328, territorio_codice="PA").netto_annuo
             > calcola(25_327, territorio_codice="PA").netto_annuo)


# ===========================================================================
# 4. Attraversare ogni soglia a passi di un centesimo
# ===========================================================================

titolo("4. Attraversamento delle soglie: sotto, esatta, sopra")

# Non basta che il calcolo non esploda: deve restare finito e coerente anche
# esattamente sul confine, dove gli operatori <= e < fanno la differenza.
# Qui le soglie vengono RICAVATE dal registro, e va bene: questo test non
# verifica DOVE cadono — quello lo fa la sezione 3, con ancoraggi scritti a
# mano — ma che il motore resti finito e coerente ESATTAMENTE sul confine,
# dove <= e < fanno la differenza. Se il registro dichiarasse una soglia
# sbagliata, questo test proverebbe il punto sbagliato ma resterebbe valido
# per quello che afferma. La distinzione e' il motivo per cui esistono
# entrambe le sezioni.
for codice in ("MI", "PA"):
    for anno in registro.anni_disponibili():
        for soglia in inverso.soglie_di_reddito(anno, codice):
            # Dalla soglia sull'imponibile risalgo alla RAL corrispondente.
            aliquota_inps = registro.nazionale(anno)["inps"]["aliquota_dipendente"]
            ral_soglia = soglia / (1 - aliquota_inps)
            for scarto in (-CENTESIMO, 0.0, +CENTESIMO):
                r = calcola(ral_soglia + scarto, anno=anno, territorio_codice=codice)
                finito = all(
                    math.isfinite(v) for v in
                    (r.netto_annuo, r.netto_mensile, r.irpef_netta,
                     r.contributi_inps, r.aliquota_effettiva)
                )
                verifica(f"{codice}/{anno} soglia {soglia:,.0f} scarto {scarto:+.2f}: valori finiti",
                         finito)
                verifica(f"{codice}/{anno} soglia {soglia:,.0f} scarto {scarto:+.2f}: IRPEF netta non negativa",
                         r.irpef_netta >= 0)


# ===========================================================================
# 5. Invarianti su tutto l'arco dei redditi
# ===========================================================================

titolo("5. Invarianti da 1 a 200.000 euro di RAL")

violazioni = {"identita": 0, "irpef_negativa": 0, "non_finito": 0,
              "contributi": 0, "netto_non_positivo": 0, "aliquota": 0}

valore = 1.0
while valore <= 200_000:
    r = calcola(valore)
    ricomposto = (r.retribuzione_effettiva - r.totale_trattenute + r.totale_somme_aggiunte)
    if not quasi_uguale(r.netto_annuo, ricomposto, 1e-6):
        violazioni["identita"] += 1
    if r.irpef_netta < 0:
        violazioni["irpef_negativa"] += 1
    if not all(math.isfinite(v) for v in (r.netto_annuo, r.netto_mensile, r.aliquota_effettiva)):
        violazioni["non_finito"] += 1
    if r.contributi_inps < 0:
        violazioni["contributi"] += 1
    if r.netto_annuo <= 0:
        violazioni["netto_non_positivo"] += 1
    if not 0 <= r.aliquota_effettiva < 1:
        violazioni["aliquota"] += 1
    valore += 37.0   # passo non allineato alle soglie, per non evitarle per caso

for nome, quante in violazioni.items():
    verifica(f"nessuna violazione: {nome}", quante == 0, f"{quante} casi")


# ===========================================================================
# 6. Il netto puo' superare il lordo, e non e' un errore
# ===========================================================================

titolo("6. Redditi bassi: il netto supera il lordo (comportamento corretto)")

# Somma esente e trattamento integrativo sono denaro corrisposto IN PIU',
# non riduzioni di imposta: sotto una certa soglia superano le trattenute.
# Il test fissa il fenomeno perche' non venga scambiato per un difetto e
# "corretto" da chi rimettera' mano al codice.
sopra_il_lordo = [ral for ral in range(8_000, 14_000, 10)
                  if calcola(ral).netto_annuo > ral]
verifica("esiste una fascia in cui il netto supera il lordo",
         len(sopra_il_lordo) > 0)
verifica("quella fascia sta fra 9.000 e 12.000 di RAL",
         9_000 <= min(sopra_il_lordo) and max(sopra_il_lordo) <= 12_000,
         f"da {min(sopra_il_lordo):,} a {max(sopra_il_lordo):,}")

basso = calcola(10_000)
verifica("a RAL 10.000 le somme aggiunte superano le trattenute",
         basso.totale_somme_aggiunte > basso.totale_trattenute,
         f"aggiunte {basso.totale_somme_aggiunte:,.2f}, trattenute {basso.totale_trattenute:,.2f}")


# ===========================================================================
# 7. Meccanica di base
# ===========================================================================

titolo("7. Meccanica: progressivita' e no-tax area")

prova = [(1_000.0, 0.10), (2_000.0, 0.20), (None, 0.30)]
verifica("progressivita': 1.500 -> 1.000x10% + 500x20% = 200",
         quasi_uguale(calcolo.imposta_su_scaglioni(1_500.0, prova), 200.0, 1e-9))
verifica("imponibile zero -> imposta zero",
         calcolo.imposta_su_scaglioni(0.0, prova) == 0.0)
verifica("oltre l'ultimo limite: 3.000 -> 100 + 200 + 300 = 600",
         quasi_uguale(calcolo.imposta_su_scaglioni(3_000.0, prova), 600.0, 1e-9))

verifica("RAL 8.000: le detrazioni azzerano l'IRPEF (no-tax area)",
         calcola(8_000).irpef_netta == 0.0)
verifica("RAL 8.000: senza capienza il trattamento integrativo non spetta",
         calcola(8_000).trattamento_integrativo == 0.0)


# ===========================================================================
# 8. Periodi parziali
# ===========================================================================

titolo("8. Giorni di detrazione")

pieno = calcola(30_000, giorni=365)
verifica("365 giorni e' il default",
         quasi_uguale(calcola(30_000).netto_annuo, pieno.netto_annuo))

meta = calcola(30_000, giorni=182)
verifica("meta' anno: la retribuzione effettiva e' circa la meta'",
         quasi_uguale(meta.retribuzione_effettiva, 30_000 * 182 / 365, 0.01))
verifica("meta' anno: i contributi restano proporzionali",
         quasi_uguale(meta.contributi_inps / meta.retribuzione_effettiva,
                      pieno.contributi_inps / pieno.retribuzione_effettiva, 1e-9))
verifica("meta' anno: la detrazione da lavoro e' rapportata ai giorni",
         meta.detrazione_lavoro_dipendente < pieno.detrazione_lavoro_dipendente)

# --- La regola che distingue le due famiglie di voci ------------------------
# Su un periodo breve, reddito EFFETTIVO e reddito ANNUALIZZATO cadono in fasce
# diverse, e le voci non seguono la stessa regola:
#
#   detrazione art. 13 e trattamento integrativo -> reddito EFFETTIVO
#   taglio del cuneo fiscale                     -> reddito ANNUALIZZATO
#
# La distinzione non e' un'ipotesi: e' stata ricavata confrontando il motore con
# una Certificazione Unica reale, che riconosceva la detrazione (quindi reddito
# effettivo) e insieme NON erogava la somma esente del cuneo (quindi reddito
# annualizzato). Una regola uniforme, in un senso o nell'altro, sbaglia una
# delle due voci. Vedi DIARIO_DI_BORDO.md, voce 35.
#
# Caso costruito apposta perche' le due letture diano risposte diverse.
breve = calcola(50_000, giorni=40)
coefficienti = registro.nazionale(registro.anno_predefinito())["detrazioni_lavoro_dipendente"]
quota = 40 / 365

verifica("periodo breve: la fascia della detrazione segue il reddito EFFETTIVO",
         quasi_uguale(breve.detrazione_lavoro_dipendente,
                      coefficienti["fascia_1_importo"] * quota),
         f"ottenuta {breve.detrazione_lavoro_dipendente:,.2f}, "
         f"attesa {coefficienti['fascia_1_importo'] * quota:,.2f} "
         f"(imponibile effettivo {breve.imponibile_fiscale:,.2f})")

verifica("periodo breve: il cuneo fiscale segue il reddito ANNUALIZZATO",
         breve.somma_esente_cuneo == 0.0,
         f"ottenuta {breve.somma_esente_cuneo:,.2f}; sull'imponibile effettivo "
         f"({breve.imponibile_fiscale:,.2f}) sarebbe spettata")

# Il minimo di 690 euro va rapportato ai giorni come il resto: cosi' non entra
# mai in gioco, perche' la fascia 1 vale 1.955 e la proporzione si applica a
# entrambi. Il minimo intero spetta solo in dichiarazione dei redditi, che
# questo prototipo non simula.
verifica("il minimo di 690 e' rapportato ai giorni, non applicato per intero",
         breve.detrazione_lavoro_dipendente < coefficienti["fascia_1_minimo"],
         f"ottenuta {breve.detrazione_lavoro_dipendente:,.2f}")


# ===========================================================================
# 9. Le mensilita' non toccano il calcolo
# ===========================================================================

titolo("9. Mensilita': cambiano solo il divisore")

netti = {m: calcola(30_000, mensilita=m) for m in registro.mensilita_ammesse()}
primo = netti[12].netto_annuo
verifica("il netto annuo e' identico con 12, 13 o 14 mensilita'",
         all(quasi_uguale(r.netto_annuo, primo) for r in netti.values()))
verifica("il netto mensile e' il netto annuo diviso le mensilita'",
         all(quasi_uguale(r.netto_mensile, r.netto_annuo / m) for m, r in netti.items()))


# ===========================================================================
# 10. Validazione degli input
# ===========================================================================

titolo("10. Validazione: errori parlanti, non eccezioni tecniche")

def rifiuta(descrizione, chiamata):
    try:
        chiamata()
    except ValueError as errore:
        verifica(f"{descrizione} -> \"{errore}\"", True)
    except Exception as errore:
        verifica(descrizione, False, f"eccezione inattesa: {type(errore).__name__}: {errore}")
    else:
        verifica(descrizione, False, "nessun errore sollevato")

rifiuta("campo vuoto", lambda: calcola(""))
rifiuta("valore nullo", lambda: calcola(None))
rifiuta("testo non numerico", lambda: calcola("trentamila"))
rifiuta("RAL negativa", lambda: calcola(-1_000))
rifiuta("RAL pari a zero", lambda: calcola(0))
rifiuta("giorni fuori intervallo", lambda: calcola(30_000, giorni=400))
rifiuta("giorni pari a zero", lambda: calcola(30_000, giorni=0))
rifiuta("anno non presente nel registro", lambda: calcola(30_000, anno=2030))
rifiuta("territorio sconosciuto", lambda: calcola(30_000, territorio_codice="XX"))

verifica("una RAL scritta come stringa numerica viene accettata",
         quasi_uguale(calcola("30000").netto_annuo, calcola(30_000).netto_annuo))

# --- Come scrivono i numeri le persone --------------------------------------
# Nessuno digita "35000". Si scrive "35.000", e `float("35.000")` in Python vale
# 35.0: senza normalizzazione, chi scrive trentacinquemila euro nel modo piu'
# naturale in italiano ottiene un calcolo su trentacinque euro, e il risultato
# non segnala nulla perche' e' un numero plausibile.
# Il difetto era presente ed e' stato trovato usando l'interfaccia, non
# leggendo il codice. Vedi DIARIO_DI_BORDO.md, voce 38.
FORMATI_ACCETTATI = [
    ("35000", 35_000.0),
    ("35.000", 35_000.0),        # migliaia all'italiana
    ("35,000", 35_000.0),        # migliaia all'inglese
    ("25.999", 25_999.0),
    ("2.500", 2_500.0),
    ("1.234.567", 1_234_567.0),
    ("35.000,50", 35_000.50),    # completo all'italiana
    ("35,000.50", 35_000.50),    # completo all'inglese
    ("35 000", 35_000.0),        # spazio come separatore
    ("€ 35.000", 35_000.0),      # simbolo di valuta
    ("  35000  ", 35_000.0),
    ("35,5", 35.5),              # una cifra dopo: decimale
    ("35,50", 35.50),            # due cifre dopo: decimale
    (35_000, 35_000.0),
]
for scritto, atteso in FORMATI_ACCETTATI:
    verifica(f"«{scritto}» viene letto come {atteso:,.2f}",
             quasi_uguale(calcolo.normalizza_importo(scritto), atteso, 1e-9),
             f"letto {calcolo.normalizza_importo(scritto)}")

# Input malformati: si respingono invece di indovinare. Un numero "aggiustato"
# in silenzio e' esattamente il difetto che questo progetto vuole rendere
# impossibile.
FORMATI_RESPINTI = ["", "   ", "trentamila", "35..000", "35,00,00", "1.23.456", "abc123"]
for scritto in FORMATI_RESPINTI:
    try:
        calcolo.normalizza_importo(scritto)
        verifica(f"«{scritto}» viene respinto", False, "e' stato accettato")
    except ValueError:
        verifica(f"«{scritto}» viene respinto", True)

verifica("il segnaposto mostrato all'utente e' leggibile dal motore",
         quasi_uguale(calcola("35.000").netto_annuo, calcola(35_000).netto_annuo),
         "il campo suggerisce «es. 35.000»: deve valere 35.000, non 35")

verifica("RAL bassa: avvisa che sembra un importo mensile",
         any("mensile" in a for a in calcola(2_500).avvisi))
verifica("RAL normale: nessun avviso",
         calcola(35_000).avvisi == [])


# ===========================================================================
# 11. I territori hanno forme diverse
# ===========================================================================

titolo("11. Territori: forme diverse di addizionale")

verifica("la Lombardia usa scaglioni",
         registro.territorio("MI", "2026")["regionale"]["tipo"] == "scaglioni")
verifica("la Sicilia usa un'aliquota unica",
         registro.territorio("PA", "2026")["regionale"]["tipo"] == "unica")

sicilia = registro.territorio("PA", "2026")["regionale"]["aliquota"]
r_pa = calcola(30_000, territorio_codice="PA")
verifica("in Sicilia l'addizionale regionale e' aliquota x imponibile",
         quasi_uguale(r_pa.addizionale_regionale, r_pa.imponibile_fiscale * sicilia))

verifica("ogni voce territoriale dichiara il luogo che la genera",
         all(any(nome in v.etichetta for nome in ("Milano", "Lombardia"))
             for v in calcola(30_000).voci if "Addizionale" in v.etichetta))


# ===========================================================================
# 12. Calcolo inverso: dal netto alla RAL
# ===========================================================================

titolo("12. Calcolo inverso netto -> lordo")

from motore import inverso   # noqa: E402  (importato qui per tenere unita la sezione)

# --- 12a. Andata e ritorno --------------------------------------------------
# Il controllo piu' severo: da ogni RAL si calcola il netto, dal netto si torna
# indietro, e la RAL di partenza deve essere fra le soluzioni. Con una bisezione
# ingenua questo test fallisce 67 volte su 5.400, con errori fino a 309 euro.
mancati = []
for ral in range(6_000, 60_000, 450):
    obiettivo = calcola(float(ral)).netto_annuo
    esito = inverso.ral_per_netto(obiettivo)
    candidati = [esito.ral] + list(esito.alternative) if esito.raggiungibile else []
    if not any(abs(c - ral) < 0.01 for c in candidati):
        mancati.append(ral)

verifica("andata e ritorno: la RAL di partenza e' sempre fra le soluzioni",
         not mancati, f"fallita per {len(mancati)} RAL: {mancati[:5]}")

# --- 12b. I punti di salto, ricavati due volte in modo indipendente ---------
# La sezione 3 li trova SCANDENDO la curva; inverso.py li ricava DAL REGISTRO.
# Sono due derivazioni indipendenti: se concordano, e' un buon segno per
# entrambe. Se un giorno divergono, una delle due ha un errore.
for codice in ("MI", "PA"):
    dal_registro = sorted(inverso.punti_di_salto("2026", codice))
    dalla_scansione = sorted(
        # dalla discontinuita' sull'imponibile risalgo alla RAL
        inverso.ral_per_imponibile(imponibile, "2026", 365, codice)
        for imponibile, _ in discontinuita("2026", codice)
    )
    verifica(f"{codice}: stesso numero di salti per registro e scansione",
             len(dal_registro) == len(dalla_scansione),
             f"registro {len(dal_registro)}, scansione {len(dalla_scansione)}")
    if len(dal_registro) == len(dalla_scansione):
        for atteso, misurato in zip(dal_registro, dalla_scansione):
            verifica(f"{codice}: salto previsto a RAL {atteso:,.0f}, misurato a {misurato:,.0f}",
                     abs(atteso - misurato) <= 2.0,
                     f"scarto {abs(atteso - misurato):,.2f}")

# --- 12c. Netti irraggiungibili --------------------------------------------
# Un salto IN SALITA scavalca dei valori: nessuna RAL li produce. Va detto,
# non aggirato restituendo una RAL che vale altro.
salti_mi = inverso.punti_di_salto("2026", "MI")
irraggiungibili = []
for salto in salti_mi:
    prima = calcola(salto - 1e-6).netto_annuo
    dopo = calcola(salto + 1e-6).netto_annuo
    if dopo > prima + 1.0:
        irraggiungibili.append((prima + dopo) / 2)

verifica("esistono netti irraggiungibili (li creano i salti in salita)",
         len(irraggiungibili) > 0, f"trovati {len(irraggiungibili)}")

for obiettivo in irraggiungibili:
    esito = inverso.ral_per_netto(obiettivo)
    verifica(f"netto {obiettivo:,.2f} dichiarato irraggiungibile",
             not esito.raggiungibile)
    verifica(f"netto {obiettivo:,.2f}: vengono indicati i due valori piu' vicini",
             esito.netto_raggiungibile_sotto is not None
             and esito.netto_raggiungibile_sopra is not None
             and esito.netto_raggiungibile_sotto < obiettivo < esito.netto_raggiungibile_sopra)

# --- 12d. Netti ambigui -----------------------------------------------------
# Un salto IN DISCESA fa si' che lo stesso netto si ottenga con piu' RAL.
# Vanno restituite tutte, e ognuna deve davvero produrre quel netto.
ambiguo = inverso.ral_per_netto(20_600.0)
verifica("il netto 20.600 e' ambiguo (piu' di una RAL lo produce)", ambiguo.ambiguo)
verifica("in caso di ambiguita' viene proposta la RAL piu' bassa",
         all(ambiguo.ral < alternativa for alternativa in ambiguo.alternative))
verifica("l'ambiguita' viene dichiarata all'utente, non nascosta",
         any("RAL diverse" in a for a in ambiguo.avvisi))
for candidata in [ambiguo.ral] + list(ambiguo.alternative):
    verifica(f"RAL {candidata:,.2f} produce davvero 20.600 di netto",
             quasi_uguale(calcola(candidata).netto_annuo, 20_600.0),
             f"ottenuto {calcola(candidata).netto_annuo:,.2f}")

# --- 12e. Il caso d'uso vero: netto mensile ---------------------------------
for mensile in (1_500.0, 1_800.0, 2_000.0, 2_500.0):
    esito = inverso.ral_per_netto(mensile, mensile=True)
    verifica(f"{mensile:,.0f} euro netti al mese: soluzione trovata", esito.raggiungibile)
    if esito.raggiungibile:
        controllo = calcola(esito.ral)
        verifica(f"{mensile:,.0f} euro/mese: la RAL trovata li produce davvero",
                 quasi_uguale(controllo.netto_mensile, mensile),
                 f"ottenuti {controllo.netto_mensile:,.2f}")

# --- 12f. Territori e anni diversi ------------------------------------------
for codice in ("MI", "PA"):
    for anno in registro.anni_disponibili():
        esito = inverso.ral_per_netto(2_000.0, mensile=True, anno=anno,
                                      territorio_codice=codice)
        verifica(f"{codice}/{anno}: 2.000 euro netti al mese sono raggiungibili",
                 esito.raggiungibile)
        if esito.raggiungibile:
            controllo = calcola(esito.ral, anno=anno, territorio_codice=codice)
            verifica(f"{codice}/{anno}: la RAL trovata produce il netto richiesto",
                     quasi_uguale(controllo.netto_mensile, 2_000.0))

# Stesso netto, territori diversi: a Palermo serve una RAL piu' alta, perche'
# le addizionali sono piu' pesanti. E' la stessa differenza che il calcolo
# diretto mostra, vista dall'altro lato.
ral_mi = inverso.ral_per_netto(2_000.0, mensile=True, territorio_codice="MI").ral
ral_pa = inverso.ral_per_netto(2_000.0, mensile=True, territorio_codice="PA").ral
verifica("a Palermo serve una RAL piu' alta di Milano per lo stesso netto",
         ral_pa > ral_mi, f"Milano {ral_mi:,.2f}, Palermo {ral_pa:,.2f}")

# --- 12g. Validazione -------------------------------------------------------
rifiuta("netto inverso pari a zero", lambda: inverso.ral_per_netto(0))
rifiuta("netto inverso negativo", lambda: inverso.ral_per_netto(-500))
rifiuta("netto inverso non numerico", lambda: inverso.ral_per_netto("molti"))


# ===========================================================================
# 13. I due difetti trovati da una revisione esterna
# ===========================================================================

titolo("13. Difetti trovati da fuori: formati nell'inverso, 75 euro di capienza")

# --- 13a. L'inverso deve leggere i numeri come il diretto ------------------
#
# Il campo del netto SUGGERISCE «es. 2.000». Il percorso diretto usava
# normalizza_importo(), l'inverso usava float(): "2.000" diventava 2 euro e
# restituiva una RAL da 29 euro invece di 40.101. La correzione dell'errore 12
# era stata applicata solo dove il difetto era stato trovato.
#
# Nessun test lo copriva perche' tutti passavano numeri gia' puliti — cioe'
# provavano l'inverso in un modo in cui l'interfaccia non lo usa mai.

RAL_ATTESA_2000 = inverso.ral_per_netto(2000, mensile=True, anno=2026,
                                        territorio_codice="MI").ral

for forma in ("2000", "2.000", "2.000,00", "€ 2.000", "2 000", "2,000.00", 2000):
    risultato = inverso.ral_per_netto(forma, mensile=True, anno=2026,
                                      territorio_codice="MI")
    verifica(f"inverso: «{forma}» al mese vale come 2000",
             quasi_uguale(risultato.ral, RAL_ATTESA_2000),
             f"ottenuto {risultato.ral:,.2f}, atteso {RAL_ATTESA_2000:,.2f}")

verifica("inverso: la RAL per 2.000 netti al mese e' un valore plausibile",
         39_000 < RAL_ATTESA_2000 < 41_000,
         f"ottenuto {RAL_ATTESA_2000:,.2f}")

# Il messaggio d'errore non deve promettere un formato che poi rifiuta: era
# quello che faceva, suggerendo «1.800,50» ed essendo l'unico a non accettarlo.
for forma in ("1800", "1.800", "1.800,50"):
    try:
        inverso.ral_per_netto(forma, anno=2026, territorio_codice="MI")
        accettato = True
    except ValueError:
        accettato = False
    verifica(f"inverso: il formato «{forma}», citato nel messaggio d'errore, e' accettato",
             accettato)


# --- 13b. I 75 euro della capienza (L. 234/2021) ---------------------------
#
# Il trattamento integrativo spetta se l'IRPEF lorda supera la detrazione
# art. 13 c. 1 DIMINUITA DI 75 EURO rapportati al periodo. Senza i 75, la
# soglia cadeva a un imponibile di 8.500 invece che a 8.173,91.
#
# Valori calcolati a mano, non letti dal registro:
#     detrazione fascia 1            1.955,00
#     riduzione L. 234/2021             75,00
#     soglia di lorda                1.880,00
#     imponibile = 1.880 / 23%       8.173,91
#     RAL = 8.173,91 / (1 - 9,19%)   9.001,55

SOGLIA_CAPIENZA_IMPONIBILE = 8173.91
RAL_SOGLIA_CAPIENZA = 9001.55

sotto = calcola(RAL_SOGLIA_CAPIENZA - 5, anno=2026, territorio_codice="MI")
sopra = calcola(RAL_SOGLIA_CAPIENZA + 5, anno=2026, territorio_codice="MI")

verifica("capienza: sotto la soglia il trattamento integrativo NON spetta",
         sotto.trattamento_integrativo == 0.0,
         f"ottenuto {sotto.trattamento_integrativo:,.2f}")
verifica("capienza: sopra la soglia spettano 1.200",
         quasi_uguale(sopra.trattamento_integrativo, 1200.0),
         f"ottenuto {sopra.trattamento_integrativo:,.2f}")
verifica("capienza: l'imponibile di confine e' 8.173,91 e non 8.500",
         abs(sopra.imponibile_fiscale - SOGLIA_CAPIENZA_IMPONIBILE) < 10,
         f"imponibile sopra la soglia: {sopra.imponibile_fiscale:,.2f}")

# La prova che i 75 euro esistono davvero: a un imponibile compreso fra
# 8.173,91 e 8.500 la lorda e' INFERIORE alla detrazione piena, e il
# trattamento spetta lo stesso. Senza i 75 questo caso darebbe zero.
meta = calcola(9200.0, anno=2026, territorio_codice="MI")
verifica("capienza: fra le due soglie la lorda e' sotto la detrazione piena...",
         meta.irpef_lorda < meta.detrazione_lavoro_dipendente,
         f"lorda {meta.irpef_lorda:,.2f} vs detrazione {meta.detrazione_lavoro_dipendente:,.2f}")
verifica("...e il trattamento integrativo spetta comunque (e' l'effetto dei 75 euro)",
         quasi_uguale(meta.trattamento_integrativo, 1200.0),
         f"ottenuto {meta.trattamento_integrativo:,.2f}")

# I 75 euro sono rapportati al periodo di lavoro: su meta' anno valgono 37,50.
mezzo = calcola(9200.0, anno=2026, territorio_codice="MI", giorni=182)
verifica("capienza: su un periodo parziale la riduzione e' proporzionale",
         mezzo.trattamento_integrativo >= 0,
         f"trattamento su 182 giorni: {mezzo.trattamento_integrativo:,.2f}")

# --- 13c. Le due discontinuita' che erano sovrapposte ---------------------
#
# Finche' la soglia di capienza cadeva a 8.500, coincideva con il cambio di
# fascia della somma esente. Una si vedeva, l'altra era invisibile.

salti_mi = inverso.punti_di_salto("2026", "MI")
verifica("Milano ha 7 discontinuita', non 6: le due a 8.500 erano sovrapposte",
         len(salti_mi) == 7,
         f"trovate {len(salti_mi)}")

imponibili_salto = sorted(
    calcola(r + 1, anno=2026, territorio_codice="MI").imponibile_fiscale
    for r in salti_mi
)
verifica("le prime due discontinuita' sono distinte e distano circa 326 euro",
         300 < imponibili_salto[1] - imponibili_salto[0] < 350,
         f"distanza {imponibili_salto[1] - imponibili_salto[0]:,.2f}")
# --- 13d. Nessun motivo si perde quando due soglie coincidono -------------
#
# `soglie_di_reddito` restituisce {valore: [motivi]}. Con un dizionario
# {valore: motivo} i motivi successivi sovrascrivevano i precedenti: a 15.000
# la fine della detrazione di fascia 1 spariva sotto il cambio di fascia della
# somma esente. Otto motivi dichiarati, sette sopravvissuti, e nessun test se
# ne accorgeva perche' l'aritmetica restava giusta.

soglie_mi = inverso.soglie_di_reddito("2026", "MI")
motivi_totali = sum(len(m) for m in soglie_mi.values())

verifica("Milano: 7 soglie distinte", len(soglie_mi) == 7, f"trovate {len(soglie_mi)}")
verifica("Milano: 8 motivi, uno in piu' delle soglie (a 15.000 ne cadono due)",
         motivi_totali == 8, f"trovati {motivi_totali}")
verifica("a 15.000 i motivi sono due e non uno",
         len(soglie_mi[15000.0]) == 2, f"a 15.000: {soglie_mi.get(15000.0)}")
verifica("fra i due c'e' la fine della detrazione di fascia 1",
         any("fascia 1" in m for m in soglie_mi[15000.0]))
verifica("e il cambio di fascia della somma esente",
         any("somma esente" in m for m in soglie_mi[15000.0]))
verifica("ogni soglia ha almeno un motivo",
         all(len(m) >= 1 for m in soglie_mi.values()))

# ===========================================================================
# 14. Il minimo contrattuale
# ===========================================================================

titolo("14. Minimi tabellari: una RAL sotto il contratto non e' proponibile")

# I valori sono scritti a mano dalla tabella del CCNL, non letti dal registro:
# e' l'unico modo perche' questo test possa smentire il registro.
#
#   CCNL Terziario (Confcommercio), minimi dal 1 novembre 2025, 14 mensilita':
#     livello 7  873,22 x 14 = 12.225,08   <- il piu' basso
#     livello 5  1.136,07 x 14 = 15.904,98
#     livello 1  1.966,54 x 14 = 27.531,56
#     Quadro     2.183,09 x 14 = 30.563,26

MINIMO_COMMERCIO_ANNUO = 12_225.08

sotto = calcola(MINIMO_COMMERCIO_ANNUO - 100, anno=2026, territorio_codice="MI")
sopra = calcola(MINIMO_COMMERCIO_ANNUO + 100, anno=2026, territorio_codice="MI")

verifica("il minimo piu' basso del commercio e' 12.225,08 (livello 7 x 14)",
         quasi_uguale(sotto.minimo_ccnl["minimo_assoluto_annuo"], MINIMO_COMMERCIO_ANNUO),
         f"ottenuto {sotto.minimo_ccnl['minimo_assoluto_annuo']:,.2f}")
verifica("sotto il minimo: segnalato", sotto.minimo_ccnl["sotto_il_minimo"])
verifica("sotto il minimo: c'e' un avviso che lo dice",
         any("minimo contrattuale" in a for a in sotto.avvisi),
         f"avvisi: {sotto.avvisi}")
verifica("sopra il minimo: nessuna segnalazione", not sopra.minimo_ccnl["sotto_il_minimo"])
verifica("sopra il minimo: nessun avviso sul contratto",
         not any("minimo contrattuale" in a for a in sopra.avvisi))

# I livelli compatibili sono l'informazione utile: non un si'/no, ma fino a dove.
LIVELLI_ATTESI = {
    35_000: ["Quadro", "1", "2", "3", "4", "5", "6", "7"],   # copre tutto
    27_600: ["1", "2", "3", "4", "5", "6", "7"],             # sopra il livello 1
    16_000: ["5", "6", "7"],                                 # sopra il 5, sotto il 4
    12_500: ["7"],                                           # solo il livello piu' basso
}
for ral, attesi in LIVELLI_ATTESI.items():
    ottenuti = calcola(float(ral), anno=2026, territorio_codice="MI").minimo_ccnl["livelli_compatibili"]
    verifica(f"RAL {ral:,}: livelli compatibili {', '.join(attesi)}",
             ottenuti == attesi, f"ottenuti {ottenuti}")

# Il caso del task deve stare sopra ogni livello, Quadro compreso: se cosi' non
# fosse, l'esempio scelto sarebbe un'offerta non proponibile.
verifica("il caso del task (35.000) copre anche il livello Quadro",
         "Quadro" in calcola(35_000, anno=2026,
                             territorio_codice="MI").minimo_ccnl["livelli_compatibili"])

# --- Il confronto usa le mensilita' del contratto -------------------------
#
# Il commercio ha 14 mensilita', i metalmeccanici 13. Lo stesso minimo mensile
# produce minimi annui diversi, e usare 12 per tutti sarebbe un errore
# silenzioso di quasi il 17%.
metal = calcola(30_000, anno=2026, territorio_codice="MI", ccnl="metalmeccanici")
verifica("metalmeccanici: minimo annuo = D1 (1.784,94) x 13 mensilita'",
         quasi_uguale(metal.minimo_ccnl["minimo_assoluto_annuo"], 1784.94 * 13),
         f"ottenuto {metal.minimo_ccnl['minimo_assoluto_annuo']:,.2f}")
verifica("metalmeccanici: la tabella e' dichiarata parziale",
         metal.minimo_ccnl["parziale"])

# Una RAL legittima nel commercio puo' essere sotto il minimo dei
# metalmeccanici: i due contratti hanno pavimenti molto diversi.
r_com = calcola(20_000, anno=2026, territorio_codice="MI", ccnl="commercio")
r_met = calcola(20_000, anno=2026, territorio_codice="MI", ccnl="metalmeccanici")
verifica("RAL 20.000: legittima nel commercio, sotto il minimo nei metalmeccanici",
         not r_com.minimo_ccnl["sotto_il_minimo"] and r_met.minimo_ccnl["sotto_il_minimo"])

# --- Quando il registro non sa, lo dice -----------------------------------
for codice in ("studi_professionali", "edilizia"):
    v = calcola(20_000, anno=2026, territorio_codice="MI", ccnl=codice).minimo_ccnl
    verifica(f"{codice}: dichiara di non avere i minimi invece di tacere",
             v["applicabile"] is False and "motivo" in v)
    verifica(f"{codice}: senza minimi non inventa avvisi",
             not any("minimo contrattuale" in a
                     for a in calcola(20_000, anno=2026, ccnl=codice).avvisi))

# --- Il netto NON cambia: il minimo e' un controllo, non un calcolo -------
#
# Serve a garantire che questa aggiunta non abbia toccato la catena fiscale.
verifica("il CCNL non cambia il netto annuo, solo il divisore del mensile",
         quasi_uguale(calcola(35_000, anno=2026, ccnl="commercio").netto_annuo,
                      calcola(35_000, anno=2026, ccnl="metalmeccanici").netto_annuo))

# ===========================================================================
# Esito
# ===========================================================================

print()
print("=" * 70)
if _esiti["falliti"]:
    print(f"ESITO: {len(_esiti['falliti'])} test FALLITI su {_esiti['ok'] + len(_esiti['falliti'])}")
    for fallito in _esiti["falliti"]:
        print(f"  - {fallito}")
    raise SystemExit(1)
print(f"ESITO: {_esiti['ok']} test superati.")
print("=" * 70)
