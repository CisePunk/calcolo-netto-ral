import { useEffect, useState } from "react";
import { coefficienti as leggiCoefficienti } from "../api";
import { statiFonte } from "../testi";

/**
 * Da dove viene ogni numero.
 *
 * È la parte che distingue questo strumento da una scatola chiusa. Non mostra
 * solo i coefficienti: mostra **quanto sono solidi**, perché in un dominio dove
 * le tabelle ufficiali escono con mesi di ritardo sulle norme, "aggiornato" non
 * è una risposta sufficiente.
 */
export default function Fonti({ anno, territorio }) {
  const [dati, setDati] = useState(null);
  const [errore, setErrore] = useState(null);

  useEffect(() => {
    let annullato = false;
    leggiCoefficienti(anno, territorio)
      .then((d) => !annullato && setDati(d))
      .catch((e) => !annullato && setErrore(e.message));
    return () => {
      annullato = true;
    };
  }, [anno, territorio]);

  if (errore) return <p className="errore">{errore}</p>;
  if (!dati) return <p className="attesa">Carico i coefficienti…</p>;

  const { primaria = 0, secondaria = 0, da_verificare = 0 } = dati.riepilogo;
  const totale = primaria + secondaria + da_verificare;

  return (
    <section className="fonti" aria-labelledby="titolo-fonti">
      <h3 id="titolo-fonti">Coefficienti e fonti</h3>

      <p className="fonti-riepilogo">
        {totale} gruppi di coefficienti per {dati.territorio.comune}, anno{" "}
        {dati.anno}: <strong>{primaria}</strong> su fonte primaria,{" "}
        <strong>{secondaria}</strong> su fonte secondaria
        {da_verificare > 0 && (
          <>
            , <strong>{da_verificare}</strong> ancora da verificare
          </>
        )}
        .
      </p>

      <details className="fonti-legenda">
        <summary>Cosa significano gli stati</summary>
        <dl>
          {Object.entries(statiFonte).map(([chiave, stato]) => (
            <div key={chiave}>
              <dt>
                <span className={`pastiglia ${chiave}`}>{stato.etichetta}</span>
              </dt>
              <dd>{stato.descrizione}</dd>
            </div>
          ))}
        </dl>
      </details>

      <table className="tabella-fonti">
        <caption className="solo-lettori">
          Coefficienti usati nel calcolo, con la norma di riferimento
        </caption>
        <thead>
          <tr>
            <th scope="col">Voce</th>
            <th scope="col">Fonte</th>
            <th scope="col">Stato</th>
          </tr>
        </thead>
        <tbody>
          {dati.voci.map((voce, indice) => (
            <tr key={indice}>
              <th scope="row">
                <span className="ambito">{voce.ambito}</span>
                {voce.voce.replace(/_/g, " ")}
              </th>
              <td>
                {voce.fonte}
                {voce.nota && <p className="fonte-nota">{voce.nota}</p>}
              </td>
              <td>
                <span className={`pastiglia ${voce.stato}`}>
                  {statiFonte[voce.stato]?.etichetta ?? voce.stato}
                </span>
                <span className="data-verifica">{voce.data_verifica}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
