# Dati privati — questa cartella non finisce nel repository

Il motore viene confrontato con una **Certificazione Unica reale**, perché
confrontarsi con un altro calcolatore online dimostra solo che due prototipi
sbagliano allo stesso modo.

Una CU però contiene dati personali. La regola di questo progetto è netta:

> **Gli importi restano sul computer di chi li possiede. Nel repository entrano
> solo il confronto e il suo esito, mai le cifre.**

Il `.gitignore` di questa cartella esclude ogni file tranne il modello vuoto e
questo testo. Anche un `git add -A` distratto non porta via nulla.

## Come si usa

```bash
cp dati_privati/cu_modello.json dati_privati/cu.json
# riempi cu.json con i valori della CU
python3 strumenti/confronta_cu.py
```

Servono **nove importi** e nient'altro: niente nome, niente codice fiscale,
niente datore di lavoro. I campi che non trovi lasciali a `null` — il confronto
salta le voci mancanti invece di fallire.

## Cosa il confronto può dimostrare, e cosa no

La CU disponibile copre un **periodo di lavoro parziale**. Detrazioni, somma
esente e trattamento integrativo sono per legge rapportate ai giorni, quindi:

- **con** il numero di giorni indicato, tutte e nove le voci sono confrontabili;
- **senza**, restano confrontabili contributi, imponibile e IRPEF lorda — cioè
  la meccanica degli scaglioni, che è il cuore del motore.

## Se qualcosa non torna

Prima di sospettare il motore, in quest'ordine:

1. **L'anno.** Una CU emessa nel 2026 riguarda i redditi **2025**, dove la
   seconda aliquota IRPEF è 35% e non 33%.
2. **Il territorio.** Le addizionali cambiano per comune e regione. L'aliquota
   di Palermo è passata da 1,002% a 1,014% a 1,404% in tre anni d'imposta.
3. **I giorni.** Detrazioni e bonus sono rapportati al periodo di lavoro.
4. **Le detrazioni che il prototipo non tratta**: familiari a carico, mutuo,
   spese sanitarie. Sono dichiarate nelle ASSUNZIONI.

Lo strumento è stato provato prima dell'uso, con una CU sintetica generata dal
motore stesso: nove voci su nove coincidenti. E ripetendo la prova con l'anno
d'imposta sbagliato, ha isolato correttamente l'unica voce che ne risente.
