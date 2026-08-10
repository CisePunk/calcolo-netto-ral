# Dove si rompe un calcolatore fiscale

Analisi di usabilità: **cosa rende difficile, per chi non è del mestiere, usare
correttamente uno strumento di calcolo retributivo** — e cosa abbiamo deciso di
fare di conseguenza.

Non è un confronto fra prodotti. È lo studio di un problema di progettazione,
condotto su uno strumento reale, pubblico e funzionante, perché studiarlo su un
caso vero è più utile che ragionare per principi generali.

**Il caso osservato:** il calcolatore dello stipendio netto di Jet HR
(`jethr.com/strumenti/calcolo-stipendio-netto`). Tutte le osservazioni sono
verificabili aprendo la pagina; quelle sulla struttura sono ricavate leggendo il
codice HTML pubblico.

---

## Premessa: i due strumenti servono a cose diverse

Prima di qualunque confronto, la struttura della pagina va guardata per intero.
Questi sono i titoli, nell'ordine in cui compaiono:

```
H1   Calcolo netto dipendente dalla RAL (aggiornato 2026)
H2   Come calcolare lo stipendio netto
H3     Step 1. Parti dallo stipendio del dipendente
H3     Step 2. Aggiungi contributi, TFR e altri costi
H4       Contributi INPS
H3       Assicurazione INAIL
H3       TFR
H3     Esempio pratico di costo azienda
H2   Tabelle costo aziendale dipendente
H3     Tabella costo aziendale CCNL Commercio (H011)
H3     Tabella costo aziendale CCNL Metalmeccanici - Industria (C011)
H2   Altre risorse
H2   Come risparmiare fino al 50% quando assumi
H2   Scopri gli altri calcolatori
```

È l'anatomia di una **pagina di contenuto con un calcolatore dentro**: guida,
esempi, tabelle di riferimento, richiamo commerciale, rimando agli altri
strumenti. Il calcolatore è il gancio; la pagina è l'obiettivo.

**Questo spiega quasi tutte le differenze che seguono, e le rende legittime.**
Uno strumento che serve a farsi trovare e a generare contatti ha ragioni ottime
per essere veloce da compilare, poco severo e visivamente leggero. Aggiungere
attriti — un campo obbligatorio in più, un avviso, una nota sulle fonti — è un
costo che quel modello di prodotto non ha motivo di pagare.

Le differenze qui sotto non sono errori altrui: sono **conseguenze di scopi
diversi**. Noi non stiamo costruendo un gancio, quindi possiamo permetterci
attriti che per loro sarebbero controproducenti.

---

## 1. Capire cosa inserire

**Come si presenta.** Il campo si chiama `Stipendio (RAL)`, con segnaposto
`IE: 30000`.

**Il problema.** *Stipendio*, nell'uso comune, significa **quanto prendo al
mese**. La parola che l'utente riconosce è quella sbagliata, e la
disambiguazione è affidata a un acronimo fra parentesi che chi non è del
mestiere non scioglie. Il segnaposto aiuta — 30000 non è un mensile — ma è un
indizio, non un'istruzione, e chi digita di fretta non lo confronta.

La distinzione fra lordo e netto è spiegata bene, ma **sotto il modulo**, nella
parte discorsiva. Si legge dopo aver compilato.

**Il costo dell'errore.** Inserire un mensile al posto della RAL produce un
risultato **plausibile**: nessuna cifra strilla, nessun avviso scatta. È un
errore che si scopre tardi — tipicamente quando un'offerta è già partita.
Questo caso è documentato: è successo davvero, a un'utente non esperta.

**La nostra scelta.**

- Etichetta senza ambiguità: **RAL — Retribuzione Annua LORDA**, con *lorda* e
  *annua* nel campo e non in un aiuto da aprire.
- Il risultato **ripete l'input**: *"Calcolato su 35.000 € lordi annui"*. L'errore
  si vede nel momento in cui si legge la risposta.
- Controllo di plausibilità: sotto ~5.000 € è quasi certamente un mensile, e lo
  strumento lo dice proponendo la correzione.
- **Modalità inversa netto → lordo**: chi ragiona in netto non deve più
  convertire a mente. È la conversione a mente che genera l'errore.

---

## 2. Capire quali campi mi riguardano

**Come si presenta.** Nell'ordine, il modulo contiene: `ral`, `tipologia`,
`agevolazioni contributive` (Under 30 / Donne / Over 50), `detrazioni fiscali`
(bonus rimpatriati), `cassaPrevidenziale` (Gestione separata / Artigiano /
Commerciante), `minore21`, `opzioni regime forfettario` con nove coefficienti
ATECO.

**Il problema.** In una pagina intitolata *"calcolo netto dipendente"* convivono
campi che riguardano il **lavoro autonomo**. Saranno mostrati in modo
condizionato, ma appartengono allo stesso modulo: chi non conosce il dominio non
ha modo di stabilire se *Cassa previdenziale* o *regime forfettario* lo
riguardino. Il dubbio, da solo, è un costo — e la risposta sbagliata al dubbio è
un errore.

**La nostra scelta.** Due schede distinte e nette — *ho il lordo* / *voglio il
netto* — e nessun campo che non appartenga al caso scelto. In modalità *alle
prime armi* l'unico campo è la RAL; tutto il resto ha default dichiarati.

---

## 3. Accorgersi di aver sbagliato

**Come si presenta.** Nel codice della pagina non compare **nessun** attributo di
validazione dichiarativa: zero `required`, zero `min`, zero `max`, zero
`pattern`. Eventuali controlli vivono nel JavaScript e non sono verificabili
dal markup.

**Il problema.** Un calcolatore fiscale ha una caratteristica ingrata: **quasi
ogni input sbagliato produce un output credibile**. Non c'è un valore che
"sembri" sbagliato. Se lo strumento non interviene, l'errore non ha modo di
emergere.

**La nostra scelta.** Gli avvisi sono la funzione principale, non un ornamento, e
sono **guidati dai dati** invece che scritti nel codice:

- importo che sembra mensile → correzione proposta in un clic;
- soglia appena superata → *"a 25.330 € di RAL scatta l'addizionale comunale di
  Milano: 100 € di lordo in più ne costano 184 di netto"*;
- avviso presente a Milano e **assente a Palermo**, dove quella soglia non
  esiste. Un avviso valido altrove è falso quanto un numero sbagliato.

---

## 4. Capire il risultato

**Come si presenta.** In uscita: costo azienda, stipendio netto, e un selettore
che converte il netto **in spritz**.

**Il problema.** Il netto è un numero solo. Da dove venga — quanto INPS, quanta
IRPEF, quante detrazioni — non è mostrato. Chi vuole capire deve scendere nella
parte discorsiva e rifare il ragionamento per conto proprio.

Lo spritz, invece, è una buona idea: rende il numero **tangibile**. Vale la pena
notarlo, perché indica un registro — leggero, antiburocratico — con cui il nostro
prodotto deve essere compatibile. Un calcolatore austero e accademico stonerebbe.

**La nostra scelta.** La tabella delle trattenute, voce per voce, è
**richiesta esplicitamente dal task** ed è anche la prova che il calcolo è
capito. Ogni voce territoriale porta con sé il luogo che la genera:
*"Addizionale comunale (Milano, 0,8%, esente fino a 23.000 €)"*, mai
*"Addizionale comunale"* e basta.

---

## 5. Poter verificare

**Come si presenta.** Sull'intera pagina: `TUIR` 0 occorrenze, `circolare` 0,
`legge di bilancio` 0, `art. 13` 0, `Agenzia delle Entrate` 0. Nessuna data di
verifica dei coefficienti.

Inoltre il calcolo **non avviene nel browser**: gli script della pagina non
contengono alcun termine fiscale — zero occorrenze di `irpef`, `aliquota`,
`detrazione`, `scaglione`, `0.0919`. I dati vengono inviati a un servizio remoto
che restituisce il risultato.

**Il problema.** Dal punto di vista di chi lo usa è una **scatola chiusa**: non
c'è modo di sapere né come si arriva al numero né su quali norme si basa. Per un
calcolatore di marketing è una scelta ragionevole — l'utente vuole il numero, non
la lezione. Ma rende impossibile la domanda *"questo dato è aggiornato?"*, che in
un dominio che cambia ogni anno è la domanda più importante.

**La nostra scelta.** Ogni coefficiente ha norma, data di verifica e **stato**
dichiarato — fonte primaria, secondaria, da verificare — consultabili in pagina.
Lo strumento dichiara quanto è sicuro di sé invece di fingere una certezza
uniforme. Sui coefficienti 2026, oggi, sono 18 voci su fonte primaria e 68
secondarie: le comunali dell'anno in corso non hanno ancora una tabella
ufficiale, e questo l'utente ha diritto di saperlo.

---

## 6. Accessibilità

**Come si presenta.** Otto icone informative sono presenti nel modulo — quindi
un aiuto in linea **esiste**. Ma nel codice non compare nessun
`aria-describedby` né `aria-label`.

**Il problema.** L'aiuto non è **associato ai campi in modo programmatico**: chi
naviga con uno screen reader incontra un campo nudo, e l'informazione che
scioglierebbe l'ambiguità resta irraggiungibile. È esattamente l'utente che ne
avrebbe più bisogno.

**La nostra scelta.** Ogni campo ha la sua descrizione collegata con
`aria-describedby`; gli avvisi vivono in una regione `aria-live`, così vengono
annunciati quando compaiono; le etichette sono complete senza dipendere da un
elemento da aprire.

---

## 7. Crescere nell'uso

**Come si presenta.** Un solo livello di interfaccia per tutti.

**Il problema.** Le due utenti hanno bisogni opposti. Chi è alle prime armi
vuole meno campi, più spiegazioni e avvisi che la fermino. Chi è esperto vuole
tutti i parametri in chiaro e nessun avviso che lo rallenti. Un'interfaccia sola
scontenta una delle due: o è troppo fitta per la prima, o troppo lenta per la
seconda.

**La nostra scelta.** Uno switch **Alle prime armi / Esperto**, ricordato e
cambiabile **in qualsiasi momento senza perdere gli input** — perché il caso da
coprire è chi si dichiara esperto, si blocca, e vuole tornare indietro senza
ricominciare.

| | Alle prime armi | Esperto |
|---|---|---|
| Input | solo la RAL | anno, territorio, CCNL, mensilità, giorni |
| Output | il netto, poi le voci una alla volta | tabella completa |
| Spiegazioni | espanse | in hover |
| Avvisi | tutti | solo quelli sostanziali |
| Fonti | nascoste | accanto a ogni coefficiente, con lo stato |

Le difese contro l'errore di input (§1) restano attive in **entrambe** le
modalità: anche l'esperto distratto sbaglia.

---

## 8. Quando lo stesso numero smette di essere informativo

Tutto quanto precede riguarda un calcolatore **informativo**: si consulta, si
legge un numero, si chiude la pagina. Se il numero è sbagliato, il costo è una
convinzione sbagliata.

Ma lo stesso calcolo, nel lavoro di tutti i giorni, non resta informativo. A un
certo punto qualcuno lo usa per **decidere**: scrive quella cifra in un'offerta,
la mette in un contratto, la comunica a una persona. Da quel momento il numero
non è più un'informazione, è un **impegno** — verso qualcuno che ci ha fatto
affidamento, e che se ne accorge dopo.

**Il salto di gravità è netto, e l'interfaccia dovrebbe rispecchiarlo:**

| | Calcolo informativo | Calcolo che diventa impegno |
|---|---|---|
| Errore tipico | ci si fa un'idea sbagliata | si assume una persona alla cifra sbagliata |
| Chi lo paga | chi ha sbagliato | **qualcun altro**, che non poteva controllare |
| Quando si scopre | subito, o mai | tardi, e da parte della persona coinvolta |
| Reversibilità | totale | il numero si corregge, la fiducia no |

**Il principio che ne deriva:** un avviso basta finché il risultato è
informativo. **Nel momento in cui una cifra sta per diventare vincolante,
l'avviso deve trasformarsi in un ripasso forte di cosa si sta usando come base** —
scritto dove il numero sta per essere usato, non all'inizio del modulo.

Concretamente, sotto il risultato:

> Stai usando **35.000 €** come retribuzione annua **lorda** — non lo stipendio
> mensile né il netto.

La forma di questo ripasso dipende dal contesto, ed è una distinzione che vale la
pena fare esplicita:

- **Dentro un flusso di creazione offerta** (dove quel numero *sta* per impegnare
  qualcuno) una **conferma da compiere** — una casella da spuntare — è
  giustificata: il gesto corrisponde a un atto reale.
- **In un calcolatore standalone** no. Una casella «Confermo che…» somiglia a un
  passo autorizzativo che non autorizza nulla: attrito senza contropartita. La
  stessa prevenzione dell'errore la dà un **riepilogo statico forte**, che ripete
  a parole cosa si sta usando come base. L'attenzione attiva, del resto, c'è già
  nell'**eco in cima al risultato**; questo ripasso la chiude, senza gesto.

Una prima versione del prototipo usava la casella da spuntare; è stata sostituita
dal riepilogo statico proprio perché lo strumento è, appunto, standalone. La
storia della scelta è in [IL-BUG-CHE-TORNA.md](../verifiche/IL-BUG-CHE-TORNA.md).

Il ripasso è scritto **a parole, non in sigle**: chi legge deve poter
riconoscere l'errore leggendo, non decifrando. Ed è la ragione per cui questo
prototipo espone anche la direzione **netto → lordo** (§1): chi ragiona in netto
non deve convertire a mente, e la conversione a mente è dove nasce l'errore.

> **Perimetro dell'analisi.** Le osservazioni di questo documento riguardano
> esclusivamente lo strumento **pubblico**, verificabile da chiunque riscaricando
> la pagina. Prodotti gestionali dietro autenticazione non sono stati esaminati e
> non se ne afferma nulla: questa sezione descrive una **classe di problema**,
> non un caso specifico.

---

## Riepilogo

| | Strumento osservato | Nostra scelta |
|---|---|---|
| Etichetta dell'input | `Stipendio (RAL)` | `RAL — Retribuzione Annua LORDA` + eco nel risultato |
| Campi non pertinenti | presenti nello stesso modulo | due schede separate |
| Validazione dichiarativa | assente nel markup | avvisi guidati dai dati |
| Dettaglio del risultato | netto e costo azienda | tabella voce per voce |
| Territorio | assente | obbligatorio e visibile |
| Fonti normative | nessuna | norma, data e stato per ogni valore |
| Trasparenza del calcolo | servizio remoto | catena esposta |
| Aiuto in linea | 8 icone, non associate | descrizioni collegate, regione `aria-live` |
| Livelli d'esperienza | uno | due, commutabili |
| Direzioni di calcolo | lordo → netto | anche netto → lordo |
| Ampiezza dei casi | agevolazioni, impatriati, partita IVA, costo azienda | un caso solo, trattato a fondo |

L'ultima riga conta quanto le altre: **il loro strumento è più largo del nostro**.
Copre agevolazioni contributive, regime impatriati, apprendisti, partite IVA e
restituisce anche il costo per l'azienda. Dichiararlo è parte dell'analisi: un
confronto che trova solo difetti nell'altro non è un'analisi, è una tesi.

Va però detto **perché** il nostro è più stretto, e non è per rinuncia. Il testo
del task fissa il caso da coprire: *"il dipendente non ha nessun tipo di
agevolazione particolare"*. Under 30, Donne, Over 50, impatriati e apprendisti
sono quindi **fuori perimetro per istruzione ricevuta**, non per limite. Il
confronto qui sopra mette a paragone due cose costruite per scopi diversi: uno
strumento che deve coprire tanti casi in fretta, e un prototipo che deve
dimostrare di aver capito **un** caso fino in fondo.

---

## Cosa abbiamo deciso di non costruire

Elencarlo serve quanto elencare ciò che c'è: uno strumento che promette meno di
quanto mantiene è più affidabile del contrario.

| Non c'è | Perché |
|---|---|
| Agevolazioni contributive (Under 30, Donne, Over 50) | escluse dal testo del task |
| Regime impatriati, apprendisti under 21 | idem |
| Partita IVA, regime forfettario | fuori dal caso "dipendente" |
| Costo per l'azienda | il task chiede il netto del dipendente e le sue trattenute |
| Familiari a carico, mutuo, spese detraibili | fuori dal caso semplice; ne va dichiarato l'effetto |
| Premi di risultato, benefit, straordinari | idem |
| TFR nel netto in busta | accantonato, non erogato |

Ognuna di queste voci sposta il risultato, e per questo va **nominata** invece
che semplicemente omessa. Un numero presentato come "il netto" senza dire cosa
non contiene è un numero che promette più di quanto vale.

---

## Una verifica che chiunque può rifare

Se le addizionali locali non entrano nel calcolo, su una **RAL di 35.000 € a
Milano** il netto dell'altro strumento dovrebbe risultare **più alto del nostro
di circa 709 €** — 454,98 di addizionale regionale più 254,27 di comunale. Il
nostro dà **26.032,22 €**.

È una previsione falsificabile e verificabile in trenta secondi, che mette alla
prova entrambe le letture: la nostra del loro strumento, e il nostro motore.

---

## Nota di metodo

Le osservazioni provengono dalla pagina pubblica e dal suo codice HTML, letto
manualmente. Il servizio di calcolo remoto **non è stato interrogato da
programma**: è un'API interna non documentata, e sollecitarla non sarebbe
corretto. Ogni confronto numerico va fatto a mano, con un clic, come lo farebbe
un utente qualsiasi.
