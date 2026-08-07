# Analisi competitiva

Chi altro risolve il problema *«quanto prende davvero in tasca questa persona?»*,
con quali mezzi, e dove resta uno spazio scoperto.

L'analisi è servita a smontare tre delle quattro cose che credevamo distintive.
È il motivo per cui si fa: se conferma tutto quello che pensavi, non l'hai fatta.

---

## Metodo

Le osservazioni non vengono da un'impressione d'uso ma dal **codice pubblico
delle pagine**, scaricato e ispezionato. Ogni riga della matrice è un conteggio
ripetibile: la presenza di un campo, di un termine normativo, di un attributo di
accessibilità.

Cercare *"TUIR"*, *"circolare"*, *"aria-describedby"* nel sorgente dà una
risposta che non dipende da quanto attentamente si è guardato. È lo stesso
principio applicato ai coefficienti: **misurare invece di ricordare**.

Nessun servizio di calcolo è stato interrogato da programma: sono API interne
non documentate, e sollecitarle non sarebbe corretto. Dove serve un confronto
numerico, si fa a mano.

---

## Perimetro

**Concorrenti diretti** — strumenti che fanno la stessa cosa: da una RAL a un
netto, gratis, sul web.

**Concorrenti indiretti** — tutto il resto che risponde alla stessa domanda:
una persona, un foglio di calcolo, un software gestionale, un modello
linguistico.

La distinzione conta perché il concorrente indiretto più forte non è un sito:
**è chiedere a qualcuno che lo sa**.

---

## Concorrenti diretti

Quattro strumenti pubblici e gratuiti, tutti aggiornati al 2026.

| | **Jet HR** | calcolastipendionetto | stipendee.it | stipendiocalcolatore |
|---|---|---|---|---|
| Comune di residenza | **assente** | solo regione | **sì** | sì (regione + comune) |
| Cita norme (TUIR, circolari) | **nessuna** | nessuna | sì | sì (TUIR, L. 207, art. 13) |
| Selettore anno d'imposta | sì | no | sì | no |
| Calcolo inverso netto → lordo | no | no | **sì** | **sì** |
| Dettaglio voce per voce | parziale | sì | sì | sì |
| Agevolazioni e casi speciali | **molte** | apprendistato, figli | sì | apprendistato, figli |
| **Dichiara l'affidabilità di ogni dato** | **no** | **no** | **no** | **no** |
| **Avvisa sulle trappole del dominio** | **no** | **no** | **no** | **no** |
| **Controlli di leggibilità** | **no** | **no** | **no** | **no** |
| `aria-describedby` sui campi | **0** | **0** | **0** | **0** |

### L'etichetta del campo principale

Vale la pena isolarla, perché è il punto in cui nasce l'errore più costoso —
scambiare il mensile per l'annuo, o il netto per il lordo:

| Strumento | Etichetta |
|---|---|
| Jet HR | `Stipendio (RAL)` |
| calcolastipendionetto.it | `Stipendio lordo annuale` |
| stipendee.it | `Retribuzione annua lorda (RAL)` |
| stipendiocalcolatore.it | `STIPENDIO LORDO ANNUALE` |

Tre strumenti su quattro scrivono la parola **lordo** nell'etichetta. Uno la
affida a un acronimo fra parentesi, accostato a *«stipendio»* — la parola che
nell'uso comune significa *«quanto prendo al mese»*.

**Conseguenza per l'analisi:** l'errore descritto in
[ANALISI_USABILITA.md](ANALISI_USABILITA.md) §1 non è un problema della
categoria. È specifico di quella formulazione, e gli altri tre lo evitano con
una parola in più.

---

## Concorrenti indiretti

| Alternativa | Perché la si sceglie | Dove cede |
|---|---|---|
| **Il consulente del lavoro** | risponde sul caso specifico, ci mette la firma | costa, ha tempi di risposta, non si interroga dieci volte per confrontare scenari |
| **Il collega che se ne intende** | gratis e immediato | risponde a memoria, e la memoria fiscale invecchia di un anno per volta |
| **Un foglio di calcolo interno** | su misura, già lì | nessuno lo aggiorna a gennaio; l'errore si propaga senza che nessuno lo veda |
| **Il software paghe** (Zucchetti, TeamSystem, Factorial, Fluida) | il calcolo è quello vero, dentro il processo | arriva **dopo** la decisione: risponde quando l'assunzione è già fatta |
| **La busta paga o la CU** | il dato reale, certificato | guarda indietro, non avanti: non aiuta a formulare un'offerta |
| **Un modello linguistico** | risposta immediata, in linguaggio naturale | numero plausibile, nessuna fonte, nessuna data: la scatola più chiusa di tutte |

**Il concorrente indiretto più forte è il primo.** Non si compete sulla
precisione — un consulente è più preciso di qualunque calcolatore. Si compete
su **quante volte puoi fare la domanda**: chi sta costruendo un'offerta la rifà
dieci volte, e nessuno telefona dieci volte al consulente.

Il più insidioso è invece l'ultimo. Un modello linguistico risponde con
sicurezza e senza provenienza, e la risposta è **verosimile** — che in questo
dominio è la caratteristica peggiore che un numero possa avere.

---

## Cosa ha cambiato questa analisi

Prima di guardare, avremmo elencato quattro differenziatori. Tre non reggono.

| Credevamo fosse distintivo | La realtà |
|---|---|
| Chiedere il **comune** | due concorrenti su tre lo fanno; uno copre 7.800 comuni |
| **Citare le norme** | due su tre le citano, con TUIR e legge di bilancio |
| Il **calcolo inverso** netto → lordo | due su tre ce l'hanno già |
| Il **selettore dell'anno** | due su quattro ce l'hanno |

Ne resta uno, e non era quello su cui avremmo scommesso.

---

## Dove lo spazio è davvero scoperto

Quattro strumenti, quattro assenze identiche. **Nessuno**:

### 1. Dichiara quanto è sicuro di ciò che dice

Citare *«TUIR»* in fondo alla pagina non è la stessa cosa che dire, accanto a
ogni singolo numero, **da quale atto viene, quando è stato verificato e se è
stato letto sull'originale o su una fonte di secondo grado**.

La differenza non è pedanteria. Le aliquote comunali 2026 non hanno ancora una
tabella ufficiale consolidata: chi le usa oggi sta usando delibere e notizie.
Dichiararlo cambia il modo in cui un HR usa il numero — e chi non lo dichiara
non è più accurato, è solo più silenzioso.

*(Nel prototipo: pannello fonti in modalità esperto, con lo stato di ogni voce.)*

### 2. Avvisa sulle trappole del dominio

Questo dominio ha discontinuità che sorprendono chiunque:

- superata la soglia comunale, **cento euro di lordo in più ne costano 184 di
  netto**;
- sotto una certa soglia **il netto supera il lordo**, perché somma esente e
  trattamento integrativo sono denaro aggiunto, non sconti;
- fra 32.000 e 40.000 € il netto cresce più lentamente, perché una detrazione
  si sta spegnendo.

Tutti e quattro gli strumenti calcolano correttamente questi effetti. **Nessuno
li nomina.** L'utente vede il numero e non sa che sta camminando su un gradino.

*(Nel prototipo: avvisi generati dai dati del territorio, non cablati.)*

### 3. È usabile da chi vede poco

Zero `aria-describedby` su quattro strumenti. Nessun controllo di dimensione del
testo, di contrasto, o di trame alternative al colore.

È un'assenza sistematica, e in questo dominio pesa: numeri lunghi, segni «−» e
«+» che ribaltano il significato di una riga, differenze nell'ultima cifra.

*(Nel prototipo: aiuto agganciato ai campi, tre leve di leggibilità, avvisi in
regione `aria-live`.)*

### 4. Si lascia verificare

Tutti calcolano altrove e restituiscono un risultato. Nessuno permette di
rispondere alla domanda *«come ci sei arrivato, e come faccio a controllarlo?»*

*(Nel prototipo: motore leggibile, 399 test che girano senza installare nulla,
e strumenti che rieseguono le verifiche — compreso quello che guasta i
coefficienti apposta per controllare che i test se ne accorgano.)*

---

## Il posizionamento che ne esce

Non *«il calcolatore più completo»*: su ampiezza di casi Jet HR è avanti, e
sull'anagrafica dei comuni lo sono gli altri.

Ma: **il calcolatore che dice quanto è sicuro di sé, avvisa dove il dominio
inganna, e resta usabile da chi fatica a leggere.**

È un posizionamento più stretto di quello di partenza, e più difendibile —
perché è l'unico che è sopravvissuto al controllo.

---

## Cosa ne facciamo, in pratica

1. **Togliere dal README l'enfasi sul comune e sulle fonti citate** come
   elementi distintivi: sono ingresso al mercato, non vantaggio.
2. **Portare in primo piano lo stato di verifica** — è l'unica cosa che nessuno
   fa, ed è anche la più difficile da copiare, perché richiede di aver fatto
   davvero la ricerca.
3. **Rendere gli avvisi sulle soglie visibili anche in modalità semplificata**:
   sono utili soprattutto a chi non sa che esistono.
4. **Tenere l'ampiezza fuori dal perimetro**, dichiarandolo. Rincorrere Jet HR
   sulle agevolazioni con quattro giorni di lavoro produrrebbe un'imitazione
   peggiore dell'originale.

---

## Fonti

Pagine pubbliche, scaricate e ispezionate il 7 agosto 2026:

- [jethr.com/strumenti/calcolo-stipendio-netto](https://www.jethr.com/strumenti/calcolo-stipendio-netto)
- [stipendee.it](https://www.stipendee.it/)
- [stipendiocalcolatore.it](https://stipendiocalcolatore.it/)
- [calcolastipendionetto.it](https://www.calcolastipendionetto.it/)

Per il panorama dei software paghe: [confronto software HR per PMI
italiane](https://www.guidasoftware.it/software-hr-per-pmi-italiane/),
[Factorial — HR software in Italy](https://factorialhr.com/blog/hr-software-italy/).
