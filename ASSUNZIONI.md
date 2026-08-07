# Assunzioni e semplificazioni

Tutto quello che questo prototipo dà per scontato, perché, e — dove è stato
possibile misurarlo — **quanto pesa sul risultato**.

Il task autorizza le semplificazioni purché esplicite. Questo documento le rende
esplicite una per una, e per alcune fa un passo in più: invece di dire *«ho
semplificato»*, dice *«ho semplificato, e vale 93 € l'anno»*. È la differenza fra
dichiarare un limite e conoscerlo.

---

## Quanto pesano, in sintesi

Le semplificazioni non sono tutte uguali. Alcune spostano il risultato, altre no.

| Semplificazione | Peso sul netto |
|---|---|
| Contributi minori previsti dai CCNL | **≈ 93 € l'anno** su RAL 35.000 |
| Familiari a carico | può valere **centinaia di euro**, in aumento del netto |
| Agevolazioni contributive | non toccano il netto del dipendente, **toccano il costo aziendale** |
| Addizionali sottratte nell'anno del reddito | zero sul netto annuo; sposta la cassa |
| Riduzione detrazioni oltre 200.000 € | 440 €, ma fuori dal caso standard |
| Mensilità (12 / 13 / 14) | **zero** sul netto annuo |

---

## 1. Il caso, come lo fissa il task

> *«Il dipendente è un impiegato a tempo indeterminato, vive a Milano, non ha
> nessun tipo di agevolazione particolare.»*

Da qui discendono tre esclusioni che **non sono nostre scelte** ma istruzioni
ricevute:

**Nessuna agevolazione contributiva.** Under 35, donne con figli minori,
apprendisti, regime impatriati: tutte fuori. È rilevante perché sono la leva
economicamente più pesante per un'azienda che assume, e per questo la loro
normativa è comunque tracciata in [METODOLOGIA.md](METODOLOGIA.md) §4 — mappata,
non implementata.

**Tempo indeterminato.** Il tempo determinato cambia il minimo della detrazione
di fascia 1 (1.380 € invece di 690) e alcune aliquote contributive.

**Milano come territorio d'esempio.** Il testo dice *«puoi assumere»*, non
*«devi»*: il territorio è quindi un parametro, e il registro contiene anche
Palermo — scelta apposta perché ha una forma diversa di addizionale.

---

## 2. Il perimetro del rapporto di lavoro

**Settore privato, aliquota contributiva ordinaria del 9,19%.**
Il settore pubblico ha aliquote e fondi diversi.

> ⚠️ **Misurato.** In una busta paga reale del CCNL Commercio l'aliquota
> effettiva risulta il **9,457%**: 0,27 punti di contributi minori previsti dal
> contratto che il prototipo non tratta. Su una RAL di 35.000 € valgono circa
> **93 € l'anno**. Il dato viene dal confronto con una Certificazione Unica
> reale; è la semplificazione più concreta di questo elenco, ed è l'unica di cui
> conosciamo l'ordine di grandezza con precisione.

**Nessun carico familiare.** Niente detrazioni per coniuge, figli o altri
familiari (art. 12 TUIR). È l'assunzione che può spostare di più il risultato in
senso **favorevole** al dipendente: chi ha familiari a carico prende più di
quanto il prototipo dichiara.

Ha anche un effetto che si vede in una voce specifica: il trattamento integrativo
fra 15.000 e 28.000 € di reddito spetta solo se le detrazioni **superano**
l'imposta lorda, cosa che nel caso semplice non accade mai. Il risultato è
correttamente zero — ma è zero **per via delle nostre semplificazioni**, non
perché la norma non esista. La regola è implementata comunque.

**Nessun premio, benefit, fringe benefit o straordinario.** Solo la retribuzione
ordinaria. Premi di risultato e welfare aziendale hanno regimi fiscali propri,
spesso agevolati.

**Nessun onere deducibile o detraibile.** Niente mutuo, spese sanitarie,
previdenza complementare, erogazioni liberali.

---

## 3. Cosa entra nel netto, e cosa no

**Il TFR non è nel netto in busta.** Matura e viene accantonato: non è denaro
che il dipendente riceve ogni mese. Includerlo gonfierebbe il netto di circa il
7% con una cifra che non arriva sul conto.

**Il costo per l'azienda non è calcolato.** Il task chiede il netto del
dipendente e le sue trattenute. Il costo aziendale — contributi a carico del
datore, INAIL, TFR accantonato — è una domanda diversa, ed è la prima estensione
elencata nel [README](README.md).

---

## 4. Le imposte locali

**Aliquota base del comune e della regione**, senza agevolazioni locali.
Molti comuni prevedono esenzioni per categorie specifiche (pensionati, redditi
assimilati, soglie differenziate): il prototipo applica la sola soglia generale.

**Le addizionali sono sottratte nell'anno del reddito.**
In busta paga funziona diversamente: si trattengono in **undici rate mensili**,
da gennaio a novembre dell'**anno successivo** a quello di riferimento.

Per una **proiezione annuale** — che è quello che il task chiede — sottrarle
nell'anno del reddito è corretto: la domanda è *«quanto costa in un anno tipo
questa RAL»*, non *«quanto esce dalla busta di marzo»*. Ma significa che il netto
mensile mostrato **non coincide al centesimo** con nessuna busta paga reale.

Peso sul netto annuo: **zero**. Peso sulla cassa mensile: reale.

---

## 5. Contributi e massimali

**Il massimale contributivo si applica ai soli iscritti dal 1° gennaio 1996.**
Il prototipo lo applica sempre. Sotto i 122.295 € di RAL la differenza non
esiste; sopra, per chi è iscritto da prima del 1996, il calcolo sarebbe diverso.
È fuori dal caso «semplice e standard», implementato e dichiarato.

**L'aliquota aggiuntiva dell'1%** oltre la prima fascia di retribuzione
pensionabile è applicata: non è una semplificazione, è la norma.

---

## 6. Periodi di lavoro parziali

Default: **anno pieno, 365 giorni**. I giorni sono un parametro, visibile in
modalità esperto.

Con giorni inferiori a 365 valgono **due regole diverse**, e non è una nostra
scelta ma quello che fa il sostituto d'imposta:

| Voce | Guarda il reddito |
|---|---|
| Detrazione art. 13, ulteriore 65 €, trattamento integrativo | **effettivo** del periodo |
| Taglio del cuneo fiscale | **annualizzato** |

La distinzione è stata ricavata confrontando il motore con una Certificazione
Unica reale, che conferma **entrambe** le letture — riconosce la detrazione e non
eroga la somma esente. Una regola uniforme, in un senso o nell'altro, sbaglia una
delle due voci. Vedi [ERRORI.md](ERRORI.md) n. 8.

**Il minimo di 690 € della detrazione di fascia 1 è rapportato ai giorni**, come
fa il sostituto d'imposta. Il minimo intero si recupera in sede di dichiarazione
dei redditi, che questo prototipo non simula: guarda la busta paga, non il 730.

---

## 7. Semplificazioni di modello

**Imponibile fiscale = reddito complessivo.** Nel caso di un dipendente senza
altri redditi le due grandezze coincidono. Con redditi da locazione, capitali o
lavoro autonomo non coinciderebbero, e le soglie delle detrazioni si
sposterebbero.

**Un solo rapporto di lavoro nell'anno.** Nessun conguaglio, nessun cambio di
datore, nessuna somma erogata da altri soggetti.

**Le mensilità non cambiano il netto annuo.** La RAL è annua: 12, 13 o 14
mensilità cambiano solo il divisore del netto mensile. È scritto anche in pagina,
perché è il primo equivoco di chi non è del mestiere.

**La riduzione di 440 € delle detrazioni oltre i 200.000 € di reddito** (L.
199/2025) non è implementata: è fuori dal caso standard. Sopra quella soglia il
prototipo sovrastima il netto di 440 €.

---

## 8. Anno d'imposta

Il default è il **2026**, l'anno corrente: uno strumento che proietta uno
stipendio deve rispondere sull'anno che il dipendente sta vivendo.

Il **2025** è presente ma serve a un'altra cosa: confrontare i conti con
documenti già emessi, come una Certificazione Unica. Usarlo per una proiezione
darebbe un risultato sbagliato — nel 2025 la seconda aliquota IRPEF era il 35% e
non il 33%.

> Le aliquote comunali **2026** non hanno ancora una tabella ufficiale
> consolidata dell'Agenzia delle Entrate: esce con la modulistica 2027. Nel
> frattempo poggiano su delibere e fonti secondarie, e il prototipo **lo
> dichiara** invece di far finta di una certezza uniforme. Vedi
> [METODOLOGIA.md](METODOLOGIA.md) §3.

---

## 9. Cosa NON è una semplificazione

Vale la pena separarle, perché su queste il prototipo non fa sconti:

- **gli scaglioni IRPEF** sono progressivi per davvero, non un'aliquota media;
- **il taglio del cuneo fiscale** è implementato in entrambe le sue forme, che
  hanno natura opposta;
- **il trattamento integrativo** include la condizione di capienza e la fascia
  ridotta fino a 28.000 €;
- **le soglie di esenzione comunali** sono soglie e non franchigie: superate, si
  paga sull'intero imponibile, con il gradino che ne consegue;
- **le addizionali regionali** gestiscono sia la forma a scaglioni sia
  l'aliquota unica, perché le regioni non si comportano tutte allo stesso modo.

---

## In sede di colloquio

Il task dice che le semplificazioni verranno *«discusse in un'eventuale
interview»*. Le tre su cui una domanda sarebbe più interessante, dal nostro punto
di vista:

1. **I contributi minori da CCNL** — l'unica di cui conosciamo la dimensione
   esatta (93 € su 35.000), e quella che richiederebbe di modellare i contratti
   invece che le sole mensilità.
2. **I familiari a carico** — la più pesante fra quelle che aumentano il netto, e
   l'unica che rende non-nullo il trattamento integrativo nella fascia
   15.000–28.000 €.
3. **Le agevolazioni contributive** — non toccano il netto del dipendente, ma
   sono la ragione per cui esiste un team di Cost-Saving. La normativa è già
   mappata; l'implementazione no, e volutamente.
