# Il bug che torna

Tre volte lo stesso difetto, in tre punti diversi del programma, a distanza di
settimane. La storia sta scritta a pezzi nel [registro degli errori](ERRORI.md),
alle voci 12, 20 e 27. Qui sta per intero, perché letta di seguito dice una cosa
che le tre voci separate non dicono.

---

## 35.000

Il primo giorno che ho aperto l'applicazione da utente invece che da chi la
scrive, ho digitato la cifra che avevo in testa da settimane: trentacinquemila
euro. L'ho scritta come la scrivo sempre, `35.000`.

Il risultato è arrivato subito, ordinato, con tutte le voci al posto giusto.
Diceva che su trentacinque euro di retribuzione annua lorda ne restavano
trentadue e spiccioli.

In Python, `float("35.000")` vale trentacinque. Il punto è il separatore
decimale, e trentacinquemila scritto all'italiana diventa un numero di due
cifre. Non c'è nessun errore: la funzione fa quello che deve, su una stringa che
significa un'altra cosa.

La parte che mi ha dato più fastidio è che il campo suggeriva, in grigio,
`es. 35.000`. Avevo scritto io il segnaposto. Lo strumento proponeva una forma e
la leggeva male.

Trecentoquattro test non l'avevano vista, e c'è una ragione: li avevo scritti io,
e chi scrive un test sa già come si digita un numero. Nessuno di quei test
passava una stringa con il punto, perché a nessuno di noi veniva in mente di
farlo. Ci vuole qualcuno che digiti come digita la gente, e quel giorno la
persona ero io, per un quarto d'ora, per caso.

Ho scritto una funzione che legge gli importi come li scrivono le persone:
`35.000`, `35.000,50`, `35 000`, `€ 35.000`, e anche `35,000.50` per chi ha
imparato l'informatica in inglese. Ventidue test nuovi. Il caso sembrava chiuso.

---

## 2.000

Settimane dopo, a lavoro finito e documentato, ho dato il progetto in lettura a
qualcuno che non l'aveva costruito.

Ha provato il percorso inverso, quello che dal netto desiderato risale al lordo
da offrire. Ha scritto `2.000` e ha ottenuto una retribuzione annua lorda di
ventinove euro.

Il calcolo diretto usava la funzione nuova. Il calcolo inverso, che vive in un
altro file e ha un altro punto d'ingresso, usava ancora `float()`. Avevo corretto
il difetto dove si era manifestato, e non dove abitava.

C'era anche un dettaglio che mi ha imbarazzata più del difetto. Il messaggio
d'errore diceva: *«Il netto deve essere un numero. Esempio: 1800 oppure
1.800,50»*. Delle tre forme che citava, quella con il punto era l'unica che
rifiutava. Lo strumento suggeriva un formato e poi lo respingeva, con la stessa
voce sicura.

Dieci test coprivano il calcolo inverso. Tutti e dieci gli passavano numeri già
puliti, `1500`, mai `"1.500"`. Provavano la funzione in un modo in cui
l'interfaccia non la usa mai.

Ho fatto usare a tutti e due i percorsi la stessa funzione. Questa volta, ho
pensato, è chiusa davvero.

---

## 3.000

Ieri, con la consegna già partita, ho chiesto quanto lordo serve per garantire
tremila euro netti al mese. Ho letto:

> Per garantire **3,00 € al mese** serve una RAL di **69.418 €**.

Il numero grande era giusto. Per tremila euro netti al mese servono davvero
circa sessantanovemila euro di lordo: il motore aveva capito benissimo, aveva
fatto il conto e l'aveva fatto bene. Sbagliata era soltanto la frase che lo
raccontava.

Ci ho messo un momento a capire perché mi sembrasse più grave, e non meno, del
fatto che un calcolo desse un risultato sbagliato. È che chi legge non ha modo di
sapere quale delle due cifre sia quella buona. Vede tre euro accanto a
sessantanovemila e conclude, ragionevolmente, che lo strumento non sappia fare i
conti. Un errore visibile si corregge. Un errore che squalifica il numero giusto
accanto a sé fa chiudere la pagina.

La causa era una riga sola. Il server risponde con il netto **annuo**,
quarantaduemila, cioè tremila per quattordici mensilità. Per mostrare il mensile
bisognava dividere, e invece di chiedere al server quanto avesse capito,
l'interfaccia si è riletta il campo di testo da sola:

```jsx
{euro(nettoMensile ? Number(netto) : inverso.netto_richiesto)}
```

`Number("3.000")` in JavaScript vale tre. È lo stesso identico difetto della
prima volta, in un'altra lingua di programmazione, dentro il browser invece che
sul server.

Poi ho aperto il file `numeri.js`, che sta nella stessa cartella. Contiene la
funzione che gestisce i formati italiani nel frontend, e in cima al suo commento
c'è scritto:

> *Il motivo per cui serve: `Number("35.000")` in JavaScript vale 35.*

L'avevo scritta io, settimane prima, per la stessa ragione. La trappola era
documentata a un file di distanza. Non è servito a niente.

---

## Quello che ho fatto invece

La correzione ovvia era chiamare la funzione giusta anche lì. Ci ho pensato per
il tempo di scriverla, e poi l'ho cancellata.

Avrebbe chiuso la terza porta e lasciato la quarta dov'era. Non sapevo dove
fosse la quarta, ed è esattamente questo il punto: non lo sapevo neanche le due
volte precedenti, e le due volte precedenti c'era.

La domanda che mi ero fatta fino a quel momento era *dove altro leggo un
numero?*. È una domanda che si risolve cercando, e cercando si trova quello che
si è capaci di immaginare. La domanda giusta era un'altra:

> **Perché due parti diverse del programma leggono lo stesso numero?**

Finché la risposta è «perché a ognuna serve», la quarta porta arriva.

Così ho tolto il motivo. Il risultato del calcolo inverso porta adesso con sé le
mensilità che ha usato, e l'API restituisce il netto mensile già diviso.
L'interfaccia non fa più nessun conto e non rilegge più niente: mostra quello che
il server ha capito. Non può disallinearsi dal calcolo nemmeno volendo, perché
non calcola.

Verificato su quattro formati e su due contratti diversi, per accertare che il
divisore venga dal CCNL e non da un numero fisso: quattordici mensilità danno
quarantaduemila euro annui, tredici ne danno trentanovemila. Tredici test nuovi.

---

## Cosa insegna

**Un difetto che ricompare tre volte in tre punti diversi non è una
distrazione.** È un pezzo di architettura che manca, e finché manca continuerà a
uscire da porte che non si sono ancora guardate.

Le prime due correzioni erano giuste e insufficienti nello stesso modo:
toglievano il sintomo dal posto in cui era comparso. La terza è stata diversa
non perché fosse più accurata, ma perché ha cambiato la domanda.

C'è una seconda cosa, meno comoda da dire. La soluzione esisteva già, scritta da
me, con la trappola annotata nel commento, in un file aperto decine di volte.
Sapere non basta. Fra il sapere una cosa e l'averla messa nel punto in cui il
programma non può farne a meno c'è tutta la distanza che conta.

E la terza, che vale per tutte e ventisette le voci del registro: **nessuna è
stata trovata rileggendo il codice.** Queste tre le hanno trovate, nell'ordine,
il fatto di usare lo strumento, una persona che non l'aveva costruito, e di nuovo
il fatto di usarlo. Rileggere il proprio codice lo conferma. Per contraddirlo
bisogna eseguirlo in un modo che non era previsto.
