# Diario di bordo

Registro di quello che è andato storto, di come ce ne siamo accorti e di cosa è
cambiato di conseguenza.

Non è un changelog: un changelog dice *cosa* è cambiato, questo dice **perché**.
Serve a rendere verificabile una cosa che altrimenti resta un'affermazione — che
i numeri sono stati controllati davvero, e non copiati da un calcolatore online.

Un coefficiente giusto e un coefficiente indovinato sono indistinguibili quando
guardi solo il risultato. Diventano distinguibili solo se puoi mostrare **il
percorso**: da dove viene il numero, cosa c'era prima, e perché è cambiato.

> Il diario si scrive **man mano**, non alla fine. Ricostruito a posteriori
> sarebbe esattamente ciò che vuole smentire.

**Formato:** ogni voce dice cosa è successo, come l'abbiamo scoperto, cosa
sarebbe costato non accorgersene, e cosa è cambiato.

---

## Giorno 1 — 6 agosto 2026

### 1. Punto di partenza: coefficienti scritti a memoria

Il motore esisteva già, con la logica di calcolo corretta e i coefficienti
riempiti "a senso", ognuno marcato `DA VERIFICARE`. Nessuno aveva una fonte.

Il piano prevedeva di verificarli prima di scrivere altro codice. Questa è stata
la decisione che ha salvato il progetto: senza, avremmo costruito interfaccia,
database e API sopra numeri sbagliati, e li avremmo scoperti — se mai — alla
fine.

**Conseguenza:** nessuna riga di codice nuova finché ogni numero non ha una fonte.

---

### 2. La seconda aliquota IRPEF era vecchia di un anno

**Cosa è successo.** Nel file c'era `35%` per lo scaglione 28.000–50.000 €. Per
l'anno d'imposta **2026** l'aliquota è **33%**, ridotta dalla Legge di Bilancio
2026 (L. 199/2025).

**Come l'abbiamo scoperto.** Prima verifica sulle fonti, cercando la norma invece
di fidarci del valore.

**Cosa sarebbe costato.** È l'errore più caro di tutti: colpisce **ogni RAL sopra
i 28.000 €**, cioè quasi tutti i casi realistici, e sbaglia per difetto di
centinaia di euro l'anno. Il netto sarebbe sembrato perfettamente plausibile.

**Cosa è cambiato.** Aliquota corretta, e soprattutto la consapevolezza che il
`730/2026` applica ancora il 35% — perché riguarda i redditi 2025. Due numeri
entrambi "veri", per anni diversi: è la trappola che ritorna al punto 11.

---

### 3. Mancava del tutto il taglio del cuneo fiscale

**Cosa è successo.** Il motore non conteneva nessuna traccia delle misure
introdotte dalla L. 207/2024: né la somma esente per i redditi fino a 20.000 €,
né l'ulteriore detrazione fino a 1.000 € per la fascia 20.000–40.000 €.

**Perché era sfuggito.** Fino al 2024 il taglio del cuneo era uno **sgravio
contributivo** — si vedeva nei contributi. Dal 2025 è diventato due misure
**fiscali** di natura diversa. Chi ricordava "il taglio del cuneo" come una
riduzione dei contributi non aveva niente da cercare nel posto giusto.

**Cosa sarebbe costato.** Fino a 1.000 € di netto sulla fascia di reddito più
comune per un impiegato. Su una RAL di 30.000 € è l'errore singolo più grosso.

**Cosa è cambiato.** Due voci nuove nel motore, e la regola che una misura
cambiata di *natura* è più pericolosa di una cambiata di *valore*: il valore lo
verifichi, la natura nemmeno la cerchi.

---

### 4. Gli scaglioni regionali della Lombardia erano inventati

**Cosa è successo.** Il file aveva **cinque** scaglioni con soglie a 55.000 e
75.000 €. La Lombardia ne ha **quattro**, con le soglie allineate a quelle IRPEF
(15.000 / 28.000 / 50.000), e l'ultima aliquota è 1,73%, non 1,74%.

**Cosa sarebbe costato.** Poche decine di euro, ma su una voce che l'utente vede
in chiaro nella tabella delle trattenute — quindi un errore piccolo e visibile,
il peggior tipo per la credibilità.

---

### 5. La soglia di esenzione di Milano non era "vecchia": era falsa

**Cosa è successo.** Il file diceva `21.000 €`. Il valore corretto è
**23.000 €** — e lo era anche l'anno prima.

**Perché è diverso dagli altri errori.** Gli altri erano valori giusti per un
anno sbagliato. Questo non corrisponde a nessun anno: era semplicemente inventato.

**Conseguenza sul metodo.** Ha tolto ogni tentazione di "aggiornare" i
coefficienti esistenti. Ogni valore è stato ripreso da zero, non corretto.

---

### 6. La soglia del +1% contributivo cambia ogni anno

**Cosa è successo.** Nel file: `55.008 €`. I valori reali sono **55.448 €** per
il 2025 e **56.224 €** per il 2026 — la prima fascia di retribuzione pensionabile
viene rivalutata ogni anno su indici ISTAT.

**Cosa è cambiato.** È la conferma più netta che i coefficienti non possono stare
nel codice: non è una norma che cambia ogni tanto, è un numero che cambia **per
costruzione** ogni dodici mesi.

---

### 7. Una detrazione citata con l'articolo sbagliato

**Cosa è successo.** L'ulteriore detrazione da 65 € era attribuita all'**art. 13
comma 1-*bis*** TUIR, con fascia 28.000–35.000 €.

Il comma 1-*bis* è **abrogato** dal D.L. 3/2020. La norma vigente è il **comma
1.1**, e la fascia è **25.000–35.000 €**.

**Cosa sarebbe costato.** 65 € su tutti i redditi tra 25.000 e 28.000 €. Poco in
denaro, molto in credibilità: citare un comma abrogato in un documento che si
vanta di avere le fonti è peggio che non citare nulla.

**Regola imparata.** La fonte va verificata insieme al valore. Un numero giusto
con una citazione sbagliata resta un numero non verificato.

---

### 8. Il trattamento integrativo si fermava troppo presto

**Cosa è successo.** Implementato solo fino a 15.000 € di reddito. In realtà
prosegue in forma ridotta fino a **28.000 €**, pari alla differenza tra detrazioni
spettanti e IRPEF lorda, con tetto di 1.200 €.

La condizione di capienza, invece, era già scritta correttamente.

---

### 9. La domanda che nessuna fonte rispondeva direttamente

**Cosa è successo.** Somma esente del cuneo fiscale e trattamento integrativo:
**si cumulano** per un reddito sotto i 15.000 €, o l'una sostituisce l'altro?

Le due misure si somigliano moltissimo — nessuna concorre a formare il reddito,
entrambe incidono solo sul netto in busta — ed è proprio per questo che è facile
scambiarle per la stessa cosa e contarne una sola.

Nessuna delle fonti divulgative le trattava insieme: ognuna spiegava la propria
misura come se l'altra non esistesse.

**Come si è chiusa.** Cercando la **circolare dell'Agenzia delle Entrate n. 4/E
del 16 maggio 2025**, cioè il documento che i sostituti d'imposta usano davvero.
**Si cumulano:** la L. 207/2024 non ha abrogato il trattamento integrativo.

**Cosa sarebbe costato.** 1.200 € su tutta la fascia bassa di reddito.

**Regola imparata.** Quando le fonti divulgative tacciono su un'interazione, la
risposta sta nei documenti operativi — circolari e istruzioni — non negli articoli
riassuntivi.

---

### 10. Il sito del Comune di Milano si è rifiutato di rispondere

**Cosa è successo.** Le pagine ufficiali del Comune di Milano rispondono `403`
alle richieste automatiche. Prima conclusione: valori da rileggere a mano prima
della consegna, quindi fonte secondaria.

**Come si è risolta.** Cercando una fonte *migliore* invece di una scorciatoia:
l'**Agenzia delle Entrate** pubblica la tabella di tutte le addizionali comunali
italiane, comune per comune. Fonte più autorevole del sito comunale, e completa.

Il PDF però non era leggibile con gli strumenti automatici — 196 pagine di
tabella compressa. È stato scaricato ed estratto in locale, cercando le righe dei
due comuni:

```
F205 MILANO   MI  0.8    23000
G273 PALERMO  PA  1.014
```

**Cosa è cambiato.** Milano e Palermo sono passate da fonte secondaria a
**primaria**. Un ostacolo tecnico ha prodotto una fonte migliore di quella di
partenza.

---

### 11. La trappola peggiore: le tabelle non sono indicizzate per anno d'imposta

**Cosa è successo.** Estraendo Palermo dalla tabella «modulistica 2025» è uscito
**1,002%**. Ma le fonti giornalistiche dicevano **1,014%** per il 2025. Una delle
due doveva essere sbagliata.

**Come l'abbiamo scoperto.** Nessuna delle due era sbagliata. Le tabelle
dell'Agenzia sono indicizzate per **modulistica**, non per anno d'imposta:

| Tabella | Anno d'imposta |
|---|---|
| modulistica 2025 | redditi **2024** |
| modulistica 2026 | redditi **2025** |

Scaricata la tabella successiva, Palermo risulta **1,014%**. Entrambi i valori
erano corretti, per anni diversi.

**Cosa sarebbe costato.** Il confronto con la Certificazione Unica sarebbe
fallito, e avremmo cercato il bug nel motore — che sarebbe stato giusto. Peggio:
avremmo potuto "aggiustare" il motore per far tornare i conti, rompendolo per
davvero.

**Perché è la voce più importante del diario.** È lo stesso identico meccanismo
del difetto che il prodotto deve prevenire lato utente: un dato **plausibile,
ufficiale e sbagliato**, che non dà nessun segnale di esserlo. L'abbiamo trovato
dal lato della ricerca invece che dal lato dell'interfaccia, ma la forma è la
stessa — ed è per questo che l'interfaccia avvisa invece di limitarsi a calcolare.

**Cosa è cambiato.** Nel registro, l'anno d'imposta è dichiarato accanto a ogni
aliquota comunale, insieme alla tabella da cui è stata letta.

---

### 12. Due territori, due forme diverse

**Cosa è successo.** Cercando Palermo per la validazione, è emerso che i due
territori non si comportano allo stesso modo:

|  | Milano / Lombardia | Palermo / Sicilia |
|---|---|---|
| Addizionale regionale | **a scaglioni** (4 fasce) | **aliquota unica** |
| Addizionale comunale | 0,8% **con** esenzione a 23.000 € | 1,014% **senza** esenzione |

**Cosa è cambiato.** Il registro non può essere una tabella
`territorio → aliquota`: deve reggere due forme di addizionale e la presenza
*opzionale* della soglia. Se avessimo modellato i dati guardando solo Milano —
cioè solo l'esempio del task — il modello sarebbe stato sbagliato e ce ne saremmo
accorti solo aggiungendo il secondo comune.

**Regola imparata.** Un solo caso d'esempio non basta a definire una struttura
dati. Il secondo caso serve a scoprire cosa era assunto senza saperlo.

---

### 13. Gli avvisi devono seguire i dati, non il codice

**Cosa è successo.** Conseguenza diretta del punto 12. La soglia di esenzione
esiste a Milano e non a Palermo: un avviso del tipo *"sei appena sopra la soglia
di esenzione"* cablato nel codice comparirebbe anche a un utente palermitano, per
cui quella soglia non esiste.

**Cosa è cambiato.** Gli avvisi sono generati dalla configurazione del territorio,
non scritti nell'interfaccia. Un avviso falso è lo stesso difetto di un numero
falso: informazione plausibile e sbagliata.

---

### 14. Un test che afferma una cosa falsa

**Cosa è successo.** Fra i test esistenti ce n'è uno che verifica che *"il netto
annuo cresce sempre al crescere della RAL"*. Sembra ovvio. È **falso**.

L'esenzione comunale di Milano è una **soglia**, non una franchigia: sotto i
23.000 € di imponibile non si paga nulla, sopra si paga lo 0,8% **sull'intero
imponibile**. Un centesimo in più di imponibile costa **circa 184 €**.

Il netto quindi **scende** attraversando quel punto — che in termini di RAL cade
intorno ai **25.330 €**.

**Cosa è cambiato.** Il test va riscritto: monotòno **ovunque tranne** nei gradini
previsti dalla configurazione, e i gradini devono cadere **esattamente** dove il
registro dice. Così una discontinuità imprevista diventa un test rosso invece di
passare inosservata.

**E una conseguenza sull'algoritmo.** La modalità inversa netto → lordo funziona
per bisezione, che presuppone una funzione crescente. Va scritta sapendo che in
quel punto la funzione salta, altrimenti su certi valori di netto restituisce una
RAL sbagliata o non converge.

---

### 15. La Certificazione Unica non era confrontabile come pensavamo

**Cosa è successo.** Il piano prevedeva di validare il motore contro una CU reale,
molto più probante di un confronto con un altro calcolatore online. Poi è emerso
che la CU disponibile copre un **periodo di lavoro parziale**, non un anno intero.

**Perché è un problema.** Detrazioni art. 13, somma esente e trattamento
integrativo sono per legge **rapportate ai giorni di lavoro nell'anno**. Una
proiezione a 365 giorni confrontata con una CU di pochi mesi darebbe uno scarto
enorme — e sarebbe colpa del confronto, non del motore.

**Cosa è cambiato.** I giorni di detrazione sono diventati un parametro, con
default 365. Il confronto torna possibile per intero, e il prodotto guadagna un
caso d'uso che per un HR è ordinario: l'**assunzione a metà anno**.

Anche senza quel parametro, la CU resta utile: valida contributi, imponibile e la
macchina degli scaglioni, cioè la parte dove gli errori sono silenziosi.

---

### 16. Un difetto osservato su uno strumento reale

**Cosa è successo.** Usando un calcolatore esistente, da utente non esperta, è
stata inserita una **RAL sbagliata per un dipendente**: non era chiaro che il
campo chiedesse il **lordo**. Nessun avviso ha intercettato l'errore.

**Perché conta più di qualunque scelta tecnica.** È l'unico dato di questo
progetto che non è un'ipotesi: è un fallimento osservato su un utente reale.

Ed è il difetto peggiore possibile per uno strumento del genere, perché è
**silenzioso** — il risultato resta plausibile — **si scopre tardi**, tipicamente
a offerta già partita, e colpisce **solo chi non è del mestiere**, cioè proprio
chi lo strumento dovrebbe aiutare.

**Cosa è cambiato.** Quasi tutta l'interfaccia discende da qui: etichette
esplicite, il risultato che ripete l'input, il controllo di plausibilità, l'aiuto
in linea su ogni voce, i due livelli di esperienza, e la modalità inversa
netto → lordo — che non si limita ad avvisare della confusione, la rende
impossibile.

---

### 17. Quanto varia il territorio: misurato, non stimato

**Cosa è successo.** Dopo il punto 12 restava una domanda: Milano e Palermo sono
due casi particolari, o la varietà è la norma? Invece di rispondere a intuito,
abbiamo analizzato **l'intera tabella dell'Agenzia delle Entrate** — tutti i
comuni italiani, anno d'imposta 2025.

**Il risultato su 7.792 comuni:**

| | |
|---|---|
| Aliquota unica | **6.645** comuni (85,3%) |
| A scaglioni | **1.147** comuni (14,7%) |
| Con soglia di esenzione | **2.773** comuni (35,6%) |
| Senza alcuna soglia | **5.019** comuni (64,4%) |
| Addizionale pari a zero | **994** comuni (12,8%) |

L'aliquota va da **0%** a **1,2%**, e le soglie di esenzione hanno **116 valori
distinti**, da 700 € a 216.000 €.

Otto capoluoghi, per capire quanto poco si somiglino:

| Comune | Aliquota | Esenzione |
|---|---|---|
| Milano | 0,8% | fino a 23.000 € |
| Roma | 0,9% | fino a 14.000 € |
| **Torino** | **0,8 / 0,8 / 1,1 / 1,2%** a scaglioni | fino a 11.790 € |
| Napoli | 1,0% | fino a 12.000 € |
| **Firenze** | **0,2%** | fino a 25.000 € |
| Bologna | 0,8% | fino a 15.000 € |
| Palermo | 1,014% | **nessuna** |
| Pescara | 0,8% | fino a 10.000 € |

Firenze applica un'aliquota **quattro volte più bassa** di Milano e in più esente
fino a 25.000 €; Palermo un'aliquota più alta e nessuna esenzione. Torino usa
quattro scaglioni dove quasi tutti usano un numero solo.

**Sul lato regionale** la forbice è ancora più larga: si va dallo **0,70%** del
Friuli-Venezia Giulia al **3,33%** di Lazio e Campania, che sono obbligate
all'aliquota massima perché in piano di rientro sanitario. Alcune regioni usano
scaglioni, altre un'aliquota unica.

**Cosa dimostra.** Che il territorio non è un dettaglio di configurazione ma una
variabile di primo livello, e che il modello dati costruito su Milano soltanto
sarebbe stato sbagliato per **il 64% dei comuni italiani** — quelli senza soglia
di esenzione — e incapace di rappresentare il 15% che usa gli scaglioni.

**Riproducibile, non raccontato.** L'analisi sta in
[strumenti/analisi_addizionali.py](strumenti/analisi_addizionali.py): si rilancia
sulla tabella ufficiale e restituisce le stesse cifre. Una verifica che si può
solo leggere è un'affermazione; una che si può rieseguire è una prova.

---

### 18. Perché Milano — e perché non è una scelta neutra

**La decisione.** Milano/Lombardia resta il territorio predefinito. Il task lo
propone come esempio, ma i dati del punto 17 dicono che è anche una buona scelta
tecnica — e non per caso:

1. **0,80% è l'aliquota più diffusa d'Italia**: la applicano **4.145 comuni**, il
   **53,2%** del totale. Non è un caso particolare, è il caso modale.
2. **Milano ha una soglia di esenzione**, quindi il percorso di codice più
   complesso — quello con il gradino — viene esercitato dal caso predefinito
   invece di restare non testato. Se avessimo scelto Palermo come default,
   la logica della soglia non si sarebbe mai attivata nella vista principale.
3. È l'esempio esplicito del task, quindi il confronto con qualunque verifica
   fatta da chi valuta parte dallo stesso presupposto.

**Ma va detto chiaramente cosa Milano *non* rappresenta.** È un default
ragionevole, non un risultato generalizzabile. Sul lato regionale la Lombardia
sta **vicino al minimo nazionale**: un netto calcolato per Milano è all'estremo
favorevole della forbice.

A parità di imponibile di 30.000 €, l'addizionale regionale in Lombardia si
calcola a scaglioni:

```
15.000 × 1,23%  =  184,50
13.000 × 1,58%  =  205,40
 2.000 × 1,72%  =   34,40
                  ────────
                   424,30 €
```

La stessa persona, con lo stesso lordo, in una regione al 3,33% pagherebbe
**999 €**: quasi **575 € l'anno** di differenza, senza che cambi nulla nel
contratto o nello stipendio. Sommando anche le differenze comunali si superano
i **600 €**.

**Conseguenza sul prodotto.** Questa è la ragione per cui il territorio è sempre
visibile e mai preselezionato in silenzio (vedi PIANO.md §5). Non è pignoleria:
è la voce che, da sola, può spostare il netto di oltre 600 € l'anno senza dare
alcun segnale.

**Conseguenza sulla documentazione.** Nelle ASSUNZIONI va scritto per esteso che
il default è Milano, che Milano è al margine favorevole della distribuzione
regionale, e che il risultato non va letto come "il netto italiano".

---

### 19. Le addizionali si pagano l'anno dopo

**Cosa è successo.** Cercando le aliquote regionali è emerso un dettaglio di
tempistica: per i dipendenti le addizionali regionale e comunale **non si pagano
nell'anno in cui il reddito è prodotto**. Vengono trattenute in busta paga in
**undici rate mensili**, da gennaio a novembre dell'anno *successivo*. Le
addizionali sui redditi 2026 si pagano nel 2027.

**Perché conta.** Il nostro modello le sottrae nello stesso anno del reddito.
Per una **proiezione annuale** è la scelta giusta — la domanda è *"quanto costa
in un anno tipo questa RAL"*, non *"quanto esce dalla busta di marzo"* — ma
significa che il netto mensile che mostriamo **non coincide** con nessuna busta
paga reale al centesimo.

**Cosa è cambiato.** Nulla nel calcolo. Una riga in più nelle ASSUNZIONI, perché
è esattamente il tipo di scarto che un esperto nota subito e su cui vale la pena
farsi trovare preparati: *lo sappiamo, ed ecco perché lo facciamo così*.

---

### 20. La somma esente era collocata nel punto sbagliato della catena

**Cosa è successo.** Scrivendo il motore è emerso che il diagramma del piano
metteva la **somma esente del cuneo fiscale** come una sottrazione
dall'imponibile, prima dell'IRPEF.

È sbagliato. La norma dice che è *"una somma che non concorre a formare il
reddito"*: non riduce la base imponibile, è **denaro corrisposto in più** che si
somma al netto, esattamente come il trattamento integrativo.

**Perché era facile sbagliare.** Le due misure del cuneo fiscale hanno nomi
simili ma natura opposta:

| Misura | Redditi | Natura |
|---|---|---|
| Somma esente | ≤ 20.000 € | si **aggiunge al netto** |
| Ulteriore detrazione | 20.000–40.000 € | **abbatte l'IRPEF** |

**Cosa sarebbe costato.** Trattarla come deduzione dell'imponibile sbaglia due
volte nella stessa direzione: abbassa l'IRPEF che non doveva abbassare, e non
aggiunge al netto quello che doveva aggiungere. Su un reddito di 18.000 € vale
diverse centinaia di euro.

**Cosa è cambiato.** Diagramma corretto nel piano, e un avvertimento in testa a
`calcolo.py`, perché è il genere di errore che si ripresenta a chi rimetterà mano
al codice fra un anno.

---

### 21. Il minimo di 690 € era codice morto, finché non abbiamo aggiunto i giorni

**Cosa è successo.** Il motore originale conteneva
`max(detrazione_piena, 690)`, che non poteva mai attivarsi: la detrazione piena
di fascia 1 è 1.955 €, sempre maggiore di 690.

Guardando la norma, il minimo di 690 € si applica **dopo** il rapporto ai giorni
di lavoro. Con l'anno pieno è irrilevante; con un periodo breve diventa
determinante — per 30 giorni la detrazione sarebbe 1.955 × 30/365 = 161 €, e la
norma la riporta a 690 €.

**Cosa è cambiato.** Quel `max` è tornato vivo, ed è ora nel posto giusto: dopo
la proporzione, non prima.

**Perché vale la pena annotarlo.** Un parametro nuovo — i giorni — ha reso
significativa una riga che sembrava inutile. Il codice morto non era morto: era
in attesa del caso d'uso che lo riguardava.

---

### 22. Il gradino di Milano, misurato

**Cosa è successo.** Il gradino previsto al punto 14 è stato verificato sul
motore funzionante, calcolando RAL vicinissime fra loro:

| RAL | Imponibile | Add. comunale | Netto annuo | Variazione |
|---|---|---|---|---|
| 25.327 € | 22.999,45 € | 0,00 € | 20.766,43 € | +0,60 € |
| **25.328 €** | **23.000,36 €** | **184,00 €** | **20.583,03 €** | **−183,40 €** |
| 25.329 € | 23.001,26 € | 184,01 € | 20.583,62 € | +0,59 € |

**Un euro di lordo in più costa 183,40 € di netto.** Non è un difetto del motore:
è la soglia di esenzione milanese che funziona come previsto.

**Cosa è cambiato.** Da ipotesi documentata a fatto misurato. Diventa un test —
il gradino deve stare esattamente lì — e un avviso in interfaccia, perché è
esattamente il tipo di sorpresa che un HR non vuole scoprire dopo aver fatto
un'offerta.

---

### 23. Il messaggio anti-errore aveva un errore

**Cosa è successo.** L'avviso che intercetta chi confonde stipendio mensile e
RAL annua usciva così:

```
2.500 € sembra un importo mensile: la RAL è ANNUA e lorda.
Se intendevi 2.500 € al mese. la RAL è circa 30.000 €.
                            ^ punto al posto della virgola
```

Una conversione ai separatori italiani applicata all'intera frase invece che ai
soli numeri: aveva trasformato in punti anche le virgole della punteggiatura.
Lo stesso difetto era presente nelle etichette delle addizionali.

**Perché finisce nel diario nonostante sia banale.** Perché stava proprio nella
funzione che esiste per prevenire gli errori dell'utente, ed è passata inosservata
alla lettura: si vedeva solo eseguendola. È un promemoria che la revisione a
occhio non sostituisce l'esecuzione — vale per la punteggiatura come per le
aliquote.

**Cosa è cambiato.** Due funzioni dedicate alla formattazione di euro e
percentuali, usate ovunque, invece di conversioni improvvisate caso per caso.

---

### 24. Il 2026 è meno verificato del 2025, e il prodotto lo dirà

**Cosa è successo.** Il registro sa contare le proprie fonti. Interrogandolo:

| Configurazione | Fonti primarie | Secondarie |
|---|---|---|
| Milano, anno 2026 | 2 | 8 |
| Palermo, anno 2025 | 4 | 5 |

L'anno **passato** è meglio documentato dell'anno **corrente**, ed è inevitabile:
le tabelle ufficiali consolidate escono dopo. Le comunali 2026 saranno confermate
solo dalla modulistica 2027.

**Cosa è cambiato.** Invece di nasconderlo, la modalità esperto lo mostra: accanto
a ogni coefficiente compare lo stato della fonte. Un calcolatore che dichiara
quanto è sicuro di sé è più utile di uno che finge una certezza uniforme —
soprattutto in un dominio dove i numeri arrivano con mesi di ritardo sulle norme.

---

### 25. Le discontinuità erano sei, non una — e poi sette

**Cosa è successo.** Prima di scrivere i test ho scandito il netto da 1 a
200.000 € di RAL, un euro alla volta, cercando ogni punto in cui salta. Mi
aspettavo il solo gradino di Milano. Ne sono usciti **sei**.

Sono **sette**. La sesta e la settima cadevano nello stesso punto, e per
settimane sono sembrate una sola — vedi la voce 41.

| Imponibile | RAL | Variazione del netto | Causa |
|---|---|---|---|
| 8.174 € | 9.002 | **+1.200,96** | scatta la capienza del trattamento integrativo |
| 8.500 € | 9.361 | **−152,22** | la somma esente scende dal 7,1% al 5,3% |
| 15.000 € | 16.519 | **−129,35** | finiscono detrazione di fascia 1 e trattamento pieno |
| 20.000 € | 22.025 | +40,60 | la somma esente lascia il posto alla detrazione del cuneo |
| 23.000 € | 25.328 | **−183,40** | soglia di esenzione comunale — *solo a Milano* |
| 25.000 € | 27.531 | +65,59 | inizia l'ulteriore detrazione di 65 € |
| 35.000 € | 38.543 | **−64,61** | finisce l'ulteriore detrazione di 65 € |

**Quattro di questi salti sono in discesa**: guadagnare di più fa guadagnare di
meno. A Palermo sono sei, non sette: manca quello comunale, perché lì la
soglia non esiste. La differenza fra i due elenchi è esattamente il dato che
distingue i due territori — una conferma indipendente che il modello li tratta
come diversi davvero, non solo sulla carta.

**Cosa è cambiato.** Il test non si limita a tollerare i salti: pretende che
siano **esattamente** questi, con il segno giusto, e che le loro posizioni
coincidano con le soglie dichiarate nel registro. Una discontinuità in più fa
fallire la suite.

---

### 26. Per i redditi bassi il netto supera il lordo

**Cosa è successo.** Cercando le invarianti ne ho scritta una che sembrava
ovvia — *il netto non può superare il lordo* — e il motore l'ha smentita.

Fra **9.002 € e 11.959 €** di RAL, il netto è **maggiore** della retribuzione
lorda. A RAL 10.000 il netto è 10.516,97 €.

**Perché è corretto.** Somma esente e trattamento integrativo non sono sconti
d'imposta: sono **denaro corrisposto in più** dal datore, che lo recupera come
credito. A RAL 10.000 valgono insieme 1.681,29 €, contro 1.164,33 € di
trattenute totali. Le somme aggiunte superano le trattenute, e il netto supera
il lordo.

**Cosa sarebbe costato.** Avrei scritto un test sbagliato e, vedendolo fallire,
avrei "corretto" un motore giusto. È il modo più insidioso di introdurre un bug:
partendo da un'intuizione ragionevole e sbagliata.

**Cosa è cambiato.** Il fenomeno è ora un test che lo **pretende**, con un
commento che spiega perché non va "aggiustato". E in interfaccia va spiegato,
perché un HR che lo vede per la prima volta penserà a un errore.

---

### 27. Anche la legge ha i suoi gradini

**Cosa è successo.** Il salto in discesa a 15.000 € nasce da una discontinuità
**della norma stessa**, non del nostro codice:

| Reddito | Detrazione art. 13 |
|---|---|
| 14.999,99 € | 1.955,00 € |
| 15.000,00 € | 1.955,00 € |
| **15.000,01 €** | **3.100,00 €** |

La formula della seconda fascia — `1.910 + 1.190 × (28.000 − R) / 13.000` —
calcolata sul confine dà 3.100 €, non 1.955 €. Le due fasce non si raccordano.

Il salto della detrazione (+1.145) compensa quasi del tutto la perdita del
trattamento integrativo (−1.200), e il residuo −129 € è ciò che resta.

**Perché lo annoto.** Chi rileggerà quel numero penserà a un errore di
arrotondamento. Non lo è: è il testo dell'articolo 13.

---

### 28. I test passavano tutti, ma tre non servivano a niente

**Cosa è successo.** La suite contava 208 test verdi. Prima di dichiararla
buona ho fatto la domanda che conta: **se un coefficiente fosse sbagliato, questi
test se ne accorgerebbero?**

Ho guastato il registro un valore alla volta — quattordici guasti — rilanciando
la suite ogni volta. Tre guasti **non hanno fatto fallire nulla**:

- rimuovere la soglia di esenzione di Milano
- azzerare le percentuali della somma esente
- inventare due scaglioni regionali in più

**La causa era strutturale, non una svista.** I test ricavavano le soglie attese
**dal registro stesso**. Cambiando il dato si spostavano insieme l'aspettativa e
il comportamento, e il confronto tornava. Un test che si adatta a ciò che
dovrebbe controllare non controlla niente.

Gli altri due buchi erano più banali ma della stessa famiglia: i casi di
riferimento erano entrambi a reddito medio, quindi somma esente e scaglioni
regionali superiori non venivano mai attraversati.

**Cosa è cambiato.** Tre correzioni:

1. Una sezione di **ancoraggi**: i valori confermati su fonte primaria sono
   scritti a mano nel test, non letti dal registro. È l'unico punto della suite
   che non può derivare da ciò che verifica.
2. Due casi di riferimento in più, calcolati a mano: **RAL 16.000** (reddito
   basso, esercita somma esente e trattamento integrativo) e **RAL 80.000**
   (esercita il +1% contributivo, il terzo scaglione IRPEF e l'ultimo scaglione
   regionale).
3. Il controllo di sensibilità è diventato uno strumento del progetto:
   [strumenti/controllo_sensibilita.py](strumenti/controllo_sensibilita.py).

Ora i quattordici guasti su quattordici vengono rilevati, e la suite è passata
da 208 a **256 test**.

**La lezione, che vale oltre questo progetto.** Un test verde dice solo che i
test non hanno trovato nulla. Può voler dire che il codice è giusto, o che i
test guardano nel posto sbagliato. L'unico modo per distinguere i due casi è
rompere il codice apposta e controllare che i test se ne accorgano.

---

### 29. La bisezione ingenua: provata prima di scartarla

**Cosa è successo.** Sapevo già che il netto non è crescente, quindi che la
bisezione non poteva funzionare. Ho voluto comunque scriverla e **misurare**
come si rompe, invece di scartarla per ragionamento.

Prova: per ogni RAL da 6.000 a 60.000 calcolo il netto, poi torno indietro. Se
l'inverso è corretto, deve tornare la RAL di partenza.

| | |
|---|---|
| RAL provate | 5.400 |
| Ritorni sbagliati di oltre 1 € | **67** (1,2%) |
| Errore massimo | **309,41 €** |

I 67 casi non sono sparsi: cadono in **tre zone**, attorno a RAL 16.500, 25.300
e 38.500. Sono esattamente i tre gradini in discesa della voce 25, visti
dall'altro lato.

**Perché valeva la pena provarla.** L'1,2% è la percentuale che rende un difetto
pericoloso: abbastanza raro da non emergere provando qualche valore a mano,
abbastanza frequente da colpire prima o poi un caso vero. E l'errore non è di
centesimi: **309 € sulla RAL da mettere in un'offerta**.

---

### 30. Due modi di rompersi, opposti fra loro

**Cosa è successo.** Indagando i 67 fallimenti è emerso che i salti in salita e
quelli in discesa producono guasti di natura diversa, e vanno trattati
diversamente.

**I salti in salita creano netti impossibili.** Quando la curva scavalca un
intervallo, quei valori non li produce nessuna RAL:

| Fra RAL | e RAL | il netto salta da | a | ampiezza |
|---|---|---|---|---|
| 9.001 | 9.002 | 8.653,61 € | 9.854,57 € | **1.200,96 €** |
| 22.024 | 22.025 | 18.738,80 € | 18.779,41 € | 40,60 € |
| 27.530 | 27.531 | 21.892,11 € | 21.957,71 € | 65,59 € |

Nessuno può guadagnare **fra 8.653 e 9.854 euro netti l'anno**: è un buco largo
milleduecento euro. La bisezione cieca però risponde lo stesso — restituisce una RAL che
vale tutt'altro, senza segnalare nulla.

**I salti in discesa creano netti ambigui.** Lo stesso importo si ottiene con
più RAL diverse: 20.600 € netti si ottengono sia con **RAL 25.050,43** sia con
**RAL 25.356,55**. Rispondere con una sola delle due, in silenzio, è un errore
travestito da risposta.

**Cosa è cambiato.** Due comportamenti distinti: se il netto è impossibile lo si
dichiara, indicando i due valori raggiungibili più vicini; se è ambiguo si
restituiscono **tutte** le soluzioni, proponendo la più bassa — la più
conveniente per chi fa l'offerta — e dicendo che ce ne sono altre.

---

### 31. La soluzione era già in casa: sappiamo dove sono i gradini

**Cosa è successo.** Il calcolo inverso non ha richiesto un algoritmo più
sofisticato, ma di **usare quello che i test avevano già stabilito**: le
posizioni esatte delle discontinuità, ricavabili dal registro.

Fra un gradino e il successivo la funzione cresce davvero. Quindi: si divide
l'intervallo delle RAL nei segmenti separati dai gradini, e in ciascuno la
bisezione è legittima. Sei segmenti a Milano, cinque a Palermo.

**Un terzo problema, scoperto solo eseguendo.** La prima versione restituiva
*tre* soluzioni per 20.600 € di netto. La terza era fasulla: al punto di salto
la bisezione converge su una RAL che vale 20.766, non 20.600. Ogni candidato va
**verificato** ricalcolando il netto, non solo trovato.

**Il risultato:**

| | Bisezione ingenua | Per segmenti con verifica |
|---|---|---|
| Andate e ritorni sbagliati su 5.400 | **67** | **0** |
| Netti impossibili | risposta silenziosamente falsa | dichiarati, con i valori vicini |
| Netti ambigui | una sola risposta arbitraria | tutte le soluzioni |

**Una verifica incrociata che vale doppio.** I punti di salto ora si ricavano in
due modi indipendenti: i test li trovano **scandendo** la curva, il calcolo
inverso li deriva **dal registro**. Un test confronta i due elenchi. Se un giorno
divergono, una delle due strade ha un errore — e lo sapremo subito, invece di
scoprirlo da un risultato sbagliato.

**Quello che il calcolo inverso dice, in concreto.** Per garantire **2.000 € netti
al mese** su quattordici mensilità serve:

| | 2025 | 2026 |
|---|---|---|
| Milano | 40.549,93 € | **40.101,12 €** |
| Palermo | 40.523,62 € | 40.440,82 € |

Due letture utili in sede di offerta: il taglio IRPEF del 2026 permette di
promettere lo stesso netto con **450 € di RAL in meno**; e a Palermo, per lo
stesso netto, serve una RAL **340 € più alta** che a Milano, per via delle
addizionali. È l'informazione che il calcolo diretto contiene ma non dice, perché
nessuno ragiona partendo dal lordo.

---

### 32. Lo strumento di confronto, provato prima di avere i dati veri

**Cosa è successo.** Per confrontare il motore con una Certificazione Unica
reale serviva uno strumento. Farsi dare i dati e poi scrivere il codice avrebbe
significato usare dati personali come banco di prova del codice stesso.

L'ordine è stato invertito: prima lo strumento, poi i dati. Il collaudo è
avvenuto su una **CU sintetica** generata dal motore stesso — un caso a 97
giorni, Palermo 2025, riscritto nel formato di una CU vera. Esito: nove voci su
nove coincidenti.

**La prova più utile è stata la seconda.** Ho rifatto il confronto cambiando un
solo dato — l'anno d'imposta da 2025 a 2026 — cioè commettendo di proposito
l'errore più probabile, quello descritto alla voce 11. Risultato:

```
  Addizionale regionale       89,05      89,05     +0,00
! Addizionale comunale        73,41     101,65    +28,24
  Trattamento integrativo      0,00       0,00     +0,00
```

Una sola voce su nove diverge, ed è esattamente quella che cambia fra i due anni
per un reddito basso: l'addizionale di Palermo, passata da 1,014% a 1,404%.
L'IRPEF resta allineata perché con quel reddito la seconda aliquota non entra in
gioco.

**Perché conta.** Uno strumento di confronto che segnala tutto in blocco è
inutile: non distingue un motore sbagliato da una configurazione sbagliata.
Questo isola la voce, e la diagnostica suggerisce di controllare **l'anno prima
del motore** — che è l'ordine giusto, visto quante volte l'anno d'imposta si è
rivelato la vera causa.

**Sulla privacy.** Gli importi non entrano nel repository: vivono in
`dati_privati/`, che ha un `.gitignore` proprio, il quale esclude tutto tranne
il modello vuoto e le istruzioni. Nemmeno un `git add -A` distratto porta via
qualcosa. Nel repository restano il confronto e il suo esito, mai le cifre.

---

### 33. "Ma noi lavoriamo sulla RAL, perché la CU?"

**La domanda che ha smontato la prima versione dello strumento.** Il prodotto
parte dal **lordo**. La CU dichiara l'**imponibile fiscale**, che è già al netto
dei contributi. Non sono la stessa cosa, e la differenza è esattamente il primo
anello della catena.

**Cosa faceva la prima versione.** Ricostruiva una "RAL equivalente" sommando i
contributi all'imponibile, e poi la annualizzava. Due ricostruzioni in fila. E
soprattutto: la riga *"imponibile fiscale"* tornava quasi **per costruzione**,
perché l'imponibile della CU era stato usato per fabbricare l'ingresso del
motore.

È lo stesso identico difetto trovato nei test alla voce 28 — una verifica che si
fabbrica la propria risposta — ripresentatosi in un altro punto del progetto a
poche ore di distanza. Segno che non era una distrazione ma un modo di
ragionare da sorvegliare.

**La correzione: due modalità dichiarate.**

| | Quando | Cosa verifica | Cosa NON verifica |
|---|---|---|---|
| **Completo** | la CU dichiara l'**imponibile previdenziale** | tutta la catena, contributi compresi | — |
| **Solo fiscale** | c'è solo l'imponibile fiscale | IRPEF, detrazioni, addizionali, bonus | il passo lordo → imponibile |

L'imponibile previdenziale, nella sezione INPS della CU, **è** il lordo del
periodo: se c'è, non si ricostruisce niente. Se non c'è, si parte dall'imponibile
dichiarato e si verifica la sola macchina tributaria — e lo strumento **scrive a
schermo** che il passo contributivo resta fuori, invece di far credere di averlo
controllato.

**Cosa è cambiato nel motore.** Per rendere possibile la seconda modalità, la
parte fiscale è stata estratta in una funzione a sé, `imposte_su_imponibile`, che
parte dall'imponibile invece che dalla RAL. `calcola` ora la usa: una sola
implementazione, due punti d'ingresso. I 302 test sono rimasti verdi, il che era
la condizione per accettare il refactor.

**La lezione.** Uno strumento di verifica va interrogato come il codice che
verifica: *da dove viene ciascun numero che sto confrontando?* Se la risposta è
"da quello che sto testando", non è una verifica.

---

### 34. Lo schema del database, provato invece che solo scritto

**Cosa è successo.** Scritto lo schema, l'ho caricato su un MySQL vero (8.4, in
Docker) e ho applicato la stessa domanda usata per i test: **i vincoli
respingono davvero i dati sbagliati?** Un `CHECK` che non scatta è decorazione.

Nove tentativi di inserimento illegale. Otto respinti correttamente:

| Tentativo | Esito |
|---|---|
| scaglione IRPEF legato a un comune (l'IRPEF è nazionale) | respinto |
| addizionale regionale "a scaglioni" con aliquota unica valorizzata | respinto |
| addizionale regionale "unica" senza aliquota | respinto |
| aliquota comunale del 150% | respinto |
| soglia di esenzione pari a zero | respinto |
| CCNL con 20 mensilità | respinto |
| parametro per un anno inesistente | respinto |
| coefficiente senza fonte | respinto |
| **due scaglioni con lo stesso ordine** | **ACCETTATO** |

**Il buco: in SQL due NULL non sono uguali fra loro.** La chiave unica includeva
`territorio`, che per gli scaglioni IRPEF è `NULL` perché l'IRPEF è nazionale.
Siccome `NULL = NULL` non è vero, il database non li considerava duplicati e
accettava due scaglioni identici.

**Cosa sarebbe costato.** Un duplicato non genera errori: genera un'imposta
sbagliata. Due volte lo scaglione al 23% significa tassare due volte i primi
28.000 euro, e il risultato resta un numero plausibile. Silenzioso, come tutti
gli errori peggiori di questo progetto.

**Cosa è cambiato.** Una colonna generata che sostituisce il NULL con un valore
convenzionale, così il confronto torna a funzionare:

```sql
territorio_chiave CHAR(2) GENERATED ALWAYS AS (COALESCE(territorio, '--')) STORED,
UNIQUE KEY uk_scaglione (ambito, anno, territorio_chiave, ordine)
```

Ricaricato lo schema, il duplicato viene respinto e un ordine diverso passa.

**Una verifica incrociata, gratuita.** Ricalcolando l'IRPEF lorda **in SQL**, con
una window function sugli scaglioni del database, su un imponibile di 31.783,50:

| Anno | Da SQL | Dal motore Python |
|---|---|---|
| 2025 | 7.764,23 | 7.764,23 |
| 2026 | 7.688,56 | 7.688,56 |

Due strade completamente diverse — un ciclo Python e una query SQL — sugli stessi
dati, stesso risultato al centesimo. Non prova che le aliquote siano giuste (per
quello servono le fonti), ma prova che il travaso dei dati dal registro al
database non ha perso né deformato niente.

**Il seed non si scrive a mano.** Lo genera
[strumenti/genera_seed.py](strumenti/genera_seed.py) da `dati/coefficienti.json`.
Se fosse scritto a mano esisterebbero due copie degli stessi numeri, e prima o
poi divergerebbero: si aggiorna il JSON, ci si dimentica del SQL, e
l'applicazione serve un'aliquota vecchia. Generandolo, la divergenza è
impossibile per costruzione.

**E `docker compose up` funziona da zero:** database creato, schema applicato,
seed caricato, pronto in una quindicina di secondi senza nessun passaggio
manuale. Provato partendo da volume vuoto, che è la condizione in cui si
troverà chi apre il repository.

---

### 35. La CU ha trovato un errore vero, e non uno da poco

**Cosa è successo.** Confrontato il motore con una Certificazione Unica reale
— rapporto breve, comune del Sud, redditi 2025 — **sei voci su nove non
tornavano.** Due in modo clamoroso: la detrazione da lavoro dipendente e il
trattamento integrativo davano **zero**, contro importi che il sostituto
d'imposta aveva riconosciuto.

**La causa: una mia semplificazione, non un refuso.** Per i periodi parziali
avevo stabilito una regola **uniforme** — tutte le soglie valutate sul reddito
annualizzato — perché sembrava più coerente e più facile da spiegare. Su un
rapporto breve l'annualizzato scavalca sia il limite della detrazione sia
quello del trattamento integrativo, e li azzera entrambi.

Il sostituto d'imposta invece li ha riconosciuti, calcolandoli sul reddito
**effettivo** del periodo.

**La legge non è uniforme, e la CU lo dimostra in tutte e due le direzioni:**

| Voce | Guarda il reddito | Prova nella CU |
|---|---|---|
| Detrazione art. 13, ulteriore 65 €, trattamento integrativo | **effettivo** | riconosciuti entrambi, ragguagliati ai giorni di lavoro |
| Taglio del cuneo fiscale | **annualizzato** | somma esente **non erogata**: sull'annualizzato non spetta |

È questo che rende il documento probante: se la regola fosse uniforme in un
senso, la somma esente sarebbe stata pagata; se lo fosse nell'altro, la
detrazione non ci sarebbe. La CU conferma **entrambe** le letture, che sono
opposte fra loro. Nessun ragionamento a tavolino ci sarebbe arrivato.

**Un dettaglio in regalo, scritto nelle annotazioni della CU:** *"la detrazione
minima è stata ragguagliata al periodo di lavoro"*. Quindi anche il minimo di
690 € va rapportato ai giorni — e così non entra mai in gioco, perché la fascia 1
vale 1.955 e la proporzione si applica a entrambi. Il minimo intero spetta solo
in sede di dichiarazione, che questo prototipo non simula. **La voce 21 di questo
diario era sbagliata**, e questa la corregge.

**Dopo la correzione: sette voci su sette, scarto massimo 0,01 €** — un
centesimo di arrotondamento su una riga sola.

E l'addizionale comunale ha confermato **per via indipendente** l'aliquota di
quel comune per il 2025: non quella dell'anno prima, né quella dell'anno dopo.

**Quello che resta fuori, e va dichiarato.** I contributi reali erano il
**9,457%** dell'imponibile previdenziale, contro il 9,19% del nostro modello: la
differenza di 0,27 punti sono contributi minori previsti dal contratto che il
prototipo non tratta. Su una RAL annua di 35.000 € varrebbe circa **93 €**. Non
è un errore: è una semplificazione, e ora ne conosciamo la dimensione invece di
ipotizzarla.

**Gli importi non stanno in questo diario.** Ci sono il metodo, lo scarto e
l'esito; non l'imponibile, non i giorni, non il comune. Sono la retribuzione di
una persona, e per chi la conosce quella combinazione la individua senza
sforzo. Uno strumento che si occupa di retribuzioni non pubblica la
retribuzione di qualcuno per dimostrare che funziona. Chi vuole rifare il
confronto lo fa sulla propria CU, con lo stesso strumento.

**Perché questa voce vale tutto il diario.** Avevo scritto — alla voce 33 — che
la CU avrebbe aggiunto "una conferma esterna, non una correzione". Sbagliato: ha
corretto un errore che 302 test non avevano visto, perché i test erano scritti
dalla stessa testa che aveva stabilito la regola sbagliata. Un documento emesso
da qualcun altro è l'unica cosa che può rompere quel cerchio.

---

### 36. Come è fatto lo strumento che già esiste

**Cosa è successo.** Prima di disegnare l'interfaccia, sono andato a vedere il
sito di Jet HR. Il fatto principale cambia l'inquadramento del task:

> **Jet HR ha già un calcolatore dello stipendio netto**, insieme ad altri nove
> strumenti gratuiti: costo azienda, IRPEF, RAL da CCNL, partita IVA, fringe
> benefit auto, KPI HR, aliquote 2026.

Quindi il task non chiede *"sai costruire un calcolatore?"*. Chiede, in
sostanza: *"costruiresti il nostro meglio di come l'abbiamo fatto noi, e sapresti
dire perché?"*.

**Tre osservazioni sul loro calcolatore**, tutte verificabili aprendo la pagina:

1. **Il campo si chiama "Stipendio (RAL)".** È esattamente la formulazione che
   ha prodotto l'errore descritto alla voce 16: *stipendio* nell'uso comune
   significa "quanto prendo al mese", e la disambiguazione è affidata a un
   acronimo fra parentesi. La distinzione lordo/netto è spiegata bene, ma **più
   in basso**, in un testo discorsivo che si legge dopo aver già compilato.

2. **Non chiede il comune.** Le addizionali locali non entrano nel calcolo.
   L'analisi sui 7.792 comuni (voce 17) dice quanto costa quell'assenza: fino a
   **oltre 600 € l'anno** di scarto fra un territorio e un altro, a parità di RAL.

3. **Non cita nessuna fonte normativa.** Nessun riferimento a leggi, circolari o
   delibere, e nessuna data di verifica dei coefficienti.

**Cosa NON ho trovato.** Nessuna discussione su Reddit, né in italiano né in
inglese: cercando per nome, per dominio e per subreddit di settore non emerge
nulla. Il confronto pubblico su questo prodotto vive altrove — Trustpilot,
Capterra, Glassdoor — non su Reddit.

**Cosa dicono le recensioni pubbliche.** Quadro misto: piattaforma apprezzata
per le funzionalità, critiche ricorrenti sulla difficoltà di dialogo con il
consulente dedicato e sui tempi di prenotazione. E una segnalazione che
somiglia in modo impressionante al nostro tema: **errori nella conversione fra
ore e giorni di ferie** durante l'onboarding. È la stessa famiglia di difetto —
una conversione fra due unità di misura, sbagliata in silenzio, che colpisce chi
non è del mestiere.

**Cosa ne ricaviamo per l'interfaccia.** Le tre differenze non sono opinioni ma
scelte con un costo misurabile accanto:

| | Loro | Noi | Perché |
|---|---|---|---|
| Etichetta | "Stipendio (RAL)" | "RAL — Retribuzione Annua **Lorda**", più il risultato che ripete l'input | l'errore osservato alla voce 16 |
| Territorio | assente | sempre visibile, mai predefinito in silenzio | vale oltre 600 €/anno (voce 17) |
| Fonti | assenti | ogni numero con norma, data e stato di verifica | sei coefficienti su sette erano sbagliati (voce 1) |

> **Nota di tono, per la consegna.** Nel README queste differenze vanno
> presentate come **scelte di progetto motivate**, non come critiche a un
> prodotto specifico. "Abbiamo reso il territorio obbligatorio perché vale 600 €
> l'anno" è un argomento; "il vostro calcolatore lo ignora" è un'altra cosa.
> L'osservazione diretta vale in conversazione, dove si può fare la domanda
> giusta invece di affermare.

---

### 37. Verificato alla fonte, non sul riassunto

**Cosa è successo.** Le tre osservazioni della voce 36 venivano da un estrattore
che aveva letto la pagina e me l'aveva riassunta. Un dettaglio suonava strano —
compariva la parola "SPRITZ" — segno che la lettura poteva essere sporca. Prima
di costruirci sopra l'interfaccia, ho scaricato la pagina e l'ho letta a mano.

**Le tre osservazioni reggono, e la terza più di quanto pensassi.**

Conteggio delle occorrenze nell'intera pagina:

| Termine | Occorrenze |
|---|---|
| `addizionale` | **0** |
| `provincia` | 0 |
| `comune` | 1 (non nel modulo) |
| `TUIR` | **0** |
| `circolare` | **0** |
| `legge di bilancio` | **0** |
| `art. 13` | **0** |
| `Agenzia delle Entrate` | **0** |

L'etichetta `Stipendio (RAL)` è confermata alla lettera, in un vero `<label>`.
Il segnaposto del campo è `IE: 30000` — un'abbreviazione inglese in un modulo
italiano, dove ci si aspetterebbe "es.".

**"SPRITZ" non era un errore di lettura.** È un'etichetta vera: un selettore che
converte il netto da euro a spritz. Dice qualcosa di utile sul tono — leggero,
antiburocratico, dichiarato anche nel loro manifesto. Un nostro prodotto austero
e accademico stonerebbe con quel registro.

**La scoperta che non mi aspettavo: il calcolo non avviene nel browser.** Gli
script della pagina non contengono nessun termine fiscale — zero occorrenze di
`irpef`, `aliquota`, `detrazione`, `scaglione`, `0.0919`. I dati vengono spediti
a un endpoint remoto che restituisce il risultato.

Il che significa che il loro calcolatore è, dal punto di vista di chi lo usa,
**una scatola chiusa**: non c'è modo di vedere come si arriva al numero. È la
stessa espressione che il testo del task usa per dire cosa *non* vuole. Non è
una critica al loro prodotto — per un calcolatore di marketing è una scelta
ragionevole — ma è esattamente il terreno su cui il nostro può distinguersi,
perché il task chiede di dimostrare di aver capito le logiche.

**Cose che il loro strumento fa e il nostro no**, e vanno riconosciute:
agevolazioni contributive per assunzione (Under 30, Donne, Over 50), regime
impatriati con e senza figli, apprendisti sotto i 21 anni, regimi di partita IVA
con i coefficienti ATECO, e in uscita anche il **costo azienda**. È più largo del
nostro; il nostro è più profondo su un caso solo.

**Un'osservazione sull'esperienza del neofita.** Nella stessa pagina intitolata
"calcolo netto dipendente" convivono campi come *Cassa previdenziale* (Gestione
separata / Artigiano / Commerciante) e *Opzioni regime forfettario* con nove
coefficienti ATECO. Saranno mostrati in modo condizionato, ma stanno nello stesso
modulo: chi non è del mestiere non ha modo di sapere se lo riguardano. È lo
stesso problema della voce 16 — non un errore di calcolo, un errore di
comprensione indotto dall'interfaccia.

**Una prova falsificabile, da fare in trenta secondi.** Se il loro calcolatore
non applica le addizionali locali, su una RAL di 35.000 € a Milano il loro netto
dovrebbe risultare **più alto del nostro di circa 709 €** — cioè 454,98 di
addizionale regionale più 254,27 di comunale. Basta aprire la loro pagina,
inserire 35.000 e confrontare con i nostri 26.032,22. Se lo scarto è quello,
conferma insieme il nostro motore e la nostra lettura del loro strumento.

> **Nota di metodo.** Non ho interrogato il loro endpoint da programma: è
> un'API interna non documentata, e sollecitarla non sarebbe corretto. Il
> confronto si fa a mano, con un clic, come lo farebbe un utente.

---

### 38. Il difetto peggiore del progetto, trovato usando l'interfaccia

**Cosa è successo.** Provata l'applicazione per la prima volta, il primo input
digitato in modo naturale ha rivelato che **non sapevamo leggere i numeri**:

| Scritto | Letto dal motore |
|---|---|
| `35.000` | **35,00 €** |
| `25.999` | 26,00 € |
| `2.500` | 2,50 € |
| `35,000` | *errore* |
| `35.000,50` | *errore* |

La causa è di una banalità imbarazzante: `float("35.000")` in Python vale
**35.0**, perché il punto è il separatore decimale. In italiano è il separatore
delle migliaia.

**Quanto era grave.**

1. **Il segnaposto del nostro campo era `es. 35.000`.** Chi copiava il nostro
   stesso esempio otteneva un calcolo su trentacinque euro.
2. Il messaggio d'errore diceva *"Esempio: 35000 oppure 35.000,50"* e poi
   **rifiutava proprio il formato che suggeriva**.
3. Il risultato non segnalava niente. 33,65 € di netto su 35 € di lordo è
   perfettamente coerente: nessun controllo poteva accorgersene, perché il
   calcolo era giusto — era il numero a essere quello sbagliato.

È **esattamente** il difetto contro cui è nato il progetto — un input frainteso
in silenzio che produce un risultato plausibile — e stava nel nostro strumento,
nel campo principale, protetto da 304 test.

**Perché 304 test non l'hanno visto.** Perché erano scritti da chi conosceva il
formato accettato. Ogni test passava `35_000` o `"30000"`: nessuno ha mai
provato a scrivere un numero *come lo scrive una persona*. I test difendevano
il calcolo, non l'ingresso al calcolo.

E infatti non è stato trovato leggendo il codice: è stato trovato **usando
l'interfaccia**, al primo tentativo, da chi non stava cercando bug.

**Cosa è cambiato.**

- Una funzione `normalizza_importo` che accetta `35.000`, `35,000`, `35.000,50`,
  `35,000.50`, `35 000`, `€ 35.000` — e li interpreta tutti correttamente.
- Gli input **malformati** (`35..000`, `35,00,00`) restano **respinti** invece
  di essere aggiustati con un'ipotesi: indovinare in silenzio su un numero rotto
  è lo stesso difetto in un'altra forma.
- Un caso resta genuinamente ambiguo: `35.000` può valere trentacinquemila o
  trentacinque e zero millesimi. Si sceglie la lettura più probabile — **tre
  cifre dopo il separatore sono migliaia** — ma la scelta viene **mostrata**
  mentre si digita: *"Ho letto 35.000 € lordi all'anno"*. Dove non si può essere
  certi, si dichiara come si è capito.
- Il messaggio d'errore ora mostra solo formati che vengono davvero accettati.
- 22 test nuovi sui formati, suite da 304 a **326**.

**La lezione, che vale più della correzione.** Una suite scritta da chi conosce
il sistema difende il sistema dagli errori che chi lo conosce immagina. Le prime
dieci righe di codice usate da una persona vera hanno trovato in un minuto
quello che centinaia di test non cercavano. **Provare non è la fase finale della
verifica: è una fonte di verifica diversa da tutte le altre.**

---

### 39. Adottare un'identità visiva altrui, misurandola

**La decisione.** Il prototipo riprende i colori di Jet HR — inchiostro
`#11150a`, accento lime `#dfeb57`, neutri verdati — mantenendo però il CSS
scritto a mano invece di Tailwind: le scelte visive restano leggibili e
commentate, che è coerente con un progetto che vuole essere ispezionabile.

**Cosa è emerso misurando invece di copiare.** Prima di usarli, i loro colori
sono stati passati al calcolo del contrasto:

| Accostamento | Rapporto | Verdetto |
|---|---|---|
| lime su bianco | **1,30 : 1** | inutilizzabile come testo |
| inchiostro su lime | **14,23 : 1** | ottimo — il lime è un **fondo** |
| inchiostro su bianco | 18,49 : 1 | testo principale |
| loro blu su bianco | 4,57 : 1 | passa di poco |

Il lime è una firma di marca, non un colore di lettura. Copiarlo dove capita
avrebbe significato **riprodurre la forma e perdere la funzione**. Nel
prototipo compare quindi solo come fondo pieno con testo scuro sopra — che è
esattamente il modo in cui lo usano loro.

Un dettaglio che il calcolo ha reso ovvio: il pulsante "Calcola" ha il testo
leggibilissimo (14,2:1) ma il **perimetro** invisibile, perché il fondo lime
sta a 1,3:1 dal bianco della scheda. Un bordo scuro non è decorazione: è ciò
che rende il pulsante un oggetto con dei confini.

**La palette dei dati resta la nostra, e non è una preferenza.** Passando i loro
colori al validatore come palette categorica: **FAIL** su banda di luminosità e
su saturazione minima. Non è un difetto del loro lavoro — non hanno mai avuto
bisogno di una palette per i dati, perché il loro strumento non mostra grafici.
Sono due mestieri diversi per gli stessi colori, e confonderli si vede subito.

**L'avviso di indipendenza.** Un repository pubblico con il marchio di
un'azienda e uno strumento che fa lo stesso mestiere può essere scambiato per
un prodotto ufficiale. In pagina, sopra tutto, c'è quindi una riga che dice
cos'è: *prototipo indipendente, esercizio per una selezione, non collegato ai
loro sistemi*. Non è una formalità — è ciò che rende la scelta di stile
difendibile in una conversazione invece che imbarazzante.

**E qui la parte più interessante.** Adottare un'identità visiva significa
anche gestire i casi in cui quell'identità non basta: una palette pensata per
la comunicazione ha colori che non reggono la lettura. Da qui i **controlli di
leggibilità**, tre leve indipendenti perché servono a persone diverse:

- **dimensione del testo** (normale / grande / molto grande);
- **contrasto alto**, che sostituisce i riempimenti tenui con bordi netti —
  perché quando le tinte spariscono la gerarchia deve sopravvivere lo stesso;
- **trame nel grafico oltre al colore**, per chi confonde certe coppie di tinte
  o stampa in bianco e nero.

Le stesse leve si attivano da sole se il sistema operativo le richiede
(`prefers-contrast`, `prefers-reduced-motion`, `forced-colors`): una preferenza
già espressa altrove non va chiesta una seconda volta.

**Perché in questo prodotto non è un accessorio.** Un calcolatore fiscale è
fatto di numeri lunghi, di segni «−» e «+» che ribaltano il significato di una
riga, e di differenze che stanno nell'ultima cifra. Chi fatica a leggere non
sbaglia "un po' di più": sbaglia in modo diverso, e su un importo che finisce
in un contratto.

---

### 40. Il controllo di sicurezza, a codice finito

Il codice era terminato. Un prototipo senza utenti registrati, senza dati
personali e senza niente da rubare: il momento in cui il controllo di sicurezza
si salta, perché non sembra esserci nulla da proteggere.

È stato fatto lo stesso, e ha trovato **tre difetti reali più due omissioni.**

**Il primo è quello che pesa.** L'API serve anche l'interfaccia compilata, con
una rotta generica che restituisce qualunque cosa corrisponda a un file dentro
`web/dist`:

```python
file = FRONTEND / percorso
if file.is_file():
    return FileResponse(file)
```

`FRONTEND / "../../dati_privati/LEGGIMI.md"` **è un file.** `pathlib` compone i
percorsi, non li giudica. Era quindi scaricabile dal browser tutto ciò che sta
sotto la radice del progetto — compresa `dati_privati/`, la cartella tenuta
fuori dal repository *proprio perché contiene una Certificazione Unica vera*.

Quella cartella ha un `.gitignore` dedicato, scritto apposta, verificato. Ha
funzionato perfettamente per la domanda a cui rispondeva — *questo file finisce
nel repository?* — e non rispondeva affatto all'altra: *questo file può uscire
da questa macchina?* **Una difesa messa nel posto giusto non protegge il dato:
protegge una via d'uscita.** Le altre restano aperte finché qualcuno non le
cerca apposta.

Corretto risolvendo il percorso e confrontandolo con la radice consentita.
`.resolve()` **prima** del confronto è la parte che conta: confrontare le
stringhe prima di normalizzarle è il modo classico di scrivere un controllo che
non controlla. Verificato su otto percorsi, cinque ostili.

**Il secondo ha una simmetria che fa quasi ridere.** Il campo della RAL
accettava `1e308`, trenta cifre di seguito, e `٣٥٠٠٠` in cifre arabo-indiane —
che `float()` in Python converte volentieri in 35000. Alla voce 38 lo stesso
campo era **troppo severo**, e leggeva `35.000` come 35 €. Adesso era troppo
permissivo, nella direzione opposta, a poche settimane di distanza. Lo stesso
punto del programma sbagliato nei due sensi: la validazione dell'ingresso non è
un problema che si risolve una volta.

**Il terzo si legge in tre caratteri.** In `docker-compose.yml`, `"3307:3306"`
sembra «la porta di questa macchina». Docker la interpreta come `0.0.0.0:3307`:
tutte le interfacce. Su una rete condivisa il database era raggiungibile da
chiunque, con la password di sviluppo scritta tre righe sopra. Il difetto non
sta in ciò che è scritto — è la forma che si trova in ogni esempio della
documentazione — sta in ciò che **non** è scritto e viene riempito da un valore
predefinito.

**Le due omissioni** erano le intestazioni di sicurezza HTTP, tutte assenti, e
l'assenza di qualunque limite di frequenza su un calcolo inverso che costa 14,6
ms contro gli 0,6 ms del diretto. Aggiunte entrambe, con il limite dichiarato
per quello che è: elementare, in memoria, insufficiente in produzione. Scritto
nel codice, così che nessuno lo scambi per una difesa completa.

**Il metodo, che è la parte trasferibile.** Nessuno dei tre si vedeva
rileggendo il codice — come nessuno dei trentanove precedenti. Si sono visti
facendo tre cose diverse fra loro:

1. **costruire una richiesta ostile e mandarla davvero**, invece di ragionare
   su cosa succederebbe;
2. **dare in pasto al motore ingressi che nessun utente scriverà mai**;
3. **rileggere la configurazione come la legge chi la esegue**, non come sembra
   scritta.

Il resoconto completo — comprese le verifiche che **non** hanno trovato niente,
che vanno elencate perché altrimenti il documento racconta metà del lavoro, e i
sei rischi che restano dichiarati aperti — sta in [SICUREZZA.md](SICUREZZA.md).

Dopo le correzioni: 375 test superati, 15 guasti deliberati su 15 rilevati,
zero violazioni della politica dei contenuti nel browser.

---

### 41. Due revisioni esterne, quattro difetti, uno dei quali fiscale

**Cosa è successo.** A lavoro considerato finito — motore, interfaccia,
sicurezza, documentazione — il progetto è stato dato in lettura a **due
revisori indipendenti**. Hanno trovato quattro difetti in poche ore. Nessuno
era stato trovato da me, dai 326 test di allora o dal controllo di sicurezza.

**Il più serio è fiscale, e cambia i numeri.** Il trattamento integrativo, sotto
i 15.000 €, spetta se l'IRPEF lorda supera la detrazione art. 13 **diminuita di
75 euro rapportati al periodo di lavoro**. L'inciso viene dal
D.Lgs. 216/2023, reso strutturale dall'art. 1 c. 3 della L. 207/2024, e la
circolare 4/E del 16 maggio 2025 lo conferma. Nel registro non c'era.

La soglia si sposta da un imponibile di 8.500 a **8.173,91**, cioè da una RAL di
9.360 a **9.002**. Chi sta in mezzo riceve 1.200 € che il motore gli negava.

**E qui la parte che vale più della correzione.** Sistemata la soglia, le
discontinuità di Milano sono passate da sei a **sette**. La capienza del
trattamento cadeva a 8.500 — esattamente dove finisce la prima fascia della
somma esente del cuneo. **Due discontinuità diverse sovrapposte nello stesso
punto**, contate come una sola per settimane, e visibili solo dopo aver corretto
un errore che non c'entrava. Una era dichiarata nel registro; l'altra non lo era
affatto, e non poteva esserlo, perché nessuno sapeva che esistesse.

La voce 25 di questo diario si intitolava *«Le discontinuità erano sei, non
una»*. Erano sette.

**Perché i test non l'avevano visto — ed è la terza volta.** Il test sulle
discontinuità ricavava le soglie **dallo stesso registro** che avrebbe dovuto
controllare, con questa motivazione scritta nel codice:

> *«Ricavarle invece di elencarle a mano significa che, se domani cambia un
> coefficiente, il test si aggiorna da solo e continua a essere vero.»*

Suona come buon senso. È l'errore 5 e l'errore 7 per la terza volta: il registro
sbagliava, il test rifaceva lo stesso conto sbagliato, ed erano d'accordo. **Un
test che si aggiorna da solo quando cambia il dato non è robusto: è cieco.**

Tre volte non è una tendenza, è una firma. Gli ancoraggi sono adesso scritti a
mano, ognuno con il proprio conto in un commento, e se un coefficiente cambia il
test **fallisce** — che è quello che deve fare.

**Gli altri tre.**

| | Difetto | Perché era invisibile |
|---|---|---|
| 20 | Il calcolo inverso leggeva `2.000` come 2 € | la correzione dell'errore 12 era stata applicata solo dove il sintomo era comparso; i dieci test dell'inverso passavano numeri già puliti |
| 22 | La frase di conferma spezzata in colonne da un `display: flex` | era visibile in uno screenshot già allegato alla documentazione: guardato, non visto |
| 23 | Gli importi tagliati sul telefono | il controllo cercava il traboccamento **della pagina**, e `overflow-x: hidden` su `body` lo silenziava |

Il 23 merita una riga in più. La regola *«nessun elemento può far scorrere la
pagina in orizzontale»* era scritta apposta, era giusta, ed è **quella che ha
nascosto il difetto**: la verifica automatica chiedeva «la pagina scorre?» e io
volevo sapere «si vede tutto?». Non sono la stessa domanda.

**Cosa cambia nel metodo.** La revisione esterna entra nell'elenco dei metodi di
verifica, e per difetti trovati per ora impiegata è **il più produttivo di
tutti**. Somiglia molto a quello che aveva funzionato con la Certificazione
Unica alle voci 35 e 8–9: qualcuno che non ha costruito la cosa la guarda con
criteri che chi l'ha costruita non ha, e non condivide gli angoli ciechi.

Costruire da soli e verificare da soli ha un limite che non si supera
aggiungendo test, perché i test li scrive la stessa testa. Si supera facendola
guardare a qualcun altro.

**Dopo le correzioni:** 375 test superati, 15 guasti deliberati su 15 rilevati,
il confronto con la CU ancora esatto al centesimo sul trattamento
integrativo, scarto zero — e la tabella degli importi leggibile a 360, 390, 768
e 1280 px.

---
## Bilancio del Giorno 1

Su sette gruppi di coefficienti, **sei contenevano almeno un errore**. L'unico
valore corretto era l'aliquota INPS del 9,19%.

| Voce | Nel file | Corretto | Impatto |
|---|---|---|---|
| Seconda aliquota IRPEF | 35% | 33% (2026) | 🔥 ogni RAL > 28k |
| Cuneo fiscale | assente | due misure | 🔥 fascia 20k–40k |
| Addizionale regionale | 5 scaglioni inventati | 4 reali | medio |
| Esenzione Milano | 21.000 € | 23.000 € | medio |
| Trattamento integrativo | fino a 15k | fino a 28k | medio |
| Soglia +1% INPS | 55.008 € | 56.224 € | basso |
| Detrazione 65 € | comma 1-*bis*, da 28k | comma 1.1, da 25k | basso |
| Aliquota INPS | 9,19% | 9,19% ✅ | — |

Il motore era **logicamente corretto e numericamente falso**. È la distinzione che
questo progetto vuole rendere visibile: il codice funzionava, i test passavano, il
risultato sembrava ragionevole. Mancava solo che fosse vero.

**Stato delle fonti a fine giornata:** 7 voci su fonte primaria, 17 su fonte
secondaria, 3 da verificare. Dichiarate una per una in
[dati/coefficienti.json](dati/coefficienti.json), non arrotondate a "verificato".
