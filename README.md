# Dalla RAL al netto

### → **[calcolo-netto-ral.onrender.com](https://calcolo-netto-ral.onrender.com)**

Digita una RAL e premi «Calcola». Nessuna installazione.

*Gira su un piano gratuito: se nessuno lo apre da un quarto d'ora, la prima
richiesta lo riaccende e può richiedere una ventina di secondi.*

Calcolatore della retribuzione netta di un dipendente a partire dalla RAL, con
il dettaglio di ogni trattenuta e la fonte normativa di ogni coefficiente.

Prototipo realizzato per la task di selezione Jet HR.

> **Prototipo indipendente.** Riprende l'identità visiva di Jet HR per mostrare
> come si inserirebbe nel loro prodotto, ma non è uno strumento ufficiale, non è
> collegato ai loro sistemi e non va usato per adempimenti reali.

---

## Provalo

```bash
docker compose up          # database
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cd web && npm install && npm run build && cd ..
.venv/bin/python -m uvicorn api.main:app
```

→ **http://127.0.0.1:8000**

I test del motore girano senza installare niente:

```bash
python3 test_motore.py     # 399 test, ~15 secondi, nessuna dipendenza

# Se hai clonato il repository e intendi modificarlo, attiva l'hook che
# blocca i commit quando i test non passano (una volta sola):
git config core.hooksPath .githooks
```

---

## Cosa fa, in trenta secondi

Impiegato del settore privato, tempo indeterminato, Milano, anno d'imposta 2026,
14 mensilità (CCNL Commercio):

| RAL | Netto annuo | Netto mensile | Trattenute |
|---|---|---|---|
| 25.000 € | 20.569,65 € | 1.469,26 € | 17,7% |
| 30.000 € | 23.425,52 € | 1.673,25 € | 21,9% |
| 35.000 € | 26.032,22 € | 1.859,44 € | 25,6% |

Per una RAL di 35.000 € la catena completa è:

```
  Retribuzione lorda                                35.000,00
− Contributi INPS (9,19%)                            3.216,50
  Imponibile fiscale                                31.783,50
  IRPEF lorda   28.000×23% + 3.783,50×33%            7.688,56
+ Detrazione lavoro dip.  1.910×(50.000−R)/22.000    1.581,52
+ Ulteriore detrazione art. 13 c. 1.1                   65,00
+ Detrazione taglio del cuneo fiscale                1.000,00
− IRPEF netta                                        5.042,03
− Addizionale regionale (Lombardia, a scaglioni)       454,98
− Addizionale comunale (Milano, 0,8%)                  254,27
═ NETTO ANNUO                                       26.032,22
```

Il calcolatore fa anche il percorso inverso: *«il candidato chiede 2.000 € netti
al mese, che RAL devo offrire?»* → **40.101,12 €**.

---

## Le quattro decisioni che contano

### 1. I coefficienti non stanno nel codice

Vivono in [dati/coefficienti.json](dati/coefficienti.json), ognuno con la norma
che lo fissa, la data di verifica e uno **stato dichiarato**: fonte primaria,
secondaria, o da verificare. Il motore contiene solo le regole; i numeri, che
sono l'unica cosa che cambia ogni anno, stanno altrove.

Non è teoria. La prima stesura aveva i coefficienti scritti a senso: alla
verifica, **sei gruppi su sette contenevano un errore** — fra cui la seconda
aliquota IRPEF ferma al 35% quando dal 2026 è 33%, e il taglio del cuneo fiscale
mancante del tutto. Il motore era logicamente corretto e numericamente falso.

### 2. Il territorio è obbligatorio, non un default silenzioso

Analizzando la tabella dell'Agenzia delle Entrate su **tutti i 7.792 comuni
italiani** ([strumenti/analisi_addizionali.py](strumenti/analisi_addizionali.py)):
l'85% usa un'aliquota unica, il 15% usa scaglioni; il 36% ha una soglia di
esenzione, il 64% nessuna. A parità di RAL, la differenza fra due territori
supera i **600 € l'anno**.

Un calcolo senza il comune è un calcolo incompleto, quindi il comune è sempre in
vista — anche in modalità semplificata.

*(Non è un vantaggio competitivo: altri calcolatori il comune lo chiedono già.
È il minimo per essere corretti. Vedi
[ANALISI_COMPETITIVA.md](documenti/ux/ANALISI_COMPETITIVA.md).)*

### 3. Perché codice e non una pagina generata

Per uno strumento usa-e-getta una pagina Lovable sarebbe stata la scelta giusta:
più veloce, e il risultato si vede subito. Qui non lo è per una ragione precisa:
**il problema di questo dominio non è calcolare, è che i numeri cambiano ogni
anno e vanno tracciati con la loro fonte**. È quella la parte che un generatore
non dà, ed è quella che rende lo strumento ancora corretto fra dodici mesi.

Il database non è decorativo per lo stesso motivo: contiene il registro dei
coefficienti con anno, territorio, fonte e stato di verifica — e i vincoli che
impediscono di inserirci dati incoerenti.

### 4. I colori: fedeli al marchio, leggibili anche da chi non li distingue

L'interfaccia riprende l'identità visiva di Jet HR — inchiostro `#11150a`,
accento lime `#dfeb57`, neutri verdati — ma **misurata prima di essere usata**.
Il lime su bianco vale 1,30 : 1 di contrasto: è un colore da **fondo**, non da
testo. Nel prototipo compare solo come superficie piena con inchiostro scuro
sopra, dove vale 14,23 : 1. Copiarlo dove capita avrebbe significato riprodurre
la forma perdendo la funzione.

La palette dei grafici nasce dallo stesso vincolo, con un'aggiunta: **restare in
famiglia con il lime senza diventare illeggibile per chi ha un deficit della
visione dei colori.** Le due cose tirano in direzioni opposte, e non è un
problema teorico — riguarda circa un uomo su dodici.

Una palette costruita attorno a un giallo-verde tende a produrre da sola la
coppia oliva ↔ terracotta, che è **esattamente quella che il daltonismo
rosso-verde collassa**. Quattro palette candidate sono state scartate proprio
per questo, prima che una passasse tutti i controlli.

Quella adottata — teal, terracotta, blu, **oliva** (il parente diretto del loro
accento), prugna — tiene le due tinte critiche lontane nell'ordine, e misura:

| Controllo | Soglia | Risultato |
|---|---|---|
| Separazione per daltonismo (peggior coppia adiacente) | ≥ 8 | **13,2** |
| Distinguibilità a vista normale | ≥ 15 | **25,7** |
| Contrasto sul fondo | ≥ 3 : 1 | **tutti e cinque** |

E comunque **nessuna informazione è affidata al solo colore**: ogni voce compare
nella legenda con nome e importo, la tabella sotto riporta tutte le cifre, e chi
ne ha bisogno può attivare le **trame** oltre alle tinte. Il colore è un aiuto,
mai l'unico canale.

---

## Dove è diverso dagli altri strumenti

Quattro calcolatori pubblici sono stati ispezionati **nel codice sorgente**, non
a impressione ([ANALISI_COMPETITIVA.md](documenti/ux/ANALISI_COMPETITIVA.md)). L'analisi ha
smontato tre dei quattro elementi che credevamo distintivi: il comune, le
citazioni normative e il calcolo inverso ce li hanno già.

Ne restano quattro, e su questi **quattro strumenti su quattro sono a zero**:

| | |
|---|---|
| **Dichiara quanto è sicuro di ogni dato** | fonte primaria, secondaria o da verificare, accanto a ogni coefficiente. Le aliquote comunali 2026 non hanno ancora una tabella ufficiale consolidata: chi le usa oggi sta usando delibere, e dirlo cambia il modo in cui un HR usa il numero |
| **Avvisa dove il dominio inganna** | superata la soglia comunale, cento euro di lordo in più ne costano 184 di netto; sotto una certa soglia il netto supera il lordo. Tutti calcolano correttamente questi effetti; nessuno li nomina |
| **È usabile da chi vede poco** | zero `aria-describedby` sui quattro strumenti esaminati. Qui l'aiuto è agganciato ai campi, e ci sono tre leve di leggibilità |
| **Si lascia verificare** | 399 test che girano senza installare niente, e strumenti che rieseguono le verifiche — compreso quello che guasta i coefficienti apposta per controllare che i test se ne accorgano |

Su **ampiezza di casi** Jet HR è avanti, e sull'anagrafica dei comuni lo sono
gli altri. Il posizionamento è più stretto di quello di partenza, ed è l'unico
sopravvissuto al controllo.

---

## Come è stato costruito

Parte del lavoro è stata svolta **con assistenza AI**, come previsto dal ruolo.
Le decisioni di scope, di stack e di priorità sono mie, così come le verifiche.

Vale la pena essere precisi su cosa questo significa, perché è il punto in cui
un lavoro assistito si distingue da un lavoro delegato: **nessun numero fiscale
è stato accettato perché proposto**. Ognuno è stato cercato sulla fonte, e
[ERRORI.md](documenti/verifiche/ERRORI.md) elenca i **ventisei casi in cui la verifica ha smentito
quello che era stato prodotto** — compresa una regola sui periodi di lavoro
parziali che sembrava più elegante ed era sbagliata, scoperta confrontando il
motore con una Certificazione Unica reale.

Quel registro è la parte del repository di cui vado più fiera: dice dove il
lavoro ha ceduto, con quale metodo se n'è accorto, e cosa è cambiato di
conseguenza.

### I metodi di verifica usati, e cosa ha trovato ciascuno

Nessuno di questi ha trovato gli errori di un altro. È la ragione per cui sono
tutti nel repository invece di essere sostituiti dal più comodo.

| Metodo | Come | Ha trovato |
|---|---|---|
| **Ricerca sulle fonti** | ogni valore cercato sull'atto, non ricordato | sei gruppi di coefficienti sbagliati su sette |
| **Test automatici** | 326, senza dipendenze, con i casi di riferimento calcolati a mano | la meccanica degli scaglioni, le soglie, le invarianti |
| **Guasto deliberato** | [controllo_sensibilita.py](strumenti/controllo_sensibilita.py) rompe un coefficiente alla volta e verifica che i test se ne accorgano | tre test che non controllavano niente |
| **Confronto con un documento reale** | [confronta_cu.py](strumenti/confronta_cu.py) contro una Certificazione Unica | una regola sui periodi parziali che 302 test non vedevano |
| **Caricamento su un database vero** | schema applicato a MySQL 8.4, con nove tentativi di inserire dati incoerenti | una chiave unica che non impediva i duplicati |
| **Validazione della palette** | ogni colore passato al controllo di separazione per daltonismo e contrasto | quattro palette candidate bocciate prima di trovarne una valida |
| **Prova nel browser a cinque larghezze** | 360, 390, 768, 1280 e 1600 pixel, con calcolo eseguito e ispezione del traboccamento orizzontale | importi formattati in due modi diversi nella stessa tabella |
| **Uso dell'interfaccia** | semplicemente usandola | i formati numerici italiani, e il tema scuro imposto |
| **Controllo di sicurezza** | richieste ostili costruite a mano contro l'API a codice finito ([SICUREZZA.md](documenti/verifiche/SICUREZZA.md)) | il server serviva qualunque file del progetto, compresa la cartella dei dati privati |
| **Revisione esterna** | il progetto dato in lettura a due revisori indipendenti, a lavoro considerato finito | **i 75 € di capienza del trattamento integrativo, mancanti dal registro** — più tre difetti di interfaccia |

L'ultima riga è quella che conta di più. **Le prime dieci righe di codice usate
da una persona vera hanno trovato in un minuto quello che centinaia di test non
cercavano** — perché i test li scrive chi già sa come si digita un numero.

Sulla verifica visiva, un esempio concreto: a schermo la stessa tabella
mostrava `1859,44 €` accanto a `26.032,22 €`. La formattazione italiana
automatica **omette il separatore delle migliaia sui numeri di quattro cifre**,
e in una colonna di importi che si leggono per confronto due convenzioni diverse
sono un invito a sbagliare riga. Non si vedeva leggendo il codice: si vedeva
guardando la pagina.

---

## Cosa non copre, e perché

Il task fissa il caso: *«impiegato a tempo indeterminato, vive a Milano, nessuna
agevolazione particolare»*. Fuori perimetro, **per istruzione ricevuta**:

| Non c'è | Perché |
|---|---|
| Agevolazioni contributive (Under 30, Donne, Over 50) | escluse dal testo del task |
| Regime impatriati, apprendisti under 21 | idem |
| Partita IVA e regime forfettario | fuori dal caso «dipendente» |
| Familiari a carico, mutuo, spese detraibili | fuori dal caso semplice |
| Costo per l'azienda | il task chiede il netto del dipendente |
| TFR nel netto in busta | accantonato, non erogato |

Due semplificazioni **misurate**, non stimate:

- l'aliquota contributiva usata è il 9,19% standard. In una busta paga reale del
  Commercio risulta il **9,457%**: 0,27 punti di contributi minori da CCNL, circa
  **93 € l'anno** su una RAL di 35.000 €;
- le addizionali sono sottratte nell'anno del reddito, mentre in busta paga si
  trattengono in undici rate nell'anno successivo. Corretto per una proiezione
  annuale; il mensile non coincide al centesimo con una busta reale.

L'elenco completo, con la motivazione di ognuna, è in
[ASSUNZIONI.md](documenti/prodotto/ASSUNZIONI.md).

---

## Cosa costruirei subito dopo

In ordine di valore sbloccato, non di difficoltà:

1. **Le agevolazioni contributive.** Under 30, Donne, Over 50, apprendisti: sono
   la leva con l'impatto economico più alto per un'azienda che assume, e la
   struttura per accoglierle c'è già — il registro tratta territorio e anno come
   dati, e un'agevolazione è un'altra dimensione dello stesso tipo. È anche
   l'unico punto in cui il calcolo passa da «quanto prende il dipendente» a
   «quanto risparmia l'azienda», che è la domanda che porta i soldi.
2. **Il costo per l'azienda**, l'altra metà della stessa domanda.
3. **Più territori.** Oggi ce ne sono due, scelti apposta perché hanno forme
   diverse di addizionale. La tabella dell'Agenzia ne contiene 7.792 e il
   caricamento è già scritto: è lavoro di dati, non di codice.
4. **Il confronto fra scenari** — due offerte affiancate, con la differenza di
   netto e di costo.

---

## La documentazione

Il codice è commentato in italiano, con le ragioni delle scelte accanto alle
scelte. Tutto il resto — ricerca, decisioni, verifiche, progettazione, diario —
sta in **[documenti/](documenti/)**, organizzato per area e con un percorso di
lettura in cima.

| Se hai | Leggi |
|---|---|
| **5 minuti** | [ASSUNZIONI.md](documenti/prodotto/ASSUNZIONI.md) — cosa lo strumento non fa, e perché |
| **20 minuti** | più [ERRORI.md](documenti/verifiche/ERRORI.md) — i ventisei errori, per metodo che li ha scoperti |
| **voglia di verificare** | [CASI_DI_PROVA.md](documenti/verifiche/CASI_DI_PROVA.md) — quattro RAL con il conto accanto, rifacibili a mano |
| **tempo** | [il dossier completo](documenti/) — fonti, prodotto, verifiche, UX, diario |


---

## Come è fatto

```
motore/       calcolo, in Python puro — nessuna dipendenza, nessuna nozione del web
  registro.py   dove stanno i coefficienti e come si leggono
  calcolo.py    le regole di calcolo, funzioni pure
  inverso.py    dal netto desiderato alla RAL
dati/         il registro dei coefficienti, versionato, con fonte e stato
database/     schema MySQL e seed generato dal registro
api/          FastAPI: traduce HTTP in chiamate al motore, non calcola nulla
web/          React: nessun dato fiscale, tutto arriva dall'API
strumenti/    verifiche riproducibili (vedi sotto)
test_motore.py  399 test, zero dipendenze
```

Tre strumenti di verifica, tutti rieseguibili:

- [strumenti/controllo_sensibilita.py](strumenti/controllo_sensibilita.py) —
  guasta un coefficiente alla volta e controlla che i test se ne accorgano.
  **14 guasti su 14 rilevati**; la prima esecuzione ne trovò 3 che passavano
  inosservati.
- [strumenti/analisi_addizionali.py](strumenti/analisi_addizionali.py) —
  l'analisi sui 7.792 comuni.
- [strumenti/confronta_cu.py](strumenti/confronta_cu.py) — confronto con una
  Certificazione Unica reale. I dati personali restano fuori dal repository.

---

## Licenza e attribuzioni

Codice e documentazione sono lavoro personale, realizzato per una selezione.
L'identità visiva richiama quella di Jet HR a scopo dimostrativo; marchi e
denominazioni appartengono ai rispettivi titolari.
