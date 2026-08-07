"""
Motore di calcolo RAL -> netto.

Funzioni pure: stessi input, stesso output, nessun effetto collaterale, nessuna
dipendenza dalla pagina web o dal database. È il cuore del prototipo, ed è
scritto perché ogni numero del risultato si possa spiegare risalendo alla riga
che lo produce.

I coefficienti non stanno qui: arrivano dal registro (registro.py), che li legge
da dati/coefficienti.json. Questo file contiene solo le REGOLE, che cambiano
raramente; il registro contiene i NUMERI, che cambiano ogni anno.

La sequenza (dipendente privato, caso semplice):

    RAL contrattuale
      x giorni/365            -> retribuzione effettiva del periodo
      - contributi INPS       (9,19% + 1% oltre la prima fascia, entro il massimale)
      = imponibile fiscale    (= reddito complessivo, nel caso semplice)

      IRPEF lorda             (scaglioni progressivi sull'imponibile)
      - detrazione lavoro dipendente        (art. 13 c. 1 TUIR)
      - ulteriore detrazione 65 euro        (art. 13 c. 1.1 TUIR)
      - ulteriore detrazione cuneo fiscale  (L. 207/2024 art. 1 c. 6)
      = IRPEF netta           (mai sotto zero)

      - addizionale regionale (a scaglioni oppure unica, secondo la regione)
      - addizionale comunale  (unica, con o senza soglia di esenzione)

      + somma esente cuneo fiscale   (L. 207/2024 art. 1 c. 4-5)
      + trattamento integrativo      (D.L. 3/2020)
      = netto annuo
      / mensilita             -> netto mensile

ATTENZIONE a due voci che è facile collocare male:

  * la SOMMA ESENTE del cuneo fiscale non riduce l'imponibile: è una somma
    corrisposta in più, che non concorre a formare il reddito. Si SOMMA al netto,
    esattamente come il trattamento integrativo. Trattarla come una deduzione
    darebbe un risultato sbagliato in entrambe le direzioni.

  * l'ULTERIORE DETRAZIONE del cuneo fiscale, invece, è una detrazione vera:
    abbatte l'IRPEF e non può portarla sotto zero.

Periodi parziali (giorni < 365): due regole diverse, non una
------------------------------------------------------------
Verificando il motore contro una Certificazione Unica reale è emerso che la
legge NON tratta allo stesso modo tutte le voci rapportate ai giorni. La prima
stesura applicava una regola uniforme — tutte le soglie valutate sul reddito
annualizzato — perché sembrava più coerente. Su un rapporto di 40 giorni
produceva detrazione e trattamento integrativo pari a ZERO, mentre il sostituto
d'imposta ne aveva riconosciuti 214,25 e 131,51.

La regola vera:

  * DETRAZIONE art. 13, ulteriore detrazione di 65 euro e TRATTAMENTO
    INTEGRATIVO guardano il reddito EFFETTIVAMENTE percepito nel periodo.
    L'importo si rapporta poi ai giorni.

  * TAGLIO DEL CUNEO FISCALE (somma esente e ulteriore detrazione) guarda il
    reddito ANNUALIZZATO, come chiarito dalla circolare 4/E del 16 maggio 2025:
    "per individuare la percentuale applicabile [...] deve rapportare il reddito
    di lavoro dipendente all'intero anno".

Le due regole danno risultati opposti sullo stesso caso: con 5.561,63 euro in 40
giorni, il reddito effettivo (5.561,63) dà diritto alla detrazione piena di
fascia 1, mentre quello annualizzato (50.750) la azzererebbe. La CU conferma
entrambe le letture: riconosce la detrazione E non eroga la somma esente del
cuneo, che sull'annualizzato non spetta.

Anche il MINIMO di 690 euro della detrazione di fascia 1 va rapportato ai giorni.
La CU lo dice esplicitamente nelle annotazioni: "la detrazione minima è stata
ragguagliata al periodo di lavoro". Il minimo intero spetta solo in sede di
dichiarazione dei redditi, che è fuori dal perimetro di questo prototipo.

Con giorni = 365, che è il default e il caso del task, le due regole coincidono.
"""

from dataclasses import dataclass, field, asdict

from . import registro

GIORNI_ANNO = 365


# ---------------------------------------------------------------------------
# Validazione dell'ingresso
# ---------------------------------------------------------------------------

# Oltre questi limiti il calcolo resta matematicamente valido ma esce dal caso
# "semplice e standard": l'interfaccia avvisa, non blocca.
RAL_MINIMA_PLAUSIBILE = 5_000.0
RAL_MASSIMA_PLAUSIBILE = 500_000.0

# Oltre questo valore non si avvisa: si rifiuta. Non e' una retribuzione, e
# accettarlo produce numeri astronomici in risposta senza alcun beneficio.
# Trovato durante il controllo di sicurezza: «1e308» veniva accettato e
# calcolato.
RAL_LIMITE_ASSOLUTO = 100_000_000.0


def normalizza_importo(testo) -> float:
    """Interpreta un importo scritto come lo scrive una persona.

    Le persone non digitano `35000`. Digitano `35.000`, `35.000,50`, `35 000`,
    `€ 35.000`, e chi ha imparato l'informatica in inglese digita `35,000.50`.
    Rifiutare tutto tranne una forma e' scortese; peggio ancora e' accettarle
    tutte leggendole male.

    Il caso che rende questa funzione necessaria: `float("35.000")` in Python
    vale **35.0**. Senza normalizzazione, chi scrive trentacinquemila euro nel
    modo piu' naturale in italiano ottiene un calcolo su trentacinque euro — e
    il risultato, essendo un numero plausibile, non segnala nulla.

    Le regole, in ordine:

      * se compaiono ENTRAMBI i separatori, quello piu' a destra e' il decimale
        e l'altro divide le migliaia: vale sia per `35.000,50` sia per
        `35,000.50`;
      * se ne compare uno solo, ripetuto, divide le migliaia: `1.234.567`;
      * se ne compare uno solo, una volta sola, decide **quante cifre lo
        seguono**: tre cifre sono migliaia (`35.000`, `25,999`), una o due sono
        decimali (`35,50`). E' una convenzione, non una certezza — per questo
        l'interfaccia mostra sempre come ha interpretato il numero.
    """
    if isinstance(testo, (int, float)) and not isinstance(testo, bool):
        return float(testo)

    pulito = str(testo).strip()
    for rumore in ("€", " ", " ", " ", "'", "_"):
        pulito = pulito.replace(rumore, "")
    if not pulito:
        raise ValueError("vuoto")

    # Solo cifre e separatori ASCII. `float()` accetterebbe anche le cifre
    # arabe o devanagari — «٣٥٠٠٠» diventa 35000 — un comportamento
    # sorprendente e, in un campo di modulo, un possibile inganno visivo.
    # Meglio rifiutare che indovinare. Emerso dal controllo di sicurezza.
    if not all(c in "0123456789.,+-" for c in pulito):
        raise ValueError("caratteri non ammessi")

    segno = -1.0 if pulito.startswith("-") else 1.0
    pulito = pulito.lstrip("+-")

    punti, virgole = pulito.count("."), pulito.count(",")

    if punti and virgole:
        decimale = "." if pulito.rfind(".") > pulito.rfind(",") else ","
        migliaia = "," if decimale == "." else "."
        intero, _, resto = pulito.rpartition(decimale)
        pulito = f"{_unisci_migliaia(intero, migliaia)}.{resto}"
    elif punti or virgole:
        separatore = "." if punti else ","
        if (punti or virgole) > 1:
            pulito = _unisci_migliaia(pulito, separatore)
        else:
            intero, _, resto = pulito.partition(separatore)
            # Tre cifre dopo il separatore: migliaia. A meno che la parte intera
            # sia solo "0", nel qual caso "0,999" e' evidentemente un decimale.
            if len(resto) == 3 and resto.isdigit() and intero not in ("", "0"):
                pulito = intero + resto
            else:
                pulito = f"{intero}.{resto}"

    return segno * float(pulito)


def _unisci_migliaia(testo: str, separatore: str) -> str:
    """Toglie i separatori delle migliaia, ma solo se sono messi bene.

    `1.234.567` diventa `1234567`. `35..000` e `35,00,00` invece restano
    respinti: sono input malformati, e indovinare cosa intendessero significa
    rischiare di calcolare in silenzio su un numero che l'utente non ha
    scritto. Meglio dire che non si e' capito.
    """
    gruppi = testo.split(separatore)
    if len(gruppi) == 1:
        return testo
    primo, seguenti = gruppi[0], gruppi[1:]
    if not (1 <= len(primo) <= 3) or not primo.isdigit():
        raise ValueError("gruppo delle migliaia malformato")
    if not all(len(g) == 3 and g.isdigit() for g in seguenti):
        raise ValueError("gruppo delle migliaia malformato")
    return "".join(gruppi)


def valida_ral(ral) -> float:
    """Controlla che la RAL sia un numero utilizzabile.

    I messaggi d'errore sono scritti per essere mostrati all'utente cosi' come
    sono, e mostrano un esempio nel formato che la funzione accetta davvero:
    suggerire una forma e poi rifiutarla e' il modo piu' rapido di far perdere
    fiducia a chi sta gia' faticando.
    """
    if ral is None or (isinstance(ral, str) and not ral.strip()):
        raise ValueError("Inserisci la RAL, cioè la retribuzione annua lorda.")
    try:
        valore = normalizza_importo(ral)
    except (TypeError, ValueError):
        raise ValueError(
            "Non riesco a leggere questo importo. Scrivilo come preferisci: "
            "35000, 35.000 oppure 35.000,50."
        )
    if valore != valore or valore in (float("inf"), float("-inf")):
        raise ValueError("La RAL deve essere un numero valido.")
    if valore < 0:
        raise ValueError("La RAL non può essere negativa.")
    if valore == 0:
        raise ValueError("La RAL deve essere maggiore di zero.")
    if valore > RAL_LIMITE_ASSOLUTO:
        raise ValueError(
            "Questo importo è troppo grande per essere una retribuzione. "
            "Il limite accettato è 100.000.000 €."
        )
    return valore


def valida_giorni(giorni) -> int:
    try:
        valore = int(giorni)
    except (TypeError, ValueError):
        raise ValueError("I giorni di detrazione devono essere un numero intero.")
    if not 1 <= valore <= GIORNI_ANNO:
        raise ValueError(f"I giorni di detrazione devono stare tra 1 e {GIORNI_ANNO}.")
    return valore


def avvisi_plausibilita(ral: float) -> list[str]:
    """Avvisi che non bloccano il calcolo ma mettono in guardia.

    Il primo è il più importante: intercetta chi inserisce uno stipendio
    MENSILE al posto della RAL annua. È un errore silenzioso — il risultato
    resta plausibile — e colpisce chi non è del mestiere.
    """
    avvisi = []
    if ral < RAL_MINIMA_PLAUSIBILE:
        avvisi.append(
            f"{formatta_euro(ral)} sembra un importo mensile: la RAL è ANNUA e lorda. "
            f"Se intendevi {formatta_euro(ral)} al mese, la RAL è circa {formatta_euro(ral * 12)}."
        )
    if ral > RAL_MASSIMA_PLAUSIBILE:
        avvisi.append(
            "Importo molto elevato: il calcolo resta valido, ma a questi livelli "
            "la retribuzione ha di norma componenti che questo prototipo non tratta."
        )
    return avvisi


# ---------------------------------------------------------------------------
# Passi singoli — ognuno isolato e verificabile per conto suo
# ---------------------------------------------------------------------------

def contributi_inps(retribuzione: float, coefficienti: dict) -> float:
    """Contributi previdenziali a carico del dipendente.

    Aliquota base sull'imponibile previdenziale, più l'aliquota aggiuntiva sulla
    sola quota oltre la prima fascia di retribuzione pensionabile. Sopra il
    massimale non si versa più nulla.
    """
    base = min(retribuzione, coefficienti["massimale_annuo"])
    ordinari = base * coefficienti["aliquota_dipendente"]
    oltre_prima_fascia = max(0.0, base - coefficienti["soglia_prima_fascia"])
    return ordinari + oltre_prima_fascia * coefficienti["aliquota_aggiuntiva"]


def imposta_su_scaglioni(imponibile: float, scaglioni) -> float:
    """Applica un'aliquota progressiva a scaglioni.

    Ogni scaglione tassa solo la parte di imponibile che vi ricade, non tutto il
    reddito: è il senso della progressività. Usata sia per l'IRPEF sia per le
    addizionali regionali a scaglioni — stessa meccanica, tabelle diverse.
    """
    imposta = 0.0
    limite_inferiore = 0.0
    for limite_superiore, aliquota in scaglioni:
        if limite_superiore is None:
            quota = max(0.0, imponibile - limite_inferiore)
        else:
            quota = max(0.0, min(imponibile, limite_superiore) - limite_inferiore)
        imposta += quota * aliquota
        if limite_superiore is None or imponibile <= limite_superiore:
            break
        limite_inferiore = limite_superiore
    return imposta


def irpef_lorda(imponibile: float, coefficienti: dict) -> float:
    return imposta_su_scaglioni(imponibile, coefficienti["scaglioni"])


def detrazione_lavoro_dipendente(reddito: float, coefficienti: dict,
                                 quota_anno: float = 1.0) -> float:
    """Detrazione art. 13 c. 1 TUIR: decresce a fasce e azzera l'imposta sui
    redditi bassi (no-tax area).

    Il minimo di 690 euro va RAPPORTATO ai giorni come il resto. Le annotazioni
    di una CU reale lo dicono a lettere: "la detrazione minima è stata
    ragguagliata al periodo di lavoro", e aggiungono che il minimo intero si può
    recuperare in sede di dichiarazione dei redditi — cosa che questo prototipo
    non simula, perché guarda la busta paga e non il 730.

    Rapportandolo, il minimo non entra mai in gioco: la fascia 1 vale 1.955
    euro, sempre più di 690, e la proporzione si applica a entrambi allo stesso
    modo. Resta scritto perché la norma lo prevede e perché rende esplicito che
    ci abbiamo guardato.
    """
    c = coefficienti
    if reddito <= c["fascia_1_limite"]:
        return max(c["fascia_1_importo"], c["fascia_1_minimo"]) * quota_anno
    if reddito <= c["fascia_2_limite"]:
        variabile = c["fascia_2_quota"] * (
            (c["fascia_2_limite"] - reddito) / c["fascia_2_divisore"]
        )
        return (c["fascia_2_base"] + variabile) * quota_anno
    if reddito <= c["fascia_3_limite"]:
        return c["fascia_3_base"] * (
            (c["fascia_3_limite"] - reddito) / c["fascia_3_divisore"]
        ) * quota_anno
    return 0.0


def ulteriore_detrazione_65(reddito: float, coefficienti: dict,
                            quota_anno: float = 1.0) -> float:
    """Art. 13 c. 1.1 TUIR: 65 euro per i redditi oltre 25.000 e fino a 35.000.

    Il comma citato non è l'1-bis, che è stato abrogato dal D.L. 3/2020.
    """
    c = coefficienti
    if c["reddito_minimo_escluso"] < reddito <= c["reddito_massimo_incluso"]:
        return c["importo"] * quota_anno
    return 0.0


def detrazione_cuneo(reddito: float, coefficienti: dict,
                     quota_anno: float = 1.0) -> float:
    """Ulteriore detrazione del taglio del cuneo fiscale (L. 207/2024 art. 1 c. 6).

    Importo pieno fino a 32.000 euro, poi decrescente in modo lineare fino ad
    azzerarsi a 40.000. È una detrazione: abbatte l'IRPEF, non il reddito.
    """
    c = coefficienti
    if reddito <= c["reddito_minimo_escluso"] or reddito > c["reddito_massimo"]:
        return 0.0
    if reddito <= c["reddito_soglia_piena"]:
        return c["importo_pieno"] * quota_anno
    decrescente = c["importo_pieno"] * (
        (c["reddito_massimo"] - reddito)
        / (c["reddito_massimo"] - c["reddito_soglia_piena"])
    )
    return decrescente * quota_anno


def somma_esente_cuneo(reddito_effettivo: float, reddito_annuale: float,
                       coefficienti: dict) -> float:
    """Somma esente del taglio del cuneo fiscale (L. 207/2024 art. 1 c. 4-5).

    NON riduce l'imponibile: è una somma corrisposta in più che non concorre a
    formare il reddito, e va sommata al netto.

    La percentuale si sceglie sul reddito ANNUALIZZATO, come chiarito dalla
    circolare 4/E 2025, e si applica al reddito effettivamente percepito: così
    il rapporto ai giorni avviene una volta sola.

    Non è a scaglioni: si applica una sola percentuale all'intero reddito.
    """
    c = coefficienti
    if reddito_annuale > c["limite_reddito_complessivo"]:
        return 0.0
    for limite, percentuale in c["fasce"]:
        if reddito_annuale <= limite:
            return reddito_effettivo * percentuale
    return 0.0


def addizionale_regionale(imponibile: float, coefficienti: dict) -> float:
    """Regioni diverse hanno forme diverse: alcune usano scaglioni progressivi,
    altre un'aliquota unica. La forma è un dato, non un ramo cablato nel codice."""
    if coefficienti["tipo"] == "scaglioni":
        return imposta_su_scaglioni(imponibile, coefficienti["scaglioni"])
    return imponibile * coefficienti["aliquota"]


def addizionale_comunale(imponibile: float, coefficienti: dict) -> float:
    """Aliquota unica, con soglia di esenzione facoltativa.

    Dove la soglia esiste è una SOGLIA, non una franchigia: superata, si paga
    sull'intero imponibile. È il gradino che rompe la monotonìa del netto —
    a Milano vale circa 184 euro per un centesimo di imponibile in più.

    Nella maggioranza dei comuni italiani (circa il 64%) la soglia non esiste
    affatto: per questo è `None` e non zero.
    """
    soglia = coefficienti.get("soglia_esenzione")
    if soglia is not None and imponibile <= soglia:
        return 0.0
    return imponibile * coefficienti["aliquota"]


def trattamento_integrativo(reddito: float, imposta_lorda: float,
                            detrazioni_art13: float, coefficienti: dict,
                            quota_anno: float = 1.0) -> float:
    """Trattamento integrativo, ex bonus Renzi (D.L. 3/2020).

    Due regimi, con condizioni opposte:

      * fino a 15.000 euro: importo pieno, ma solo se c'è CAPIENZA, cioè se
        l'IRPEF lorda supera la detrazione da lavoro dipendente **diminuita di
        75 euro rapportati al periodo di lavoro**. Sotto la no-tax area non
        spetta, perché non c'è imposta da cui detrarre.

        La catena delle norme, perché la citazione sbagliata è facile:

          * D.L. 3/2020 art. 1 — istituisce il trattamento integrativo;
          * L. 234/2021 art. 1 c. 3 — introduce la condizione di capienza,
            SENZA i 75 euro;
          * D.Lgs. 216/2023 art. 1 — alza la detrazione art. 13 da 1.880 a
            1.955 e, nello stesso momento, introduce i 75 euro per il solo
            2024;
          * L. 207/2024 art. 1 c. 3 — li rende strutturali dal 2025.

        I 75 euro non sono un importo erogato: **neutralizzano l'aumento della
        detrazione**, così che la soglia di capienza resti dov'era. Ai fini
        della capienza la detrazione vale 1.955 - 75 = 1.880, cioè il valore
        precedente alla riforma.

        Questa è anche la prova interna che la fonte non può essere la
        L. 234/2021: è del 2021, e non poteva neutralizzare un aumento
        disposto nel 2023. La prima stesura di questo commento la citava
        comunque — vedi ERRORI.md, voce 24.

        Ometterli non cambia nulla ai redditi medi, ma sposta il gradino di
        1.200 euro: senza, cadeva a un imponibile di 8.500 (RAL 9.360); con,
        cade a 8.173,91 (RAL 9.002). Trovato da una revisione esterna, non dai
        nostri test — che certificavano la soglia sbagliata.

      * da 15.000 a 28.000 euro: spetta solo se le detrazioni spettanti
        SUPERANO l'imposta lorda, e vale quell'eccedenza, con tetto di 1.200.
        Nel caso semplice — nessun familiare a carico, nessun mutuo, nessuna
        spesa detraibile — l'unica detrazione è quella dell'art. 13, che a
        questi redditi è sempre inferiore all'imposta lorda: il risultato è
        quindi zero. La regola è implementata comunque, perché è la norma; il
        fatto che restituisca zero è una conseguenza delle nostre
        semplificazioni, non una scorciatoia.

    Resta in vigore accanto al taglio del cuneo fiscale: le due misure si
    CUMULANO, la L. 207/2024 non ha abrogato questa.
    """
    c = coefficienti
    if reddito > c["soglia_massima"]:
        return 0.0
    if reddito <= c["soglia_importo_pieno"]:
        # La riduzione sta nel registro, con la sua fonte: e' un numero della
        # norma, e i numeri della norma non si scrivono nel codice.
        riduzione = c.get("riduzione_detrazione_capienza", 0.0) * quota_anno
        if imposta_lorda > detrazioni_art13 - riduzione:
            return c["importo"] * quota_anno
        return 0.0
    eccedenza = detrazioni_art13 - imposta_lorda
    if eccedenza <= 0:
        return 0.0
    return min(c["importo"] * quota_anno, eccedenza)


def imposte_su_imponibile(imponibile: float, quota_anno: float,
                          nazionali: dict, territoriali: dict) -> dict:
    """Tutta la parte FISCALE, a partire dall'imponibile gia' calcolato.

    Estratta apposta perche' e' l'unico pezzo che un documento fiscale reale —
    una Certificazione Unica — puo' testimoniare: la CU dichiara l'imponibile,
    non il lordo. Potendo partire da li' si verifica il motore senza ricostruire
    una RAL a ritroso, che introdurrebbe ipotesi al posto di misure.

    Il passo LORDO -> imponibile (i contributi) resta fuori: va verificato
    separatamente, e solo se il documento dichiara l'imponibile previdenziale.
    """
    # Reddito annualizzato: serve SOLO al taglio del cuneo fiscale. Tutte le
    # altre voci guardano il reddito effettivamente percepito. Vedi la nota in
    # testa al modulo: la distinzione e' confermata da una CU reale.
    annuale = imponibile / quota_anno if quota_anno else 0.0

    lorda = irpef_lorda(imponibile, nazionali["irpef"])

    # Reddito EFFETTIVO
    detrazione_lavoro = detrazione_lavoro_dipendente(
        imponibile, nazionali["detrazioni_lavoro_dipendente"], quota_anno)
    detrazione_65 = ulteriore_detrazione_65(
        imponibile, nazionali["ulteriore_detrazione_65"], quota_anno)

    # Reddito ANNUALIZZATO (circolare 4/E 2025)
    detrazione_cuneo_fiscale = detrazione_cuneo(
        annuale, nazionali["cuneo_ulteriore_detrazione"], quota_anno)

    detrazioni = detrazione_lavoro + detrazione_65 + detrazione_cuneo_fiscale

    return {
        "imponibile_annuale": annuale,
        "irpef_lorda": lorda,
        "detrazione_lavoro_dipendente": detrazione_lavoro,
        "ulteriore_detrazione_65": detrazione_65,
        "detrazione_cuneo": detrazione_cuneo_fiscale,
        "detrazioni_totali": detrazioni,
        "irpef_netta": max(0.0, lorda - detrazioni),
        "addizionale_regionale": addizionale_regionale(imponibile, territoriali["regionale"]),
        "addizionale_comunale": addizionale_comunale(imponibile, territoriali["comunale"]),
        "somma_esente_cuneo": somma_esente_cuneo(
            imponibile, annuale, nazionali["cuneo_somma_esente"]),
        # Reddito EFFETTIVO, come per la detrazione art. 13.
        "trattamento_integrativo": trattamento_integrativo(
            imponibile, lorda, detrazione_lavoro,
            nazionali["trattamento_integrativo"], quota_anno),
    }


# ---------------------------------------------------------------------------
# Risultato — tutte le voci, non solo il netto finale
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Voce:
    """Una riga della tabella delle trattenute.

    `provenienza` porta con sé il territorio per le voci che ne dipendono: un
    numero non deve mai staccarsi dal luogo che lo genera.
    """
    etichetta: str
    importo: float
    segno: int  # -1 trattenuta, +1 somma aggiunta, 0 voce informativa
    provenienza: str = ""


@dataclass(frozen=True)
class Risultato:
    # parametri usati
    ral: float
    anno: str
    territorio: str
    comune: str
    regione: str
    giorni: int
    mensilita: int
    ccnl: str

    # catena di calcolo
    retribuzione_effettiva: float
    contributi_inps: float
    imponibile_fiscale: float
    irpef_lorda: float
    detrazione_lavoro_dipendente: float
    ulteriore_detrazione_65: float
    detrazione_cuneo: float
    detrazioni_totali: float
    irpef_netta: float
    addizionale_regionale: float
    addizionale_comunale: float
    somma_esente_cuneo: float
    trattamento_integrativo: float

    # risultati
    totale_trattenute: float
    totale_somme_aggiunte: float
    netto_annuo: float
    netto_mensile: float
    aliquota_effettiva: float

    voci: list = field(default_factory=list)
    avvisi: list = field(default_factory=list)
    # Rapporto con il minimo tabellare del CCNL: a quali livelli corrisponde
    # questa RAL, o se non ne raggiunge nessuno. Vedi verifica_minimo_ccnl().
    minimo_ccnl: dict = field(default_factory=dict)

    def come_dizionario(self) -> dict:
        return asdict(self)




def avvisi_minimo_ccnl(verifica: dict, mensilita: int) -> list[str]:
    """L'avviso da mostrare quando la RAL non regge il confronto col contratto.

    Un solo avviso, e solo nel caso che conta davvero: sotto il minimo di
    ogni livello. Elencare i livelli compatibili quando tutto è a posto e'
    informazione utile, ma non e' un allarme, e mescolare le due cose
    insegna a ignorare gli allarmi.
    """
    if not verifica.get("applicabile") or not verifica.get("sotto_il_minimo"):
        return []
    # Il prefisso permette all'interfaccia di distinguere questo avviso dagli
    # altri senza doverne leggere il testo. NON blocca il calcolo: il risultato
    # viene mostrato lo stesso, perche' sapere quanto resterebbe in tasca e'
    # utile anche quando l'offerta va rifatta — e perche' uno strumento che si
    # rifiuta di rispondere insegna solo ad aggirarlo.
    return [
        "[minimo-ccnl] "
        f"{formatta_euro(verifica['minimo_assoluto_annuo'])} è il minimo contrattuale "
        f"più basso di questo CCNL (livello {verifica['livello_piu_basso']}, "
        f"{mensilita} mensilità): la RAL inserita sta sotto. Il minimo tabellare non è "
        "derogabile in peggio, quindi a tempo pieno un'offerta così non è proponibile. "
        "Se si tratta di un part-time il minimo si riduce in proporzione alle ore, e "
        "questo prototipo non modella l'orario."
    ]

def verifica_minimo_ccnl(ral: float, codice_ccnl: str, mensilita: int) -> dict:
    """La RAL sta sopra il minimo contrattuale? E a quali livelli corrisponde?

    Perché serve, e perché non è un dettaglio da specialisti
    ---------------------------------------------------------
    Una RAL sotto il minimo tabellare del CCNL non è un'offerta bassa: è
    un'offerta che **non si può fare**. Il minimo contrattuale è inderogabile
    in peius, e uno strumento che calcola serenamente il netto di una RAL
    illegittima sta aiutando qualcuno a sbagliare con precisione.

    È anche l'informazione che serve prima di tutte le altre a chi scrive
    un'offerta: non «quanto resta in tasca» ma «questa cifra sta in piedi?».

    Cosa restituisce
    ----------------
    Tre esiti possibili, tenuti distinti perché significano cose diverse:

      * `applicabile = False` — il registro non ha i minimi di quel contratto.
        Lo strumento dichiara di non sapere invece di tacere, che a un utente
        somiglia troppo a un via libera.
      * `sotto_il_minimo = True` — la RAL non raggiunge nemmeno il livello più
        basso. Nessun inquadramento a tempo pieno la giustifica.
      * altrimenti, `livelli_compatibili` elenca gli inquadramenti che quella
        RAL copre. È la risposta utile: non un sì o un no, ma *fino a dove*.

    I limiti, che vanno detti insieme al risultato
    ----------------------------------------------
    Il minimo tabellare è paga base ed ex contingenza. Non comprende terzo
    elemento provinciale, scatti di anzianità e superminimi: la retribuzione
    reale di un livello è quasi sempre più alta del suo minimo. Il confronto
    dice quindi «non è al di sotto», non «è corretta».

    E vale per il **tempo pieno**. Un part-time ha minimi proporzionati alle
    ore, e una RAL legittimamente più bassa: questo prototipo non modella
    l'orario, quindi l'avviso lo scrive invece di far finta di saperlo.
    """
    minimi = registro.minimi_di(codice_ccnl)
    if not minimi:
        return {
            "applicabile": False,
            "motivo": "Il registro non contiene i minimi tabellari di questo contratto.",
        }

    livelli = minimi["livelli"]
    # Le mensilità del contratto sono il moltiplicatore: tredicesima e
    # quattordicesima sono una mensilità ciascuna, quindi il minimo annuo è il
    # minimo mensile per il numero di mensilità.
    annui = {nome: importo * mensilita for nome, importo in livelli.items()}
    nome_piu_basso = min(annui, key=annui.get)
    minimo_assoluto = annui[nome_piu_basso]

    compatibili = sorted(
        (nome for nome, annuo in annui.items() if ral >= annuo),
        key=lambda nome: annui[nome], reverse=True,
    )

    return {
        "applicabile": True,
        "parziale": bool(minimi.get("parziale")),
        "sotto_il_minimo": ral < minimo_assoluto,
        "minimo_assoluto_annuo": minimo_assoluto,
        "livello_piu_basso": nome_piu_basso,
        "livelli_compatibili": compatibili,
        "livello_massimo_coperto": compatibili[0] if compatibili else None,
        "in_vigore_da": minimi.get("in_vigore_da"),
        "fonte": minimi.get("_fonte"),
        "stato": minimi.get("_stato"),
    }

def calcola(ral, anno=None, territorio_codice=None, giorni=GIORNI_ANNO,
            ccnl=None, mensilita=None) -> Risultato:
    """Da una RAL al dettaglio completo del netto.

    Tutti i parametri hanno un default preso dal registro, mai cablato qui:
    l'anno più recente, il territorio predefinito (Milano, che è l'esempio del
    task e anche il caso più diffuso), il CCNL predefinito.
    """
    ral = valida_ral(ral)
    giorni = valida_giorni(giorni)

    anno = str(anno) if anno is not None else registro.anno_predefinito()
    territorio_codice = territorio_codice or registro.territorio_predefinito()
    ccnl = ccnl or registro.ccnl_predefinito()
    mensilita = int(mensilita) if mensilita is not None else registro.mensilita_di(ccnl)
    if mensilita <= 0:
        raise ValueError("Le mensilità devono essere un numero positivo.")

    naz = registro.nazionale(anno)
    terr = registro.territorio(territorio_codice, anno)
    anagrafica = registro.anagrafica_territorio(territorio_codice)

    quota_anno = giorni / GIORNI_ANNO
    minimo_ccnl = verifica_minimo_ccnl(ral, ccnl, mensilita)

    # --- dal lordo all'imponibile ------------------------------------------
    retribuzione = ral * quota_anno
    contributi = contributi_inps(retribuzione, naz["inps"])
    imponibile = retribuzione - contributi

    # --- imposte, detrazioni e bonus ----------------------------------------
    fiscale = imposte_su_imponibile(imponibile, quota_anno, naz, terr)
    lorda = fiscale["irpef_lorda"]
    detrazione_lavoro = fiscale["detrazione_lavoro_dipendente"]
    detrazione_65 = fiscale["ulteriore_detrazione_65"]
    detrazione_cuneo_fiscale = fiscale["detrazione_cuneo"]
    detrazioni = fiscale["detrazioni_totali"]
    netta = fiscale["irpef_netta"]
    regionale = fiscale["addizionale_regionale"]
    comunale = fiscale["addizionale_comunale"]
    esente = fiscale["somma_esente_cuneo"]
    integrativo = fiscale["trattamento_integrativo"]

    # --- ricomposizione -----------------------------------------------------
    trattenute = contributi + netta + regionale + comunale
    aggiunte = esente + integrativo
    netto_annuo = retribuzione - trattenute + aggiunte
    netto_mensile = netto_annuo / mensilita
    aliquota_effettiva = trattenute / retribuzione if retribuzione else 0.0

    luogo = f"{anagrafica['comune']} / {anagrafica['regione']}"
    voci = [
        Voce("Retribuzione lorda", retribuzione, 0),
        Voce("Contributi INPS a carico del dipendente", contributi, -1),
        Voce("Imponibile fiscale", imponibile, 0),
        Voce("IRPEF lorda", lorda, 0),
        Voce("Detrazione per lavoro dipendente", detrazione_lavoro, +1),
        Voce("Ulteriore detrazione (art. 13 c. 1.1)", detrazione_65, +1),
        Voce("Detrazione taglio del cuneo fiscale", detrazione_cuneo_fiscale, +1),
        Voce("IRPEF netta", netta, -1),
        Voce(_etichetta_regionale(terr["regionale"], anagrafica["regione"]),
             regionale, -1, anagrafica["regione"]),
        Voce(_etichetta_comunale(terr["comunale"], anagrafica["comune"]),
             comunale, -1, anagrafica["comune"]),
        Voce("Somma esente taglio del cuneo fiscale", esente, +1),
        Voce("Trattamento integrativo", integrativo, +1),
    ]

    return Risultato(
        ral=ral, anno=anno, territorio=territorio_codice,
        comune=anagrafica["comune"], regione=anagrafica["regione"],
        giorni=giorni, mensilita=mensilita, ccnl=ccnl,
        retribuzione_effettiva=retribuzione,
        contributi_inps=contributi,
        imponibile_fiscale=imponibile,
        irpef_lorda=lorda,
        detrazione_lavoro_dipendente=detrazione_lavoro,
        ulteriore_detrazione_65=detrazione_65,
        detrazione_cuneo=detrazione_cuneo_fiscale,
        detrazioni_totali=detrazioni,
        irpef_netta=netta,
        addizionale_regionale=regionale,
        addizionale_comunale=comunale,
        somma_esente_cuneo=esente,
        trattamento_integrativo=integrativo,
        totale_trattenute=trattenute,
        totale_somme_aggiunte=aggiunte,
        netto_annuo=netto_annuo,
        netto_mensile=netto_mensile,
        aliquota_effettiva=aliquota_effettiva,
        voci=voci,
        avvisi=avvisi_plausibilita(ral) + avvisi_minimo_ccnl(minimo_ccnl, mensilita),
        minimo_ccnl=minimo_ccnl,
    )


def formatta_percentuale(valore: float) -> str:
    """0.008 -> '0,8%'. Separatore decimale italiano, zeri finali tolti."""
    testo = f"{valore * 100:.4f}".rstrip("0").rstrip(".")
    return testo.replace(".", ",") + "%"


def formatta_euro(valore: float, decimali: int = 0) -> str:
    """23000 -> '23.000 €'; con decimali=2 -> '23.000,00 €'.

    Converte i separatori all'uso italiano lavorando SOLO sul numero: applicare
    la sostituzione a una frase intera trasformava in punti anche le virgole
    della punteggiatura (vedi DIARIO_DI_BORDO.md, voce 23).
    """
    testo = f"{valore:,.{decimali}f}"
    return testo.replace(",", "\x00").replace(".", ",").replace("\x00", ".") + " €"


def _etichetta_regionale(coefficienti: dict, regione: str) -> str:
    if coefficienti["tipo"] == "scaglioni":
        return f"Addizionale regionale ({regione}, a scaglioni)"
    return f"Addizionale regionale ({regione}, {formatta_percentuale(coefficienti['aliquota'])})"


def _etichetta_comunale(coefficienti: dict, comune: str) -> str:
    aliquota = formatta_percentuale(coefficienti["aliquota"])
    soglia = coefficienti.get("soglia_esenzione")
    if soglia is None:
        return f"Addizionale comunale ({comune}, {aliquota}, nessuna esenzione)"
    return f"Addizionale comunale ({comune}, {aliquota}, esente fino a {formatta_euro(soglia)})"
