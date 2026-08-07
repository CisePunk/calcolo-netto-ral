# Metodologia

Come si passa da una RAL a un netto, quale norma governa ogni passaggio, e in
che punto del codice quella norma è applicata.

Il documento risponde a tre domande diverse, ed è diviso di conseguenza:

1. **Come si calcola** — la catena, spiegata per un lettore;
2. **Quale norma è stata applicata dove** — la tabella di tracciabilità;
3. **Come si mantiene vero** — cosa fare quando la normativa cambia.

---

## 1. La catena di calcolo

```
RAL contrattuale
  × giorni/365 ─────────────────────→ retribuzione effettiva del periodo
  − contributi INPS a carico del dipendente
  ═══════════════════════════════════
  = imponibile fiscale  (= reddito complessivo, nel caso semplice)

    IRPEF lorda, a scaglioni progressivi
      − detrazione per lavoro dipendente
      − ulteriore detrazione di 65 €
      − ulteriore detrazione da taglio del cuneo fiscale
  ═══════════════════════════════════
  = IRPEF netta  (mai sotto zero)

  − addizionale regionale
  − addizionale comunale
  + somma esente da taglio del cuneo fiscale
  + trattamento integrativo
  ═══════════════════════════════════
  = netto annuo
  ÷ mensilità ──────────────────────→ netto mensile
```

### I tre punti in cui è facile sbagliare

**I contributi non si tassano.** L'IRPEF non si calcola sulla RAL ma
sull'imponibile, cioè sulla RAL meno i contributi previdenziali a carico del
lavoratore. Chi applica le aliquote alla RAL sbaglia in eccesso di qualche
centinaio di euro.

**Le due misure del cuneo fiscale hanno natura opposta.** La *somma esente*
(redditi fino a 20.000 €) è denaro corrisposto in più: **si somma al netto**.
L'*ulteriore detrazione* (20.000–40.000 €) è una detrazione vera: **abbatte
l'IRPEF**. Trattare la prima come una deduzione dall'imponibile sbaglia due
volte nella stessa direzione.

**Le soglie non sono franchigie.** Dove esiste una soglia di esenzione
comunale, superarla comporta il pagamento **sull'intero imponibile**, non sulla
sola quota eccedente. A Milano questo produce un gradino di circa 184 €: cento
euro di lordo in più ne possono costare 184 di netto.

---

## 2. Tracciabilità: quale norma, dove

Ogni riga collega un atto normativo alla funzione che lo applica e al modo in
cui il valore è stato verificato.

### Perché questa tabella esiste

Non è archivistica: è manutenzione, e risponde a un problema con una scadenza.

**La legge di bilancio viene approvata entro il 31 dicembre ed entra in vigore
il 1° gennaio.** Chi mantiene uno strumento di calcolo retributivo ha giorni,
non mesi, per capire cosa è cambiato e dove intervenire. E ogni giorno di
ritardo non produce un errore visibile: produce **buste paga e offerte
sbagliate che sembrano giuste**, perché un netto calcolato con le aliquote
dell'anno prima è un numero perfettamente plausibile.

Senza tracciabilità, la domanda *«la legge di bilancio ha cambiato la seconda
aliquota IRPEF: cosa devo toccare?»* si risponde **rileggendo il motore**, e
sperando di non dimenticare un punto. Con la tabella, si risponde consultandola:
due righe del registro, zero righe di codice.

Il caso è reale ed è già successo qui. Il passaggio della seconda aliquota dal
35% al 33% — introdotto dalla L. 199/2025 — ha comportato:

| Con i coefficienti nel codice | Con il registro e questa tabella |
|---|---|
| trovare tutte le occorrenze del valore | cercare «L. 199/2025» nella tabella |
| capire quali test vanno riscritti | modificare due voci del registro |
| rischiare di aggiornare il 2026 e dimenticare il 2025 | i due anni sono righe diverse, entrambe verificate |

C'è una seconda ragione, meno ovvia. La tabella riporta anche **lo stato della
fonte**: un valore letto sull'atto ufficiale e uno preso da una rassegna
specialistica non vanno ricontrollati con la stessa urgenza. Sapere quali sono i
diciotto valori su fonte primaria e quali i sessantotto su fonte secondaria
significa poter **ordinare il lavoro di verifica** invece di rifarlo tutto ogni
anno.

### Contributi previdenziali

| Norma | Cosa fissa | Dove è applicata | Stato |
|---|---|---|---|
| L. 335/1995 e circolari INPS annuali | aliquota IVS a carico del lavoratore, 9,19% | `calcolo.contributi_inps()` | secondaria |
| **Art. 3-*ter* D.L. 384/1992** | aliquota aggiuntiva dell'1% sulla quota oltre la prima fascia | `calcolo.contributi_inps()` | primaria |
| INPS, minimali e massimali annuali | prima fascia (56.224 € nel 2026) e massimale (122.295 €) | registro, `nazionale.inps` | secondaria |

### IRPEF

| Norma | Cosa fissa | Dove è applicata | Stato |
|---|---|---|---|
| **Art. 11 TUIR** | struttura a scaglioni progressivi | `calcolo.imposta_su_scaglioni()` | primaria |
| **L. 199/2025** (Legge di Bilancio 2026) | seconda aliquota al 33% dal 1/1/2026 | registro, `nazionale.2026.irpef` | primaria |
| D.Lgs. 216/2023 | assetto a tre aliquote, 35% per il 2025 | registro, `nazionale.2025.irpef` | primaria |

### Detrazioni

| Norma | Cosa fissa | Dove è applicata | Stato |
|---|---|---|---|
| **Art. 13 c. 1 TUIR** | detrazione per lavoro dipendente, decrescente a fasce | `calcolo.detrazione_lavoro_dipendente()` | secondaria |
| **Art. 13 c. 1.1 TUIR** | ulteriore detrazione di 65 € fra 25.000 e 35.000 € | `calcolo.ulteriore_detrazione_65()` | primaria |

> Il comma 1-*bis*, che si trova citato spesso, è **abrogato** dal D.L. 3/2020.
> La prima stesura di questo progetto lo citava: un numero giusto con una
> citazione sbagliata resta un numero non verificato.

### Taglio del cuneo fiscale

| Norma | Cosa fissa | Dove è applicata | Stato |
|---|---|---|---|
| **L. 207/2024 art. 1 c. 4–5** | somma esente per redditi fino a 20.000 € (7,1% / 5,3% / 4,8%) | `calcolo.somma_esente_cuneo()` | secondaria |
| **L. 207/2024 art. 1 c. 6** | ulteriore detrazione fino a 1.000 €, decrescente fra 32.000 e 40.000 € | `calcolo.detrazione_cuneo()` | primaria |
| **Circolare Agenzia Entrate 4/E del 16/5/2025** | per il cuneo il reddito va **annualizzato**; le due misure si **cumulano** con il trattamento integrativo | `calcolo.imposte_su_imponibile()` | primaria |

> La circolare risolve la questione che nessuna fonte divulgativa affrontava:
> somma esente e trattamento integrativo **si cumulano**. Sbagliarlo valeva
> 1.200 € su tutta la fascia bassa di reddito.

### Trattamento integrativo

| Norma | Cosa fissa | Dove è applicata | Stato |
|---|---|---|---|
| **Art. 1 D.L. 3/2020** (conv. L. 21/2020) | 1.200 € fino a 15.000 €, ridotto fino a 28.000 €, con condizione di capienza | `calcolo.trattamento_integrativo()` | secondaria |

### Addizionali locali

| Norma | Cosa fissa | Dove è applicata | Stato |
|---|---|---|---|
| Leggi regionali (Lombardia, Sicilia) | aliquote regionali, a scaglioni o unica | `calcolo.addizionale_regionale()` | secondaria |
| L. 199/2025 | facoltà per le Regioni di mantenere gli scaglioni preesistenti fino al 2028 | registro, note territoriali | secondaria |
| Delibere comunali | aliquota comunale e soglia di esenzione | `calcolo.addizionale_comunale()` | — |
| **Agenzia delle Entrate, tabella addizionali comunali** | i valori effettivi per ogni comune italiano | registro, `territori.*.comunale` | **primaria** |

> ⚠️ **La trappola.** Le tabelle dell'Agenzia sono indicizzate per
> **modulistica**, non per anno d'imposta: la tabella *«modulistica 2026»*
> contiene le aliquote dei redditi **2025**. Prendere la tabella con l'anno che
> si sta cercando produce un'aliquota sbagliata di un anno, con tutta l'aria di
> essere una fonte ufficiale.

### Periodi di lavoro parziali

| Norma / fonte | Cosa fissa | Dove è applicata |
|---|---|---|
| Art. 13 TUIR («rapportate al periodo di lavoro nell'anno») | detrazioni proporzionali ai giorni, sul reddito **effettivo** | `calcolo.imposte_su_imponibile()` |
| Circolare AdE 4/E 2025 | per il cuneo, reddito **annualizzato** | idem |
| Annotazioni della CU | il minimo di 690 € va **ragguagliato** al periodo | `calcolo.detrazione_lavoro_dipendente()` |

> Le due regole sono **opposte** e convivono. Una regola uniforme — che era la
> nostra prima scelta perché sembrava più elegante — produce zero dove il
> sostituto d'imposta la riconosce, ragguagliata ai giorni. Vedi
> [ERRORI.md](../verifiche/ERRORI.md) n. 8.

---

## 3. Come si mantiene vero

I coefficienti stanno in [dati/coefficienti.json](../../dati/coefficienti.json), con
la fonte e la data accanto a ognuno. Aggiornare l'anno significa aggiungere un
blocco a quel file e rigenerare il seed del database: il codice non si tocca.

### Il calendario: quando guardare, non solo dove

La tabella di tracciabilità dice **cosa** toccare. Questo calendario dice
**quando** andare a vedere se qualcosa è cambiato — e serve perché le fonti non
escono tutte insieme, e alcune escono **mesi dopo** che la norma è già in
vigore.

| Quando | Cosa esce | Impatto | Cosa fare |
|---|---|---|---|
| **entro il 31 dicembre** | Legge di bilancio, in vigore dal 1° gennaio | 🔥 aliquote IRPEF, cuneo fiscale, detrazioni | leggerla subito: da gennaio ogni calcolo usa i valori nuovi |
| **fine gennaio / inizio febbraio** | Circolare INPS su minimali e massimali | prima fascia del +1%, massimale | aggiornamento automatico ogni anno, per rivalutazione ISTAT |
| **primavera** | Circolari dell'Agenzia sulle misure nuove | regole di **applicazione** | è qui che si trovano le regole che la norma non dice |
| **~marzo (bozza), ~giugno (definitiva)** | Tabella addizionali comunali dell'Agenzia | aliquote e soglie di tutti i comuni | ⚠️ la *modulistica N* contiene l'anno d'imposta **N−1** |
| **entro l'approvazione del bilancio comunale** | Delibere dei singoli comuni | aliquota e soglia del comune | consolidate poi nella tabella dell'Agenzia |
| **raramente** | Leggi regionali sulle addizionali | aliquote regionali | cambiano di rado, ma cambiano |

**La conseguenza operativa più importante** sta nella riga in grassetto: fra il
1° gennaio e la pubblicazione della tabella consolidata dell'Agenzia passano
**mesi**. In quella finestra le addizionali comunali dell'anno in corso poggiano
su delibere e rassegne, non su una fonte primaria.

Non è un difetto da nascondere: è la ragione per cui il registro ha un campo
`stato`, e per cui il prototipo **lo dichiara all'utente** invece di far finta
di una certezza uniforme. Oggi, sui coefficienti 2026, sono 18 voci su fonte
primaria e 68 su fonte secondaria — e le comunali dell'anno in corso stanno fra
le seconde.

### La verifica periodica, in ordine di priorità

1. **Legge di bilancio** — impatto più alto, finestra più stretta.
2. **Circolare INPS minimali e massimali** — cambia ogni anno per automatismo.
3. **Circolari dell'Agenzia** sulle misure nuove.
4. **Tabella addizionali comunali** — quando esce, promuove a fonte primaria i
   valori che nel frattempo erano secondari.
5. **Delibere regionali.**

Dopo ogni aggiornamento:

```bash
python3 test_motore.py                       # 399 test
python3 strumenti/controllo_sensibilita.py   # i test si accorgono dei guasti?
python3 strumenti/genera_seed.py             # rigenera il seed dal registro
```

---

## 4. Normativa per l'estensione più utile: le agevolazioni

Il prototipo **non** implementa le agevolazioni: il task le esclude
esplicitamente (*«nessuna agevolazione particolare»*). Ma sono la leva con
l'impatto economico più alto per un'azienda che assume, e la mappa normativa va
tracciata prima di costruire, non dopo.

Quanto segue è **ricerca preliminare, non implementazione**: i riferimenti sono
stati raccolti e verificati come fonti, i valori non sono entrati nel registro.

### Esoneri contributivi per nuove assunzioni

| Norma | Misura |
|---|---|
| **L. 199/2025** (Legge di Bilancio 2026) e **D.L. 30 aprile 2026 n. 62** | tre esoneri per le assunzioni stabili effettuate dal 1/1 al 31/12/2026 |
| **INPS, circolari 55, 56 e 57 del 14 maggio 2026** | istruzioni operative |

- **Giovani under 35 in condizione di svantaggio**: esonero del 100% della
  contribuzione (esclusi premi e contributi INAIL), fino a **500 €/mese per 24
  mesi**; **650 €** nel Mezzogiorno. Novità rispetto al passato: non conta più
  la storia contrattuale, ma la condizione di svantaggio effettiva.
- **Donne con almeno tre figli minori**, senza lavoro regolarmente retribuito da
  almeno sei mesi: fino a **650 €/mese per 24 mesi**; **800 €** nella ZES unica
  del Mezzogiorno.

### Maxi-deduzione del costo del lavoro

| Norma | Misura |
|---|---|
| **D.Lgs. 216/2023**, prorogata dalla Legge di Bilancio 2025 per 2025–2027 | deduzione maggiorata sul costo delle nuove assunzioni a tempo indeterminato che producono incremento occupazionale netto |

**120%** del costo ordinario, **130%** per categorie meritevoli di maggior tutela
(under 30, donne svantaggiate, persone con disabilità). Su un dipendente da
30.000 € di costo, la deduzione vale 36.000 €: circa **1.440 € di IRES
risparmiata** all'anno.

### Regime impatriati

| Norma | Misura |
|---|---|
| **Art. 5 D.Lgs. 209/2023** | tassazione del solo **50%** del reddito da lavoro per cinque anni (**60%** di riduzione con figli minori), entro 600.000 € annui di reddito agevolabile |

Requisiti: residenza estera nei tre periodi d'imposta precedenti (sette se si
rientra presso lo stesso datore di lavoro estero), trasferimento della residenza
fiscale in Italia, attività svolta prevalentemente in territorio italiano,
laurea oppure ventiquattro mesi di esperienza qualificata.

### Perché questa è l'estensione giusta

È l'unico punto in cui il calcolo cambia di natura: smette di rispondere a
*«quanto prende il dipendente»* e comincia a rispondere a **«quanto risparmia
l'azienda»**. È la domanda che porta i soldi, ed è quella che un HR pone davvero
prima di assumere.

La struttura per accoglierle esiste già: il registro tratta anno e territorio
come dati con la loro fonte, e un'agevolazione è un'altra dimensione dello
stesso tipo — con in più una **data di scadenza**, perché questi incentivi
nascono e muoiono con le leggi di bilancio. Il campo `vigenza` nel registro
serve esattamente a questo.

> **Nota di metodo, valida per l'estensione quanto per il prototipo.** Nessuno di
> questi valori entra nel codice finché non ha una fonte e una data accanto. La
> ricerca qui sopra è il primo passo, non l'ultimo: prima di implementare, ogni
> numero va letto sull'atto — circolare INPS, non articolo di giornale.

---

## Fonti

Tutte le fonti consultate, con lo stato di verifica di ciascun valore, sono
elencate in [RICERCA_FONTI.md](RICERCA_FONTI.md). I riferimenti per la sezione
sulle agevolazioni:

- [Bonus giovani, donne e ZES: prime istruzioni INPS (Finanza & Fisco)](https://www.finanzaefisco.com/bonus-giovani-donne-e-zes/)
- [Esoneri contributivi assunzioni 2026 (FiscoeTasse)](https://www.fiscoetasse.com/approfondimenti/17188-esoneri-contributivi-2026-i-nuovi-bonus-assunzioni-al-100.html)
- [Maxi-deduzione costo del lavoro 2026](https://www.studiogiaquinta.it/blog/maxi-deduzione-costo-lavoro-2026/)
- [Regime impatriati 2026 (Fiscomania)](https://fiscomania.com/regime-impatriati-rientro-dei-cervelli/)
- [Agenzia delle Entrate — risposta n. 82/2026 sugli impatriati](https://www.agenziaentrate.gov.it/portale/documents/20143/9761612/Risposta+n.+82_2026/15959ef8-1432-3a70-8af0-beb4d6b9b795)
