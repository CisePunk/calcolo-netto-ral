import { useState } from "react";
import { euro, percentuale } from "../api";
import { aiutoPerVoce, spiegazioni } from "../testi";
import Ripartizione from "./Ripartizione";

/**
 * Il risultato: prima l'eco dell'input, poi il netto, poi il perché.
 *
 * L'ordine non è casuale. La prima cosa che si legge è **cosa è stato
 * calcolato**, scritto per esteso: è lì che un errore di inserimento diventa
 * visibile, nel momento in cui si guarda la risposta invece che settimane dopo.
 */
export default function Risultato({ dati, esperto }) {
  const [confermato, setConfermato] = useState(false);

  const nettoSuperaLordo = dati.netto_annuo > dati.retribuzione_effettiva;
  const annoPieno = dati.giorni === 365;

  return (
    <section className="risultato" aria-labelledby="titolo-risultato">
      <h2 id="titolo-risultato" className="solo-lettori">
        Risultato del calcolo
      </h2>

      {/* 1. L'eco dell'input, in parole */}
      <p className="eco">
        Calcolato su <strong>{euro(dati.ral, 0)} lordi annui</strong> —{" "}
        {dati.comune}, anno d'imposta {dati.anno}, {dati.mensilita} mensilità
        {!annoPieno && <> , {dati.giorni} giorni di lavoro</>}.
      </p>

      {/* 2. Il numero */}
      <div className="netto">
        <div className="netto-principale">
          <span className="netto-etichetta">Netto mensile</span>
          <span className="netto-valore">{euro(dati.netto_mensile)}</span>
          <span className="netto-nota">
            su {dati.mensilita} mensilità
          </span>
        </div>
        <div className="netto-secondario">
          <span className="netto-etichetta">Netto annuo</span>
          <span className="netto-valore-piccolo">{euro(dati.netto_annuo)}</span>
        </div>
      </div>

      <p className="riepilogo-trattenute">
        Su {euro(dati.retribuzione_effettiva, 0)} di lordo, se ne trattengono{" "}
        <strong>{euro(dati.totale_trattenute)}</strong>
        {dati.totale_somme_aggiunte > 0 && (
          <> e se ne aggiungono {euro(dati.totale_somme_aggiunte)}</>
        )}
        . Aliquota effettiva:{" "}
        <strong>{percentuale(dati.aliquota_effettiva)}</strong>.
      </p>

      {nettoSuperaLordo && (
        <p className="nota-sorpresa">{spiegazioni.nettoSopraLordo}</p>
      )}

      {/* 3. Il colpo d'occhio: dove va a finire il lordo */}
      <Ripartizione dati={dati} />

      {/* 4. Il perché in cifre: voce per voce */}
      <h3>Come si arriva a questo numero</h3>
      <table className="voci">
        <caption className="solo-lettori">
          Dettaglio delle trattenute e delle somme aggiunte
        </caption>
        <thead>
          <tr>
            <th scope="col">Voce</th>
            <th scope="col" className="numerica">
              Importo
            </th>
          </tr>
        </thead>
        <tbody>
          {dati.voci.map((voce, indice) => (
            <VoceRiga key={indice} voce={voce} esperto={esperto} />
          ))}
          <tr className="riga-totale">
            <th scope="row">Netto annuo</th>
            <td className="numerica">{euro(dati.netto_annuo)}</td>
          </tr>
        </tbody>
      </table>

      {/* 5. La conferma: il momento in cui il numero smette di essere
             informativo e sta per diventare un impegno. */}
      {!esperto && (
        <div className="conferma">
          <label>
            <input
              type="checkbox"
              checked={confermato}
              onChange={(e) => setConfermato(e.target.checked)}
            />
            {/* Il testo va in UN SOLO span. Senza, il `display: flex`
                dell'etichetta trasforma ogni frammento — i due <strong> e i
                tre pezzi di testo fra loro — in altrettanti elementi flex, e
                il `gap` li separa come fossero colonne: la frase si spezza e
                la virgola resta staccata dalla parola che segue.
                Proprio la riga che serve a non confondere lordo e mensile.
                Trovato guardando la pagina, non il codice. */}
            <span>
              Confermo che <strong>{euro(dati.ral, 0)}</strong> è la
              retribuzione annua <strong>lorda</strong>, non lo stipendio
              mensile né il netto.
            </span>
          </label>
          {confermato && (
            <p className="conferma-esito">
              Bene. Puoi usare {euro(dati.ral, 0)} come RAL nell'offerta: il
              dipendente riceverà {euro(dati.netto_mensile)} al mese su{" "}
              {dati.mensilita} mensilità.
            </p>
          )}
        </div>
      )}
    </section>
  );
}

function VoceRiga({ voce, esperto }) {
  const [aperto, setAperto] = useState(false);
  const aiuto = aiutoPerVoce(voce.etichetta);
  const informativa = voce.segno === 0;

  return (
    <>
      <tr className={informativa ? "riga-informativa" : ""}>
        <th scope="row">
          <span className="segno" aria-hidden="true">
            {voce.segno === -1 ? "−" : voce.segno === 1 ? "+" : ""}
          </span>
          {voce.etichetta}
          {voce.segno === -1 && <span className="solo-lettori"> (trattenuta)</span>}
          {voce.segno === 1 && <span className="solo-lettori"> (somma aggiunta)</span>}
          {aiuto && (
            <button
              type="button"
              className="apri-aiuto piccolo"
              aria-expanded={aperto}
              onClick={() => setAperto((v) => !v)}
            >
              {aperto ? "nascondi" : "cos'è?"}
            </button>
          )}
        </th>
        <td className="numerica">{euro(voce.importo)}</td>
      </tr>
      {aperto && aiuto && (
        <tr className="riga-aiuto">
          <td colSpan={2}>{aiuto}</td>
        </tr>
      )}
    </>
  );
}
