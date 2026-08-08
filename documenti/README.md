# Il dossier

Tutto il percorso: come sono state trovate le fonti, cosa è stato deciso e
perché, che cosa è stato verificato e con quale metodo, dove ha ceduto.

Sta qui e non nella radice perché la porta d'ingresso del repository è il
prodotto, non la ricerca. Ma la ricerca **è** metà del lavoro, e in un task che
valuta esplicitamente *«la capacità di ricerca da fonti appropriate»* e *«la
capacità di strutturare le informazioni»*, riassumerla sarebbe stato come
consegnare l'indice al posto del libro.

---

## Se hai cinque minuti

**[prodotto/ASSUNZIONI.md](prodotto/ASSUNZIONI.md)** — ogni semplificazione,
motivata e, dove misurabile, quantificata. Dice cosa lo strumento non fa,
prima che ve ne accorgiate voi.

## Se ne hai venti

Aggiungi **[verifiche/ERRORI.md](verifiche/ERRORI.md)** — i ventisette errori
commessi, ordinati per **passaggio in cui sono nati** e per **metodo che li ha
scoperti**. Nessuno è stato trovato rileggendo il codice, ed è la conclusione
più utile di tutto il dossier.

## Se vuoi verificare i numeri

**[verifiche/CASI_DI_PROVA.md](verifiche/CASI_DI_PROVA.md)** — quattro RAL con
la catena riga per riga e il conto accanto, rifacibili con una calcolatrice.
Più il confronto con una Certificazione Unica reale, che ha smentito il motore.

---

## La presentazione

**[Jet-HR-Product-Builder.pdf](presentazione/Jet-HR-Product-Builder.pdf)** — undici pagine.
È il percorso raccontato per intero: il caso, le fonti che hanno corretto sei gruppi di
coefficienti su sette, la lettura di tutte le tabelle comunali italiane, i sette gradini in
cui il netto non cresce col lordo, e i ventisette errori con il metodo che ha trovato ciascuno.

Chi ha poco tempo può leggere solo quella.

---

## Tutto, per area

### [ricerca/](ricerca/) — da dove vengono i numeri

| | |
|---|---|
| [RICERCA_FONTI.md](ricerca/RICERCA_FONTI.md) | Ogni coefficiente con la norma e lo stato di verifica, per il 2026 e il 2025. Comprese le tabelle dei minimi contrattuali |
| [METODOLOGIA.md](ricerca/METODOLOGIA.md) | La catena di calcolo, la tabella **norma → codice**, e il calendario di quando le fonti escono |

### [prodotto/](prodotto/) — cosa è stato deciso

| | |
|---|---|
| [ASSUNZIONI.md](prodotto/ASSUNZIONI.md) | Ogni semplificazione, motivata e quantificata |
| [DECISIONI_DI_PRODOTTO.md](prodotto/DECISIONI_DI_PRODOTTO.md) | Cosa è stato deciso, su quale evidenza, e i casi in cui la decisione ha corretto la proposta tecnica |
| [PIANO.md](prodotto/PIANO.md) | Il piano di lavoro iniziale — un artefatto, non una consegna: è utile per vedere quanto è cambiato |

### [verifiche/](verifiche/) — cosa è stato controllato, e cosa ha ceduto

| | |
|---|---|
| [CASI_DI_PROVA.md](verifiche/CASI_DI_PROVA.md) | I quattro casi calcolati a mano + il confronto con una CU reale |
| [ERRORI.md](verifiche/ERRORI.md) | I ventisette errori, per passaggio e per metodo che li ha scoperti |
| [SICUREZZA.md](verifiche/SICUREZZA.md) | Il controllo di sicurezza: cosa è stato provato, cosa ha ceduto, i rischi che restano |

### [ux/](ux/) — come è fatta l'interfaccia, e perché così

| | |
|---|---|
| [ANALISI_COMPETITIVA.md](ux/ANALISI_COMPETITIVA.md) | Quattro strumenti ispezionati nel sorgente, diretti e indiretti |
| [ANALISI_USABILITA.md](ux/ANALISI_USABILITA.md) | Dove si rompe un calcolatore fiscale per chi non è del mestiere |
| [ARCHITETTURA_INFORMAZIONE.md](ux/ARCHITETTURA_INFORMAZIONE.md) | Mappa degli stati, gerarchia dei contenuti, wireframe |
| [design/](ux/design/) | Il progetto Figma: contenuti, montaggio, e le esportazioni che lo rendono leggibile anche senza Figma |

### [diario/](diario/) — il percorso in ordine di accadimento

| | |
|---|---|
| [DIARIO_DI_BORDO.md](diario/DIARIO_DI_BORDO.md) | Quarantuno voci scritte man mano, mescolate alle scoperte sul dominio |

Il diario è un **artefatto di lavoro**, non una consegna: racconta la stessa
storia degli altri documenti in ordine cronologico e con più dettagli. Sta qui
perché è la prova che i documenti sopra non sono stati scritti alla fine per
sembrare metodici.

---

## Una nota sul volume

Sono circa quarantamila parole, ed è una scelta che va difesa invece che
nascosta.

L'annuncio dice *«eviti il perfezionismo»*, e ha ragione: il perfezionismo è
rifinire una cosa che nessuno userà. Ma due dei tre criteri di valutazione del
task sono **ricerca** e **strutturazione**, e sono esattamente le due cose che
un prototipo funzionante non dimostra da solo. Un calcolatore corretto e uno
sbagliato si somigliano: la differenza sta in quali fonti sono state lette,
quali semplificazioni sono state scelte, e quante volte la verifica ha smentito
chi la faceva.

Quello che sarebbe stato perfezionismo — e non è stato fatto — è aggiungere
altri comuni, altri contratti, altre funzioni. Il perimetro è rimasto quello
del task: **impiegato a tempo indeterminato, Milano, nessuna agevolazione**.
