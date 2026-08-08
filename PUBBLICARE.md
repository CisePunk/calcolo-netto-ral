# Pubblicare una modifica

Il giro completo, dalla correzione al sito aggiornato. Sono sei passi e due
comandi: gli altri li fanno le macchine.

---

## Il giro

```
1  modifichi                     motore/, api/, web/src/, dati/
2  provi                         python3 test_motore.py
3  costruisci come Render         docker build -t prova .
4  provi l'immagine               docker run -d -e PORT=8100 -p 8100:8100 prova
5  pubblichi                      git add -A && git commit && git push
6  verifichi                      bash strumenti/verifica_pubblicazione.sh <URL>
```

I passi 3 e 4 si possono saltare per una modifica ai documenti. **Non** per una
al codice: l'immagine che gira su Render è la stessa che si costruisce qui, e
provarla prima è l'unico modo per non scoprire un guasto dal messaggio d'errore
di un servizio remoto.

---

## 1–2. Modifica e prova

```bash
python3 test_motore.py                       # 413 test, ~15 secondi
python3 strumenti/controllo_sensibilita.py   # 17 guasti, ~4 minuti
```

Il primo dopo ogni modifica. Il secondo quando tocchi il registro dei
coefficienti o i test.

**Non serve ricordarsi di leggerne l'esito**: l'hook `pre-commit` blocca il
commit se i test non passano. Se hai clonato il repository da zero, attivalo una
volta sola:

```bash
git config core.hooksPath .githooks
```

> Se il controllo di sensibilità viene interrotto a metà, il registro resta
> guasto sul disco. Rilancialo: si accorge da solo e ripristina.

---

## 3–4. Costruisci e prova l'immagine

```bash
docker build -t prova .
docker run -d --name prova -e PORT=8100 -p 8100:8100 prova
bash strumenti/verifica_pubblicazione.sh http://127.0.0.1:8100
docker rm -f prova
```

Tredici controlli: calcolo, formati italiani, avviso sul minimo contrattuale,
quattro intestazioni di sicurezza, cinque percorsi ostili.

---

## 5. Pubblica

```bash
git add -A
git commit -m "cosa cambia e perché"
git push
```

---

## 6. Fai partire il deploy su Render

**Se Auto-Deploy è acceso**, parte da solo: quattro-sei minuti.

**Se non parte:**

1. [dashboard.render.com](https://dashboard.render.com) → servizio **`calcolo-netto-ral`**
2. **Manual Deploy** → **Deploy latest commit**
3. In **Settings**, metti **Auto-Deploy** su **Yes** così la prossima volta è automatico

Nei log devono passare i due stadi — `npm ci`, `✓ built in …`, poi `pip
install` — e chiudere con:

```
Uvicorn running on http://0.0.0.0:10000
==> Your service is live 🎉
```

---

## 7. Verifica che sia davvero online

```bash
bash strumenti/verifica_pubblicazione.sh https://calcolo-netto-ral.onrender.com
```

Deve dire **«Il link si può mandare»**. Se qualche riga è rossa, il deploy non è
passato o è passato a metà.

**Il controllo più veloce** per sapere se il codice nuovo è arrivato: chiedi
all'API una cosa che prima non c'era.

```bash
curl -s -X POST https://calcolo-netto-ral.onrender.com/api/inverso \
  -H 'content-type: application/json' \
  -d '{"netto":"3.000","mensile":true}' | grep -o netto_richiesto_mensile
```

Se stampa il nome del campo, online c'è la versione nuova. Sostituisci quel
campo con qualcosa introdotto dall'ultima modifica.

> **Non confrontare i nomi dei bundle.** Render compila il frontend dentro
> l'immagine, con la sua versione di Node: lo stesso sorgente può produrre un
> hash diverso da quello che ottieni tu con `npm run build`. Questa guida lo
> suggeriva, e dava falsi allarmi — il deploy era passato e il confronto diceva
> di no.

Se il deploy non parte da solo pur avendo Auto-Deploy «On Commit»:
**Manual Deploy → Deploy latest commit**. È successo, e non abbiamo capito
perché; il rimedio funziona comunque.

---

## Dove sta cosa

| | |
|---|---|
| Sito | https://calcolo-netto-ral.onrender.com |
| Repository | https://github.com/CisePunk/calcolo-netto-ral |
| Servizio | Render, piano gratuito, Francoforte |
| Non si spegne perché | un timer sul VPS `164.132.198.90` chiama `/api/salute` ogni 10 minuti |

Il piano gratuito dà 750 ore al mese e tenerlo sveglio ne consuma circa 720: ci
sta un servizio solo. Se ne pubblichi un altro, uno dei due dovrà dormire.

Per fermare il ping:

```bash
ssh root@164.132.198.90 'systemctl disable --now sveglia-calcolo.timer'
```

---

## Se qualcosa va storto

| Sintomo | Dove guardare |
|---|---|
| Il commit viene rifiutato | i test non passano — l'hook te lo dice e suggerisce la causa |
| Il build fallisce su Render | rifallo in locale con `docker build`: stessa immagine, errore più leggibile |
| Il sito risponde ma è la versione vecchia | il deploy non è partito: **Manual Deploy** |
| Prima apertura lentissima | il servizio si era spento: controlla il timer sul VPS |
| Numeri diversi da quelli attesi | `git diff dati/coefficienti.json` — un controllo di sensibilità interrotto lascia il registro guasto |
