# Registro degli errori

Ogni errore commesso durante la costruzione di questo prototipo, **il passaggio
in cui è stato commesso**, e come è venuto fuori.

Non è un elenco di bug corretti: quello lo racconta il diario. Qui interessa
un'altra domanda, più utile: **in quale momento del lavoro si sbaglia, e quale
tipo di verifica trova quel tipo di errore.** Perché la risposta, alla fine, è
che ogni metodo di verifica ha trovato errori che nessun altro metodo avrebbe
trovato — e la conseguenza pratica è che non se ne può usare uno solo.

Il [diario di bordo](DIARIO_DI_BORDO.md) racconta la stessa storia in ordine
cronologico, mescolata alle scoperte sul dominio. Qui restano soltanto **gli
errori nostri**.

## Perché questo file fa parte della consegna

Il task chiede un prototipo *"di cui hai capito le logiche e di cui sei in
controllo"*. Essere in controllo di qualcosa non significa non aver sbagliato:
significa **sapere dove ha ceduto, come ce ne siamo accorti, e cosa è cambiato
nel modo di lavorare di conseguenza**.

Un repository che mostra solo il risultato finale chiede di essere creduto sulla
parola. Le stesse ventitré voci qui elencate sono la prova che il controllo
c'è stato davvero: ognuna ha una data, un metodo che l'ha scoperta e una
correzione verificabile. Nessuna è stata trovata a posteriori per riempire un
documento — il registro è cresciuto insieme al codice, ed è per questo che
contiene anche errori scomodi, come una regola sbagliata che era stata scelta
apposta perché sembrava più elegante.

C'è anche una ragione pratica. Il testo del task dice che le semplificazioni
verranno *"discusse in un'eventuale interview"*: questo file è il materiale di
quella conversazione già preparato, con le domande difficili poste per primi da
noi invece che da chi legge.

---

## Quadro d'insieme

| # | Errore | Passaggio in cui è nato | Trovato da |
|---|---|---|---|
| 1 | Sei coefficienti sbagliati su sette | prima stesura del motore | ricerca sulle fonti |
| 2 | Somma esente collocata nel punto sbagliato della catena | stesura del piano | scrittura del codice |
| 3 | Invariante falsa: "il netto non supera il lordo" | scrittura delle invarianti | esecuzione sul motore |
| 4 | Test di monotonìa che affermava il falso | test della prima stesura | ragionamento sulle soglie |
| 5 | Tre test che non controllavano niente | scrittura della suite | **guasto deliberato dei dati** |
| 6 | Chiave unica inefficace sui valori NULL | progettazione dello schema | **caricamento su un database vero** |
| 7 | Strumento di verifica che si fabbricava la risposta | progettazione della verifica | **una domanda dell'autrice** |
| 8 | Regola uniforme sui periodi parziali | decisione di semplificazione | **un documento reale (CU)** |
| 9 | Minimo di 690 € non rapportato ai giorni | implementazione delle detrazioni | **un documento reale (CU)** |
| 10 | Analisi fondata su un riassunto invece che sulla fonte | ricerca sul prodotto esistente | rilettura sospettosa |
| 11 | Punteggiatura rovinata nel messaggio anti-errore | scrittura degli avvisi | esecuzione |
| 12 | **Numeri italiani letti male: `35.000` = 35 €** | validazione dell'ingresso | **uso dell'interfaccia** |
| 13 | Tema scuro inventato e non scavalcabile | identità visiva | **uso dell'interfaccia** |
| 14 | Importi formattati in due modi nella stessa tabella | formattazione dei numeri | **prova nel browser** |
| 15 | Un blocco di CSS cancellato da una modifica automatica | manutenzione del foglio di stile | **prova nel browser** |
| 16 | Controlli il cui effetto era invisibile finché non si calcolava | progettazione dei controlli | **uso dell'interfaccia** |
| 17 | **Il server serviva qualunque file del progetto** | rotta per l'interfaccia compilata | **controllo di sicurezza** |
| 18 | Il motore accettava importi assurdi e cifre non latine | validazione dell'ingresso | **controllo di sicurezza** |
| 19 | Il database affacciato su tutta la rete locale | configurazione di Docker | **controllo di sicurezza** |
| 20 | **Il calcolo inverso non sapeva leggere i numeri italiani** | correzione dell'errore 12 | **revisione esterna** |
| 21 | **Trattamento integrativo: mancavano i 75 € della capienza** | ricerca sulle fonti | **revisione esterna** |
| 22 | La frase di conferma spezzata in colonne da un `display: flex` | stesura del foglio di stile | **revisione esterna** |
| 23 | Gli importi tagliati sul telefono, senza che nulla lo segnalasse | tabella responsive | **revisione esterna** |

Ventitré errori. **Nessuno è stato trovato rileggendo il codice.**

---

## Gli errori, per passaggio

### Passaggio: prima stesura del motore

#### 1. Sei coefficienti sbagliati su sette

Il motore è nato con la logica corretta e i numeri riempiti "a senso", ognuno
marcato `DA VERIFICARE`. Alla verifica, su sette gruppi di coefficienti sei
contenevano almeno un errore:

| Voce | Scritto | Corretto |
|---|---|---|
| Seconda aliquota IRPEF | 35% | **33%** (L. 199/2025) |
| Taglio del cuneo fiscale | assente | due misure, fino a 1.000 € |
| Scaglioni regionali Lombardia | 5, soglie a 55k e 75k | 4, soglie 15k/28k/50k |
| Esenzione comunale Milano | 21.000 € | **23.000 €** |
| Soglia +1% INPS | 55.008 € | 56.224 € (2026) |
| Detrazione 65 € | art. 13 c. 1-*bis*, da 28k | **c. 1.1**, da 25k |
| Trattamento integrativo | fino a 15k | fino a 28k |

**La distinzione che conta:** cinque erano valori *veri per un altro anno*. Uno
— la soglia di Milano — non corrispondeva a nessun anno: era inventato. Da qui
la decisione di **riprendere ogni valore da zero invece di aggiornarlo**, perché
correggere presuppone che il punto di partenza abbia un senso.

Il motore era **logicamente corretto e numericamente falso**: il codice
funzionava, i test passavano, il risultato sembrava ragionevole. Mancava solo
che fosse vero.

→ diario, voci 1–8

---

### Passaggio: stesura del piano

#### 2. La somma esente nel punto sbagliato della catena

Il diagramma del piano metteva la somma esente del cuneo fiscale come
sottrazione dall'imponibile, prima dell'IRPEF. È invece **denaro corrisposto in
più**, che si somma al netto.

L'errore nasce da due misure con nomi simili e natura opposta:

| Misura | Redditi | Cosa fa |
|---|---|---|
| Somma esente | ≤ 20.000 € | si **aggiunge al netto** |
| Ulteriore detrazione | 20.000–40.000 € | **abbatte l'IRPEF** |

Trattarla come deduzione sbaglia **due volte nella stessa direzione**: abbassa
l'IRPEF che non doveva abbassare e non aggiunge al netto quello che doveva
aggiungere.

**Trovato scrivendo il codice**: implementare una regola costringe a decidere
dove va ogni voce, e a quel punto l'ambiguità del diagramma è emersa da sola.

→ diario, voce 20

---

### Passaggio: scrittura dei test

#### 3. Un'invariante falsa: "il netto non può superare il lordo"

Sembrava ovvia. Il motore l'ha smentita: fra **9.002 € e 11.959 €** di RAL il
netto è **maggiore** del lordo. È corretto — somma esente e trattamento
integrativo sono denaro corrisposto in più, non sconti d'imposta, e a quei
livelli superano le trattenute.

**Il rischio evitato:** vedere il test fallire e "correggere" un motore giusto.
È il modo più insidioso di introdurre un difetto — partendo da un'intuizione
ragionevole e sbagliata.

Il fenomeno è ora un test che lo **pretende**, con il commento che spiega perché
non va aggiustato.

#### 4. Un test di monotonìa che affermava il falso

*"Il netto annuo cresce sempre al crescere della RAL"* è falso: la soglia di
esenzione comunale di Milano fa **scendere** il netto di 183,40 € quando la si
supera. Il test è diventato: monotòno **ovunque tranne** nei gradini previsti
dalla configurazione, e i gradini devono cadere esattamente dove il registro
dice.

#### 5. Tre test che non controllavano niente

La suite contava 208 test verdi. Guastando il registro un valore alla volta —
quattordici guasti — **tre non hanno fatto fallire nulla**:

- rimuovere la soglia di esenzione di Milano
- azzerare le percentuali della somma esente
- inventare due scaglioni regionali in più

**La causa era strutturale.** I test ricavavano le soglie attese **dal registro
stesso**: cambiando il dato si spostavano insieme l'aspettativa e il
comportamento, e il confronto tornava. *Un test che si adatta a ciò che dovrebbe
controllare non controlla niente.*

Corretto con una sezione di **ancoraggi** — i valori da fonte primaria scritti a
mano nel test, l'unico punto che non può derivare da ciò che verifica — e due
casi di riferimento in più, a reddito basso e alto.

**Trovato guastando i dati di proposito.** Nessuna rilettura avrebbe mostrato
che tre test erano decorativi: erano verdi, e la ragione per cui erano verdi non
si vede leggendoli.

→ diario, voci 14, 26, 28

---

### Passaggio: progettazione del database

#### 6. La chiave unica che non impediva i duplicati

Nove tentativi di inserire dati illegali; otto respinti, uno accettato: **due
scaglioni IRPEF identici**.

In SQL **due NULL non sono uguali fra loro**. La chiave unica includeva
`territorio`, che per gli scaglioni IRPEF è `NULL` perché l'IRPEF è nazionale:
il database non li considerava duplicati.

**Cosa sarebbe costato:** un duplicato non genera errori, genera un'imposta
sbagliata. Due volte lo scaglione al 23% significa tassare due volte i primi
28.000 €, e il risultato resta plausibile.

Chiuso con una colonna generata che sostituisce il NULL con un valore
convenzionale.

**Trovato caricando lo schema su un MySQL vero e provando a violarlo.** Leggere
il `CREATE TABLE` non lo mostrava: la regola sui NULL è del motore, non della
sintassi.

→ diario, voce 34

---

### Passaggio: progettazione degli strumenti di verifica

#### 7. Uno strumento di confronto che si fabbricava la risposta

Lo strumento per confrontare il motore con una Certificazione Unica ricostruiva
una "RAL equivalente" sommando i contributi all'imponibile dichiarato dalla CU.
Risultato: la riga *"imponibile fiscale"* tornava **per costruzione**, perché il
dato della CU era stato usato per fabbricare l'ingresso del motore.

È lo **stesso identico difetto dell'errore n. 5**, in un altro punto del
progetto e a poche ore di distanza. Due volte in un giorno non è una
distrazione: è un modo di ragionare da sorvegliare.

Corretto con due modalità dichiarate: **completa** quando la CU dichiara
l'imponibile previdenziale (che è il lordo vero, e non si ricostruisce niente),
**solo fiscale** quando c'è solo l'imponibile — e in quel caso lo strumento
**scrive a schermo** che il passo contributivo non è verificato, invece di far
credere di averlo controllato.

**Trovato da una domanda:** *"ma noi lavoriamo sulla RAL, perché la CU?"*.

→ diario, voce 33

---

### Passaggio: decisione di semplificazione

#### 8. Una regola uniforme dove la legge non è uniforme

Per i periodi di lavoro parziali avevo stabilito che **tutte** le soglie si
valutassero sul reddito annualizzato. Sembrava più coerente e più facile da
spiegare.

Su un rapporto di 40 giorni il motore dava **zero** dove il sostituto d'imposta
aveva riconosciuto sia la detrazione sia il trattamento integrativo.

La regola vera è **doppia**:

| Voce | Guarda il reddito |
|---|---|
| Detrazione art. 13, ulteriore 65 €, trattamento integrativo | **effettivo** |
| Taglio del cuneo fiscale | **annualizzato** |

**Il documento le conferma entrambe, che sono opposte:** riconosce la detrazione
*e* non eroga la somma esente. Se la regola fosse uniforme in un senso la somma
esente sarebbe stata pagata; se lo fosse nell'altro la detrazione non ci
sarebbe.

#### 9. Il minimo di 690 € non rapportato ai giorni

Il minimo della detrazione di fascia 1 veniva applicato per intero anche sui
periodi brevi. Le annotazioni della stessa CU lo dicono a lettere: *"la
detrazione minima è stata ragguagliata al periodo di lavoro"*, e il minimo
intero si recupera in sede di dichiarazione — che questo prototipo non simula.

**Entrambi trovati da un documento emesso da qualcun altro.** 302 test non li
avevano visti, perché erano scritti dalla stessa testa che aveva stabilito la
regola sbagliata. Un documento esterno è l'unica cosa che rompe quel cerchio.

→ diario, voce 35

---

### Passaggio: ricerca sul prodotto esistente

#### 10. Un'analisi fondata su un riassunto invece che sulla fonte

Tre affermazioni sul calcolatore esistente sono state fatte sulla base di un
riassunto della pagina, non della pagina. Un dettaglio del riassunto suonava
strano, e la rilettura alla fonte era d'obbligo.

Le tre affermazioni hanno retto — e una si è rivelata più netta del previsto —
ma il dettaglio sospetto **non era sporcizia dell'estrattore**: era un'etichetta
vera. Ci sarebbe stato un errore in un documento destinato a chi quel prodotto
lo conosce meglio di noi.

**Regola adottata:** un'affermazione su qualcosa che non abbiamo letto
direttamente non entra in un documento. Il perimetro dell'analisi lo dice
esplicitamente.

→ diario, voci 36–37

---

### Passaggio: scrittura degli avvisi

#### 11. Il messaggio anti-errore aveva un errore

L'avviso che intercetta chi confonde stipendio mensile e RAL annua usciva così:

```
Se intendevi 2.500 € al mese. la RAL è circa 30.000 €.
                            ↑ punto al posto della virgola
```

Una conversione ai separatori italiani applicata all'intera frase invece che ai
soli numeri. Banale — ma stava **proprio nella funzione che esiste per prevenire
gli errori altrui**, ed è passata inosservata alla lettura: si vedeva solo
eseguendola.

→ diario, voce 23

---

### Passaggio: validazione dell'ingresso

#### 12. Non sapevamo leggere i numeri italiani

Il più grave di tutti.

| Scritto | Letto |
|---|---|
| `35.000` | **35,00 €** |
| `25.999` | 26,00 € |
| `2.500` | 2,50 € |
| `35.000,50` | *errore* |

`float("35.000")` in Python vale **35.0**: il punto è il separatore decimale,
mentre in italiano divide le migliaia.

**Tre aggravanti:**

1. Il segnaposto del nostro campo era `es. 35.000`: **chi copiava il nostro
   esempio otteneva 35 euro**.
2. Il messaggio d'errore suggeriva `35.000,50` e poi **rifiutava proprio quel
   formato**.
3. Nessun controllo poteva accorgersene. 33,65 € di netto su 35 € di lordo è
   perfettamente coerente: il calcolo era giusto, era il numero a essere quello
   sbagliato.

È **esattamente il difetto contro cui è nato il progetto** — un input frainteso
in silenzio che produce un risultato plausibile — nel campo principale, protetto
da 304 test.

**Perché i test non l'hanno visto:** passavano tutti `35_000` o `"30000"`.
Nessuno ha mai provato a scrivere un numero **come lo scrive una persona**. La
suite difendeva il calcolo, non l'ingresso al calcolo.

Corretto con una funzione che accetta `35.000`, `35,000`, `35.000,50`,
`35,000.50`, `35 000`, `€ 35.000`; che **respinge** gli input malformati invece
di indovinarli; e che, dove l'ambiguità è reale, **mostra come ha capito** —
*"Ho letto 35.000 € lordi all'anno"* — mentre si digita.

**Trovato usando l'interfaccia, al primo tentativo, da chi non stava cercando
bug.**

→ diario, voce 38

---

### Passaggio: identità visiva

#### 13. Un tema scuro inventato, e imposto

**Cosa è successo.** Adottando i colori di Jet HR ho costruito anche un tema
scuro, tingendo i grigi con il loro inchiostro oliva `#11150a` — ragionando che
la coerenza di marca dovesse valere anche al buio.

Misurato dopo:

| Ruolo | Colore | Verde in eccesso |
|---|---|---|
| Schede | `#191c14` | 3 punti |
| Sfondo pagina | `#0e100a` | 2 punti |
| Bordi | `#333828` | 5 punti |

Pochi punti di verde dentro uno scuro, su superfici grandi, non leggono come
"scuro di marca": leggono come **cachi**. La descrizione ricevuta —
*«verde cacca molle»* — è esattamente il fenomeno.

**Due errori, non uno.** Il secondo è più grave del colore: **Jet HR non ha un
tema scuro** (zero occorrenze di `prefers-color-scheme` nella loro pagina),
quindi non stavo replicando la loro identità, la stavo **inventando**. E
l'avevo agganciata alla preferenza del sistema operativo senza offrire un modo
per dissentire: chi ha il computer in modalità scura si trovava imposto un tema
che nessuno aveva scelto.

**Cosa è cambiato.**

- Grigi **neutri**: il marchio resta nel lime, che sul fondo scuro ha finalmente
  il contrasto che sul bianco gli manca. Un solo elemento porta identità.
- Un controllo esplicito **Come il sistema / Chiaro / Scuro**, che scavalca la
  preferenza del sistema operativo e resta salvato.
- Il tema effettivo si calcola in JavaScript invece che con una media query: i
  valori scuri esistono **in un posto solo**, invece di essere duplicati fra
  media query e attributo, dove sarebbero divergiuti.

**Perché rientra nel quadro.** È il secondo errore di fila trovato **usando
l'applicazione**, dopo i formati numerici. E ha la stessa forma di un errore già
visto qui: rispettare `prefers-color-scheme` sembrava attenzione all'utente, ma
applicare una preferenza **senza offrire un'alternativa** è decidere al posto
suo. È la versione visiva del difetto di fondo di questo progetto — fare la
cosa plausibile invece di quella verificata.

---

### Passaggio: formattazione dei numeri

#### 14. Due convenzioni diverse nella stessa colonna

**Cosa è successo.** Aprendo la pagina in un browser vero, la tabella del
risultato mostrava:

```
  NETTO MENSILE      1859,44 €      ← senza separatore
  NETTO ANNUO       26.032,22 €     ← con separatore
```

**La causa.** La formattazione italiana automatica **omette il separatore delle
migliaia sui numeri di quattro cifre**. È una convenzione tipografica legittima
presa isolatamente; in una colonna di importi che si leggono per confronto è
un'altra cosa: due numeri scritti con regole diverse, uno accanto all'altro,
invitano a sbagliare riga.

Nello stesso controllo è emerso anche che le percentuali uscivano come `74.4%`
con il punto, perché la funzione usata per arrotondare non conosce la virgola
decimale italiana.

**Perché non si vedeva prima.** Il codice era corretto: chiamava la
formattazione standard con la lingua giusta. L'errore non stava in cosa il
codice faceva, ma in **cosa il risultato sembrava**. Nessun test sui numeri
poteva rilevarlo, perché i valori erano esatti.

**Cosa è cambiato.** Raggruppamento forzato sugli importi, e una funzione
dedicata alle percentuali. Entrambe con il commento che spiega il perché,
perché è il genere di riga che qualcuno "semplificherà" fra sei mesi.

**Come è stato trovato.** Con una prova automatica nel browser a cinque
larghezze — 360, 390, 768, 1280 e 1600 pixel — che apre la pagina, esegue un
calcolo ed estrae il testo mostrato. Serviva a verificare l'adattamento agli
schermi stretti; ha trovato un difetto che con l'adattamento non c'entrava
niente.

---

### Passaggio: manutenzione del foglio di stile

#### 15. Un blocco di CSS cancellato senza che nessuno se ne accorgesse

**Cosa è successo.** Provando le tre modalità per il daltonismo, le trame non
comparivano in nessuna. Cercando la causa nel foglio di stile compilato:
**una sola occorrenza** di `repeating-linear-gradient` invece di sette.

Un'intera sezione era sparita dal sorgente: scala del testo, regole delle trame,
metà dell'alto contrasto, gli stili del pannello di leggibilità, e le due media
query che raccolgono le preferenze del sistema operativo.

**La causa.** Una modifica automatica che sostituiva una porzione di file
tagliandola **per indici** — dall'inizio di un blocco fino a un commento
successivo — invece che per contenuto. Fra quei due punti, nel frattempo, era
finito dell'altro. Il taglio si è portato via anche quello.

**Perché non se n'è accorto nessuno.**

- Il foglio di stile **non ha test**, e non ne avrebbe di sensati: nessuno
  scrive asserzioni su una regola CSS.
- La compilazione è andata a buon fine: un CSS più corto è un CSS valido.
- La pagina continuava a funzionare e ad avere un aspetto normale. Le regole
  cancellate governavano tutte funzioni **che si attivano solo se qualcuno le
  chiede** — testo grande, alto contrasto, trame. Nessuna è visibile per default.

È la peggiore combinazione possibile: una perdita silenziosa in codice che
serve proprio a chi ha più bisogno che funzioni.

**Cosa è cambiato.** Blocco ricostruito e riverificato in un browser vero:
trame 5 su 5 nelle due modalità per il daltonismo e 0 su 5 in standard, testo a
22,4 px con la scala massima, bordi a 2 px in alto contrasto.

**La lezione.** Le modifiche automatiche a un file vanno ancorate al
**contenuto** — cerca questo testo, sostituisci quello — mai a posizioni
calcolate, perché la posizione dipende da tutto ciò che è stato aggiunto nel
frattempo. E le funzioni che si attivano su richiesta vanno riprovate
esplicitamente: non essendo visibili per default, la loro assenza non si nota
usando la pagina normalmente.

---

### Passaggio: progettazione dei controlli

#### 16. Tre pulsanti che sembravano rotti perché non mostravano niente

**Cosa è successo.** Le modalità per il daltonismo governano **solo i colori del
grafico**. Aprendo il pannello di leggibilità e premendo i pulsanti *prima* di
aver fatto un calcolo, sullo schermo non cambiava nulla — perché il grafico non
c'era ancora.

Chi provava i controlli concludeva ragionevolmente che fossero rotti. Non lo
erano.

**Perché è un difetto e non un malinteso.** Un controllo che non mostra il
proprio effetto è indistinguibile da un controllo guasto, e la distinzione non
può essere chiesta all'utente. Peggio: qui riguardava proprio le funzioni di
accessibilità, cioè quelle che una persona prova **prima** di cominciare a
usare lo strumento — quando il grafico, per definizione, non esiste ancora.

**Cosa è cambiato.** Nel pannello sono comparsi cinque campioni che mostrano i
colori correnti, con le loro trame, più una riga che **scrive** la modalità
attiva. Ora premere un pulsante produce sempre un effetto visibile, anche a
pagina vuota.

La riga scritta ha anche un valore diagnostico: se i campioni non cambiano ma
il testo sì, il problema è nello schermo o in un filtro colore del sistema
operativo, non nell'applicazione. È una distinzione che da sola risparmia
un'indagine — e in questo caso ne è costata una.

**Una nota sull'onestà della diagnosi.** Non è certo che questo fosse il motivo
per cui i controlli sembravano inerti: nello stesso giro erano state aggiunte
anche le intestazioni contro la cache del file principale. Il difetto però
esisteva a prescindere, ed è stato corretto per quello che è, non per quello
che si sospettava avesse causato.

---

### Passaggio: controllo di sicurezza

I tre che seguono sono venuti fuori tutti insieme, a codice finito, da un
controllo fatto apposta. Il resoconto completo — comprese le verifiche che non
hanno trovato niente e i rischi che restano — sta in
[SICUREZZA.md](SICUREZZA.md).

#### 17. Il server serviva qualunque file del progetto

**Cosa è successo.** L'API serve anche l'interfaccia compilata: una rotta
generica raccoglie tutto ciò che non comincia per `/api/` e, se corrisponde a un
file dentro `web/dist`, lo restituisce.

```python
file = FRONTEND / percorso
if file.is_file():
    return FileResponse(file)
```

Solo che `FRONTEND / "../../dati_privati/LEGGIMI.md"` **è un file.** `pathlib`
compone i percorsi, non li giudica: `..` risale di una cartella e basta.

Era quindi raggiungibile dal browser tutto ciò che sta sotto la radice del
progetto. Compresa `dati_privati/` — la cartella tenuta fuori dal repository
**proprio perché contiene una Certificazione Unica vera.**

**Perché fa più impressione degli altri.** La protezione di quella cartella era
stata pensata, scritta e verificata: c'è un `.gitignore` dedicato che esclude
tutto tranne il modello vuoto. Ha funzionato esattamente per quello per cui era
stato scritto — Git — e non ha protetto da una strada che nessuno aveva pensato
di guardare. **Una difesa messa nel posto giusto non è una difesa del dato: è
una difesa di una via d'uscita.** Le altre restano aperte finché qualcuno non le
cerca.

**Cosa è cambiato.** Il percorso viene risolto e poi confrontato con la radice
consentita: se dopo la risoluzione non sta più dentro, non esiste. `.resolve()`
prima del confronto è la parte che conta — normalizza `..`, i collegamenti
simbolici e i separatori ripetuti. Confrontare le stringhe *prima* di risolverle
è il modo classico di scrivere un controllo che non controlla.

Verificato su otto percorsi: i tre legittimi passano, i cinque ostili — fra cui
`%2e%2e/index.html` e `../../dati_privati/LEGGIMI.md` — vengono respinti.

**La lezione.** Comporre un percorso con dati che arrivano da fuori è
un'operazione che va sempre chiusa con un controllo di contenimento, anche
quando la cartella di partenza sembra innocua. E un `.gitignore` risponde a una
domanda sola: *questo file finisce nel repository?* Non risponde a *questo file
può uscire da questa macchina?*

---

#### 18. Il motore accettava importi assurdi e cifre non latine

**Cosa è successo.** La validazione della RAL rifiutava correttamente il testo,
i valori negativi e le quote fuori scala. Non rifiutava:

- `1e308`, prossimo al massimo rappresentabile: il calcolo proseguiva e
  restituiva importi privi di significato, senza segnalare nulla;
- una cifra di trenta caratteri;
- `٣٥٠٠٠` in cifre arabo-indiane e `३५०००` in devanagari, che `float()` in
  Python converte volentieri in 35000.

**Perché l'ultimo è il più interessante.** Non perché sia pericoloso: perché in
un campo di modulo significa che **due stringhe visivamente diverse producevano
lo stesso importo**, e nessuna delle due era quella che l'utente credeva di aver
scritto. In uno strumento che serve a mettersi d'accordo su una cifra,
un'ambiguità grafica non è un dettaglio tecnico.

C'è anche una simmetria fastidiosa con l'errore 12: lì il problema era che
`35.000` veniva letto come 35, perché il parser era troppo severo con una
convenzione italiana legittima. Qui è l'opposto — troppo permissivo con una
convenzione che nessun utente italiano userà mai. **Lo stesso campo, sbagliato
nelle due direzioni opposte, a tre settimane di distanza.**

**Cosa è cambiato.** Un tetto assoluto a cento milioni e un filtro sui caratteri
ammessi: solo cifre e separatori ASCII. Meglio rifiutare che indovinare — chi
digita davvero in devanagari riceve un errore chiaro invece di un risultato che
sembra giusto.

---

#### 19. Il database affacciato su tutta la rete locale

**Cosa è successo.** In `docker-compose.yml`:

```yaml
- "3307:3306"
```

Sembra «la porta 3307 di questa macchina». Docker però interpreta la forma senza
prefisso come `0.0.0.0:3307`: **tutte le interfacce.** Su una rete condivisa —
un ufficio, una biblioteca, un bar — il database era raggiungibile da chiunque,
con la password di sviluppo scritta in chiaro tre righe sopra.

**Perché non si era visto.** Perché la riga non è sbagliata: è la forma che si
trova in ogni esempio della documentazione, e in locale funziona benissimo. Il
difetto non sta in ciò che è scritto, sta in ciò che **non** è scritto e viene
riempito da un valore predefinito. È il tipo di errore che si trova solo
chiedendosi *come legge questa riga chi la esegue*, invece di *cosa volevo dire
scrivendola*.

**Cosa è cambiato.** `127.0.0.1:3307:3306`. La password è rimasta `sviluppo`,
consapevolmente: una password diversa ma comunque scritta nel repository non è
più sicura, è teatro. Ciò che rende accettabile quella debole è che la porta ora
non esce dalla macchina e che dentro c'è solo il registro dei coefficienti —
dati pubblici, rigenerabili con un comando.

---

### Passaggio: revisione esterna, a lavoro finito

Le quattro voci che seguono sono state trovate da **due revisioni indipendenti**
richieste quando il progetto era considerato finito. Nessuna è stata trovata da
me, dai 326 test di allora o dal controllo di sicurezza.

Vale la pena dirlo prima di raccontarle: **è il metodo che ha funzionato meglio
di tutti**, per numero di difetti trovati per ora impiegata. E somiglia molto a
quello che aveva funzionato con la Certificazione Unica (errori 8 e 9): qualcuno
che non ha costruito la cosa la guarda con criteri che chi l'ha costruita non ha.

#### 20. Il calcolo inverso non sapeva leggere i numeri italiani

**Cosa è successo.** L'errore 12 — `35.000` letto come 35 € — era stato corretto
scrivendo `normalizza_importo()`. La correzione era stata applicata **solo al
percorso in cui il difetto era stato trovato**, cioè il calcolo diretto. Il
calcolo inverso continuava a usare `float()`.

| Scritto nel campo | RAL restituita |
|---|---|
| `2000` | 40.101,12 € |
| `2.000` | **29,12 €** |
| `2.000,00` | *rifiutato* |

E il messaggio d'errore diceva: *«Il netto deve essere un numero. Esempio: 1800
oppure 1.800,50»* — **proponeva un formato che era l'unico a non accettare.**

**Perché nessun test l'ha visto.** Perché tutti e dieci i test del calcolo
inverso passavano numeri già puliti: `ral_per_netto(1500)`, mai
`ral_per_netto("1.500")`. Provavano l'inverso **in un modo in cui l'interfaccia
non lo usa mai**. La suite copriva la funzione, non il percorso.

**La lezione, che è diversa da quella dell'errore 12.** Lì avevo imparato che i
formati italiani vanno gestiti. Qui il difetto non è stato non saperlo: è stato
**correggere nel punto in cui il sintomo si era manifestato invece che in tutti
i punti che hanno la stessa causa.** Quando si corregge un difetto di lettura
dell'ingresso, la domanda successiva è sempre: *quante altre porte ha questo
programma?*

---

#### 21. Trattamento integrativo: mancavano i 75 € della capienza

**Cosa è successo.** Il trattamento integrativo da 1.200 € spetta, sotto i
15.000 di reddito, se l'IRPEF lorda supera la detrazione da lavoro dipendente.
Il codice implementava esattamente questo. La norma però dice di più:

> «…sia di ammontare superiore a quello della detrazione spettante ai sensi
> dell'articolo 13, comma 1, del citato testo unico, **diminuita dell'importo di
> 75 euro rapportato al periodo di lavoro nell'anno**»

L'inciso è stato inserito dal **D.Lgs. 216/2023** per il solo 2024 e reso
strutturale dall'**art. 1 c. 3 della L. 207/2024**; la circolare **4/E del 16
maggio 2025** lo conferma. Ai fini della capienza la detrazione vale quindi
1.955 − 75 = **1.880** — cioè il valore precedente alla riforma, perché i 75 €
servono a **neutralizzare** l'aumento da 1.880 a 1.955 disposto dallo stesso
D.Lgs. 216/2023.

*(La prima stesura di questa voce attribuiva l'inciso alla L. 234/2021: era
sbagliato, ed è l'errore 24.)*

**Cosa cambiava.** La soglia si sposta da un imponibile di 8.500 a **8.173,91**,
cioè da una RAL di 9.360 a **9.002**: 358 € più in basso. Chi sta in mezzo
riceve 1.200 € che il motore gli negava.

**Perché nessun test l'ha visto — ed è la parte peggiore.** Il test sulle
discontinuità ricavava le soglie **dallo stesso registro** che avrebbe dovuto
controllare, con questa motivazione scritta nel codice:

> *«Ricavarle invece di elencarle a mano significa che, se domani cambia un
> coefficiente, il test si aggiorna da solo e continua a essere vero.»*

È l'**errore 5 ripetuto**, in un punto diverso, con la stessa giustificazione
che sembrava buon senso. Il registro sbagliava, il test rifaceva lo stesso conto
sbagliato, ed erano d'accordo. Un test che si aggiorna da solo quando cambia il
dato non è robusto: **è cieco**.

Fa tre volte, contando gli errori 5 e 7. Non è più una tendenza: è la mia
firma. La domanda va posta ogni singola volta.

**Cosa è cambiato.**

- I 75 € stanno **nel registro**, con la norma e la circolare come fonte, e lo
  stato marcato `primaria`.
- Gli ancoraggi delle discontinuità sono **riscritti a mano**, ognuno con il
  suo conto in un commento. Se domani un coefficiente cambia, il test
  **fallisce** — ed è il comportamento corretto: un cambio di aliquota deve
  costringere qualcuno a guardare.
- Il controllo di sensibilità ha un guasto in più che toglie i 75 €: adesso fa
  fallire otto test.

**E un regalo inatteso.** Sistemata la soglia, le discontinuità di Milano sono
diventate **sette invece di sei**. La capienza del trattamento cadeva a 8.500 —
esattamente dove finisce la prima fascia della somma esente del cuneo. **Due
discontinuità diverse, sovrapposte nello stesso punto**, contate come una sola
per settimane. Una era dichiarata nel registro, l'altra non lo era affatto, e
nessuno poteva accorgersene finché coincidevano.

---

#### 22. La frase di conferma spezzata in colonne

**Cosa è successo.** L'etichetta della casella di conferma ha `display: flex`
con `gap: 0.6rem`. Dentro c'erano la casella, tre pezzi di testo e due
`<strong>`. In flexbox **ogni frammento di testo fra due elementi diventa un
elemento flex a sé**, e il `gap` li separa come fossero colonne.

Risultato a schermo:

> ☐ Confermo    **35.000 €**    è la retribuzione    **lorda**    , non lo stipendio…

con la frase spezzata su più colonne e la virgola staccata dalla parola che
segue. Sette elementi flex al posto di due.

**Perché fa male.** È **la riga che serve a non confondere lordo e mensile** —
cioè l'unica funzione per cui questo strumento esiste, dopo il calcolo. E il
difetto era visibile in uno degli screenshot allegati alla documentazione: era
già stato guardato, senza essere visto.

Il README celebra la verifica visiva nel browser come il metodo che trova ciò
che i test non vedono (errori 14 e 15). Questo ci è passato davanti.

**Cosa è cambiato.** Il testo è avvolto in un solo `<span>`: due elementi flex,
la casella e la frase. Verificato a 360 e 390 px: due elementi, nessun
traboccamento.

---

#### 23. Gli importi tagliati sul telefono, in silenzio

**Cosa è successo.** Su uno schermo da 360 px la tabella delle voci — quella con
tutti gli importi, cioè **il risultato per cui lo strumento esiste** — era larga
352 px dentro un riquadro da 294. Scorreva, come previsto dalla regola generale
che dice di far scorrere le tabelle di numeri invece di comprimerle. Ma senza
alcun segno visibile.

A schermo si leggeva `35.0(`, `3.2`, `26.03`. Gli importi c'erano, erano
raggiungibili con una strisciata laterale, e **niente lo diceva**.

**Perché la verifica automatica non l'ha preso.** Il controllo cercava il
traboccamento orizzontale **della pagina**, e la pagina non traboccava:

```css
html, body { overflow-x: hidden; }
```

quella riga — scritta apposta perché *«nessun elemento può far scorrere la
pagina in orizzontale»* — **silenziava esattamente il sintomo che il controllo
cercava**. Una difesa corretta che ha nascosto il difetto di un'altra.

È la stessa forma dell'errore 15: una regola giusta in generale, applicata a un
caso in cui produce il contrario di quello che serve.

**Cosa è cambiato.** Sotto i 26rem la tabella smette di essere una tabella e
diventa un elenco: etichetta su una riga, importo a capo, allineato a destra e
in grassetto. L'intestazione resta ai lettori di schermo. Verificato a 360, 390,
768 e 1280 px: nessuno scorrimento, ogni importo dentro la finestra.

**La lezione.** Un controllo automatico verifica ciò che gli si chiede, non ciò
che si vuole sapere. Chiedevo *«la pagina scorre?»* e volevo sapere *«si vede
tutto?»*. Non sono la stessa domanda, e la differenza fra le due era nascosta in
una riga di CSS scritta mesi prima con ottime intenzioni.

---
## Cosa insegna il quadro d'insieme

Raggruppando i ventitré errori per **metodo che li ha trovati**:

| Metodo di verifica | Errori trovati |
|---|---|
| Ricerca sulle fonti ufficiali | 1 (sette coefficienti) |
| Scrittura del codice | 2 |
| Esecuzione del codice | 3, 11 |
| Ragionamento sulle soglie | 4 |
| **Guasto deliberato dei dati** | 5 (tre buchi nei test) |
| **Caricamento su un database vero** | 6 |
| **Una domanda dell'autrice** | 7 |
| **Un documento emesso da altri** | 8, 9 |
| Rilettura sospettosa | 10 |
| **Uso dell'interfaccia** | 12, 13, 16 |
| **Prova nel browser a più larghezze** | 14, 15 |
| **Richieste ostili costruite apposta** | 17, 18 |
| **Rilettura della configurazione come la legge chi la esegue** | 19 |
| **Revisione esterna a lavoro finito** | 20, 21, 22, 23 |

**Nessun metodo ha trovato gli errori di un altro.** I test non hanno visto la
regola sui periodi parziali; il documento reale non avrebbe mai mostrato il buco
dei NULL nel database; nessuna quantità di test avrebbe rivelato che
`35.000` valeva 35, perché chi li scriveva sapeva già come si digita un numero.

E soprattutto: **nessuno dei ventitré è stato trovato rileggendo il codice.**

Le tre verifiche più produttive sono anche le tre che si tende a saltare perché
sembrano superflue quando tutto è verde:

1. **rompere apposta** ciò che si è costruito e controllare che qualcuno se ne
   accorga;
2. **confrontarsi con qualcosa fatto da altri** — un documento, un database
   reale, una persona che fa una domanda;
3. **usarlo**, da utente, senza cercare difetti.

A queste il controllo di sicurezza ne ha aggiunta una quarta, che ha una forma
diversa dalle altre tre: **provare a fare, da fuori, ciò che il codice non si
aspetta.** Le prime tre partono da come lo strumento dovrebbe essere usato;
questa parte da come *potrebbe* essere usato da qualcuno che non ha nessuna
intenzione di collaborare. È l'unico dei quattro metodi che ha trovato un
difetto in una parte del progetto già considerata finita — e il resoconto
completo, con le verifiche che non hanno trovato niente e i rischi che restano
aperti, sta in [SICUREZZA.md](SICUREZZA.md).

Un errore ricorre **tre volte** in questo elenco, ai numeri 5, 7 e 21, in punti
diversi del progetto e a settimane di distanza: **costruire una verifica che
deriva la propria risposta da ciò che dovrebbe controllare**. Presentarsi tre
volte non lo qualifica come tendenza: lo qualifica come **la mia firma**. La
prima volta era una svista, la seconda una tendenza, la terza è un difetto di
metodo che va contrastato con una regola, non con l'attenzione. La regola è
che ogni verifica di un numero fiscale porta accanto il proprio conto scritto
a mano — e la domanda da farsi, ogni volta che si scrive un controllo, è una
sola:

> *Da dove viene il numero con cui sto confrontando? Se viene da ciò che sto
> verificando, non sto verificando niente.*
