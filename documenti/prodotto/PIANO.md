# Product Builder — Calcolatore RAL → Netto

Piano di lavoro per il task Jet HR. Nome di lavoro: **product-builder**. Il nome
del prodotto lo decidiamo dopo.

> **Revisione 2** — dopo la ricerca sulle fonti (vedi [RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md))
> e le decisioni su stack, anno d'imposta e livelli d'esperienza.

---

## 1. Cosa chiede il task, e cosa valuta davvero

**Richiesta letterale:** una pagina web dove l'utente inserisce una RAL, preme
*Calcola*, e vede il netto annuale, il netto mensile e le tasse/trattenute.

**Cosa valutano davvero** (dal testo):

1. Saper **cercare le informazioni giuste dalle fonti giuste**.
2. Saper **strutturare** quelle informazioni in una soluzione.
3. Un **prototipo funzionante** su un caso semplice e standard.

E l'avvertimento esplicito: *non* conta saper usare Lovable o simili — conta aver
costruito qualcosa **di cui capisci le logiche e di cui sei in controllo**.

**Conseguenza sul come costruiamo:** niente scatola nera. Il motore è scritto a
mano, ogni coefficiente ha una fonte e una data accanto, e ci sono test su casi
noti. La differenza tra chi passa e chi no non è la UI: è poter spiegare, riga
per riga, perché quel netto è quel netto.

**La prova che il metodo funziona:** la prima stesura dei coefficienti conteneva
**sei errori su sette voci** — la seconda aliquota IRPEF ancora al 35% invece del
33%, il taglio del cuneo fiscale del tutto assente, gli scaglioni regionali
sbagliati. Il motore era logicamente corretto e numericamente falso. È il
racconto migliore che possiamo portare in interview: non "abbiamo azzeccato i
numeri", ma "abbiamo costruito il processo che li ha smascherati".

---

## 2. Il dominio: come si arriva dal lordo al netto

```
RAL (lordo annuo)
  − Contributi INPS a carico del dipendente (9,19% + 1% oltre la prima fascia)
  ─────────────────────────────────────────────────────────
  = Imponibile fiscale  (= reddito complessivo, nel caso semplice)

    IRPEF lorda (scaglioni 23 / 33 / 43%)
      − Detrazione per lavoro dipendente (art. 13 c. 1 TUIR)
      − Ulteriore detrazione 65 € (art. 13 c. 1.1)
      − Ulteriore detrazione cuneo fiscale (redditi 20.000–40.000)
  ─────────────────────────────────────────────────────────
  = IRPEF netta (mai sotto zero)

  − Addizionale regionale (a scaglioni oppure unica, secondo la regione)
  − Addizionale comunale (unica, con o senza soglia di esenzione)
  + Somma esente cuneo fiscale (redditi ≤ 20.000)
  + Trattamento integrativo (redditi ≤ 28.000, se c'è capienza)
  ─────────────────────────────────────────────────────────
  = Netto annuo
  ÷ mensilità (12 / 13 / 14, da CCNL) → Netto mensile
```

I valori esatti di ogni voce, con fonte e stato di verifica, stanno in
[RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md). Qui interessa la **sequenza**;
lì i **numeri**. Separarli è il punto di tutta l'architettura.

**Le due voci che è facile sbagliare** — e che nella prima stesura erano sbagliate:

- **Il taglio del cuneo fiscale** non è più uno sgravio contributivo: sotto i
  20.000 € è una *somma esente da IRPEF*, tra 20.000 e 40.000 € è una *ulteriore
  detrazione*. Vale fino a 1.000 € di netto sulla fascia più popolata.
- **Il trattamento integrativo** non si esaurisce a 15.000 €: prosegue ridotto
  fino a 28.000 €, e ha una condizione di capienza che lo azzera sotto la no-tax
  area.

> **Principio guida:** i numeri fiscali cambiano ogni anno. Nessun coefficiente
> viene scritto "a memoria" dentro il codice. Ognuno vive nel registro, con
> **fonte + data di verifica**. In interview, *"questo 33% viene dalla L. 199/2025"*
> vale più di un numero giusto senza provenienza.

---

## 3. Ambito e semplificazioni — dichiarate, non nascoste

**Date dal task:** impiegato a tempo indeterminato; domicilio a Milano; nessuna
agevolazione particolare.

Nota: il task dice *"puoi assumere"*, non *"devi assumere"*. Milano è un esempio
concesso, non un vincolo — per questo il territorio è un parametro (§4).

**Aggiunte da noi (da elencare nel README):**

- settore privato, aliquota contributiva standard 9,19%
- nessun carico familiare (niente detrazioni per coniuge/figli)
- nessun premio, benefit, fringe benefit, straordinario
- niente TFR nel calcolo del netto in busta (accantonato a parte)
- addizionali con l'aliquota base del comune/regione, senza agevolazioni locali
- il massimale contributivo si applica ai soli iscritti dal 1996: lo
  implementiamo ma lo segnaliamo come fuori dal caso standard
- proiezione su **anno pieno per default** (365 giorni di detrazione): nessun
  conguaglio, nessun cambio di datore in corso d'anno. I giorni sono un parametro
  opzionale (§4), non una costante
- **territorio predefinito Milano**, che è l'esempio del task ed è anche il caso
  modale (lo 0,80% è l'aliquota comunale più diffusa d'Italia, 53,2% dei comuni).
  Ma **la Lombardia sta vicino al minimo nazionale** dell'addizionale regionale:
  il risultato di Milano non va letto come "il netto italiano". A parità di RAL,
  una regione in piano di rientro sanitario costa oltre 600 € l'anno in più
- le **addizionali sono sottratte nell'anno del reddito**, mentre in busta paga
  vengono trattenute in undici rate nell'anno successivo: corretto per una
  proiezione annuale, ma il mensile non coincide al centesimo con una busta reale

Ogni semplificazione è una riga nel README con una motivazione di una frase. È
proprio ciò che il task dice che verrà *"discusso in un'eventuale interview"*.

---

## 4. Architettura

Tre strati, separati apposta perché la logica resti ispezionabile.

```
┌─────────────────────────────────────────────┐
│  React            interfaccia, due livelli  │
│                   esperto / alle prime armi │
└──────────────────────┬──────────────────────┘
                       │  HTTP/JSON
┌──────────────────────▼──────────────────────┐
│  FastAPI          validazione input         │
│  (Python)         motore = funzioni pure    │
└──────────────────────┬──────────────────────┘
                       │
┌──────────────────────▼──────────────────────┐
│  MySQL            registro dei coefficienti │
│                   anno · territorio · CCNL  │
│                   valore · fonte · data     │
└─────────────────────────────────────────────┘
```

**Perché Python nel mezzo:** il motore è già scritto e testato in Python, ed è il
linguaggio su cui siamo più solidi. Il calcolo non si riscrive in un linguaggio
meno padroneggiato solo per uniformità — il task premia il controllo, non la
moda dello stack.

**Perché MySQL si guadagna il posto.** Un calcolatore è in fondo una funzione
pura: un database potrebbe sembrare decorativo. Non lo è, se contiene la cosa
giusta. Il problema reale del dominio è che **i coefficienti cambiano ogni anno,
cambiano per territorio e vanno tracciati con la loro fonte**. Il registro rende
questo esplicito:

| campo | esempio |
|---|---|
| `anno` | 2026 |
| `territorio` | Lombardia / Milano — oppure `NAZIONALE` |
| `voce` | `irpef.scaglione_2.aliquota` |
| `valore` | 0.33 |
| `fonte` | L. 199/2025 (Legge di Bilancio 2026) |
| `data_verifica` | 2026-08-06 |
| `stato` | primaria / secondaria / aperta |

Così la parte amministrativa non è un CRUD messo lì per far vedere che sappiamo
usare un ORM: **è la risposta al problema che il dominio pone davvero.** E il
`stato` in tabella è ciò che rende onesta la ricerca del §1: l'interfaccia può
dire all'utente quali numeri sono confermati su fonte primaria e quali no.

**Come si amministra:** i coefficienti entrano da **migration e seed versionati
in git** — tracciabili e revisionabili come il codice — e una pagina
**`/coefficienti` di sola lettura** li espone tutti con valore, fonte, data di
verifica e stato. Niente CRUD con autenticazione: il task non chiede un gestionale,
e ogni ora spesa lì è un'ora sottratta al motore e all'interfaccia. La pagina di
sola lettura dimostra il valore del registro; il pannello di amministrazione
dimostrerebbe solo che sappiamo scrivere un login.

**I quattro parametri che diventano dati e non costanti:**

- **Anno d'imposta** — 2026 di default. Serve anche il 2025 per la validazione (§6).
- **Territorio** — Milano/Lombardia di default (l'esempio del task), Palermo/Sicilia
  per il banco di prova reale.
- **CCNL** — quattro contratti (**Commercio 14** mensilità come default, più
  Metalmeccanici, Studi professionali, Edilizia), e determina **solo le
  mensilità**, non i minimi tabellari.
  Non tocca il calcolo fiscale: la RAL è annua, quindi le mensilità cambiano solo
  il divisore del netto mensile, mai il netto annuo. In pagina va detto
  esplicitamente, perché è il primo equivoco del neofita.
- **Giorni di detrazione** — 365 di default, cioè il caso standard del task.
  Detrazioni art. 13, somma esente e trattamento integrativo sono per legge
  *rapportate al periodo di lavoro nell'anno*: renderle proporzionali ai giorni è
  una moltiplicazione, non logica nuova. Copre l'**assunzione infrannuale**, che
  per un HR è ordinaria amministrazione, e rende confrontabile una CU di periodo
  parziale (§6). Visibile solo in modalità esperto.

### Il motore deve reggere qualunque importo

Requisito non negoziabile: **il calcolo funziona a prescindere dalla cifra
inserita**. Non "funziona sui casi che abbiamo provato". Un calcolatore che si
comporta bene a 35.000 € e male a 19.999 € è peggio di uno rotto, perché il
difetto è invisibile.

Il dominio è pieno di **soglie**, e ogni soglia è un punto in cui il codice può
sbagliare di un centesimo o di mille euro:

| Soglia | Cosa scatta |
|---|---|
| 8.500 € | no-tax area / capienza del trattamento integrativo |
| 15.000 € | fine detrazione piena; cambio percentuale somma esente |
| 20.000 € | fine somma esente → inizio ulteriore detrazione |
| 23.000 € | esenzione addizionale comunale **(solo Milano)** |
| 25.000 / 35.000 € | detrazione aggiuntiva di 65 € |
| 28.000 € | secondo scaglione IRPEF; fine trattamento integrativo |
| 32.000 / 40.000 € | tratto decrescente della detrazione da 1.000 € |
| 50.000 € | terzo scaglione IRPEF; azzeramento detrazioni art. 13 |
| 56.224 € | +1% contributivo |
| 122.295 € | massimale contributivo |

**Come lo verifichiamo:** un test che attraversa ogni soglia a passi di un
centesimo (sotto, esatto, sopra), più una scansione continua da 0 a 200.000 € che
controlla le invarianti — netto mai superiore al lordo, IRPEF netta mai negativa,
somma delle voci sempre uguale al netto, nessun valore `NaN` o infinito.

> ⚠️ **Una scoperta che rompe un test esistente.** Il test attuale afferma che *"il
> netto annuo cresce sempre al crescere della RAL"*. Con l'esenzione di Milano
> implementata correttamente **è falso**: appena superati i 23.000 € di imponibile
> il netto **scende** di circa 184 €. Non è un bug nostro, è un gradino della
> norma. Il test va riscritto: monotòno **ovunque tranne** nei gradini previsti
> dalla configurazione, e i gradini devono cadere **esattamente** dove il registro
> dice. Così una discontinuità sconosciuta diventa un test fallito, invece di
> passare inosservata.

---

## 5. Interfaccia: chi la usa, e due livelli di esperienza

**Chi la usa.** Lo strumento guarda **avanti**: da una RAL ipotetica dice cosa
resta in tasca. Non certifica il passato — non è una CU, non è un cedolino.

Il task lo lascia intendere nel modo in cui è scritto: *"quanto è il netto che
percepisce **il dipendente** e quanto sono le tasse che **deve** pagare"*. Il
dipendente è in terza persona: chi usa lo strumento sta **ragionando su di lui**.
È il caso d'uso quotidiano di Jet HR — un HR o un imprenditore che valuta
un'offerta: *"se propongo 35k, quanto porta a casa questa persona?"*.

Quindi il taglio è **strumento HR**, con l'output però scritto in modo che resti
leggibile anche al dipendente che se lo calcola da solo. Un linguaggio, due
letture: è esattamente ciò che i due livelli qui sotto realizzano.

### Due direzioni di calcolo

Lo strumento risponde a **due** domande, non una:

| | Domanda | Come |
|---|---|---|
| **Lordo → netto** | *"Se propongo 35.000 € di RAL, quanto porta a casa?"* | il motore, diretto |
| **Netto → lordo** | *"Il candidato chiede 2.000 € netti al mese: che RAL devo offrire?"* | bisezione sulla stessa funzione |

La seconda è la domanda che un HR fa davvero quando tratta un'assunzione, e **non
richiede una riga di logica fiscale nuova**: il netto cresce in modo monotòno col
lordo (salvo i gradini noti, §4), quindi si trova la RAL per tentativi dimezzando
l'intervallo — poche righe sopra il motore che già esiste.

Ha però un valore che va oltre la comodità: **risolve alla radice** la confusione
lordo/netto descritta qui sotto, invece di limitarsi ad avvisarne. Chi ragiona in
netto non è più costretto a convertire a mente — ed è proprio la conversione a
mente che genera l'errore.

Le due direzioni sono due schede in cima alla pagina, mai due campi ambigui nello
stesso form.

### Il difetto osservato sul campo — da cui nasce tutto il resto

Non è una supposizione: usando uno strumento di calcolo esistente, da utente non
esperta, **è stata inserita una RAL sbagliata per un dipendente** perché non era
chiaro che il campo chiedesse il **lordo** e non il netto. L'errore non è stato
intercettato da nessun avviso.

È il difetto peggiore che un calcolatore di questo tipo possa avere, per tre
motivi: è **silenzioso** (il risultato resta plausibile), **si scopre tardi** —
tipicamente quando l'offerta è già partita — e colpisce **solo chi non è del
mestiere**, cioè proprio chi lo strumento dovrebbe aiutare.

Da qui quattro difese, che valgono in **entrambe** le modalità:

1. **L'etichetta non è mai ambigua.** Non "RAL" da solo, ma *"RAL — Retribuzione
   Annua **Lorda**"*, con "lordo" e "annua" evidenziati nel campo, non in un
   tooltip da scoprire.
2. **Il risultato ripete l'input.** Sopra il netto, sempre: *"Calcolato su
   35.000 € **lordi annui**"*. Se l'input era sbagliato, l'errore si vede nel
   momento in cui si legge la risposta, non tre mesi dopo.
3. **Controllo di plausibilità.** Un valore sotto i ~5.000 € è quasi certamente
   un **mensile**; uno in certe fasce può essere un **netto** scambiato per lordo.
   In quei casi l'avviso è esplicito: *"Sembra un importo mensile — la RAL è
   annua. Intendevi 30.000 €?"*, con la correzione applicabile in un clic.
4. **Aiuto in linea su ogni voce**, input e output: ogni riga ha il suo "cosa
   vuol dire", espanso di default per il neofita, a portata di hover per l'esperto.

> **Nota per la consegna.** Nel README questa sezione va scritta come *principio
> di progettazione* — "gli errori di input in questo dominio sono silenziosi e
> costosi, quindi l'interfaccia li previene attivamente" — non come critica a un
> prodotto specifico. L'aneddoto è forte, ma vale in conversazione, non in un
> repository pubblico.

### Il territorio non è un default silenzioso

La stessa logica vale — anzi, vale **di più** — per comune e regione. Un errore
sulla RAL almeno produce un numero strano; un errore sul territorio produce un
numero **corretto per la città sbagliata**, e non c'è nulla, nel risultato, che
possa insospettire.

Non è un dettaglio di configurazione, perché i territori **non si comportano allo
stesso modo** (vedi [RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md) §9):

|  | Milano / Lombardia | Palermo / Sicilia |
|---|---|---|
| Addizionale regionale | a scaglioni, 1,23 → 1,73% | aliquota unica 1,23% |
| Addizionale comunale | 0,80% **con esenzione** sotto 23.000 € | 1,014% (2025), **nessuna esenzione** |

Regole conseguenti:

1. **Il territorio è sempre visibile**, in entrambe le modalità, accanto alla RAL
   — non sepolto nelle opzioni avanzate. Milano è **preselezionato e dichiarato**
   (*"Milano — cambia"*), mai preselezionato in silenzio.
2. **Ogni voce territoriale porta con sé la sua provenienza** in output:
   *"Addizionale comunale (Milano, 0,80%)"*, non *"Addizionale comunale"*. Il
   numero non si stacca mai dal luogo che lo genera.
3. **Gli avvisi sono guidati dai dati del territorio, non cablati.** L'alert sulla
   soglia di esenzione deve comparire a Milano e **non** comparire a Palermo, dove
   quella soglia non esiste. Un avviso milanese mostrato a un utente palermitano
   sarebbe lo stesso identico difetto: un'informazione plausibile e falsa.

**Lo scenario milanese che a Palermo non esiste — e va reso esplicito.** La soglia
di Milano è una *soglia*, non una franchigia: sotto 23.000 € di imponibile non si
paga nulla, sopra si paga lo 0,80% **sull'intero imponibile**. Un centesimo in più
di imponibile costa **circa 184 €** di addizionale. È un gradino vero, e va detto
sia all'utente sia nella documentazione.

### Due livelli di esperienza

Uno switch **Alle prime armi / Esperto**, con lo stato ricordato e cambiabile in
qualsiasi momento — anche a metà compilazione, senza perdere gli input. Il caso da
coprire è chi si dichiara esperto, si blocca, e vuole tornare indietro senza
ricominciare.

| | **Alle prime armi** | **Esperto** |
|---|---|---|
| Input | uno solo: la RAL. Il resto ha default sensati, nascosti dietro "opzioni avanzate" | tutti i parametri in chiaro: anno, territorio, CCNL, mensilità, giorni di detrazione |
| Output | il netto in grande, poi le voci una alla volta | tabella completa, tutte le voci insieme |
| Spiegazioni | ogni voce ha un "cosa vuol dire" espandibile | assenti, disponibili in hover |
| Alert | attivi: RAL fuori scala, soglie appena superate, equivoci comuni | solo avvisi sostanziali |
| Fonti | nascoste | visibili accanto a ogni coefficiente, con stato di verifica |

**Gli alert che servono davvero** — non decorativi, ma quelli che intercettano un
malinteso vero:

- *"Il netto mensile è diviso per 14 mensilità, non 12: il netto annuo non cambia."*
- *"Con questa RAL sei appena sopra la soglia di esenzione dell'addizionale
  comunale: 100 € di lordo in più ne costano più di 100 in addizionale."*
- *"Questo importo non include TFR né tredicesima come voce separata: sono già
  dentro la RAL."*
- *"Il taglio del cuneo fiscale si azzera a 40.000 €: sopra questa soglia il netto
  cresce più lentamente."*

**Validazione input** (vale per entrambi i livelli): campo vuoto → nessun calcolo;
non numerico, negativo o zero → rifiutato con spiegazione; valori assurdi (5 € o
5.000.000 €) → avviso, ma si procede dichiarando che è fuori dal caso standard;
separatori misti (virgola/punto/migliaia) → normalizzati, non fatti esplodere.
Gli errori parlano in italiano semplice, mai con codici tecnici.

---

## 6. Validazione: cosa può dimostrare un documento reale, e cosa no

Confrontarsi con un altro calcolatore online dimostra solo che due prototipi
sbagliano allo stesso modo. Un documento reale è un metro più forte — ma va
usato per quello che può davvero misurare.

**Il documento è una Certificazione Unica, non un cedolino.** Un cedolino è un
mese e contiene ratei, conguagli e TFR che il modello non simula. La CU è annua
ed espone imponibile, IRPEF, detrazioni e addizionali nella stessa forma del
nostro output.

**Il vincolo che decide tutto: la CU disponibile copre un periodo di lavoro
parziale.** Detrazioni art. 13, somma esente e trattamento integrativo sono per
legge *rapportate ai giorni di lavoro nell'anno*. Una proiezione a 365 giorni
confrontata con una CU di pochi mesi darebbe uno scarto enorme — e sarebbe colpa
del confronto, non del motore.

Da qui la scelta dei giorni come parametro (§4). Con `giorni` impostato sul
periodo reale, la CU torna confrontabile per intero. Senza, resta comunque un
test parziale ma tutt'altro che inutile:

| Voce | Con 365 giorni | Con giorni reali | Perché |
|---|---|---|---|
| Contributi INPS | ✅ | ✅ | proporzionali: `contributi ÷ imponibile` = 9,19% a qualunque periodo |
| Imponibile fiscale | ✅ | ✅ | è lordo − contributi, nessuna annualizzazione |
| **IRPEF lorda** | ✅ | ✅ | gli scaglioni sull'imponibile reale devono dare l'imposta lorda della CU — **è il test della macchina progressiva, il cuore del motore** |
| Aliquote addizionali | ✅ | ✅ | rapporto addizionale/imponibile contro le tabelle Sicilia/Palermo |
| Detrazioni art. 13 | ❌ | ✅ | rapportate ai giorni |
| Cuneo fiscale e trattamento integrativo | ❌ | ✅ | rapportati ai giorni |
| Netto finale | ❌ | ✅ | dipende dalle precedenti |

Anche nella colonna peggiore restano validati contributi, imponibile e il motore
degli scaglioni: la parte meccanica dove gli errori sono silenziosi.

**Attenzione all'anno:** la CU è emessa nel 2026 ma riguarda i redditi **2025** —
quindi va confrontata con i coefficienti **2025**, seconda aliquota al **35%**,
non al 33%. È il motivo per cui l'anno vive nel registro: la validazione gira sul
2025, il prodotto risponde sul 2026. Confonderli farebbe fallire il test su un
motore corretto.

**Attenzione al territorio:** la CU è di un residente a **Palermo**. Le
addizionali sono quelle siciliane e palermitane, non milanesi. Il registro le
contiene entrambe, quindi non serve nessuna forzatura — ed è la dimostrazione che
parametrizzare il territorio non era teoria.

> ⚠️ **Privacy — regola ferma.** La CU contiene dati personali e **non entra nel
> repository**, in nessuna forma, nemmeno in un file ignorato. La validazione si
> esegue in locale. Nei CASI DI PROVA finiscono solo cifre arrotondate e prive di
> riferimenti personali, oppure un caso sintetico ricostruito che riproduce la
> stessa struttura. Da verificare esplicitamente prima del primo push.

Accanto al caso reale restano 3–4 RAL standard (25k, 35k, 50k, 70k) confrontate
con un calcolatore pubblico, come controllo di sanità.

---

## 7. Documentazione (parte del voto, non un extra)

- **README** — cos'è, come si usa, come si lancia, il link live.
- **METODOLOGIA** — la catena del §2 scritta per un lettore, con le fonti. Nasce
  da [RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md), che è già il grosso del lavoro.
- **ASSUNZIONI** — l'elenco del §3, ognuna motivata in una frase.
- **CASI DI PROVA** — il confronto con la CU (anonimizzato) e le RAL standard.
- **[DIARIO_DI_BORDO.md](../diario/DIARIO_DI_BORDO.md)** — cosa è andato storto, come ce ne
  siamo accorti, cosa è cambiato. Si scrive **man mano**, non alla fine: è il
  documento che rende verificabile la ricerca invece di limitarsi a dichiararla.
  Un coefficiente giusto e uno indovinato sono indistinguibili se guardi solo il
  risultato; diventano distinguibili solo mostrando il percorso.
- **[ERRORI.md](../verifiche/ERRORI.md)** — gli errori **nostri**, ordinati per il passaggio
  in cui sono nati e per il metodo che li ha scoperti. Il task chiede un
  prototipo *"di cui sei in controllo"*: essere in controllo non vuol dire non
  aver sbagliato, vuol dire sapere dove ha ceduto e come ce ne siamo accorti.
  È anche il materiale già pronto per la discussione in interview, con le
  domande scomode poste per prime da noi.
- **[ANALISI_USABILITA.md](../ux/ANALISI_USABILITA.md)** — dove si rompe un
  calcolatore fiscale per chi non è del mestiere, studiato su uno strumento
  reale e pubblico, con le scelte che ne discendono.

---

## 8. Consegna

**Il repo GitHub è il deliverable principale.** Il task lo consente
esplicitamente: *"repo GitHub, folder con i documenti, website live; come
preferisci"*. Non serve un dominio acquistato.

**Il link live è un di più, non un obbligo.** I piani gratuiti (Render, Fly.io e
simili) includono un sottodominio: pubblicare non costa nulla. Il vincolo reale
non è il dominio ma l'**affidabilità** — molti piani gratuiti sospendono il
servizio dopo inattività, e chi apre il link dopo giorni aspetta 30–60 secondi di
avvio. Su un link che verrà aperto una volta sola, è un rischio serio.

Quindi, in ordine:

1. **Il repo funziona**, con `docker compose up` che parte al primo colpo su una
   macchina pulita. Questa è la garanzia che non dipende da nessuno.
2. **README con screenshot** delle due modalità e del risultato, così il lavoro è
   leggibile anche senza eseguire niente.
3. **Deploy gratuito**, *se* si dimostra stabile a una prova fatta con qualche
   giorno di anticipo. Se il servizio si addormenta, il link non si manda: meglio
   un repo solido che un link che gira a vuoto.

**Ordine di lavoro:** prima farlo funzionare in locale, poi pubblicarlo. Su GitHub
ci va codice già verificato, non un cantiere.

> **Regola di attribuzione.** Il repository è lavoro personale dell'autrice.
> Nessun riferimento ad assistenti o strumenti di AI compare nei commit, nel
> README o nella documentazione — nessuna firma di co-autore, nessuna nota
> generata automaticamente. L'eventuale uso di strumenti verrà dichiarato
> dall'autrice di persona in sede di colloquio. Da verificare prima del primo
> push, inclusi i messaggi di commit.

**Email:** rispondere all'invito **senza cambiare l'oggetto**, con
**task@jethr.com in CC**, e il link nel corpo (no allegati).

---

## 9. Stato dei lavori

- [x] Ricerca fonti 2026 → [RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md)
- [x] Chiuse le 3 questioni fiscali bloccanti (cumulo, formula 32k–40k, fascia 65 €)
- [x] Ricerca aliquote Sicilia/Palermo → due forme diverse di addizionale
- [ ] Recuperare il set completo dei coefficienti **2025** (IRPEF al 35%) per la validazione
- [ ] Motore aggiornato: coefficienti corretti + cuneo fiscale + trattamento integrativo completo + giorni
- [ ] Validazione contro la CU reale
- [ ] Schema MySQL + seed
- [ ] Backend FastAPI
- [ ] Frontend React con i due livelli
- [ ] Documentazione
- [ ] Deploy e invio

**Ordine non negoziabile:** il motore non si dichiara finito finché non regge
contro la CU. Interfaccia e database vengono dopo — sono il modo di mostrare un
calcolo giusto, non un modo di renderlo giusto.

---

## 10. Questioni aperte

**Fiscali** — ✅ **tutte chiuse.** Cumulo, formula 32k–40k e fascia dei 65 € sono
risolte con riferimento normativo in [RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md).
Restano solo verifiche di conferma, non ostacoli.

**Di prodotto** — ✅ **tutte decise:**

| Decisione | Esito |
|---|---|
| Stack | React → FastAPI → MySQL |
| Anno d'imposta | 2026 (2025 nel registro, per la validazione) |
| Territorio | Milano/Lombardia default **visibile**; Palermo/Sicilia per il confronto CU |
| Mensilità | parametro 12/13/14, default 14 (Commercio) |
| Giorni di detrazione | parametro, default 365, solo in modalità esperto |
| Direzioni di calcolo | **due**: lordo → netto e netto → lordo |
| CCNL | 4 contratti, solo mensilità |
| Amministrazione | seed versionato + pagina `/coefficienti` di sola lettura |
| Consegna | repo GitHub; link live solo se stabile |
| Attribuzione | nessun riferimento a strumenti di AI nel repo (§8) |

**Il piano è chiuso. Si può scrivere il codice.**

Restano solo verifiche di conferma sulle fonti (elencate in
[RICERCA_FONTI.md](../ricerca/RICERCA_FONTI.md)) e il recupero del set 2025, che
non bloccano l'inizio del lavoro sul motore.
