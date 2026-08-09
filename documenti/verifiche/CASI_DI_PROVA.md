# Casi di prova

I numeri con cui il motore viene messo alla prova, **calcolati a mano prima di
essere scritti nel codice**, e il confronto con un documento emesso da un
sostituto d'imposta.

---

## Perché non basta dire «i test passano»

Un test verifica che il codice faccia quello che chi l'ha scritto si aspettava.
Se l'aspettativa viene dal codice stesso — o dallo stesso registro che il codice
legge — il test è verde e non dimostra niente. È successo davvero, tre volte, ed
è documentato in [ERRORI.md](ERRORI.md) al numero 5.

Da qui due regole, che valgono per tutto questo file:

1. **Ogni valore atteso è stato ricavato applicando la norma a mano**, non
   copiando l'uscita del motore. Sotto ogni riga c'è il conto, così che chiunque
   possa rifarlo con una calcolatrice e contraddirci.
2. **Un caso da solo non basta.** Quattro RAL scelte per attraversare punti
   diversi della legge: sotto la soglia comunale, sopra, dove le detrazioni si
   azzerano, dove i bonus si accendono. Una voce che vale zero in tutti e
   quattro i casi resterebbe senza protezione, e sparirebbe dal registro senza
   che nessun test se ne accorga.

Tutto è **Milano, anno d'imposta 2026, CCNL commercio (14 mensilità)** salvo
dove indicato — il caso fissato dal task.

---

## La catena, una volta sola

Gli stessi otto passi per tutti i casi. Il dettaglio delle norme sta in
[METODOLOGIA.md](../ricerca/METODOLOGIA.md).

```
  RAL
  − contributi INPS                 9,19 % (+1 % oltre 56.224 €)
  = imponibile fiscale
  → IRPEF lorda                     scaglioni 23 / 33 / 43 %
  − detrazione lavoro dipendente    art. 13 TUIR
  − ulteriore detrazione 65 €       art. 13 c. 1.1, fra 25.000 e 35.000
  − detrazione cuneo fiscale        L. 207/2024, fra 20.000 e 40.000
  = IRPEF netta                     (mai sotto zero)
  − addizionale regionale           4 scaglioni Lombardia
  − addizionale comunale            0,8 % oltre 23.000 € di imponibile
  + somma esente cuneo              fino a 20.000 € — si SOMMA, non si sottrae
  + trattamento integrativo         fino a 28.000 €, se c'è capienza
  = NETTO ANNUO
```

Le ultime due voci sono denaro corrisposto **in più**, non sconti d'imposta.
Trattarle come deduzioni è un errore che sbaglia due volte nella stessa
direzione, ed è il numero 2 di [ERRORI.md](ERRORI.md).

---

## Caso 1 — RAL 35.000 € · il caso di riferimento

Il caso centrale: attraversa due scaglioni IRPEF, tutte e tre le detrazioni e
la soglia comunale.

| Voce | Conto | Importo |
|---|---|---:|
| Contributi INPS | 35.000 × 9,19 % | **3.216,50** |
| Imponibile fiscale | 35.000 − 3.216,50 | **31.783,50** |
| IRPEF lorda | 28.000 × 23 % + 3.783,50 × 33 % | **7.688,56** |
| Detrazione lavoro dip. | 1.910 × (50.000 − 31.783,50) / 22.000 | **1.581,52** |
| Ulteriore detrazione 65 € | spetta: 25.000 < 31.783,50 ≤ 35.000 | **65,00** |
| Detrazione cuneo | fascia 20.000–32.000: importo pieno | **1.000,00** |
| IRPEF netta | 7.688,56 − 1.581,52 − 65 − 1.000 | **5.042,03** |
| Addizionale regionale | 15.000×1,23 % + 13.000×1,58 % + 3.783,50×1,72 % | **454,98** |
| Addizionale comunale | 31.783,50 × 0,8 % (oltre la soglia di 23.000) | **254,27** |
| Somma esente cuneo | oltre 20.000: non spetta | 0,00 |
| Trattamento integrativo | oltre 28.000: non spetta | 0,00 |
| **Netto annuo** | 35.000 − 3.216,50 − 5.042,03 − 454,98 − 254,27 | **26.032,22** |
| **Netto mensile** | 26.032,22 / 14 | **1.859,44** |

**Cosa protegge questo caso:** la meccanica degli scaglioni progressivi, la
formula decrescente dell'art. 13 nella terza fascia, e i quattro scaglioni
regionali della Lombardia.

---

## Caso 2 — RAL 25.000 € · sotto la soglia comunale

Scelto apposta perché l'imponibile (22.702,50) resta **sotto i 23.000 €** di
esenzione comunale di Milano. Senza questo caso, cancellare la soglia dal
registro non farebbe fallire nulla.

| Voce | Conto | Importo |
|---|---|---:|
| Contributi INPS | 25.000 × 9,19 % | **2.297,50** |
| Imponibile fiscale | 25.000 − 2.297,50 | **22.702,50** |
| IRPEF lorda | 22.702,50 × 23 % (tutto nel primo scaglione) | **5.221,58** |
| Detrazione lavoro dip. | 1.910 + 1.190 × (28.000 − 22.702,50) / 13.000 | **2.394,93** |
| Ulteriore detrazione 65 € | 22.702,50 < 25.000: **non** spetta | 0,00 |
| Detrazione cuneo | fascia 20.000–32.000 | **1.000,00** |
| IRPEF netta | 5.221,58 − 2.394,93 − 1.000 | **1.826,65** |
| Addizionale regionale | 15.000×1,23 % + 7.702,50×1,58 % | **306,20** |
| Addizionale comunale | imponibile sotto 23.000: **esente** | **0,00** |
| **Netto annuo** | | **20.569,65** |
| **Netto mensile** | / 14 | **1.469,26** |

**Cosa protegge questo caso:** la soglia di esenzione comunale, la seconda
fascia della detrazione art. 13 (quella con la parte fissa più quella
decrescente), e il limite inferiore dei 65 €.

**Il dettaglio che vale la pena guardare.** Fra 25.000 e 35.000 di RAL il lordo
cresce di 10.000 € e il netto di 5.462,57: **il 54,6 %.** Non è una curiosità —
è il numero che manca in quasi tutte le conversazioni su un aumento.

---

## Caso 3 — RAL 16.000 € · dove i bonus si accendono

Le due voci che si **sommano** al netto valgono zero nei casi 1 e 2, quindi
resterebbero senza protezione. Qui esistono entrambe.

| Voce | Conto | Importo |
|---|---|---:|
| Contributi INPS | 16.000 × 9,19 % | **1.470,40** |
| Imponibile fiscale | 16.000 − 1.470,40 | **14.529,60** |
| IRPEF lorda | 14.529,60 × 23 % | **3.341,81** |
| Detrazione lavoro dip. | fascia 1 (imponibile ≤ 15.000): importo pieno | **1.955,00** |
| Detrazione cuneo | sotto 20.000: **non** spetta | 0,00 |
| IRPEF netta | 3.341,81 − 1.955,00 | **1.386,81** |
| Addizionale regionale | tutto nel primo scaglione, 1,23 % | **178,71** |
| Addizionale comunale | sotto la soglia di 23.000 | **0,00** |
| **Somma esente cuneo** | 14.529,60 × 5,3 % (fascia 8.500–15.000) | **+770,07** |
| **Trattamento integrativo** | con capienza: lorda 3.341,81 > detrazione | **+1.200,00** |
| **Netto annuo** | 16.000 − 1.470,40 − 1.386,81 − 178,71 **+ 770,07 + 1.200,00** | **14.934,15** |
| **Netto mensile** | / 14 | **1.066,72** |

**Cosa protegge questo caso:** le percentuali della somma esente, la condizione
di capienza del trattamento integrativo, e — soprattutto — **il segno**. Se
qualcuno trattasse quelle due voci come deduzioni, questo caso fallirebbe di
1.970,07 €.

**Qui vive la sorpresa del progetto.** A questi livelli i bonus superano le
trattenute: fra **9.002 e 11.959 € di RAL il netto è maggiore del lordo.** È
corretto, è previsto da un test che lo *pretende*, ed è documentato in
[ERRORI.md](ERRORI.md) al numero 3 — perché la prima versione dei test lo
dichiarava impossibile.

---

## Caso 4 — RAL 80.000 € · dove tutto si spegne

| Voce | Conto | Importo |
|---|---|---:|
| Contributi INPS | 80.000 × 9,19 % + (80.000 − 56.224) × 1 % | **7.589,76** |
| Imponibile fiscale | 80.000 − 7.589,76 | **72.410,24** |
| IRPEF lorda | 28.000×23 % + 22.000×33 % + 22.410,24×43 % | **23.336,40** |
| Detrazione lavoro dip. | oltre 50.000: **azzerata** | 0,00 |
| Ulteriore detrazione 65 € | oltre 35.000: non spetta | 0,00 |
| Detrazione cuneo | oltre 40.000: non spetta | 0,00 |
| IRPEF netta | = lorda, nessuna detrazione | **23.336,40** |
| Addizionale regionale | tutti e quattro gli scaglioni | **1.156,00** |
| Addizionale comunale | 72.410,24 × 0,8 % | **579,28** |
| **Netto annuo** | | **47.338,56** |
| **Netto mensile** | / 14 | **3.381,33** |

**Cosa protegge questo caso:** il contributo aggiuntivo dell'1 % oltre la prima
fascia pensionabile, il terzo scaglione IRPEF al 43 %, l'azzeramento delle tre
detrazioni e l'ultimo scaglione regionale.

**Il numero che colpisce:** su 80.000 € di RAL restano **47.338,56 €**, cioè il
**59,2 %**. Su 35.000 ne restano il 74,4 %.

---

## Il confronto che conta: una Certificazione Unica reale

I quattro casi qui sopra hanno un limite che va detto: **sono stati calcolati
dalla stessa testa che ha scritto il motore.** Se quella testa ha capito male
una norma, il conto a mano e il codice sbagliano insieme, e il test resta verde.

L'unico modo di rompere quel cerchio è confrontarsi con un conteggio fatto da
qualcun altro. Una Certificazione Unica è emessa da un sostituto d'imposta: se i
numeri coincidono, il motore ha retto contro un calcolo vero, non contro
un'altra approssimazione.

Lo fa [strumenti/confronta_cu.py](../../strumenti/confronta_cu.py). I dati restano
sulla macchina di chi lo lancia: si leggono da `dati_privati/cu.json`, che il
`.gitignore` di quella cartella tiene fuori dal repository. **Chi legge il
repository vede il metodo, mai gli importi di qualcun altro.**

### Le due modalità, e perché sono due

La CU **non contiene una RAL.** Dichiara l'imponibile fiscale, che è già al
netto dei contributi — cioè salta proprio il primo passo della nostra catena.

Una prima versione dello strumento ricostruiva una «RAL equivalente» sommando i
contributi all'imponibile. Era circolare: la riga «imponibile fiscale» tornava
per costruzione, perché era stata usata per costruire l'ingresso. Lo strumento
di verifica si fabbricava la propria risposta — lo stesso difetto trovato nei
test, in un punto diverso del progetto e a poche ore di distanza
([ERRORI.md](ERRORI.md) n. 7).

| Modalità | Quando | Cosa verifica |
|---|---|---|
| **Completo** | la CU dichiara l'imponibile **previdenziale** | tutta la catena, contributi compresi, senza ricostruire niente |
| **Solo fiscale** | c'è solo l'imponibile fiscale | IRPEF, detrazioni, addizionali, bonus. Il passo lordo → imponibile resta **non verificato**, e lo strumento lo dichiara invece di far finta |

### L'esito

Rapporto **breve, in un comune del Sud, redditi 2025** — quindi fuori dal caso
del task, ed è il motivo per cui è stato utile: ha esercitato i periodi
parziali, che a Milano su un anno intero non si vedono.

Al primo confronto **sei voci su nove non tornavano**, due delle quali a zero
contro importi che il sostituto d'imposta aveva riconosciuto: la detrazione da
lavoro dipendente e il trattamento integrativo.

La causa non era un refuso ma **una semplificazione scelta apposta**: valutare
tutte le soglie sul reddito annualizzato, perché sembrava più coerente e più
facile da spiegare. La legge non è uniforme, e la CU lo dimostra **in tutte e
due le direzioni**:

| Voce | Guarda il reddito | Prova nella CU |
|---|---|---|
| Detrazione art. 13, 65 €, trattamento integrativo | **effettivo** | entrambi riconosciuti, ragguagliati ai giorni |
| Taglio del cuneo fiscale | **annualizzato** | somma esente **non erogata**: sull'annualizzato non spetta |

È questo che rende il documento probante. Se la regola fosse uniforme in un
senso, la somma esente sarebbe stata pagata; se lo fosse nell'altro, la
detrazione non ci sarebbe. La CU conferma **entrambe** le letture, che sono
opposte fra loro. Nessun ragionamento a tavolino ci sarebbe arrivato — e 302
test non l'avevano vista, perché scritti da chi aveva scelto la regola
sbagliata.

**Dopo la correzione: sette voci su sette, scarto massimo 0,01 €** — un
centesimo di arrotondamento su una sola riga, zero su tutte le altre. Il
confronto è stato rieseguito dopo la correzione dei 75 € di capienza
(errore 21) e continua a tornare esatto.

L'addizionale comunale ha inoltre confermato **per via indipendente**
l'aliquota di quel comune per il 2025: non quella dell'anno prima, né quella
dell'anno dopo. Un numero preso da una tabella e ritrovato dentro un documento
che nessuno di noi ha compilato.

### Quello che il confronto ha lasciato fuori

I contributi reali erano il **9,457 %** dell'imponibile previdenziale, contro il
9,19 % del nostro modello. La differenza di 0,27 punti sono contributi minori
previsti dal contratto che il prototipo non tratta.

Su una RAL di 35.000 € varrebbe circa **93 € l'anno**. Non è un errore: è una
semplificazione — e adesso ne conosciamo la dimensione invece di ipotizzarla.
Sta in [ASSUNZIONI.md](../prodotto/ASSUNZIONI.md), quantificata.

### Perché qui non ci sono gli importi

Il confronto è stato eseguito **in locale, contro una Certificazione Unica
reale**. In questo repository ci sono lo strumento, il metodo e il modello
vuoto; **non gli importi**.

Non è prudenza formale. Quei numeri — imponibile, giorni, comune, anno — non
contengono nome né codice fiscale, e per un estraneo non identificano nessuno.
Ma per chi già conosce la persona la combinazione la individua senza sforzo, e
permette di ricostruire reddito, durata del rapporto e trattenute. **Uno
strumento che si occupa di retribuzioni non può pubblicare la retribuzione di
qualcuno per dimostrare che funziona.**

Il che è anche una decisione di prodotto, non solo di riservatezza:
**verificabilità senza pubblicazione dei dati del dipendente.** Chi vuole
rifare il confronto lo fa sulla propria CU, con lo stesso strumento:

```bash
cp dati_privati/cu_modello.json dati_privati/cu.json
# riempire cu.json — servono solo gli importi, nessun dato identificativo
python3 strumenti/confronta_cu.py
```

`dati_privati/` ha un `.gitignore` che esclude tutto tranne il modello vuoto e
le istruzioni. Durante il controllo di sicurezza è emerso che quel `.gitignore`
proteggeva la cartella da Git ma **non dal server web**: vedi
[SICUREZZA.md](SICUREZZA.md), punto 1.

---

## Come si rifà tutto

```bash
python3 test_motore.py                      # 413 test, zero dipendenze
python3 strumenti/controllo_sensibilita.py  # 17 guasti deliberati, 17 rilevati
python3 strumenti/confronta_cu.py           # richiede una propria CU in dati_privati/
```

Il secondo è quello che rende credibile il primo: rompe il registro **un
coefficiente alla volta** e verifica che i test se ne accorgano. Una suite che
resta verde mentre i dati sono guasti conta zero, e le prime tre volte che è
stata lanciata è successo esattamente questo.
