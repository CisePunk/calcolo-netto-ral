# Controllo di sicurezza

**Data:** 7 agosto 2026 · **Perimetro:** motore, API, interfaccia, database,
strumenti · **Metodo:** manuale, con verifica eseguita di ogni conclusione.

---

## Perché un prototipo viene controllato

Questo strumento non tratta dati personali, non ha utenti registrati e non ha
niente da rubare. La tentazione è di saltare il controllo.

Il motivo per cui non è stato saltato è che **le tre cose che sono venute fuori
non dipendevano da quanto è importante l'applicazione.** Erano difetti presenti
nel codice per come è scritto, e sarebbero stati identici in un prodotto vero
con dentro le retribuzioni di duemila persone. La differenza fra un prototipo e
quel prodotto non sta nel codice: sta in cosa gli si mette accanto.

E una delle tre, quella più seria, permetteva di leggere **la cartella che in
questo progetto contiene un documento fiscale reale.**

---

## Quadro d'insieme

| # | Verifica | Esito |
|---|---|---|
| 1 | Lettura di file arbitrari dal server | ❌ **trovata e corretta** |
| 2 | Ingressi estremi (numeri enormi, cifre non latine) | ❌ **trovati e corretti** |
| 3 | Intestazioni di sicurezza HTTP | ❌ assenti → aggiunte |
| 4 | Limite di frequenza sulle richieste | ❌ assente → aggiunto |
| 5 | Database esposto sulla rete locale | ❌ trovato → corretto |
| 6 | Iniezione SQL nel generatore del seed | ✅ già protetto |
| 7 | Iniezione di codice nell'interfaccia | ✅ nessun vettore |
| 8 | Fuga di informazioni nei messaggi d'errore | ⚠️ input riflesso → troncato |
| 9 | CORS | ✅ ristretto correttamente |
| 10 | Dipendenze di terze parti | ✅ zero vulnerabilità note |
| 11 | Consumo di risorse per richiesta | ✅ misurato, accettabile |
| 12 | Dati personali nel repository | ✅ esclusi per costruzione |
| 13 | Chiavi API nella storia di Git (180 oggetti, 11 modelli) | ✅ nessuna — vedi l'aggiornamento in coda |
| 14 | Esposizione dei segreti CI (CVE-2026-54316 / 12537) | ✅ non applicabile: 0 workflow, 0 segreti, issue chiuse |

**Tre difetti reali, due omissioni, una debolezza minore.** Nessuno era visibile
leggendo il codice con l'occhio di chi l'ha scritto: sono venuti fuori tutti
provando a fare, da fuori, cose che il codice non si aspettava.

---

## 1. Lettura di file arbitrari (la più seria)

**Come funzionava.** L'API serve anche l'interfaccia compilata. Una rotta
generica raccoglie tutto ciò che non è `/api/...` e, se corrisponde a un file
dentro `web/dist`, lo restituisce:

```python
file = FRONTEND / percorso        # ← qui
if file.is_file():
    return FileResponse(file)
```

`FRONTEND / "../../dati_privati/LEGGIMI.md"` **è un file.** `pathlib` compone i
percorsi, non li giudica: `..` risale di una cartella e basta.

**Cosa era raggiungibile.** Tutto ciò che sta sotto la radice del progetto:
`api/main.py`, `dati/coefficienti.json`, gli strumenti — e `dati_privati/`, la
cartella tenuta fuori dal repository **proprio perché contiene una
Certificazione Unica vera.** Il `.gitignore` la protegge da Git. Non la
proteggeva dal server web.

**La correzione.** Il percorso viene risolto e poi confrontato con la radice
consentita: se dopo la risoluzione non sta più dentro, non esiste.

```python
candidato = (FRONTEND / percorso).resolve()
radice = FRONTEND.resolve()
if candidato == radice or radice in candidato.parents:
    return candidato if candidato.is_file() else None
return None
```

`.resolve()` prima del confronto è la parte che conta: normalizza `..`,
i collegamenti simbolici e i separatori ripetuti. Confrontare le stringhe prima
di risolverle è il modo classico di scrivere un controllo che non controlla.

**Verifica eseguita.**

| Richiesta | Prima | Dopo |
|---|---|---|
| `index.html` | servito | servito |
| `./index.html` | servito | servito |
| `assets/../index.html` | servito | servito |
| `../../api/main.py` | **servito** | respinto |
| `../../dati_privati/LEGGIMI.md` | **servito** | respinto |
| `../../../../etc/passwd` | **servito** | respinto |
| `%2e%2e/index.html` | **servito** | respinto |
| `..` | errore | respinto |

**Nota onesta.** Molti server normalizzano il percorso prima di consegnarlo
all'applicazione, e dietro a un proxy questo difetto potrebbe non essere
sfruttabile. È esattamente il tipo di ragionamento che porta a non correggere:
una difesa che dipende da cosa c'è davanti non è una difesa del codice, è una
fortuna. Se domani l'applicazione gira dietro qualcos'altro, la fortuna finisce
senza che nessuno se ne accorga.

---

## 2. Ingressi estremi

Il campo della RAL accettava:

- `1e308` — notazione scientifica, prossimo al massimo di un `float`. Il calcolo
  proseguiva e produceva importi privi di significato.
- `"9" * 30` — un miliardo di miliardi di miliardi di euro.
- `٣٥٠٠٠` (cifre arabo-indiane) e `३५०००` (devanagari) — `float()` in Python le
  accetta e le converte in 35000.

L'ultimo è il più interessante, e non perché sia pericoloso di per sé: è che in
un campo di modulo **due stringhe visivamente diverse producevano lo stesso
importo**, e nessuna delle due era quella che l'utente credeva di aver scritto.
In uno strumento che serve a mettersi d'accordo su una cifra, un'ambiguità
grafica non è un dettaglio tecnico.

**La correzione.** Un limite assoluto e un filtro sui caratteri ammessi:

```python
RAL_LIMITE_ASSOLUTO = 100_000_000.0

if not all(c in "0123456789.,+-" for c in pulito):
    raise ValueError("caratteri non ammessi")
```

Meglio rifiutare che indovinare. Se qualcuno digita davvero una RAL in
devanagari, riceve un errore chiaro invece di un risultato che sembra giusto.

---

## 3. Intestazioni di sicurezza

Erano **tutte assenti**. Aggiunte in un middleware:

| Intestazione | Valore | A cosa serve qui |
|---|---|---|
| `Content-Security-Policy` | `default-src 'self'`, `frame-ancestors 'none'`, `object-src 'none'` … | La pagina non carica **niente** da fuori: nessun carattere tipografico remoto, nessuna libreria da CDN. Questo permette una politica strettissima. |
| `X-Content-Type-Options` | `nosniff` | Impedisce al browser di indovinare il tipo di un file servito. |
| `X-Frame-Options` | `DENY` | Nessuno può incorniciare la pagina. Su uno strumento con un pulsante di conferma il clickjacking non è teorico. |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | La RAL digitata sta nella query string. Senza questa, finisce nei log di chiunque venga raggiunto da un link. |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), payment=()` | Rinuncia esplicita a permessi che non servono. |

L'unico allentamento è `style-src 'unsafe-inline'`, necessario perché le
larghezze dei segmenti del grafico sono calcolate e scritte in linea. È
annotato nel codice, non nascosto.

**Verifica eseguita** — risposta del server dopo la correzione:

```
content-security-policy: default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; …
x-content-type-options: nosniff
x-frame-options: DENY
referrer-policy: strict-origin-when-cross-origin
permissions-policy: geolocation=(), microphone=(), camera=(), payment=()
```

**Un difetto nato dalla correzione stessa.** Alla prima stesura le intestazioni
c'erano su tutte le risposte **tranne una**: il `429` del limite di frequenza
usciva nudo. Starlette costruisce la pila dei middleware al contrario —
l'ultimo registrato è il più esterno — e il limite, registrato dopo, chiudeva
la richiesta prima che passasse dallo strato delle intestazioni.

Non si vedeva provando la pagina, perché quella risposta arriva solo dopo
centoventi richieste in un minuto. Si è vista **mandandone centoventuno e
guardando l'intestazione della risposta bloccata.** I due blocchi sono stati
invertiti e l'ordine è annotato nel codice con il motivo, perché è il tipo di
riga che qualcuno riordinerà in buona fede.

È il caso in miniatura di tutto il resto: una difesa che c'è, che funziona, e
che non copre l'unico percorso che nessuno aveva provato a percorrere.

---

## 4. Limite di frequenza

**Misura.** Calcolo diretto: **0,6 ms**. Calcolo inverso (netto → lordo, per
bisezione su ogni segmento): **14,6 ms**, circa venticinque volte tanto.

Non è un costo alto in assoluto, ma è asimmetrico: fare la richiesta costa a chi
la manda molto meno di quanto costi a chi la serve. Senza alcun limite, un solo
client occupa il servizio a costo quasi nullo per sé.

**La correzione.** Un limite in memoria, 120 richieste al minuto per indirizzo,
applicato solo ai percorsi `/api/`. Verifica: la 121ª richiesta consecutiva
riceve `429 Too Many Requests` con `Retry-After: 60`; la pagina continua a
essere servita normalmente.

**Limite dichiarato.** È volutamente elementare. Lo stato sta in memoria: con
più processi o più macchine il conteggio si moltiplica, e non regge una
distribuzione su molti indirizzi. È scritto nel codice perché chi legge non lo
scambi per una difesa completa. In produzione questo lavoro va a un reverse
proxy o al gestore dell'hosting, non a un middleware applicativo.

---

## 5. Database esposto

`docker-compose.yml` pubblicava la porta così:

```yaml
- "3307:3306"
```

Docker interpreta questa forma come `0.0.0.0:3307`: **tutte le interfacce**. Su
una rete condivisa — un ufficio, una biblioteca, un bar — il database è
raggiungibile da chiunque, con la password di sviluppo scritta in chiaro nel
file. Corretto in `127.0.0.1:3307:3306`.

**Sulla password.** Resta `sviluppo`, sovrascrivibile da variabile d'ambiente.
Non è stata cambiata perché una password diversa ma comunque scritta nel
repository non è più sicura: sarebbe teatro. Ciò che rende accettabile la
password debole è che la porta ora non esce dalla macchina, e che il database
contiene **solo il registro dei coefficienti** — dati pubblici, rigenerabili con
un comando. Non ci sono retribuzioni dentro.

---

## 6. Le verifiche che non hanno trovato niente

Vanno elencate anche queste, altrimenti il documento racconta solo metà del
lavoro.

**Iniezione SQL nel generatore del seed.** `strumenti/genera_seed.py` scrive SQL
partendo dal JSON dei coefficienti. Gli apostrofi vengono raddoppiati, i valori
numerici passano da `float()`. Controllato che nel file generato non compaia
`DROP`, `;--` o `/*` fuori dalle stringhe. Il file è generato da dati che
stanno nel repository, non da input esterno: il rischio è basso a monte, ma il
codice regge comunque.

**Iniezione nell'interfaccia.** Zero occorrenze di `innerHTML`,
`dangerouslySetInnerHTML`, `eval`, `new Function`. React scherma il testo per
impostazione predefinita e non è stato aggirato in nessun punto.

**CORS.** Ristretto a `localhost:5173` e `127.0.0.1:5173`, i due indirizzi del
server di sviluppo. Verificato che una richiesta con `Origin` ostile non riceva
alcuna intestazione CORS in risposta.

**Dipendenze.** `npm audit`: **0 vulnerabilità**. Il motore Python non ha
dipendenze — è una scelta di progetto, e qui si vede il secondo motivo per cui è
stata fatta: nessuna dipendenza è anche nessuna dipendenza da aggiornare.
Verificato inoltre che Playwright, usato solo per le prove, non sia finito fra
le dipendenze del pacchetto.

**Messaggi d'errore.** Nessuna traccia di stack trace, percorsi assoluti o
dettagli interni nelle risposte. Il codice del territorio e del CCNL vengono
però *rimandati indietro* nel messaggio: rispedire al mittente un ingresso
arbitrariamente lungo trasforma un errore di battitura in una risposta di
dimensione scelta da chi chiama. Aggiunto `_abbreviato()`, che taglia a 24
caratteri.

**Preferenze salvate nel browser.** `localStorage` contiene solo quattro
preferenze di leggibilità — nessuna RAL, nessun risultato, niente che riguardi
una persona. Erano però rilette senza controllo: un valore rimasto da una
versione precedente finiva in un attributo `data-` a cui nessuna regola CSS
corrisponde, e la pagina restava **senza tema**, senza alcun errore visibile.
Aggiunto un elenco di valori ammessi per ciascuna leva, validati uno per uno
così che una preferenza corrotta non butti via anche le altre tre.

---

## Rischi che restano, dichiarati

Un documento di sicurezza che finisce con «adesso è sicuro» è un documento che
non è stato scritto fino in fondo.

1. **Il limite di frequenza non regge una distribuzione.** Molti indirizzi
   diversi lo aggirano per costruzione. In produzione serve un livello sopra.
2. **Non c'è autenticazione**, perché non c'è niente da proteggere: lo strumento
   è pubblico e senza stato. Diventa un problema **il giorno in cui qualcuno ci
   attacca l'anagrafica dei dipendenti** — che è esattamente la direzione in cui
   uno strumento del genere tende a crescere.
3. **Il calcolo passa in query string.** Comodo per condividere un link, ma
   la RAL finisce nella cronologia e nei log del server. Accettabile per un
   simulatore; da rivedere se un giorno l'importo è quello di una persona
   identificabile.
4. **La password del database è debole**, mitigata dal fatto che la porta non
   esce dalla macchina e che dentro ci sono solo dati pubblici.
5. **`style-src 'unsafe-inline'`** resta necessario. Si toglie sostituendo gli
   stili in linea con proprietà personalizzate CSS: fattibile, non fatto.
6. **Non c'è stato un test di penetrazione**, né un'analisi automatica con
   strumenti dedicati. Questo è un controllo manuale, fatto da chi ha scritto il
   codice — con tutti i limiti che questo comporta, primo fra tutti che si
   cercano gli errori che si è capaci di immaginare.

---

## Cosa ha trovato cosa

| Metodo | Difetti trovati |
|---|---|
| **Costruire una richiesta ostile e mandarla davvero** | 1 (lettura file), 8 (input riflesso) |
| **Dare in pasto ingressi assurdi al motore** | 2 (numeri enormi, cifre non latine) |
| **Guardare la risposta del server invece della pagina** | 3 (intestazioni assenti) |
| **Misurare quanto costa una richiesta** | 4 (nessun limite) |
| **Leggere la configurazione come la legge Docker, non come sembra scritta** | 5 (database esposto) |

Lo schema è lo stesso degli altri difetti raccolti in [ERRORI.md](ERRORI.md):
**nessuno è stato trovato rileggendo il codice.** Rileggere il proprio codice
lo conferma; per contraddirlo bisogna eseguirlo in un modo che non era previsto.

---

## Dopo le correzioni

```
413 test superati
17/17 mutazioni rilevate
```

Le correzioni hanno toccato la validazione dell'ingresso, che è coperta da test.
Nessuna regressione.

---

## Aggiornamento del 7 agosto 2026 — le vulnerabilità sulle chiavi API

Sono uscite in pochi giorni quattro segnalazioni che riguardano l'esposizione di
chiavi API: LiteLLM (CVE-2026-42208, iniezione SQL pre-autenticazione), Ruflo
(CVE-2026-59726, CVSS 10.0, accesso senza password), n8n (CVE-2026-21858,
CVSS 10.0) e una coppia che tocca **Claude Code e Gemini CLI nei sistemi di
integrazione continua** — CVE-2026-54316 e CVE-2026-12537.

Quest'ultima è l'unica che poteva riguardarci, ed è stata verificata invece che
esclusa a occhio, perché parte di questo lavoro è stata svolta con assistenza AI
e il repository è pubblico.

### Il meccanismo, e perché non ci tocca

Lo sfruttamento richiede **tre condizioni insieme**:

| Condizione | Da noi |
|---|---|
| Un workflow di integrazione continua che esegua quegli strumenti | **0 workflow.** Non esiste nemmeno la cartella `.github/` |
| Un innesco raggiungibile da utenti non fidati (tipicamente le issue) | **issue disattivate** al momento della creazione del repository |
| Segreti disponibili al runner | **0 segreti** configurati |

Nessuna delle tre. La catena non si chiude in nessun punto.

Vale la pena aggiungere che il progetto **non usa nessuna chiave API**: il
motore non ha dipendenze, l'interfaccia non contatta domini esterni — è la
stessa proprietà che permette una politica dei contenuti strettissima (punto 3)
— e nel codice non c'è una sola lettura di variabile d'ambiente.

### Verifica eseguita sulla storia, non solo sui file di adesso

Un segreto cancellato resta negli oggetti di Git. Sono stati quindi esaminati
**tutti i 180 oggetti** mai esistiti nel repository, non l'albero corrente, con
undici modelli: chiavi OpenAI, Anthropic, GitHub (classiche e fine-grained),
AWS, Google, Slack, Stripe, token JWT, chiavi private e URL con credenziali
incorporate.

Un solo riscontro, ed è stato **guardato invece che archiviato**: era una
sequenza di byte casuali dentro `09-esperto-risultato-e-fonti.png`. Un file
binario, non del testo con dentro una password. È il tipo di riscontro che si
liquida come falso positivo senza controllare, ed è così che ogni tanto ne passa
uno vero.

### Le altre tre segnalazioni

LiteLLM, n8n e Ruflo non sono fra le dipendenze — verificato su
`requirements.txt` e `package.json`, che contengono in tutto due pacchetti
Python e le dipendenze di Vite. Non è un merito: è la conseguenza della scelta
di non avere dipendenze, che qui mostra il terzo motivo per cui è stata fatta.

### Cosa è stato irrigidito lo stesso

Nessuna delle tre condizioni era soddisfatta, ma due potevano diventarlo domani
— basta che qualcuno aggiunga un workflow, o riapra le issue.

| Impostazione | Prima | Ora |
|---|---|---|
| GitHub Actions | abilitate (predefinito) | **disattivate** |
| Permessi predefiniti dei workflow | scrittura (predefinito) | **sola lettura** |
| Issue, wiki, projects, discussions | issue e wiki già chiuse | **tutte chiuse** |

Actions è disattivato perché **a questo progetto non serve**: i test si lanciano
con un comando e senza dipendenze, e chi vuole verificarli lo fa in locale in
quindici secondi. Una funzione accesa senza che nessuno la usi è solo superficie
d'attacco che nessuno guarda.

I permessi in sola lettura restano impostati anche con Actions spento: se un
giorno qualcuno lo riaccende, riparte dal comportamento prudente invece che da
quello predefinito.

### Sulla macchina di sviluppo

Claude Code installato: **2.1.183**, oltre la 2.1.163 che corregge
CVE-2026-54316. Gemini CLI non installato.

### Il rischio che resta

Una vulnerabilità di questa classe **non si chiude una volta**: la porta era
chiusa perché non l'avevamo ancora aperta, non perché fosse stata rinforzata. Il
giorno in cui questo prototipo avesse una pipeline di rilascio — cioè il primo
giorno di vita vera — le tre condizioni tornerebbero tutte disponibili insieme.

La regola da portarsi dietro è quella indicata dagli stessi avvisi:
**qualunque workflow attivabile da un utente esterno va trattato come codice
ostile**, e non deve mai vedere i segreti nello stesso passaggio in cui tocca
input non fidato.

