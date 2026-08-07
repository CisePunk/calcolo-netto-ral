# Ricerca fonti — anni d'imposta 2026 e 2025

Esito del Giorno 1. Ogni coefficiente che entrerà nel motore è elencato qui con
il valore, la norma che lo fissa e — soprattutto — **quanto è solido**.

I valori in forma utilizzabile stanno in [dati/coefficienti.json](dati/coefficienti.json),
che è la fonte di verità da cui leggono il motore e il seed del database. Questo
documento spiega **da dove vengono**; quel file **li contiene**.

Il **2026** è l'anno del prodotto. Il **2025** (§10) serve solo per il confronto
con una Certificazione Unica reale.

Lo stato di verifica è dichiarato onestamente, perché è la differenza tra "il
numero è giusto" e "so perché il numero è giusto":

| Stato | Significato |
|---|---|
| ✅ **Primaria** | Confermato su fonte ufficiale (norma, INPS, Agenzia Entrate, ente locale) |
| 🟡 **Secondaria** | Concorde su più fonti specialistiche, ma non ancora letto sull'atto ufficiale |
| 🔴 **Aperta** | Questione non risolta, incide sul risultato, va chiusa prima della consegna |

> **Nota di metodo.** Le pagine del Comune di Milano bloccano l'accesso
> automatico, quindi le addizionali comunali sono state prese da una fonte
> migliore: la **tabella ufficiale dell'Agenzia delle Entrate**, che raccoglie le
> aliquote deliberate da tutti i comuni italiani. Milano e Palermo sono così
> confermate su fonte primaria (§7, §9) — con una trappola sull'indicizzazione
> per anno che vale la pena leggere.

---

## 1. Contributi previdenziali INPS a carico del dipendente

| Voce | Valore 2026 | Stato |
|---|---|---|
| Aliquota IVS c/dipendente (FPLD) | **9,19%** | 🟡 Secondaria |
| Aliquota aggiuntiva oltre prima fascia | **+1,00%** | ✅ Primaria (art. 3-*ter* D.L. 384/1992) |
| Prima fascia di retribuzione pensionabile | **56.224 €/anno** (4.685 €/mese) | 🟡 Secondaria |
| Massimale contributivo annuo | **122.295 €** | 🟡 Secondaria |

L'aliquota totale FPLD resta il 33%: 23,81% al datore, 9,19% al lavoratore.

**Cosa cambia rispetto al file attuale:** la soglia del +1% era `55.008 €`
(valore di un altro anno). Per il 2026 è **56.224 €**.

**Semplificazione da dichiarare:** il massimale di 122.295 € vale solo per chi è
iscritto per la prima volta dal 1/1/1996. Fuori dal caso "semplice e standard";
lo implementiamo ma lo segnaliamo.

---

## 2. IRPEF — scaglioni progressivi

| Scaglione | Aliquota 2026 | Aliquota 2025 |
|---|---|---|
| fino a 28.000 € | **23%** | 23% |
| da 28.000 a 50.000 € | **33%** ⚠️ | 35% |
| oltre 50.000 € | **43%** | 43% |

Stato: ✅ **Primaria** — Legge di Bilancio 2026 (**L. 199/2025**), che rende
strutturale il taglio della seconda aliquota dal 35% al 33% a decorrere dal
1° gennaio 2026.

> ⚠️ **È l'errore più costoso del file attuale.** Con la 35% ancora dentro, ogni
> RAL sopra i 28.000 € produce un netto sbagliato per difetto. Su una RAL di
> 45.000 € lo scarto è nell'ordine delle centinaia di euro l'anno.

Attenzione a non confondersi in sede di verifica: il **730/2026** applica ancora
il 35%, perché riguarda i redditi *2025*. Il 33% si vede in busta paga nel 2026 e
nella dichiarazione del 2027. Un calcolatore che proietta il netto **oggi** deve
usare il 33%.

---

## 3. Detrazioni per lavoro dipendente (art. 13 TUIR)

| Fascia di reddito complessivo | Detrazione | Stato |
|---|---|---|
| fino a 15.000 € | **1.955 €** | 🟡 Secondaria |
| da 15.000 a 28.000 € | **1.910 + 1.190 × (28.000 − R) / 13.000** | 🟡 Secondaria |
| da 28.000 a 50.000 € | **1.910 × (50.000 − R) / 22.000** | 🟡 Secondaria |
| oltre 50.000 € | **0** | 🟡 Secondaria |

**Ulteriore detrazione: 65 €** per redditi complessivi **superiori a 25.000 € e
non oltre 35.000 €**, rapportata al periodo di lavoro nell'anno.

> ✅ **Questione chiusa.** La norma è l'**art. 13 comma 1.1** TUIR, non il comma
> 1-*bis* come scritto nella prima stesura: quel comma è stato **abrogato** dal
> D.L. 3/2020. La fascia corretta è **25.000–35.000 €**, non 28.000–35.000.
> Il file attuale sbaglia di 65 € su tutti i redditi tra 25k e 28k.

**Riduzione per redditi alti:** dal 2026 le detrazioni sono ridotte di **440 €**
per chi supera i **200.000 €** di reddito complessivo (escluse spese sanitarie,
erogazioni ai partiti, premi per rischio calamità). Fuori dal nostro caso
standard, ma degno di una riga nel README.

---

## 4. Taglio del cuneo fiscale — la voce che nel file manca del tutto

Riformato dalla L. 207/2024 e confermato per il 2026. **Non è più uno sgravio
contributivo**: sono due misure fiscali distinte, a seconda del reddito.

### a) Redditi fino a 20.000 € → *somma esente da IRPEF*

Percentuale applicata al **reddito da lavoro dipendente**:

| Reddito da lavoro | Percentuale |
|---|---|
| fino a 8.500 € | **7,1%** |
| da 8.500 a 15.000 € | **5,3%** |
| da 15.000 a 20.000 € | **4,8%** |

Stato: 🟡 Secondaria. Esempio di controllo: 18.000 € → 864 € esenti (4,8%).

### b) Redditi da 20.000 a 40.000 € → *ulteriore detrazione*

| Reddito complessivo | Detrazione |
|---|---|
| da 20.000 a 32.000 € | **1.000 €** fissi |
| da 32.000 a 40.000 € | **decrescente**, fino ad azzerarsi a 40.000 € |
| oltre 40.000 € | **0** |

> ✅ **Questione chiusa.** La formula del tratto decrescente è lineare:
>
> ```
> detrazione = 1.000 × (40.000 − reddito complessivo) / 8.000
> ```
>
> Fonte: **art. 1 comma 6 della L. 207/2024**. Vale per redditi da 32.000,01 a
> 40.000 €, e come le altre va **riproporzionata al periodo di lavoro**.
> Fascia 20.000,01–32.000 €: 1.000 € fissi. Oltre 40.000 €: nulla.

> Questa è la voce con **più impatto sul caso standard** e nel motore attuale non
> esiste. Da sola vale 1.000 € di netto per un impiegato tra 20k e 32k.

---

## 5. Trattamento integrativo (ex bonus Renzi)

Resta in vigore nel 2026, **accanto** al cuneo fiscale.

| Reddito complessivo | Importo |
|---|---|
| fino a 15.000 € | **1.200 €** pieni |
| da 15.000 a 28.000 € | ridotto: differenza tra detrazioni spettanti e IRPEF lorda, max 1.200 € |
| oltre 28.000 € | **0** |

**Condizione di capienza:** l'IRPEF lorda sui redditi da lavoro dipendente deve
essere *strettamente maggiore* delle detrazioni art. 13. Sotto la no-tax area
(~8.500 €) il bonus non spetta, perché non c'è imposta da cui detrarre.

Stato: 🟡 Secondaria.

> ✅ **Questione chiusa — ed era la più delicata della ricerca. Sì, si cumulano.**
> Il trattamento integrativo **non è stato abrogato** dalla L. 207/2024: convive
> con la somma esente (≤20k) e con l'ulteriore detrazione (20k–40k). Un
> dipendente sotto i 15.000 € prende **entrambe** le misure.
>
> Riferimento: **circolare Agenzia delle Entrate n. 4/E del 16 maggio 2025**.
> Le due somme si assomigliano — nessuna delle due concorre a formare il reddito,
> entrambe incidono solo sul netto in busta — ed è proprio per questo che è facile
> scambiarle per la stessa misura e contarne una sola.
>
> Il file attuale implementa **solo** il trattamento integrativo, con la
> condizione di capienza corretta ma senza la fascia 15k–28k.

---

## 6. Addizionale regionale IRPEF — Lombardia

Quattro scaglioni sull'imponibile IRPEF:

| Scaglione | Aliquota |
|---|---|
| fino a 15.000 € | **1,23%** |
| da 15.000 a 28.000 € | **1,58%** |
| da 28.000 a 50.000 € | **1,72%** |
| oltre 50.000 € | **1,73%** |

Stato: 🟡 Secondaria (concordi Regione Lombardia e banca dati MEF).

La Lombardia ha **mantenuto il vecchio sistema a quattro scaglioni**, facoltà
concessa fino al 2028 dalla Legge di Bilancio 2026: non si è allineata alle tre
aliquote statali.

**Cosa cambia rispetto al file attuale:** il file ha **cinque** scaglioni con
soglie a 55.000 e 75.000 €. Sbagliato: le soglie seguono quelle IRPEF
(15.000 / 28.000 / 50.000) e l'ultima aliquota è 1,73%, non 1,74%.

---

## 7. Addizionale comunale IRPEF — Milano

| Voce | Valore |
|---|---|
| Aliquota | **0,80%**, unica |
| Soglia di esenzione | **23.000 €** di imponibile |

Stato: ✅ **Primaria** — letti nella tabella ufficiale dell'Agenzia delle Entrate
*«Addizionali comunali — modulistica 2026»* (anno d'imposta 2025), riga
`F205 MILANO MI 0.8 23000`. Gli stessi valori compaiono nella tabella
*modulistica 2025* (anno d'imposta 2024): l'aliquota milanese è **stabile su due
anni d'imposta**.

> ⚠️ Per l'anno d'imposta **2026** questi valori restano 🟡 secondari: la tabella
> ufficiale che li confermerà è la *modulistica 2027*, non ancora pubblicata.
> Non è un difetto della ricerca, è il calendario delle fonti — e va detto
> all'utente, non nascosto.

**Meccanica da non sbagliare:** la soglia è una *soglia di esenzione*, non una
franchigia. Superati i 23.000 €, l'addizionale si paga **sull'intero imponibile**,
non solo sulla quota eccedente. Il motore attuale lo fa già correttamente.

**Cosa cambia rispetto al file attuale:** la soglia era `21.000 €`. È
**23.000 €**, e lo era già nel 2024: il valore di partenza era semplicemente
sbagliato, non "vecchio di un anno".

Esiste una proposta del Comune di alzare la soglia a 25.000 € e portare
l'aliquota massima allo 0,9% per i redditi alti: è una **richiesta al governo
centrale**, non una norma in vigore. Non entra nel motore; resta annotata qui.

---

## 8. Mensilità — CCNL

Il CCNL Terziario, Distribuzione e Servizi (Confcommercio) prevede **14
mensilità**: tredicesima a dicembre, quattordicesima a luglio. Stato: 🟡
Secondaria.

**Ma è una scelta di presentazione, non di calcolo.** La RAL è annua: il numero
di mensilità non tocca né i contributi, né l'IRPEF, né il netto annuo. Cambia
solo il divisore del netto mensile. Per questo diventa un **input selezionabile**
(12 / 13 / 14) invece di una costante, con default 14.

---

## 9. Sicilia e Palermo — il territorio di controllo

Servono per il confronto con la CU reale (vedi PIANO.md §6), e nel farlo hanno
rivelato qualcosa di importante sul modello dati.

### Addizionale regionale — Sicilia

| Voce | Valore |
|---|---|
| Aliquota | **1,23%**, **unica** — nessuno scaglione |

Stato: 🟡 Secondaria (Regione Siciliana, portale tributi).

### Addizionale comunale — Palermo

| Voce | 2025 | 2026 |
|---|---|---|
| Aliquota | **1,014%** | **1,404%** |
| Soglia di esenzione | **nessuna** | nessuna |

Stato: **2025** ✅ Primaria — tabella ufficiale Agenzia delle Entrate
*«modulistica 2026»* (anno d'imposta 2025), riga `G273 PALERMO PA 1.014`.
**2026** 🟡 Secondaria — deliberazione del Consiglio comunale, non ancora recepita
nelle tabelle ufficiali.

L'aumento è imposto dal **piano di riequilibrio finanziario** concordato con lo
Stato, dopo il monitoraggio del Ministero dell'Interno. La progressione è
documentata su tre anni d'imposta:

| Anno d'imposta | Aliquota | Tabella AdE |
|---|---|---|
| 2024 | 1,002% | modulistica 2025 |
| 2025 | **1,014%** | modulistica 2026 |
| 2026 | 1,404% | *non ancora pubblicata* |

> ⚠️ Per il confronto con la CU (redditi **2025**) va usata l'aliquota **1,014%**.
> Usare la 1,404% — o la 1,002% — farebbe fallire il test su un motore corretto.

> 🔑 **Trappola scoperta durante la verifica.** Le tabelle dell'Agenzia sono
> indicizzate per **modulistica**, non per anno d'imposta: la tabella
> *«modulistica 2025»* contiene le aliquote dei redditi **2024**. Prendere la
> tabella con l'anno che si sta cercando è l'errore naturale, e produce
> un'aliquota sbagliata di un anno con l'aria di essere una fonte ufficiale.
> È lo stesso genere di errore silenzioso che il prodotto deve prevenire lato
> utente — qui l'abbiamo trovato lato ricerca.

### 🔑 Cosa ci insegna sul modello dati

Confrontando i due territori emerge che **non hanno la stessa forma**:

| | Lombardia / Milano | Sicilia / Palermo |
|---|---|---|
| Addizionale regionale | **a scaglioni** (4 fasce) | **aliquota unica** |
| Addizionale comunale | aliquota unica **con** soglia di esenzione (23.000 €) | aliquota unica **senza** soglia |

Il registro non può quindi essere una semplice tabella `territorio → aliquota`:
deve reggere **due forme di addizionale** (unica / a scaglioni) e la **presenza o
assenza** della soglia di esenzione. Una constatazione che vale la pena portare in
interview: è emersa dalla ricerca, non da un'ipotesi a tavolino — ed è esattamente
il tipo di scoperta che un calcolatore con i numeri cablati non fa mai.

---

## 10. Il set 2025 — solo per la validazione

Serve a confrontare il motore con una Certificazione Unica reale, **non** a fare
proiezioni: chi calcola oggi uno stipendio deve usare il 2026.

Quasi tutto è identico ai valori 2026. Cambiano **quattro** voci, e sono tutte
insidiose perché il numero sbagliato non sembra sbagliato:

| Voce | 2025 | 2026 |
|---|---|---|
| **Seconda aliquota IRPEF** | **35%** | 33% |
| Prima fascia INPS (+1%) | 55.448 € | 56.224 € |
| Massimale contributivo | 120.607 € | 122.295 € |
| **Addizionale comunale Palermo** | **1,014%** | 1,404% |

Fonte per i valori INPS: **circolare INPS n. 26 del 30 gennaio 2025** (minimali e
massimali). Stato 🟡 secondaria.

**Identiche nei due anni**, quindi non fonte di errore: aliquota INPS 9,19%,
detrazioni art. 13, ulteriore detrazione da 65 €, cuneo fiscale, trattamento
integrativo, addizionale regionale Lombardia e Sicilia, addizionale comunale
Milano.

> ⚠️ **L'insidia numero uno della validazione.** Il motore col 33% confrontato con
> una CU dei redditi 2025 produce uno scarto di centinaia di euro su ogni RAL
> sopra i 28.000 €, e sembra un bug del motore. Non lo è: è l'anno sbagliato.
> Prima di dichiarare fallita una verifica, controllare **sempre** che l'anno del
> registro coincida con l'anno del documento.

---

## Riepilogo: cosa era sbagliato nel motore

Su sette gruppi di coefficienti, **sei contenevano almeno un errore**:

| Voce | Nel file | Corretto 2026 | Impatto |
|---|---|---|---|
| Seconda aliquota IRPEF | 35% | **33%** | 🔥 Alto — ogni RAL > 28k |
| Cuneo fiscale | **assente** | somma esente + detrazione 1.000 € | 🔥 Alto — RAL 20k–40k |
| Addizionale regionale | 5 scaglioni, soglie 55k/75k | 4 scaglioni, soglie 15k/28k/50k | Medio |
| Esenzione comunale Milano | 21.000 € | **23.000 €** | Medio — fascia 21k–23k |
| Soglia +1% INPS | 55.008 € | **56.224 €** | Basso — RAL alte |
| Ulteriore detrazione 65 € | da 28.000 € | da **25.000 €** | Basso |
| Trattamento integrativo | solo fino a 15k | + fascia 15k–28k | Medio |
| Aliquota INPS 9,19% | 9,19% | ✅ confermata | — |

Conferma il principio del piano: **nessun coefficiente scritto a memoria**. Il
motore era logicamente corretto e numericamente sbagliato.

---

## Da chiudere prima della consegna

Le tre questioni fiscali bloccanti sono **chiuse** (§3, §4b, §5), così come le
addizionali di Milano e Palermo, ora su fonte primaria. Restano verifiche di
conferma, non ostacoli:

1. 🟡 Confermare 9,19%, prima fascia e massimale sulla **circolare INPS 2026**
2. 🟡 Confermare le percentuali della somma esente (7,1 / 5,3 / 4,8%) leggendo la
   **circolare AdE 4/E del 16 maggio 2025** per esteso
3. 🟡 Confermare gli importi delle **detrazioni art. 13** sul testo dell'articolo
4. 🟡 Verificare le **mensilità dei tre CCNL** diversi dal Commercio (marcati
   `da_verificare` in [dati/coefficienti.json](dati/coefficienti.json))
5. 🟡 A ridosso della consegna: ricontrollare che le comunali **2026** non siano
   cambiate, e se nel frattempo è uscita la tabella AdE modulistica 2027

---

## Fonti consultate

- [Legge di Bilancio 2026 — analisi norme fiscali (Finanza & Fisco)](https://www.finanzaefisco.com/disegno-di-legge-di-bilancio-2026-a-s-1689-una-prima-analisi-delle-norme-fiscali/)
- [IRPEF 2026: scaglioni, aliquote e novità (Informazione Fiscale)](https://www.informazionefiscale.it/IRPEF-scaglioni-aliquote-calcolo)
- [IRPEF 2026: come si calcola (IPSOA)](https://www.ipsoa.it/guide/irpef-calcolo)
- [Contributi INPS 2026: minimali e massimali (EC News)](https://www.ecnews.it/lavoro/news-del-giorno/contributi-inps-2026-stabiliti-minimali-massimali/)
- [Retribuzioni minime e massimali contributivi 2026 (FiscoeTasse)](https://www.fiscoetasse.com/normativa-prassi/13549-retribuzioni-minime-e-massimali-contributivi-2026-i-nuovi-importi.html)
- [Lavoratori dipendenti: limite minimo di retribuzione 2026 (INPS)](https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.02.lavoratori-dipendenti-limite-minimo-di-retribuzione-giornaliera-2026.html)
- [Detrazioni lavoro dipendente 2026 (Informazione Fiscale)](https://www.informazionefiscale.it/detrazioni-lavoro-dipendente-importo-calcolo)
- [Detrazioni per redditi da lavoro dipendente (Fiscomania)](https://fiscomania.com/detrazioni-per-redditi-da-lavoro-dipendente/)
- [Taglio del cuneo fiscale: novità 2026 (Coverflex)](https://www.coverflex.com/it/blog/taglio-cuneo-fiscale)
- [Taglio cuneo fiscale: guida ed esempi Agenzia (FiscoeTasse)](https://www.fiscoetasse.com/new-rassegna-stampa/1178-taglio-cuneo-fiscale-ecco-le-novita-2025.html)
- [Busta paga 2026: la Manovra e il netto dei dipendenti (PMI.it)](https://www.pmi.it/economia/lavoro/484539/manovra-2026-lavoratori-bonus-novita-fisco.html)
- [Trattamento integrativo 2026: requisiti, soglie, calcolo (Fiscomania)](https://fiscomania.com/trattamento-integrativo-come-funziona/)
- [Addizionale Regionale all'IRPEF (Regione Lombardia)](https://www.regione.lombardia.it/bollo-auto-e-tributi-regionali/red-addizionale-regionale-irpef)
- [Addizionale regionale IRPEF — banca dati MEF, Lombardia](https://www1.finanze.gov.it/finanze2/dipartimentopolitichefiscali/fiscalitalocale/addregirpef/addregirpef.php?reg=10)
- [Addizionali IRPEF: vecchie aliquote regionali fino al 2028 (PMI.it)](https://www.pmi.it/economia/mercati/481567/addizionali-irpef-vecchie-aliquote-fino-al-2028.html)
- [Aliquota addizionale comunale IRPEF (Comune di Milano)](https://servizicrm.comune.milano.it/centro-supporto/KA-01934/Aliquota-addizionale-comunale-IRPEF)
- [Esenzioni addizionale comunale IRPEF (Comune di Milano)](https://servizicrm.comune.milano.it/centro-supporto/KA-01737/Esenzioni-addizionale-comunale-IRPEF)
- [Addizionale comunale IRPEF — banca dati MEF, Milano](https://www1.finanze.gov.it/finanze2/dipartimentopolitichefiscali/fiscalitalocale/nuova_addcomirpef/risultato.htm?anno=9999&lista=1&pagina=lombardia.htm&cm=&pr=MI&cc=F205&r=1)
- [Soglia esenzione addizionale IRPEF dal 2026 (MilanoToday)](https://www.milanotoday.it/politica/addizionale-irpef-soglia-esenzione-2026.html)
- [Circolare Agenzia delle Entrate n. 6 del 29 maggio 2025 — riordino detrazioni (PDF ufficiale)](https://www.agenziaentrate.gov.it/portale/documents/20143/8410823/CIRCOLARE_RIORDINO_DETRAZIONI+n.+6+del+29+maggio+2025.pdf/41d27442-ed03-83bb-abd9-b2c236043a5b)
- [Circolare Agenzia delle Entrate n. 4/E del 16 maggio 2025 (Bollettino ADAPT)](https://www.bollettinoadapt.it/la-circolare-dellagenzia-delle-entrate-n-4-e-del-16-maggio-2025/)
- [Art. 13 TUIR — Altre detrazioni (Brocardi)](https://www.brocardi.it/testo-unico-imposte-redditi/titolo-i/capo-i/art13.html)
- [Nuova somma integrativa e ulteriore detrazione, commi 4–9 (Studio Dalmaschio)](https://www.studiodalmaschio.it/2025/01/dnuova-somma-integrativa-e-ulteriore-detrazione-lavoro-dipendente-comma-4-9/)
- [Trattamento integrativo e cuneo fiscale 2025 — cumulabilità (Confcommercio Faenza)](https://www.ascomfaenza.it/lavoro/trattamento-integrativo-e-cuneo-fiscale-anno-2025/)
- [Ulteriore detrazione L. 207/2024 in busta paga (Studio Cesco)](https://studiocesco.it/ulteriore-detrazione-l-207-2024-nella-busta-paga-2025/)
- [Addizionale regionale all'IRPEF (Regione Siciliana — portale tributi)](https://www.regione.sicilia.it/istituzioni/regione/strutture-regionali/assessorato-economia/dipartimento-finanze-credito/portale-tributi/addizionale-irpef)
- [Elenco aliquote addizionale comunale, anno d'imposta 2025 (MEF)](https://www.finanze.gov.it/it/fiscalita/fiscalita-regionale-e-locale/Addizionale-comunale-allIRPEF/aliquote-applicabili/elenco-aliquote-2025/)
- [Addizionale comunale IRPEF — banca dati MEF, Palermo](http://www.globallaboratory.it/pit/addcom/r19/p60/addizionale_comunale_palermo.htm)
- [Aumento addizionale IRPEF Palermo 2026 (PalermoToday)](https://www.palermotoday.it/politica/comune-aumento-irpef-2026.html)
