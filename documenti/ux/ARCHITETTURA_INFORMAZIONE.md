# Architettura dell'informazione e wireframe

Come è organizzato quello che l'utente vede, in che ordine, e perché in
quest'ordine e non in un altro.

I wireframe sono in caratteri di testo invece che in immagini per una ragione
pratica: stanno nel repository, si leggono in una `diff`, e si aggiornano
insieme al codice. Un'immagine esportata da uno strumento di disegno diverge dal
prodotto il giorno dopo averla fatta.

---

## 1. Che tipo di oggetto è

Non è un sito con delle pagine: è **uno strumento con degli stati**. La
distinzione conta, perché sposta il lavoro di architettura da *«dove metto le
pagine»* a *«cosa è visibile quando, e cosa può cambiare senza far ricominciare
da capo»*.

```
                      ┌──────────────────────────────┐
                      │   /  — il calcolatore        │
                      └──────────────┬───────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        │                            │                            │
   DIREZIONE                    ESPERIENZA                   LEGGIBILITÀ
   (2 schede)                   (2 livelli)                  (4 leve)
        │                            │                            │
  ┌─────┴─────┐              ┌───────┴───────┐          ┌─────────┴─────────┐
  │           │              │               │          │ tema              │
lordo→netto  netto→lordo   alle prime armi  esperto     │ dimensione testo  │
                                             │          │ contrasto         │
                                             │          │ visione colori    │
                                        ┌────┴────┐     └───────────────────┘
                                        │ fonti   │
                                        │ e stato │
                                        └─────────┘
```

Le tre dimensioni sono **indipendenti**: si può essere in «netto → lordo», da
esperto, con testo grande e senza colore. Sono 2 × 2 × (4 leve) combinazioni, e
nessuna azzera le altre.

**La regola che tiene insieme tutto:** cambiare una qualsiasi di queste
impostazioni **non perde mai quello che l'utente ha scritto**. Il caso da coprire
è chi si dichiara esperto, si blocca, e vuole tornare indietro senza
ricominciare.

---

## 2. Gerarchia dei contenuti

L'ordine verticale della pagina non è estetico: segue l'ordine in cui si
formano le domande di chi la usa.

| # | Blocco | Risponde a | Sempre visibile? |
|---|---|---|---|
| 1 | Titolo e sottotitolo | *«cos'è questa cosa?»* | sì |
| 2 | Avviso di indipendenza | *«è ufficiale?»* | sì |
| 3 | Leggibilità | *«riesco a leggerlo?»* | sì, richiudibile |
| 4 | Schede di direzione | *«ho il lordo o il netto?»* | sì |
| 5 | Campo principale | *«cosa devo inserire?»* | sì |
| 6 | Territorio | *«dove lavora questa persona?»* | sì |
| 7 | Parametri avanzati | *«e tutto il resto?»* | solo esperto |
| 8 | Avvisi | *«ho sbagliato qualcosa?»* | quando servono |
| 9 | Eco dell'input | *«cosa ha capito?»* | dopo il calcolo |
| 10 | Il netto | *«quanto prende?»* | dopo il calcolo |
| 11 | Ripartizione | *«quanto se ne va?»* | dopo il calcolo |
| 12 | Tabella voce per voce | *«perché?»* | dopo il calcolo |
| 13 | Conferma | *«posso fidarmi a usarlo?»* | solo neofita |
| 14 | Fonti e stato | *«da dove viene questo numero?»* | solo esperto |

**Il punto 3 sta in alto per una ragione precisa.** Chi ha bisogno di
ingrandire il testo ne ha bisogno *prima* di leggere, non dopo. Metterlo in
fondo, come si usa, significa chiedere di leggere per trovare il modo di
leggere.

**Il punto 9 viene prima del 10.** L'eco dell'input precede il risultato perché è
lì che un errore di inserimento diventa visibile — nel momento in cui si guarda
la risposta, non settimane dopo.

---

## 3. Wireframe — telefono, modalità «alle prime armi»

Il caso più stretto e più frequente: un HR che controlla un'offerta fra un
colloquio e l'altro.

```
┌──────────────────────────────────────┐
│  Dalla RAL al netto                  │   1
│  Quanto resta davvero in tasca…      │
│                                      │
│  ┌────────────────┐                  │
│  │Alle prime armi │  Esperto         │   ← ricordato, commutabile
│  └────────────────┘                  │     senza perdere nulla
├──────────────────────────────────────┤
│ ⓘ Prototipo indipendente. Non è uno  │   2
│   strumento ufficiale di Jet HR.     │
├──────────────────────────────────────┤
│ ◐ Leggibilità                     ▸  │   3  richiuso per default
├──────────────────────────────────────┤
│ ┌──────────────────────────────────┐ │   4
│ │ Ho il LORDO, voglio il netto     │ │      scheda attiva
│ ├──────────────────────────────────┤ │
│ │ Voglio garantire un NETTO        │ │
│ └──────────────────────────────────┘ │
│                                      │
│  RAL — Retribuzione Annua ▓LORDA▓    │   5  la parola chiave
│  ┌──────────────┐  € all'anno        │      è evidenziata,
│  │ 35.000       │                    │      non fra parentesi
│  └──────────────┘                    │
│  Ho letto 35.000 € lordi all'anno    │   ← eco viva, mentre digiti
│                                      │
│  ╭──────────────────────────────────╮│
│  │ Che cos'è la RAL. È lo stipendio ││   aiuto già APERTO:
│  │ ANNUO e LORDO scritto nel        ││   chi non conosce il
│  │ contratto…                       ││   dominio non sa di
│  │ Se stai pensando a 1.800 € o     ││   avere una domanda
│  │ 2.500 €, quello è un mensile.    ││
│  ╰──────────────────────────────────╯│
│                                      │
│  Comune di residenza                 │   6  sempre visibile,
│  ┌──────────────────────────────────┐│      mai un default
│  │ Milano (Lombardia) — predefinito ││      silenzioso
│  └──────────────────────────────────┘│
│  ╭──────────────────────────────────╮│
│  │ Perché serve il comune. …fra due ││
│  │ comuni la differenza può         ││
│  │ superare i 600 € l'anno.         ││
│  ╰──────────────────────────────────╯│
│                                      │
│        ┌──────────────────┐          │
│        │     Calcola      │          │   pieno lime, bordo scuro
│        └──────────────────┘          │   (il lime da solo è 1,3:1)
└──────────────────────────────────────┘
                  │
                  ▼  il fuoco si sposta qui
┌──────────────────────────────────────┐
│  Calcolato su 35.000 € lordi annui   │   9  l'eco PRIMA del numero
│  — Milano, anno 2026, 14 mensilità   │
│                                      │
│  NETTO MENSILE                       │  10
│  1.859,44 €      NETTO ANNUO         │
│  su 14 mensilità 26.032,22 €         │
│                                      │
│  Su 35.000 € di lordo se ne          │
│  trattengono 8.967,78 €.             │
│  Aliquota effettiva: 25,6%.          │
│                                      │
│  DOVE FINISCONO I 35.000 € DI LORDO  │  11
│  ▐████████████████▌▐██▌▐███▌▐▌▐▌     │
│  ■ Resta al dipendente   26.032,22 € │
│  ■ Contributi INPS        3.216,50 € │
│  ■ IRPEF netta            5.042,03 € │
│  ■ Addizionale regionale    454,98 € │
│  ■ Addizionale comunale     254,27 € │
│                                      │
│  Come si arriva a questo numero      │  12
│  ┌──────────────────────┬───────────┐│
│  │ Retribuzione lorda   │ 35.000,00 ││
│  │   cos'è?             │           ││   ogni riga ha
│  │ − Contributi INPS    │  3.216,50 ││   la sua spiegazione
│  │ … (tabella scorre    │           ││
│  │    dentro il riquadro)│          ││
│  └──────────────────────┴───────────┘│
│                                      │
│  ╭──────────────────────────────────╮│  13
│  │ ☐ Confermo che 35.000 € è la     ││   il momento in cui
│  │   retribuzione annua LORDA,      ││   il numero smette di
│  │   non lo stipendio mensile.      ││   essere informativo
│  ╰──────────────────────────────────╯│
└──────────────────────────────────────┘
```

---

## 4. Wireframe — modalità «esperto»

Le differenze, non l'intera schermata.

```
┌──────────────────────────────────────┐
│  RAL — Retribuzione Annua ▓LORDA▓    │
│  ┌──────────┐ € all'anno  [cosa      │  ← aiuto CHIUSO,
│  └──────────┘              vuol dire?]│    disponibile su richiesta
│  Sto calcolando su 35.000 €          │
│                                      │
│  Comune ┌────────────────────────┐   │  ← resta visibile: anche
│         │ Milano (Lombardia)     │   │    l'esperto distratto
│         └────────────────────────┘   │    sbaglia territorio
│ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│  Anno d'imposta  [2026 — corrente ▾] │  7  parametri in chiaro
│  CCNL            [Commercio — 14 ▾]  │
│  Mensilità       [14 ▾]              │
│  Giorni          [365] su 365        │
└──────────────────────────────────────┘
        …
┌──────────────────────────────────────┐
│  Coefficienti e fonti                │  14  compare SOLO qui
│                                      │
│  10 gruppi per Milano, anno 2026:    │
│  2 su fonte primaria, 8 secondaria.  │
│                                      │
│  ┌────────────┬──────────┬─────────┐ │
│  │ NAZIONALE  │ L. 199/  │primaria │ │
│  │ irpef      │ 2025 …   │06-08-26 │ │
│  ├────────────┼──────────┼─────────┤ │
│  │ Milano     │ Comune   │secondar.│ │
│  │ comunale   │ di Mi… │06-08-26 │ │
│  └────────────┴──────────┴─────────┘ │
│                                      │
│  (su telefono ogni riga diventa       │
│   una scheda: tre colonne di testo   │
│   lungo non ci stanno)               │
└──────────────────────────────────────┘
```

La conferma (13) **non compare** in modalità esperto: chi conosce il dominio non
ha bisogno di dichiarare di aver capito la differenza fra lordo e netto, e
chiederglielo ogni volta sarebbe un attrito senza contropartita.

---

## 5. Wireframe — schermo largo (proposta)

L'impaginazione attuale è a colonna unica anche su desktop: dopo il calcolo la
pagina **scorre** al risultato. Funziona, ma su uno schermo largo lascia due
terzi di spazio vuoto e costringe a un movimento che non servirebbe.

```
ATTUALE (colonna unica)              PROPOSTA (due colonne, ≥ 64rem)
┌───────────────────────┐            ┌─────────────┬─────────────────┐
│      intestazione     │            │        intestazione           │
├───────────────────────┤            ├─────────────┬─────────────────┤
│      leggibilità      │            │ leggibilità │                 │
├───────────────────────┤            ├─────────────┤   eco input     │
│       schede          │            │   schede    │                 │
├───────────────────────┤            ├─────────────┤   IL NETTO      │
│                       │            │             │                 │
│       modulo          │            │   modulo    │   ripartizione  │
│                       │            │             │                 │
│      [Calcola]        │            │  [Calcola]  │   tabella       │
├───────────────────────┤            │             │                 │
│   ↓ scorri ↓          │            │             │   conferma      │
├───────────────────────┤            │             │                 │
│      risultato        │            │             │   fonti         │
└───────────────────────┘            └─────────────┴─────────────────┘
                                       modificare un parametro a sinistra
                                       aggiorna il risultato a destra,
                                       nel campo visivo
```

**Perché non è ancora fatto.** È l'unico punto di questo documento che descrive
qualcosa che non esiste. Vale la pena essere espliciti sul motivo: la colonna
unica funziona su tutte le larghezze e su telefono la scrollata resta comunque
la risposta giusta; le due colonne migliorano un caso solo, quello desktop, e
richiedono di ripensare l'ordine di lettura per chi naviga da tastiera. È un
miglioramento reale ma non prioritario rispetto a ciò che manca alla consegna.

---

## 6. Gli stati che nessuno progetta

Un calcolatore sembra avere due stati — vuoto e con risultato. Ne ha nove, e
sei riguardano il calcolo inverso.

| Stato | Quando | Cosa mostra |
|---|---|---|
| **Vuoto** | all'apertura | modulo, aiuti aperti se neofita |
| **Interpretazione** | mentre si digita | *«Ho letto 35.000 € lordi all'anno»* |
| **Non interpretabile** | input malformato | *«Non riesco a leggere questo importo»*, con esempi validi |
| **In corso** | dopo il clic | pulsante disabilitato, *«Calcolo…»* |
| **Risultato** | esito normale | eco, netto, ripartizione, tabella |
| **Errore** | valore rifiutato | messaggio del motore, in italiano, senza codici |
| **Sospetto** | importo implausibile | *«Sembra un importo mensile. Intendevi 30.000 €?»* |
| **Netto ambiguo** | inverso, più soluzioni | tutte le RAL che lo producono, con la più bassa proposta |
| **Netto impossibile** | inverso, nessuna soluzione | i due valori raggiungibili più vicini |

Gli ultimi due esistono perché il netto **non cresce con continuità** al crescere
del lordo: ci sono sei punti di discontinuità. Nessun altro calcolatore
esaminato li nomina — tutti li calcolano correttamente, e tutti tacciono.

---

## 7. Percorsi principali

```
«Devo fare un'offerta»            «Il candidato chiede 2.000 netti»
        │                                       │
   scheda LORDO                            scheda NETTO
        │                                       │
   inserisce RAL                          inserisce netto + mensile/annuo
        │                                       │
   ← eco: cosa ho letto                    ← eco: cosa ho letto
        │                                       │
   verifica il comune                      verifica il comune
        │                                       │
     Calcola ──────┐                     Calcola ──────┐
        │          │                          │         │
   netto + voci    │                    RAL + dettaglio │
        │          │                          │         │
   conferma        │                    se ambiguo:     │
   («è il lordo»)  │                    mostra tutte    │
        │          │                          │         │
        ▼          ▼                          ▼         ▼
   usa la cifra  cambia parametro        usa la RAL  cambia parametro
                 (nulla si perde)                    (nulla si perde)
```

---

## 8. Decisioni di architettura, e il loro perché

| Decisione | Alternativa scartata | Perché |
|---|---|---|
| Una pagina sola con stati | pagine separate per direzione e livello | cambiare vista non deve far ricominciare; un ricaricamento perderebbe l'input |
| Leggibilità **in alto** | in fondo, come si usa | chi deve ingrandire il testo lo deve fare *prima* di leggere |
| Territorio **sempre visibile** | dentro le opzioni avanzate | vale oltre 600 € l'anno e non dà alcun segnale se sbagliato |
| Aiuti **aperti** per il neofita | icone da cliccare | chi non conosce il dominio non sa di avere una domanda |
| Aiuti **chiusi** per l'esperto | sempre aperti | per lui sono rumore, e il rumore fa saltare le righe |
| Eco dell'input **prima** del numero | solo il numero | è l'unico punto in cui un errore d'inserimento diventa visibile |
| Fonti **solo** in modalità esperto | sempre visibili | per il neofita sono un muro; per l'esperto sono la ragione per fidarsi |
| Conferma **solo** per il neofita | sempre | all'esperto sarebbe attrito senza contropartita |
| Tabella che **scorre** su telefono | tabella compressa | comprimere una colonna di numeri la rende illeggibile |
| Fonti che diventano **schede** su telefono | tabella che scorre | tre colonne di testo lungo non si leggono scorrendo |

---

## 9. Cosa manca

Onestà sullo stato: questo documento descrive l'architettura **realizzata**,
tranne dove indicato.

- **Le due colonne su schermo largo** (§5) sono una proposta, non una
  realizzazione.
- **La navigazione fra più calcoli** — confrontare due offerte affiancate — non
  esiste, ed è la prima estensione che cambierebbe l'architettura invece di
  aggiungersi ad essa.
- **La pagina `/coefficienti` autonoma** non esiste: il registro è consultabile
  solo dentro il risultato, in modalità esperto. Come pagina a sé sarebbe
  linkabile e citabile, che è il modo in cui un consulente la userebbe.
