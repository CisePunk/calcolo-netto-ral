# Guida alla composizione del file Figma — i contenuti

Tutto il contenuto già raccolto, nell'ordine in cui va montato. Serve a
trasformare la composizione in un lavoro di impaginazione invece che di
raccolta.

> **Le misure stanno altrove.** Formato dei riquadri, griglia, scala
> tipografica, componenti e disposizione riquadro per riquadro sono in
> [COSTRUZIONE_FIGMA.md](COSTRUZIONE_FIGMA.md). Qui c'è *cosa* dire, lì *come*
> montarlo.

---

## A chi è destinato, e perché non è il repository

Il processo di selezione prevede tre passaggi: task tecnica, colloquio con il
**Cost Saving Lead**, colloquio con il **Chief of Staff**. Sono tre lettori con
tre domande diverse, e un artefatto solo non le serve tutte.

| Interlocutore | La sua domanda | L'artefatto giusto |
|---|---|---|
| Chi valuta la task | *«funziona, ed è verificabile?»* | il repository |
| **Cost Saving Lead** | *«ha capito il dominio e sa dove sono i soldi?»* | **questo file** |
| Chief of Staff | *«come ragiona e come decide?»* | questo file, più il registro delle decisioni |

Al responsabile di prodotto non si consegna il codice: si consegna il progetto,
i numeri e le decisioni. I due artefatti devono rimandarsi a vicenda — dal file
un link al repository, dal README un link al file.

**Cosa NON va messo qui.** Un mockup dell'interfaccia. L'applicazione esiste e
funziona: una sua rappresentazione statica sarebbe una seconda verità che
invecchia dal giorno dopo. Vanno invece le cose che il codice **non sa mostrare
a colpo d'occhio**: il ragionamento, il sistema, l'evoluzione.

---

## Struttura del file

Sette pagine, in quest'ordine — che è anche l'ordine in cui si racconta.

```
01 · Il problema
02 · La ricerca
03 · Il sistema di colore
04 · Architettura e flussi
05 · Gli stati dell'interfaccia
06 · Evoluzione — prima e dopo
07 · Cosa costruirei dopo
```

---

## Materiali già disponibili

### Schermate — `design/schermate/` (19 file, 2×)

| File | Cosa mostra |
|---|---|
| `01-vuoto-neofita-scrivania` | stato iniziale, desktop |
| `02-eco-input` | *«Ho letto 35.000 € lordi all'anno»* mentre si digita |
| `03-risultato-neofita-scrivania` | risultato completo, pagina intera |
| `04-vuoto-neofita-telefono` | stato iniziale, telefono |
| `05-risultato-neofita-telefono` | risultato completo, telefono |
| `06-input-non-interpretabile` | input malformato, respinto con esempi validi |
| `07-avviso-sembra-mensile` | *«2.500 € sembra un importo mensile»* |
| `08-esperto-parametri` | anno, CCNL, mensilità, giorni in chiaro |
| `09-esperto-risultato-e-fonti` | pannello delle fonti con lo stato di verifica |
| `10-pannello-leggibilita` | le quattro leve |
| `11/12/13-visione-*` | la ripartizione nelle tre modalità di visione |
| `14-alto-contrasto` | riempimenti tenui sostituiti da bordi |
| `15-testo-molto-grande` | scala del testo al massimo |
| `16-tema-scuro` | tema scuro |
| `17-inverso-netto-mensile` | *«2.000 € netti al mese → RAL 40.101»* |
| `18-netto-ambiguo` | due RAL producono lo stesso netto |
| `19-netto-impossibile` | nessuna RAL produce quel netto |

### Diagrammi — `design/diagrammi/` (SVG vettoriali, modificabili in Figma)

- `curva-netto-discontinuita.svg` — la curva del netto con le sei
  discontinuità, l'ingrandimento sul gradino di Milano e l'elenco delle cause.
- `schermata-01-apertura.svg` — **schermata annotata** allo stato iniziale,
  modalità «alle prime armi», con dieci richiami numerati.
- `schermata-02-opzioni-aperte.svg` — **schermata annotata** in modalità
  esperto, pannello di leggibilità aperto e parametri avanzati visibili.

Le due schermate annotate sono **wireframe vettoriali**, non catture: importate
in Figma restano modificabili elemento per elemento, e i richiami sono oggetti
separati dal disegno. Vanno nella pagina **04 · Architettura e flussi**, o in
una pagina propria se si preferisce dare loro spazio.

Sono generate da [`strumenti/genera_schermate_annotate.py`](../strumenti/genera_schermate_annotate.py):
se l'interfaccia cambia, si rigenerano invece di essere ridisegnate a mano.

---

## Stili di colore da creare

Nomina gli stili così: gli stessi nomi sono usati nel codice, quindi il file e
il prodotto restano leggibili insieme.

### Marchio

| Nome stile | Valore | Uso | Misura |
|---|---|---|---|
| `marchio/inchiostro` | `#11150a` | testo principale | 18,5 : 1 su bianco |
| `marchio/lime` | `#dfeb57` | **solo fondi** | 1,3 : 1 su bianco |
| `marchio/su-lime` | `#11150a` | testo sul lime | 14,2 : 1 |
| `neutro/carta` | `#ffffff` | superfici |
| `neutro/sfondo` | `#f4f7ee` | fondo pagina |
| `neutro/bordo` | `#dce0da` | separatori |
| `testo/tenue` | `#4e5549` | testo secondario | 7,7 : 1 |
| `interazione/accento` | `#44660a` | collegamenti | 6,7 : 1 |

> Il lime a 1,3 : 1 è il dato che spiega tutta la sezione: è un colore di marca,
> non di lettura. Va messo in evidenza nella pagina 03.

### Serie dati — standard

| Nome | Valore | Voce |
|---|---|---|
| `serie/1-netto` | `#0a9184` | resta al dipendente |
| `serie/2-contributi` | `#d0552a` | contributi INPS |
| `serie/3-irpef` | `#3457c8` | IRPEF netta |
| `serie/4-regionale` | `#6f8f0a` | addizionale regionale |
| `serie/5-comunale` | `#9c3d8f` | addizionale comunale |

### Serie dati — daltonismo rosso-verde

`#0072b2` · `#d55e00` · `#56b4e9` · `#e69f00` · `#cc79a7`

### Serie dati — senza colore

`#262626` · `#454545` · `#646464` · `#838383` · `#a2a2a2`

---

## Pagina per pagina

### 01 · Il problema

**Titolo:** *Un numero sbagliato che sembra giusto*

Contenuto pronto:

> Usando un calcolatore esistente, da utente non esperta, ho inserito una RAL
> sbagliata per un dipendente: non era chiaro che il campo chiedesse il **lordo**.
> Nessun avviso ha intercettato l'errore.

Il difetto in tre punti, da impaginare come tre blocchi:

| | |
|---|---|
| **Silenzioso** | il risultato resta plausibile: nessuna cifra strilla |
| **Tardivo** | si scopre quando l'offerta è già partita |
| **Selettivo** | colpisce solo chi non è del mestiere, cioè chi lo strumento dovrebbe aiutare |

Confronto delle etichette, dalle quattro pagine pubbliche esaminate:

| Strumento | Etichetta del campo |
|---|---|
| Jet HR | `Stipendio (RAL)` |
| calcolastipendionetto.it | `Stipendio lordo annuale` |
| stipendee.it | `Retribuzione annua lorda (RAL)` |
| stipendiocalcolatore.it | `STIPENDIO LORDO ANNUALE` |

Chiusura: *tre su quattro scrivono «lordo» nell'etichetta. Uno lo affida a un
acronimo fra parentesi, accanto alla parola che nell'uso comune significa
«quanto prendo al mese».*

---

### 02 · La ricerca

**Titolo:** *Sei coefficienti sbagliati su sette*

| Voce | Trovato | Corretto |
|---|---|---|
| Seconda aliquota IRPEF | 35% | **33%** (L. 199/2025) |
| Taglio del cuneo fiscale | assente | due misure, fino a 1.000 € |
| Scaglioni regionali Lombardia | 5, soglie inventate | 4, allineati all'IRPEF |
| Esenzione comunale Milano | 21.000 € | **23.000 €** |
| Soglia +1% INPS | 55.008 € | 56.224 € |
| Detrazione 65 € | comma abrogato | art. 13 c. 1.1, da 25.000 |
| Aliquota INPS 9,19% | 9,19% | ✓ unico corretto |

Due riquadri da evidenziare:

**La trappola delle tabelle ufficiali.** Le tabelle dell'Agenzia delle Entrate
sono indicizzate per *modulistica*, non per anno d'imposta: la tabella
«modulistica 2026» contiene le aliquote dei redditi **2025**. Prendere quella
con l'anno che si cerca produce un'aliquota sbagliata di un anno, con l'aria di
essere una fonte ufficiale.

**7.792 comuni analizzati.** 85% aliquota unica, 15% a scaglioni; 36% con soglia
di esenzione, 64% senza; 116 soglie diverse, da 700 a 216.000 €. Fra due
territori, oltre **600 € l'anno** a parità di RAL.

---

### 03 · Il sistema di colore

**Titolo:** *Fedeli al marchio, leggibili da chi non distingue i colori*

Struttura consigliata su tre strati sovrapponibili, così si mostra l'evoluzione
accendendo e spegnendo:

```
strato 3 · senza colore      (grigi + trame)
strato 2 · daltonismo r-v    (blu / vermiglio / azzurro / ambra / rosa)
strato 1 · standard          (teal / terracotta / blu / oliva / prugna)
```

Il ragionamento, pronto:

> Una palette costruita attorno a un giallo-verde produce da sola la coppia
> oliva ↔ terracotta, che è **esattamente quella che il daltonismo rosso-verde
> collassa**. Quattro palette candidate sono state scartate per questo.

| Controllo | Soglia | Palette generica | Palette adottata |
|---|---|---|---|
| Separazione per daltonismo | ≥ 8 | 9,1 | **13,2** |
| Distinguibilità a vista normale | ≥ 15 | 19,6 | **25,7** |
| Toni sopra 3 : 1 di contrasto | tutti | 2 su 5 | **5 su 5** |

Immagini da usare: `11-visione-standard`, `12-visione-rosso-verde`,
`13-visione-senza-colore`, affiancate.

---

### 04 · Architettura e flussi

**Titolo:** *Non un sito con pagine: uno strumento con stati*

Le tre dimensioni indipendenti, da disegnare come diagramma:

```
                  il calcolatore
                        │
      ┌─────────────────┼─────────────────┐
  DIREZIONE        ESPERIENZA        LEGGIBILITÀ
   2 schede         2 livelli           4 leve
```

**La regola che le tiene insieme:** cambiare una qualsiasi impostazione non
perde mai quello che l'utente ha scritto.

I due percorsi principali:

```
«devo fare un'offerta»              «il candidato chiede 2.000 netti»
   RAL → eco → comune → calcola        netto → eco → comune → calcola
   → netto + voci → conferma           → RAL → se ambiguo, tutte le soluzioni
```

Due scelte di gerarchia da annotare, perché sono contro-intuitive:

- **La leggibilità sta in alto**, non in fondo: chi deve ingrandire il testo lo
  deve fare *prima* di leggere.
- **L'eco dell'input viene prima del numero**: è l'unico punto in cui un errore
  di inserimento diventa visibile.

---

### 05 · Gli stati dell'interfaccia

**Titolo:** *Nove stati, non due*

| Stato | Immagine |
|---|---|
| Vuoto | `01`, `04` |
| Interpretazione dell'input | `02` |
| Input non interpretabile | `06` |
| Risultato | `03`, `05` |
| Avviso di plausibilità | `07` |
| Modalità esperto | `08`, `09` |
| **Netto ambiguo** | `18` |
| **Netto impossibile** | `19` |
| Leggibilità | `10`, `14`, `15`, `16` |

Gli ultimi due meritano un riquadro: esistono perché **il netto non cresce con
continuità**. Nessuno dei quattro calcolatori esaminati li nomina — tutti li
calcolano correttamente, e tutti tacciono.

Qui va il diagramma `curva-netto-discontinuita.svg`.

---

### 06 · Evoluzione — prima e dopo

**Titolo:** *Sedici errori, e come sono venuti fuori*

Il grafico più utile della presentazione: **quale metodo di verifica ha trovato
cosa**.

| Metodo | Errori trovati |
|---|---|
| Ricerca sulle fonti | 1 |
| Scrittura ed esecuzione del codice | 3 |
| **Guasto deliberato dei dati** | 1 (tre test che non controllavano niente) |
| **Caricamento su un database vero** | 1 |
| **Una domanda posta** | 1 |
| **Un documento emesso da altri** | 2 |
| **Uso dell'interfaccia** | 3 |
| **Prova nel browser** | 2 |

Chiusura, da mettere in grande:

> Nessun metodo ha trovato gli errori di un altro.
> E **nessuno dei sedici** è stato trovato rileggendo il codice.

Coppie prima/dopo da impaginare affiancate:

| Prima | Dopo |
|---|---|
| `Stipendio (RAL)` | `RAL — Retribuzione Annua LORDA` + eco dell'input |
| `35.000` letto come 35 € | interpretazione mostrata mentre si digita |
| colori base generici | palette imparentata col marchio, validata |
| tema scuro imposto dal sistema | chiaro di default, scuro come scelta |
| nessuna alternativa al colore | tre modalità di visione |

---

### 07 · Cosa costruirei dopo

**Titolo:** *Dove sono i soldi*

In ordine di valore sbloccato:

**1. Le agevolazioni contributive.** Normativa già mappata:

| Norma | Misura |
|---|---|
| D.L. 30 aprile 2026 n. 62, circolari INPS 55/56/57 | esonero 100% under 35 svantaggiati: **500 €/mese per 24 mesi** (650 al Sud) |
| idem | donne con tre figli minori: **650 €/mese** (800 in ZES unica) |
| D.Lgs. 216/2023 | maxi-deduzione **120%**, **130%** per categorie tutelate |
| Art. 5 D.Lgs. 209/2023 | impatriati: tassato il **50%** del reddito (60% con figli minori) |

> È l'unico punto in cui il calcolo cambia di natura: smette di rispondere a
> *«quanto prende il dipendente»* e comincia a rispondere a **«quanto risparmia
> l'azienda»**. È la domanda che porta i soldi.

**2. Il costo per l'azienda** — l'altra metà della stessa domanda.
**3. Più territori** — la struttura c'è, ne mancano 7.790.
**4. Il confronto fra scenari** — due offerte affiancate.

---

## Nota da mettere nel file

> Documentazione di **processo**, non specifica. Il prodotto funzionante è nel
> repository e ha la precedenza in caso di discordanza. Composto il 7 agosto
> 2026.

Serve a evitare che il file venga letto come contratto sul comportamento del
prodotto: è il rischio di ogni documento di design fatto dopo la
realizzazione, e dichiararlo lo disinnesca.
