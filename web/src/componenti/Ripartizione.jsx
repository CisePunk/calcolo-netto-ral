import { useState } from "react";
import { euro, percentuale } from "../api";

/**
 * Dove va a finire il lordo: una barra sola, divisa in parti.
 *
 * Perché questa forma e non un'altra. Il dato è una parte-su-tutto di un
 * totale unico — quanto del lordo resta e quanto se ne va — e la domanda che
 * l'utente si fa è "quanto mi tolgono?". Una barra impilata risponde in un
 * colpo d'occhio; una torta costringerebbe a confrontare angoli, che si legge
 * peggio; cinque barre separate perderebbero il fatto che sono parti di uno
 * stesso intero.
 *
 * Il colore segue la VOCE, non la sua grandezza: la stessa voce ha lo stesso
 * colore su qualunque RAL, così confrontando due calcoli si riconoscono le
 * parti invece di doverle rileggere.
 *
 * L'identità non è mai affidata al solo colore: ogni voce compare nella
 * legenda con il suo importo, e la tabella qui sotto riporta tutto in cifre.
 */

// Slot categorici, in ordine fisso. La sequenza è stata verificata con il
// validatore della palette sulla superficie bianca di questa pagina: passa la
// separazione per daltonismo e la soglia di distinguibilità a vista normale.
const COLORI = {
  netto: "var(--serie-1)",
  contributi_inps: "var(--serie-2)",
  irpef_netta: "var(--serie-3)",
  addizionale_regionale: "var(--serie-4)",
  addizionale_comunale: "var(--serie-5)",
  aggiunte: "var(--serie-6)",
};

export default function Ripartizione({ dati }) {
  const [inEvidenza, setInEvidenza] = useState(null);

  const lordo = dati.retribuzione_effettiva;
  const aggiunte = dati.totale_somme_aggiunte;

  // La parte di lordo che sopravvive alle trattenute. Le somme aggiunte non
  // vengono dal lordo — sono denaro in più — quindi stanno fuori da questa
  // quota e si vedono come segmento a parte, oltre il 100%.
  const nettoDalLordo = lordo - dati.totale_trattenute;

  const parti = [
    { chiave: "netto", nome: "Resta al dipendente", valore: nettoDalLordo },
    { chiave: "contributi_inps", nome: "Contributi INPS", valore: dati.contributi_inps },
    { chiave: "irpef_netta", nome: "IRPEF netta", valore: dati.irpef_netta },
    {
      chiave: "addizionale_regionale",
      nome: `Addizionale regionale (${dati.regione})`,
      valore: dati.addizionale_regionale,
    },
    {
      chiave: "addizionale_comunale",
      nome: `Addizionale comunale (${dati.comune})`,
      valore: dati.addizionale_comunale,
    },
  ].filter((p) => p.valore > 0.005);

  if (aggiunte > 0.005) {
    parti.push({
      chiave: "aggiunte",
      nome: "Somme aggiunte al netto",
      valore: aggiunte,
      oltreIlLordo: true,
    });
  }

  const scala = lordo + Math.max(0, aggiunte);

  return (
    <figure className="ripartizione">
      <figcaption>
        Dove finiscono i {euro(lordo, 0)} di lordo
      </figcaption>

      <div
        className="barra"
        role="img"
        aria-label={parti
          .map((p) => `${p.nome}: ${euro(p.valore)}`)
          .join("; ")}
      >
        {parti.map((parte) => (
          <div
            key={parte.chiave}
            className={
              "segmento" +
              (inEvidenza === parte.chiave ? " evidenziato" : "") +
              (parte.oltreIlLordo ? " oltre" : "")
            }
            style={{
              width: `${(parte.valore / scala) * 100}%`,
              // backgroundColor e NON background: la proprietà abbreviata
              // azzera background-image, e siccome lo stile in linea batte il
              // foglio di stile, le trame per il daltonismo non comparirebbero
              // mai. Difetto trovato provando le tre modalità in un browser
              // vero, non leggendo il codice.
              backgroundColor: COLORI[parte.chiave],
            }}
            onMouseEnter={() => setInEvidenza(parte.chiave)}
            onMouseLeave={() => setInEvidenza(null)}
            title={`${parte.nome}: ${euro(parte.valore)}`}
          />
        ))}
      </div>

      {/* La legenda porta i valori: è il "sollievo" richiesto quando alcuni
          colori non raggiungono il contrasto minimo sulla superficie chiara.
          Nessuna informazione è affidata al solo colore. */}
      <ul className="legenda">
        {parti.map((parte) => {
          const quota = parte.valore / lordo;
          return (
            <li
              key={parte.chiave}
              className={inEvidenza === parte.chiave ? "evidenziato" : ""}
              onMouseEnter={() => setInEvidenza(parte.chiave)}
              onMouseLeave={() => setInEvidenza(null)}
            >
              <span
                className="pastiglia-colore"
                style={{ backgroundColor: COLORI[parte.chiave] }}
                aria-hidden="true"
              />
              <span className="legenda-nome">{parte.nome}</span>
              <span className="legenda-valore">{euro(parte.valore)}</span>
              <span className="legenda-quota">
                {parte.oltreIlLordo ? "+" : ""}
                {percentuale(quota)}
              </span>
            </li>
          );
        })}
      </ul>
    </figure>
  );
}
