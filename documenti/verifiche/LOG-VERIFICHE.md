# Log delle verifiche — 9 agosto 2026

Registro tecnico: comando eseguito → esito. Nessun commento, solo cosa è stato
fatto e cosa ha risposto. Il documento discorsivo è [SICUREZZA.md](SICUREZZA.md).

Bersaglio: `https://calcolo-netto-ral.onrender.com` (sito pubblicato) e il
repository `CisePunk/calcolo-netto-ral`.

---

## Richieste ricevute

1. «fai un giro di verifica su tutto il dalla ral al netto, incluso verifica cve»
2. «hai fatto le verifiche di sicurezza su ral?»
3. «hai pubblicato il report dei controlli sicurezza?»
4. «solo i check fatti, comandi eseguiti, i risultati ottenuti — niente filosofia»

---

## 1. Stato del repository

```
git fetch -q origin
git rev-list --left-right --count origin/main...main
git status --porcelain
```
Esito: `0  0` (locale e remoto allineati), albero pulito.

---

## 2. CVE — dipendenze installate vs versione che corregge

Versioni lette da:
```
.venv/bin/pip list | grep -iE "fastapi|uvicorn|starlette|pydantic|anyio"
python3 -c "import json; d=json.load(open('web/package-lock.json')); ..."
```
Installate: fastapi 0.141.1 · starlette 1.4.1 · uvicorn 0.52.1 · pydantic 2.13.4
· react 19.2.8 · vite 8.2.1.

Confronto (ricerca web delle CVE 2026 + confronto versioni):

| Pacchetto | Installata | CVE | Fix | Esito |
|---|---|---|---|---|
| Vite | 8.2.1 | CVE-2026-39363 / 39364 (file read dev server) | 8.0.5 | non vulnerabile |
| Starlette | 1.4.1 | CVE-2026-48710 (BadHost, auth bypass) | 1.0.1 | non vulnerabile |
| Starlette | 1.4.1 | CVE-2025-62727 (ReDoS) | 0.49.1 | non vulnerabile |

```
cd web && npm audit --omit=dev      → found 0 vulnerabilities
cd web && npm audit                 → found 0 vulnerabilities
```

Nota tecnica: Vite è dipendenza di **build**, non di runtime. Il container di
produzione compila il frontend e serve file statici via FastAPI; il dev server
di Vite non è in esecuzione. La CVE `/@fs/` non è raggiungibile a runtime a
prescindere dalla versione — che è comunque patchata.

---

## 3. Probe del dev server Vite sul sito vivo

```
curl -s -o /dev/null -w '%{http_code}' --path-as-is "$U/@fs/../.env"
curl -s --path-as-is "$U/@fs/../.env" | head -c 120
```
Esito: risposta = `<!doctype html>` (ripiego single-page). Nessun file `.env`,
nessun dev server esposto. Ripetuto per `/@vite/client`, `/src/main.jsx`,
`/@fs/..%252f..%252f..%252fapp/.env`: tutti ripiego SPA.

Nota tecnica: lo stato HTTP era `200` perché ogni percorso ignoto ricade su
`index.html`. Conta il **corpo**, non lo stato — verificato che il corpo sia la
pagina, non il file.

---

## 4. Intestazioni di sicurezza (risposta del server)

```
curl -s -D - -o /dev/null "$U/" | grep -iE "^(content-security-policy|x-frame-options|x-content-type-options|referrer-policy|permissions-policy)"
```
Esito:
```
content-security-policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; …
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: geolocation=(), microphone=(), camera=(), payment=()
```
Cinque su cinque presenti.

---

## 5. Attraversamento percorsi (stato + contenuto)

```
for p in /../dati_privati/LEGGIMI.md /../api/main.py /../dati/coefficienti.json /../../etc/passwd ; do
  curl -s -o /dev/null -w '%{http_code}' --path-as-is "$U$p"
  curl -s --path-as-is "$U$p" | grep -iE "root:.*:0:0:|import |_fonte|Certificazione|coefficienti"
done
```
Esito:

| Percorso | HTTP | File trapelato |
|---|---|---|
| `/../dati_privati/LEGGIMI.md` | 400 | no |
| `/../api/main.py` | 400 | no |
| `/../dati/coefficienti.json` | 400 | no |
| `/../../etc/passwd` | 400 | no |

Nota tecnica: `400 Bad Request` = il server rifiuta la richiesta malformata,
non serve il file. `--path-as-is` impedisce a curl di normalizzare `..` da solo
(altrimenti la richiesta ostile partirebbe già innocua). Il grep sul contenuto
conferma che nessun file reale esce.

---

## 6. Verifica funzionale sul sito vivo

```
bash strumenti/verifica_pubblicazione.sh https://calcolo-netto-ral.onrender.com
```
Esito: **13 / 13**.
```
la pagina risponde                     ok
controllo di salute                    ok
interfaccia compilata servita          ok
35.000 -> 26.032,22 netti              ok
formati italiani: 35.000 = 35000       ok
avviso minimo contrattuale su 10.000   ok
CSP / X-Frame / nosniff / Referrer     ok
HTTPS certificato valido               ok
nessuna fuga di file (5 percorsi)      ok
```

---

## 7. Segreti nella storia di Git

```
git rev-list --objects --all            → 266 oggetti
# scansione con 6 modelli (OpenAI, Anthropic, GitHub, AWS, Google, chiavi private, URL con password)
```
Esito: nessun segreto in nessun oggetto della storia.

Dati privati versionati:
```
git ls-files dati_privati
```
Esito: solo `.gitignore`, `LEGGIMI.md`, `cu_modello.json` (modello vuoto). Nessun
`cu.json`, nessun `.env`.

---

## 8. Test e mutazioni (rieseguiti)

```
python3 test_motore.py                        → 413 test superati
python3 strumenti/controllo_sensibilita.py    → 17 guasti su 17 rilevati
```

---

## Esito complessivo

Nessun difetto aperto sul sito pubblicato. Tutte le CVE dello stack: versioni
patchate. Repository pulito. Documentato in [SICUREZZA.md](SICUREZZA.md),
aggiornamento del 9 agosto.

## Come ripetere tutto

```
python3 test_motore.py
python3 strumenti/controllo_sensibilita.py
bash strumenti/verifica_pubblicazione.sh https://calcolo-netto-ral.onrender.com
cd web && npm audit
```
