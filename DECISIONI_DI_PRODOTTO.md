# Registro delle decisioni di prodotto

Cosa è stato deciso, da chi, su quale evidenza, e cosa ne è venuto fuori.

Gli altri documenti raccontano **il risultato**. Questo racconta **la
direzione**: le domande poste, le verifiche richieste, e i punti in cui una
scelta di prodotto ha corretto una proposta tecnica.

Serve perché in un lavoro assistito la parte che distingue è proprio questa.
Costruire è la conseguenza; decidere cosa costruire, cosa verificare e quando
fermarsi è il lavoro.

---

## Come leggerlo

Ogni voce ha quattro righe:

| | |
|---|---|
| **Proposta** | cosa suggeriva l'analisi tecnica |
| **Decisione** | cosa è stato deciso |
| **Evidenza** | su cosa poggia |
| **Esito** | cosa ne è seguito, incluso quando è andata male |

Le decisioni che **divergono** dalla proposta sono marcate ⟳. Sono nove su
diciannove, e sono le più interessanti: se la direzione si limitasse a
ratificare, non sarebbe direzione.

---

## Impostazione

### 1. Lo stack ⟳

| | |
|---|---|
| **Proposta** | pagina statica HTML/CSS/JS, motore riscritto in JavaScript, nessun build, pubblicabile ovunque |
| **Decisione** | React, MySQL, motore Python conservato |
| **Evidenza** | *«dobbiamo far vedere quello che so fare e che ho studiato»* — e l'annuncio, che chiede di saper scegliere fra Lovable, no-code e codice production grade |
| **Esito** | il motore Python non è stato riscritto, quindi non è stato reintrodotto alcun errore nella traduzione. MySQL ha dovuto **guadagnarsi il posto**: contiene il registro dei coefficienti con fonte e stato, non è decorativo. Provandolo su un database vero è emerso un difetto (chiave unica inefficace sui NULL) che nessuna lettura dello schema avrebbe mostrato |

### 2. L'anno d'imposta

| | |
|---|---|
| **Proposta** | 2026, l'anno corrente |
| **Decisione** | accolta |
| **Evidenza** | uno strumento che proietta uno stipendio deve rispondere sull'anno che il dipendente sta vivendo |
| **Esito** | ha portato alla scoperta più costosa della ricerca: la seconda aliquota IRPEF era ferma al 35% quando dal 2026 è 33%. Il 2025 è rimasto nel registro, e si è rivelato indispensabile per il confronto con la Certificazione Unica |

### 3. Le mensilità ⟳

| | |
|---|---|
| **Proposta** | fissare 13 mensilità |
| **Decisione** | *«il CCNL commercio ne ha 14 e non è il solo. Qual è l'esempio che danno loro?»* |
| **Evidenza** | il testo del task **non dà nessun esempio numerico**, verificato rileggendolo |
| **Esito** | la domanda ha cambiato il progetto: se non c'è un esempio da seguire, le mensilità non sono una costante da scegliere ma **un parametro**. Da lì la constatazione che non toccano il netto annuo — e l'avviso in pagina che lo dice, perché è il primo equivoco del neofita |

---

## Correttezza

### 4. Il territorio non è trattabile ⟳

| | |
|---|---|
| **Proposta** | territorio come parametro, con Milano predefinito |
| **Decisione** | *«al momento dell'input, la regione deve essere evidenziata, non è una condizione trattabile»* |
| **Evidenza** | l'analisi su tutti i 7.792 comuni italiani: oltre 600 € l'anno di differenza a parità di RAL |
| **Esito** | il comune è sempre visibile in **entrambe** le modalità, ogni voce territoriale porta con sé il luogo che la genera, e gli avvisi sono **guidati dai dati del territorio**: quello sulla soglia comunale compare a Milano e non a Palermo, dove quella soglia non esiste |

### 5. Deve funzionare a prescindere dall'importo ⟳

| | |
|---|---|
| **Proposta** | test sui casi rappresentativi |
| **Decisione** | *«l'automazione deve funzionare a prescindere dall'importo inserito»* |
| **Evidenza** | il dominio è pieno di soglie, e ogni soglia è un punto in cui il codice può sbagliare |
| **Esito** | dodici soglie mappate e attraversate a passi di un centesimo. Ha prodotto la scoperta tecnica più rilevante del progetto: **il netto non cresce sempre col lordo**. Sei discontinuità, tre in discesa. Un test esistente affermava il contrario ed è stato riscritto |

### 6. La Certificazione Unica ⟳

| | |
|---|---|
| **Proposta** | confronto con un calcolatore pubblico |
| **Decisione** | *«ti carico direttamente la CU»* |
| **Evidenza** | confrontarsi con un altro calcolatore dimostra solo che due prototipi sbagliano allo stesso modo |
| **Esito** | ha **smentito il motore**. Una regola sui periodi di lavoro parziali, scelta perché sembrava più elegante, dava zero dove il sostituto d'imposta riconosceva sia la detrazione sia il trattamento integrativo. 302 test non l'avevano vista, perché scritti dalla stessa testa che aveva scelto la regola sbagliata |

### 7. La domanda che ha smontato lo strumento di verifica ⟳

| | |
|---|---|
| **Proposta** | strumento di confronto con la CU, dichiarato pronto |
| **Decisione** | *«ma noi lavoriamo sulla RAL, perché la CU?»* |
| **Evidenza** | la CU dichiara l'imponibile, non il lordo |
| **Esito** | lo strumento ricostruiva una «RAL equivalente» a partire dal dato della CU, quindi una delle righe del confronto tornava **per costruzione**. Riscritto con due modalità dichiarate, e con l'avvertenza a schermo di cosa **non** viene verificato. Una domanda ha corretto un errore di metodo che era già stato dichiarato risolto |

---

## Esperienza d'uso

### 8. I due livelli di esperienza

| | |
|---|---|
| **Proposta** | — |
| **Decisione** | *«mettiamo uno switch esperto / alle prime armi, con la possibilità di passare dall'uno all'altro»* |
| **Evidenza** | *«metti che uno si sente esperto e poi non sa cosa fare?»* |
| **Esito** | è diventato il vincolo architetturale principale: cambiare modalità **non azzera niente**. Da lì la scelta di un'unica pagina con stati invece di viste separate |

### 9. Il difetto osservato su uno strumento reale

| | |
|---|---|
| **Proposta** | — |
| **Decisione** | riferito un errore vissuto: RAL sbagliata inserita per un dipendente, perché non era chiaro che il campo chiedesse il lordo |
| **Evidenza** | esperienza diretta, non ipotesi. E l'analisi competitiva l'ha poi circoscritta: tre calcolatori su quattro scrivono «lordo» nell'etichetta; uno lo affida a un acronimo fra parentesi |
| **Esito** | quasi tutta l'interfaccia discende da qui — etichetta esplicita, eco dell'input nel risultato, controllo di plausibilità, passaggio di conferma, e la **modalità inversa netto → lordo**, che non si limita ad avvisare della confusione ma la rende impossibile |

### 10. Miglioramenti per ipovedenti

| | |
|---|---|
| **Proposta** | — |
| **Decisione** | *«proponiamo qualche miglioramento visivo, per esempio per ipovedenti»* |
| **Evidenza** | un calcolatore fiscale è fatto di numeri lunghi e di segni «−» e «+» che ribaltano il significato di una riga |
| **Esito** | tre leve indipendenti — dimensione del testo, contrasto, visione dei colori — più il rispetto automatico delle preferenze di sistema. È diventato uno dei quattro elementi che l'analisi competitiva ha confermato come **assenti in tutti e quattro** gli strumenti esaminati |

### 11. Il tasto daltonismo

| | |
|---|---|
| **Proposta** | un interruttore per le trame |
| **Decisione** | *«metti il tasto daltonismo»* |
| **Evidenza** | rosso-verde e blu-giallo confondono coppie diverse: una soluzione unica ne serve bene uno solo |
| **Esito** | tre modalità invece di una, ognuna validata. La modalità «senza colore» copre tritanopia, visione monocromatica e stampa in bianco e nero. Provandole è emerso che i pulsanti **non mostravano alcun effetto** finché non si era calcolato qualcosa: corretto con un'anteprima nel pannello |

### 12. Il fondo scuro ⟳

| | |
|---|---|
| **Proposta** | tema scuro automatico, secondo le preferenze del sistema |
| **Decisione** | *«è inquietante per la materia che trattiamo»* |
| **Evidenza** | giudizio di prodotto: uno strumento che calcola una busta paga deve rassicurare, non fare atmosfera |
| **Esito** | chiaro come default indipendentemente dal sistema operativo, scuro come scelta esplicita. Ha anche fatto emergere che il tema scuro era **inventato** — Jet HR non ne ha uno — e che i grigi tinti col loro oliva leggevano come cachi |

### 13. Lo scorrimento al risultato

| | |
|---|---|
| **Proposta** | — |
| **Decisione** | *«bisogna scrollare per arrivare all'output, io direi di spostarsi subito»* |
| **Evidenza** | osservazione d'uso |
| **Esito** | fatto, e con un'aggiunta: il risultato riceve anche **il fuoco**, perché chi naviga da tastiera resterebbe sul pulsante e chi usa uno screen reader non saprebbe che è comparso qualcosa |

---

## Identità visiva

### 14. Adottare i colori del marchio ⟳

| | |
|---|---|
| **Proposta** | identità neutra, per non simulare un prodotto ufficiale |
| **Decisione** | adottare i colori di Jet HR, mantenendo però il CSS scritto a mano invece di Tailwind |
| **Evidenza** | dimostrare di saper lavorare dentro un design system esistente |
| **Esito** | adottati **dopo averli misurati**: il lime vale 1,30 : 1 su bianco, quindi è un colore da fondo e non da testo. Il rischio segnalato — che un repository pubblico col marchio altrui sembri ufficiale — è stato gestito con un avviso di indipendenza in cima alla pagina, che rende la scelta difendibile invece che imbarazzante |

### 15. La palette dei dati ⟳

| | |
|---|---|
| **Proposta** | palette categorica generica, già validata |
| **Decisione** | *«sono colori base, io resterei su qualcosa che stia bene con i loro colori»* |
| **Evidenza** | coerenza visiva con il marchio |
| **Esito** | **quattro palette candidate bocciate** prima di trovarne una valida. Il motivo è strutturale: una palette costruita attorno a un giallo-verde produce da sola la coppia oliva ↔ terracotta, che è esattamente quella che il daltonismo rosso-verde collassa. Quella adottata ha margini migliori della generica, e per la prima volta tutti i toni superano il contrasto 3 : 1 |

### 16. I gradienti ⟳ (in parte)

| | |
|---|---|
| **Proposta** | riempimenti piatti ovunque |
| **Decisione** | *«a me piacciono i gradienti»* |
| **Evidenza** | preferenza estetica, in un prodotto che nessuno è obbligato a usare |
| **Esito** | accolta con una riga netta: **gradienti sulla cornice, piatto sui dati**. Un segmento percorso da un gradiente cambia colore lungo la sua lunghezza, e chi legge non ha modo di sapere se quella variazione significhi qualcosa. Sulla cornice non c'è nessun significato da proteggere. In alto contrasto spariscono |

---

## Metodo e consegna

### 17. Tracciare gli errori

| | |
|---|---|
| **Proposta** | diario di bordo cronologico |
| **Decisione** | *«segna gli errori in un file a parte, e il passaggio con l'errore»* |
| **Evidenza** | *«rientra nella politica di dimostrare i passaggi fatti e la capacità di rivedere gli errori in fase di test»* |
| **Esito** | il registro separato ha fatto emergere una cosa che il diario nascondeva: **lo stesso errore compare due volte** — costruire una verifica che ricava la propria risposta da ciò che dovrebbe controllare. In punti diversi del progetto, a poche ore di distanza. Due volte non è una distrazione: è una tendenza, e il file la nomina come tale |

### 18. Dichiarare l'uso dell'AI ⟳

| | |
|---|---|
| **Proposta** | inizialmente: nessun riferimento nel repository, dichiarazione a voce in colloquio |
| **Decisione** | dichiararlo nel README, dopo aver letto l'annuncio |
| **Evidenza** | *«costruirai con l'AI i tool»*, e *«se hai costruito un impero usando solo Claude Code ci interessi ancora di più»* |
| **Esito** | decisione **ribaltata** alla luce di un'evidenza nuova, che è il modo in cui una decisione dovrebbe cambiare. Nel README la dichiarazione è formulata come argomento e non come nota a piè di pagina, con il registro degli errori come prova: dodici casi in cui la verifica ha smentito quanto era stato prodotto |

### 19. Vogliono vedere la logica, non lo strumento

| | |
|---|---|
| **Proposta** | proseguire con le rifiniture dell'interfaccia |
| **Decisione** | *«hanno detto che l'esempio non aveva agevolazioni. Loro vogliono vedere la logica, non veramente lo strumento»* |
| **Evidenza** | il testo del task: due criteri su tre riguardano il ragionamento |
| **Esito** | il README è stato riscritto per aprire con il risultato e le decisioni, tenendo la profondità disponibile ma non imposta. Il frontend è rimasto deliberatamente piccolo: ogni elemento c'è perché rende leggibile un pezzo del ragionamento |

---

## Cosa hanno in comune

Riletti insieme, i diciannove punti mostrano tre ricorrenze.

**Le decisioni migliori sono nate da domande, non da indicazioni.** *«Qual è
l'esempio che danno loro?»* ha trasformato una costante in un parametro. *«Ma
noi lavoriamo sulla RAL, perché la CU?»* ha smontato uno strumento di verifica
già dichiarato pronto. Nessuna delle due era una richiesta di funzionalità:
erano domande sul perché.

**Nove decisioni su diciannove hanno corretto la proposta tecnica.** E fra
queste ci sono quelle che hanno prodotto i risultati migliori: il territorio
obbligatorio, la robustezza a qualsiasi importo, la CU, la palette imparentata
col marchio. Una direzione che si limita a ratificare non serve a niente.

**Le decisioni sono cambiate quando è cambiata l'evidenza.** La dichiarazione
sull'uso dell'AI è stata ribaltata dopo aver letto l'annuncio. Il tema scuro è
passato da automatico a esplicito dopo una prova d'uso. Non è incoerenza: è
l'unico modo in cui una decisione dovrebbe cambiare.

---

## Le decisioni ancora aperte

Onestà sullo stato, come negli altri documenti.

| Questione | Stato |
|---|---|
| Impaginazione a due colonne su schermo largo | disegnata, non realizzata |
| Pagina dei coefficienti autonoma e linkabile | non fatta |
| Confronto fra due offerte affiancate | fuori perimetro, cambierebbe l'architettura |
| Quanti CCNL oltre ai quattro attuali | aperta; le mensilità di tre su quattro restano da verificare |
| Dove pubblicare | repository certo; link live solo se il servizio si dimostra stabile |
