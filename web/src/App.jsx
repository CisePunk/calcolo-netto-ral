import { useEffect, useRef, useState } from "react";
import * as api from "./api";
import { euro } from "./api";
import Campo from "./componenti/Campo";
import Risultato from "./componenti/Risultato";
import Fonti from "./componenti/Fonti";
import Leggibilita from "./componenti/Leggibilita";
import { aiutoCampi } from "./testi";
import { interpretaImporto } from "./numeri";
import "./stile.css";

/**
 * Mostra come è stato capito il numero, mentre lo si scrive.
 *
 * È la difesa contro un errore che il codice non può risolvere da solo:
 * `35.000` può voler dire trentacinquemila (uso italiano) o trentacinque e
 * zero millesimi. Si sceglie l'interpretazione più probabile — tre cifre dopo
 * il separatore sono migliaia — ma la scelta va **mostrata**, non nascosta.
 */
function ComeHoLetto({ testo, periodo }) {
  if (!testo || !String(testo).trim()) return null;
  const valore = interpretaImporto(testo);
  if (valore === null) {
    return (
      <p className="come-ho-letto non-capito">
        Non riesco a leggere questo importo. Scrivilo come preferisci: 35000,
        35.000 oppure 35.000,50.
      </p>
    );
  }
  const grezzo = String(testo).replace(/[^\d.,]/g, "");
  const gia = grezzo === String(valore);
  return (
    <p className="come-ho-letto">
      {gia ? "Sto calcolando su " : "Ho letto "}
      <strong>{euro(valore, valore % 1 === 0 ? 0 : 2)}</strong> {periodo}.
    </p>
  );
}

/**
 * Calcolatore RAL → netto.
 *
 * Due decisioni governano tutta l'interfaccia:
 *
 *   1. Nessun dato fiscale è scritto qui dentro. Anni, comuni, contratti e
 *      mensilità arrivano da /api/opzioni. Aggiungere un comune al registro lo
 *      fa comparire in pagina senza toccare questo file.
 *
 *   2. Cambiare modalità non azzera niente. Chi si dichiara esperto, si blocca
 *      e torna indietro deve ritrovare quello che aveva scritto: è il caso che
 *      rende utile avere due modalità invece di una sola.
 */
export default function App() {
  const [opzioni, setOpzioni] = useState(null);
  const [esperto, setEsperto] = useState(false);
  const [direzione, setDirezione] = useState("lordo"); // "lordo" | "netto"

  const [ral, setRal] = useState("");
  const [netto, setNetto] = useState("");
  const [nettoMensile, setNettoMensile] = useState(true);

  const [anno, setAnno] = useState(null);
  const [territorio, setTerritorio] = useState(null);
  const [ccnl, setCcnl] = useState(null);
  const [mensilita, setMensilita] = useState(null);
  const [giorni, setGiorni] = useState(365);

  const [risultato, setRisultato] = useState(null);
  const [inverso, setInverso] = useState(null);
  const [errore, setErrore] = useState(null);
  const [inCorso, setInCorso] = useState(false);
  const zonaRisultato = useRef(null);

  // Dopo il calcolo il risultato viene portato in vista E riceve il fuoco.
  //
  // La scrollata da sola non basta: chi naviga con la tastiera resterebbe con
  // il cursore sul pulsante, e chi usa uno screen reader non saprebbe che è
  // comparso qualcosa. Spostare il fuoco risolve entrambi i casi, e la
  // scrollata dolce diventa istantanea per chi ha chiesto meno animazioni.
  useEffect(() => {
    if (!risultato || !zonaRisultato.current) return;
    const menoMovimento = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    zonaRisultato.current.scrollIntoView({
      behavior: menoMovimento ? "auto" : "smooth",
      block: "start",
    });
    zonaRisultato.current.focus({ preventScroll: true });
  }, [risultato]);

  useEffect(() => {
    api
      .opzioni()
      .then((o) => {
        setOpzioni(o);
        setAnno(o.anno_predefinito);
        setTerritorio(o.territorio_predefinito);
        setCcnl(o.ccnl_predefinito);
      })
      .catch((e) => setErrore(e.message));
  }, []);

  // Il CCNL determina le mensilità, ma in modalità esperto si possono
  // sovrascrivere: il valore scelto a mano non va perso cambiando contratto.
  const mensilitaEffettive =
    mensilita ?? opzioni?.ccnl.find((c) => c.codice === ccnl)?.mensilita ?? 14;

  const territorioScelto = opzioni?.territori.find((t) => t.codice === territorio);

  async function invia(evento) {
    evento.preventDefault();
    setErrore(null);
    setInCorso(true);
    const comuni = { anno, territorio, ccnl, mensilita: mensilitaEffettive, giorni };
    try {
      if (direzione === "lordo") {
        setInverso(null);
        setRisultato(await api.calcola({ ral, ...comuni }));
      } else {
        const esito = await api.inverso({ netto, mensile: nettoMensile, ...comuni });
        setInverso(esito);
        setRisultato(esito.dettaglio ?? null);
      }
    } catch (e) {
      setErrore(e.message);
      setRisultato(null);
      setInverso(null);
    } finally {
      setInCorso(false);
    }
  }

  if (!opzioni) {
    return (
      <main className="pagina">
        <p className="attesa">{errore ?? "Carico…"}</p>
      </main>
    );
  }

  return (
    <main className="pagina">
      <header className="intestazione">
        <div>
          <h1>Dalla RAL al netto</h1>
          <p className="sottotitolo">
            Quanto resta davvero in tasca a un dipendente, e perché. Ogni voce è
            spiegata e ogni coefficiente ha la sua fonte.
          </p>
        </div>

        <fieldset className="modalita">
          <legend className="solo-lettori">Livello di esperienza</legend>
          <button
            type="button"
            className={!esperto ? "scelta attiva" : "scelta"}
            aria-pressed={!esperto}
            onClick={() => setEsperto(false)}
          >
            Alle prime armi
          </button>
          <button
            type="button"
            className={esperto ? "scelta attiva" : "scelta"}
            aria-pressed={esperto}
            onClick={() => setEsperto(true)}
          >
            Esperto
          </button>
        </fieldset>
      </header>

      {/* Il prototipo riprende l'identità visiva di Jet HR per mostrare come si
          inserirebbe nel loro prodotto. Proprio per questo deve essere
          impossibile scambiarlo per uno strumento ufficiale: l'avviso non è una
          formalità, è ciò che rende la scelta di stile difendibile. */}
      <p className="avviso-indipendenza" role="note">
        <strong>Prototipo indipendente.</strong> Esercizio di progettazione
        realizzato per una selezione: non è uno strumento ufficiale di Jet HR,
        non è collegato ai loro sistemi e non va usato per adempimenti reali.
      </p>

      <Leggibilita />

      <div className="schede" role="tablist" aria-label="Direzione del calcolo">
        <button
          role="tab"
          aria-selected={direzione === "lordo"}
          className={direzione === "lordo" ? "scheda attiva" : "scheda"}
          onClick={() => setDirezione("lordo")}
        >
          Ho il <strong>lordo</strong>, voglio il netto
        </button>
        <button
          role="tab"
          aria-selected={direzione === "netto"}
          className={direzione === "netto" ? "scheda attiva" : "scheda"}
          onClick={() => setDirezione("netto")}
        >
          Voglio garantire un <strong>netto</strong>
        </button>
      </div>

      <form onSubmit={invia} className="modulo">
        {direzione === "lordo" ? (
          <Campo
            etichetta="RAL — Retribuzione Annua"
            etichettaEvidenziata="LORDA"
            aiuto={aiutoCampi.ral}
            aiutoAperto={!esperto}
            suffisso="€ all'anno"
            sotto={<ComeHoLetto testo={ral} periodo="lordi all'anno" />}
          >
            {({ id, describedBy }) => (
              <input
                id={id}
                aria-describedby={describedBy}
                className="numero grande"
                inputMode="decimal"
                placeholder="es. 35.000"
                value={ral}
                onChange={(e) => setRal(e.target.value)}
                autoFocus
              />
            )}
          </Campo>
        ) : (
          <>
            <Campo
              etichetta="Netto da garantire"
              aiuto={aiutoCampi.netto}
              aiutoAperto={!esperto}
              suffisso={nettoMensile ? "€ al mese" : "€ all'anno"}
              sotto={
                <ComeHoLetto
                  testo={netto}
                  periodo={nettoMensile ? "netti al mese" : "netti all'anno"}
                />
              }
            >
              {({ id, describedBy }) => (
                <input
                  id={id}
                  aria-describedby={describedBy}
                  className="numero grande"
                  inputMode="decimal"
                  placeholder="es. 2.000"
                  value={netto}
                  onChange={(e) => setNetto(e.target.value)}
                  autoFocus
                />
              )}
            </Campo>
            <fieldset className="periodo">
              <legend>L'importo che hai scritto è</legend>
              <label>
                <input
                  type="radio"
                  checked={nettoMensile}
                  onChange={() => setNettoMensile(true)}
                />{" "}
                mensile
              </label>
              <label>
                <input
                  type="radio"
                  checked={!nettoMensile}
                  onChange={() => setNettoMensile(false)}
                />{" "}
                annuo
              </label>
            </fieldset>
          </>
        )}

        {/* Il territorio è sempre visibile, in entrambe le modalità: è la voce
            che può spostare il risultato di centinaia di euro senza dare alcun
            segnale, quindi non può essere un default silenzioso. */}
        <Campo
          etichetta="Comune di residenza"
          aiuto={aiutoCampi.territorio}
          aiutoAperto={!esperto}
        >
          {({ id, describedBy }) => (
            <select
              id={id}
              aria-describedby={describedBy}
              value={territorio ?? ""}
              onChange={(e) => setTerritorio(e.target.value)}
            >
              {opzioni.territori.map((t) => (
                <option key={t.codice} value={t.codice}>
                  {t.comune} ({t.regione})
                  {t.predefinito ? " — predefinito" : ""}
                </option>
              ))}
            </select>
          )}
        </Campo>

        {esperto && (
          <div className="avanzate">
            <Campo etichetta="Anno d'imposta" aiuto={aiutoCampi.anno}>
              {({ id, describedBy }) => (
                <select
                  id={id}
                  aria-describedby={describedBy}
                  value={anno ?? ""}
                  onChange={(e) => setAnno(Number(e.target.value))}
                >
                  {opzioni.anni.map((a) => (
                    <option key={a} value={a}>
                      {a}
                      {a === opzioni.anno_predefinito ? " — corrente" : ""}
                    </option>
                  ))}
                </select>
              )}
            </Campo>

            <Campo etichetta="CCNL" aiuto={aiutoCampi.ccnl}>
              {({ id, describedBy }) => (
                <select
                  id={id}
                  aria-describedby={describedBy}
                  value={ccnl ?? ""}
                  onChange={(e) => {
                    setCcnl(e.target.value);
                    setMensilita(null);
                  }}
                >
                  {opzioni.ccnl.map((c) => (
                    <option key={c.codice} value={c.codice}>
                      {c.nome} — {c.mensilita} mensilità
                    </option>
                  ))}
                </select>
              )}
            </Campo>

            <Campo etichetta="Mensilità" aiuto={aiutoCampi.mensilita}>
              {({ id, describedBy }) => (
                <select
                  id={id}
                  aria-describedby={describedBy}
                  value={mensilitaEffettive}
                  onChange={(e) => setMensilita(Number(e.target.value))}
                >
                  {opzioni.mensilita_ammesse.map((m) => (
                    <option key={m} value={m}>
                      {m}
                    </option>
                  ))}
                </select>
              )}
            </Campo>

            <Campo
              etichetta="Giorni di detrazione"
              aiuto={aiutoCampi.giorni}
              suffisso="su 365"
            >
              {({ id, describedBy }) => (
                <input
                  id={id}
                  aria-describedby={describedBy}
                  className="numero"
                  type="number"
                  min="1"
                  max="365"
                  value={giorni}
                  onChange={(e) => setGiorni(Number(e.target.value))}
                />
              )}
            </Campo>
          </div>
        )}

        <button type="submit" className="calcola" disabled={inCorso}>
          {inCorso ? "Calcolo…" : "Calcola"}
        </button>
      </form>

      {/* Gli avvisi vivono in una regione annunciata: chi non li vede comparire
          deve comunque sentirseli leggere. */}
      <div aria-live="polite" className="avvisi">
        {errore && (
          <p className="errore" role="alert">
            {errore}
          </p>
        )}
        {risultato?.avvisi?.map((avviso, i) => (
          <p key={i} className="avviso">
            {avviso}
          </p>
        ))}
        {inverso?.avvisi?.map((avviso, i) => (
          <p key={i} className="avviso">
            {avviso}
          </p>
        ))}
      </div>

      <div
        ref={zonaRisultato}
        tabIndex={-1}
        className="zona-risultato"
        aria-label={risultato ? "Risultato del calcolo" : undefined}
      >
      {inverso && (
        <section className="esito-inverso">
          {inverso.raggiungibile ? (
            <p className="eco">
              Per garantire{" "}
              <strong>
                {euro(nettoMensile ? Number(netto) : inverso.netto_richiesto)}
                {nettoMensile ? " al mese" : " all'anno"}
              </strong>{" "}
              serve una RAL di <strong>{euro(inverso.ral, 0)}</strong>.
            </p>
          ) : (
            <p className="eco">
              Nessuna RAL produce esattamente questo netto. I valori
              raggiungibili più vicini sono{" "}
              <strong>{euro(inverso.netto_raggiungibile_sotto)}</strong> e{" "}
              <strong>{euro(inverso.netto_raggiungibile_sopra)}</strong>.
            </p>
          )}
        </section>
      )}

      {risultato && <Risultato dati={risultato} esperto={esperto} />}

      {esperto && risultato && (
        <Fonti anno={risultato.anno} territorio={risultato.territorio} />
      )}
      </div>

      <footer className="piede">
        <p>
          Prototipo. Copre il caso di un impiegato del settore privato a tempo
          indeterminato, senza agevolazioni contributive né familiari a carico.
          Le semplificazioni sono elencate nel file ASSUNZIONI del repository.{" "}
          <span className="compilazione">
            Versione del {__COMPILAZIONE__} UTC.
          </span>
        </p>
        {territorioScelto && !esperto && (
          <p className="piede-nota">
            Stai calcolando per <strong>{territorioScelto.comune}</strong>. Le
            addizionali locali cambiano da un comune all'altro: a parità di
            lordo la differenza può superare i 600 € l'anno.
          </p>
        )}
      </footer>
    </main>
  );
}
