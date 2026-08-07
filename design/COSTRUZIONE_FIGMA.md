# Costruzione del file Figma

Le misure, la griglia, gli stili e la disposizione dei riquadri pagina per
pagina. I **contenuti** sono nella [guida](GUIDA_FIGMA.md); qui c'è come
montarli.

Tutto è dimensionato per essere costruito una volta e riusato: sei componenti
coprono l'intera presentazione, e ogni pagina è composizione di quelli.

---

## 1. Impostazione del file

**Formato dei riquadri: 1920 × 1080** (16:9). Si proietta, si condivide a
schermo e si esporta in PDF senza riadattare nulla. Una presentazione a
riquadri liberi costringe chi guarda a inseguire il puntatore.

```
Pagine (in ordine di racconto)
  00 · Sistema          ← stili, componenti, griglia. Non si presenta.
  01 · Il problema
  02 · La ricerca
  03 · Il sistema di colore
  04 · Architettura e flussi
  05 · Gli stati
  06 · Evoluzione
  07 · Cosa costruirei dopo
```

**Nomi dei riquadri:** `NN.M — titolo breve` (`03.2 — Le quattro palette`).
Il numero rende l'ordine leggibile nel pannello dei livelli, che è dove si
naviga davvero quando il file cresce.

**Griglia** — da salvare come stile e applicare a ogni riquadro:

| | |
|---|---|
| Colonne | 12 |
| Margine | 120 px |
| Distanza fra colonne | 24 px |
| Larghezza colonna | 118 px (calcolata) |
| Righe guida orizzontali | 96 px dall'alto (titolo), 240 px (contenuto), 96 px dal basso |

---

## 2. Scala tipografica

Sette stili, non di più. Una scala che ne ha quindici non è una scala: è un
elenco di eccezioni.

| Nome stile | Dimensione / interlinea | Peso | Uso |
|---|---|---|---|
| `Display` | 56 / 64 | 700 | titolo di pagina |
| `Titolo` | 40 / 48 | 700 | titolo di riquadro |
| `Sottotitolo` | 28 / 36 | 600 | occhiello, secondo livello |
| `Corpo` | 20 / 30 | 400 | testo corrente |
| `Corpo piccolo` | 16 / 24 | 400 | tabelle, didascalie lunghe |
| `Etichetta` | 14 / 20 | 700 | richiami — **maiuscolo, spaziatura +6%** |
| `Dato` | 72 / 72 | 700 | numeri grandi — **cifre tabulari** |

Carattere: quello di sistema (`Inter` in Figma è l'equivalente più vicino).
Nessun carattere display o graziato: il prodotto usa il sans di sistema, e il
file deve somigliargli.

**Spaziature** — solo questi valori: `8 · 16 · 24 · 32 · 48 · 64 · 96 · 128`.
Vietato l'occhio: se serve 37, serve 32 o 48.

---

## 3. I sei componenti

Costruiscili nella pagina `00 · Sistema`, poi usa solo istanze. Tutti con
disposizione automatica, così i testi lunghi non rompono l'impaginazione.

### `Richiamo`

Il più usato. Disposizione **orizzontale**, spazio 16, allineamento in alto.

```
┌───┐  ETICHETTA IN MAIUSCOLO        ← Etichetta, colore inchiostro
│ 3 │  una riga di perché             ← Corpo piccolo, colore tenue
└───┘
 ↑ cerchio 32 px, riempimento #0a9184, numero bianco 700
```

Larghezza: adattata al contenuto, massimo 320 px. Oltre, il richiamo diventa un
paragrafo con una freccia attaccata.

### `Dato`

Disposizione **verticale**, spazio 8.

```
26.032,22 €     ← Dato, cifre tabulari
NETTO ANNUO     ← Etichetta, colore tenue
su 14 mensilità ← Corpo piccolo, colore tenue
```

### `Confronto`

Due colonne affiancate, disposizione **orizzontale**, spazio 48, larghezze
uguali (`fill`).

```
┌─────────────────────┐   ┌─────────────────────┐
│ PRIMA               │   │ DOPO                │
│ ───────────────     │   │ ───────────────     │
│ contenuto           │   │ contenuto           │
└─────────────────────┘   └─────────────────────┘
  bordo 1 px #dce0da        bordo 2 px #11150a
  riempimento bianco        riempimento #f6f9cf
```

Il **dopo** è più marcato del **prima**: la gerarchia visiva deve dire da sola
qual è la conclusione.

### `Campione colore`

Disposizione **orizzontale**, spazio 16, allineamento centrale.

```
▇▇▇▇  serie/1-netto      #0a9184   resta al dipendente
 ↑ 64 × 40, raggio 6, bordo 1 px rgba(17,21,10,.15)
```

### `Citazione`

Barra verticale lime a sinistra (larghezza 6, altezza piena), riempimento
`#f6f9cf`, spaziatura interna 32, raggio 8. Testo in `Corpo`.

### `Intestazione pagina`

Disposizione **verticale**, spazio 16, ancorata a 96 px dall'alto.

```
02 · LA RICERCA          ← Etichetta, colore #0a9184
Sei coefficienti         ← Display
sbagliati su sette
una riga di contesto     ← Corpo, colore tenue, larghezza max 8 colonne
```

---

## 4. Colori da creare come stili

Vedi la [guida](GUIDA_FIGMA.md) per i valori. Organizzali in quattro gruppi,
che è il modo in cui Figma li mostra a cartelle:

```
marchio/    inchiostro · lime · su-lime
neutro/     carta · sfondo · bordo
testo/      principale · tenue · muto
serie/      1-netto … 5-comunale   (+ le due varianti daltonismo e senza colore)
```

---

## 5. Disposizione, pagina per pagina

Le coordinate sono dentro il riquadro 1920 × 1080. `C1…C12` sono le colonne.

---

### 01 · Il problema — tre riquadri

**`01.1 — L'errore`**

```
┌────────────────────────────────────────────────────────────┐
│ y=96    01 · IL PROBLEMA                                   │
│ y=136   Un numero sbagliato                                │  Display
│         che sembra giusto                                  │
│                                                            │
│ y=340   ┌── Citazione, C1–C7 ────────────────────────────┐ │
│         │ «Ho inserito una RAL sbagliata per un          │ │
│         │  dipendente: non era chiaro che il campo       │ │
│         │  chiedesse il lordo.»                          │ │
│         └────────────────────────────────────────────────┘ │
│                                                            │
│ y=620   SILENZIOSO        TARDIVO         SELETTIVO        │  tre `Richiamo`
│         il risultato      si scopre a     colpisce chi        senza cerchio,
│         resta plausibile  offerta partita non è del mestiere  C1-C4 / C5-C8 / C9-C12
└────────────────────────────────────────────────────────────┘
```

**`01.2 — Le quattro etichette`**
Tabella a quattro righe, C2–C11, righe alte 88. La riga di Jet HR marcata con
riempimento `#f6f9cf`. Sotto, in `Sottotitolo`: *tre su quattro scrivono
«lordo»*.

**`01.3 — Il costo`**
Un solo `Dato` gigante centrato: **1 errore · 1 persona · 1 contratto**, e sotto
una riga in `Corpo`.

---

### 02 · La ricerca — quattro riquadri

**`02.1 — Sei su sette`**
Tabella C1–C12, sette righe alte 72. Colonna «trovato» in colore tenue con
barratura, colonna «corretto» in inchiostro 700. L'ultima riga (9,19% corretto)
in verde `#1a7a3c`.

**`02.2 — La trappola delle tabelle`**
Diagramma a due colonne:

```
   modulistica 2025  ──→  redditi 2024
   modulistica 2026  ──→  redditi 2025      ← evidenziata
```
Sotto, `Citazione` con l'avvertenza.

**`02.3 — 7.792 comuni`**
Quattro `Dato` in fila: **85%** aliquota unica · **15%** a scaglioni · **36%**
con soglia · **64%** senza. Sotto: *116 soglie diverse, da 700 a 216.000 €*.

**`02.4 — Oltre 600 € l'anno`**
Barra di confronto fra due territori a parità di RAL.

---

### 03 · Il sistema di colore — tre riquadri

**`03.1 — Il lime misurato`**
Due `Confronto` affiancati:

```
lime su bianco        inchiostro su lime
   1,30 : 1              14,23 : 1
 non leggibile          perfettamente leggibile
```
Conclusione in `Sottotitolo`: *è un colore da fondo, non da testo*.

**`03.2 — Le quattro palette scartate`**
Quattro righe da cinque `Campione colore`, ognuna con l'esito a destra in rosso
`#a8341f`: *bocciata — oliva ↔ terracotta collassa*. La quinta riga, in verde:
*adottata*.

> È il riquadro che dimostra il metodo. Mostrare i tentativi falliti vale più
> del risultato: il risultato da solo sembra una scelta di gusto.

**`03.3 — Le tre modalità`**
**Tre strati sovrapponibili**, stessa posizione e dimensione, nomi:

```
▸ strato · senza colore     (nascosto)
▸ strato · daltonismo r-v   (nascosto)
▸ strato · standard         (visibile)
```
Dentro ciascuno, l'immagine corrispondente (`11/12/13-visione-*`). Si presenta
accendendo e spegnendo: è l'unico modo per far vedere che **la struttura non
cambia, cambia solo il canale**.

---

### 04 · Architettura e flussi — tre riquadri

**`04.1 — Tre dimensioni indipendenti`** — il diagramma ad albero.

**`04.2 — Schermata all'apertura`** — importa
`schermata-01-apertura.svg`, scala al 78% e centra. Le annotazioni sono già
dentro: **sciogli il gruppo una volta sola** (`Ungroup`) e diventano livelli
modificabili.

**`04.3 — Schermata con le opzioni aperte`** — idem con
`schermata-02-opzioni-aperte.svg`.

---

### 05 · Gli stati — due riquadri

**`05.1 — Nove stati`**
Griglia 3 × 3 di riquadri 400 × 260, spazio 32. Ogni cella: cattura ridotta +
`Richiamo` con il nome dello stato. Le due celle **netto ambiguo** e **netto
impossibile** con bordo 2 px inchiostro.

**`05.2 — Perché esistono`**
Il diagramma `curva-netto-discontinuita.svg` a piena larghezza, C1–C12.
Sotto, una riga in `Sottotitolo`: *nessuno dei quattro calcolatori esaminati li
nomina*.

---

### 06 · Evoluzione — tre riquadri

**`06.1 — Sedici errori`**
Barre orizzontali, una per metodo di verifica, lunghezza proporzionale agli
errori trovati. Ordinate per quantità.

**`06.2 — La riga che conta`**
Un solo riquadro di testo centrato, `Display`:

> Nessun metodo ha trovato gli errori di un altro.
> Nessuno dei sedici è stato trovato rileggendo il codice.

Niente altro nel riquadro. Una pagina con una frase sola pesa più di una piena.

**`06.3 — Prima e dopo`**
Cinque `Confronto` impilati, spazio 32.

---

### 07 · Cosa costruirei dopo — due riquadri

**`07.1 — Dove sono i soldi`**
Quattro righe con la norma a sinistra (C1–C4, `Corpo piccolo` tenue) e la misura
a destra (C5–C12, `Sottotitolo`). I numeri — 500 €/mese, 650 €, 120%, 50% — come
`Dato` piccolo.

**`07.2 — Il salto`**
Due riquadri affiancati:

```
oggi risponde a           domani risponderebbe a
«quanto prende            «quanto risparmia
 il dipendente»            l'azienda»
```
Il secondo con riempimento lime. Sotto: *è la domanda che porta i soldi*.

---

## 6. Ordine di costruzione

Costruire in quest'ordine fa risparmiare i rifacimenti:

1. **Stili** — colori, poi tipografia, poi griglia. Prima di qualsiasi riquadro.
2. **I sei componenti** nella pagina `00`.
3. **Un riquadro completo** — consigliato `03.1`, che usa `Confronto`,
   `Intestazione pagina` e `Dato`. Se funziona quello, funziona tutto.
4. **Le pagine 01 → 07**, in ordine.
5. **Gli SVG** per ultimi: si importano e si posizionano, non richiedono
   decisioni.
6. **Rilettura in vista prototipo** a schermo intero: gli errori di
   impaginazione si vedono lì, non nel piano di lavoro.

---

## 7. Esportazione e condivisione

| Cosa | Come |
|---|---|
| Link da mandare | condivisione **in sola lettura**, «chiunque abbia il link» |
| PDF di scorta | esporta tutti i riquadri a 2×, un file solo |
| Copertina | il riquadro `01.1` |
| Nota nel file | *documentazione di processo, non specifica — il prodotto funzionante è nel repository* |

**Nel repository** va il link al file. **Nel file** va il link al repository e
all'applicazione. Chi arriva da una parte deve poter raggiungere l'altra senza
chiedere.

### Come finisce dentro il repository

Figma è un servizio in cloud: non esiste un modo sensato di versionarlo in Git.
Il file `.fig` è un blocco binario che Git non sa confrontare e che non si apre
senza un account. Ma **mettere solo il link significa che il giorno in cui quel
link smette di funzionare — permessi cambiati, spazio di lavoro chiuso, piano
scaduto — la parte di progettazione del lavoro sparisce.**

Quindi entrambe le cose, senza che la seconda dipenda dalla prima:

| Cosa va nel repository | Dove | A cosa serve |
|---|---|---|
| **PNG di ogni riquadro**, 2× | `design/figma/riquadri/` | GitHub li mostra **in pagina**, senza account e senza scaricare niente. È la copia che sopravvive al link. |
| **PDF** di tutta la presentazione | `design/figma/presentazione.pdf` | Per chi la vuole leggere di seguito o stampare. GitHub lo apre nel browser. |
| **`.fig`** (*File → Salva copia locale*) | `design/figma/progetto.fig` | Archivio: permette di riaprire il file se l'originale si perde. Non si legge da GitHub. |
| **Link Figma** in sola lettura | in cima al [README](../README.md) | Per chi vuole vedere i **livelli** — cioè come è costruito, che è il punto. |

Poi, una volta sola:

```
python3 strumenti/genera_presentazione.py
```

Legge i PNG in `design/figma/riquadri/`, li ordina come vanno guardati e scrive
`design/PRESENTAZIONE.md`: ogni riquadro con il suo titolo, raggruppato per
pagina. Chi apre il repository vede la presentazione scorrendo, senza cliccare
niente. Rifarla dopo una modifica costa un comando.

**Sul peso.** GitHub avvisa sopra i 50 MB per file e rifiuta sopra i 100. Un
`.fig` con dentro venti immagini a 2× ci arriva più in fretta di quanto sembri:
se supera la soglia, si esporta a 1× invece che a 2× — la leggibilità a schermo
resta, e il PDF di scorta copre chi vuole ingrandire.

---

## 8. Se il tempo stringe

Nell'ordine in cui taglierei, se restassero poche ore:

| Priorità | Riquadri | Perché |
|---|---|---|
| **Irrinunciabili** | `01.1`, `02.1`, `03.2`, `06.2` | il problema, la ricerca, il metodo, la conclusione |
| Importanti | `03.3`, `05.2`, `07.1` | accessibilità, discontinuità, dove sono i soldi |
| Utili | `04.2`, `04.3`, `06.3` | già pronti come SVG, costano solo posizionamento |
| Sacrificabili | `01.3`, `02.4`, `05.1` | ripetono cose dette altrove |

Quattro riquadri raccontano già tutta la storia. Ventuno la raccontano meglio,
ma **una presentazione incompleta e curata batte una completa e affrettata**.
