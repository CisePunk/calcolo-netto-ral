import { useId, useState } from "react";

/**
 * Un campo con la sua spiegazione, agganciata in modo accessibile.
 *
 * L'aggancio è il punto: l'aiuto non è un'icona che apre un riquadro, è un
 * testo collegato al campo con `aria-describedby`. Chi naviga con uno screen
 * reader lo sente insieme all'etichetta, invece di trovare un campo nudo e
 * un'icona che non sa di poter aprire.
 *
 * In modalità "guidata" la spiegazione è già aperta: chi non conosce il
 * dominio non sa di avere una domanda, quindi non va messo nella condizione di
 * doverla fare.
 */
export default function Campo({
  etichetta,
  etichettaEvidenziata,
  aiuto,
  aiutoAperto = false,
  suffisso,
  sotto,
  children,
}) {
  const id = useId();
  const idAiuto = `${id}-aiuto`;
  const [aperto, setAperto] = useState(aiutoAperto);

  const mostraAiuto = aiuto && (aiutoAperto || aperto);

  return (
    <div className="campo">
      <div className="campo-intestazione">
        <label htmlFor={id}>
          {etichetta}
          {etichettaEvidenziata && (
            <>
              {" "}
              <strong className="evidenza">{etichettaEvidenziata}</strong>
            </>
          )}
        </label>

        {aiuto && !aiutoAperto && (
          <button
            type="button"
            className="apri-aiuto"
            aria-expanded={aperto}
            aria-controls={idAiuto}
            onClick={() => setAperto((v) => !v)}
          >
            {aperto ? "nascondi" : "cosa vuol dire?"}
          </button>
        )}
      </div>

      <div className="campo-controllo">
        {/* Il controllo riceve id e aria-describedby dal genitore: è così che
            l'aiuto resta legato al campo anche per chi non lo vede. */}
        {children({ id, describedBy: mostraAiuto ? idAiuto : undefined })}
        {suffisso && <span className="suffisso">{suffisso}</span>}
      </div>

      {sotto}

      {mostraAiuto && (
        <div className="aiuto" id={idAiuto}>
          {aiuto.titolo && <strong>{aiuto.titolo}. </strong>}
          {aiuto.testo}
          {aiuto.equivoco && <p className="aiuto-equivoco">{aiuto.equivoco}</p>}
        </div>
      )}
    </div>
  );
}
