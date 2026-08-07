/**
 * Interpretazione degli importi scritti a mano.
 *
 * Questa funzione rispecchia `normalizza_importo` del motore Python. La
 * duplicazione è voluta e limitata a un solo scopo: mostrare **subito**, mentre
 * si digita, come è stato capito il numero. L'autorità resta il server — è il
 * suo risultato che compare nella risposta, e l'eco nel riepilogo è quello che
 * conta davvero.
 *
 * Il motivo per cui serve: `Number("35.000")` in JavaScript vale 35, esattamente
 * come `float("35.000")` in Python vale 35.0. Chi scrive trentacinquemila euro
 * nel modo più naturale in italiano otterrebbe un calcolo su trentacinque euro,
 * e il risultato — essendo un numero plausibile — non segnalerebbe nulla.
 */

/** Restituisce il numero interpretato, oppure null se non si capisce. */
export function interpretaImporto(testo) {
  if (typeof testo === "number") return Number.isFinite(testo) ? testo : null;
  if (testo === null || testo === undefined) return null;

  let pulito = String(testo).trim();
  for (const rumore of ["€", " ", " ", " ", "'", "_"]) {
    pulito = pulito.split(rumore).join("");
  }
  if (!pulito) return null;

  const segno = pulito.startsWith("-") ? -1 : 1;
  pulito = pulito.replace(/^[+-]/, "");
  if (!/^[\d.,]+$/.test(pulito)) return null;

  const punti = (pulito.match(/\./g) || []).length;
  const virgole = (pulito.match(/,/g) || []).length;

  if (punti && virgole) {
    const decimale = pulito.lastIndexOf(".") > pulito.lastIndexOf(",") ? "." : ",";
    const migliaia = decimale === "." ? "," : ".";
    const taglio = pulito.lastIndexOf(decimale);
    const intero = uniscMigliaia(pulito.slice(0, taglio), migliaia);
    if (intero === null) return null;
    pulito = `${intero}.${pulito.slice(taglio + 1)}`;
  } else if (punti || virgole) {
    const separatore = punti ? "." : ",";
    if ((punti || virgole) > 1) {
      const unito = uniscMigliaia(pulito, separatore);
      if (unito === null) return null;
      pulito = unito;
    } else {
      const taglio = pulito.indexOf(separatore);
      const intero = pulito.slice(0, taglio);
      const resto = pulito.slice(taglio + 1);
      // Tre cifre dopo il separatore: sono migliaia. Una o due: decimali.
      pulito =
        resto.length === 3 && /^\d{3}$/.test(resto) && intero !== "" && intero !== "0"
          ? intero + resto
          : `${intero}.${resto}`;
    }
  }

  const valore = Number(pulito);
  return Number.isFinite(valore) ? segno * valore : null;
}

/**
 * Toglie i separatori delle migliaia solo se sono messi bene.
 * `35..000` e `35,00,00` restano rifiutati: indovinare su un input malformato
 * significa calcolare in silenzio su un numero che nessuno ha scritto.
 */
function uniscMigliaia(testo, separatore) {
  const gruppi = testo.split(separatore);
  if (gruppi.length === 1) return testo;
  const [primo, ...seguenti] = gruppi;
  if (!/^\d{1,3}$/.test(primo)) return null;
  if (!seguenti.every((g) => /^\d{3}$/.test(g))) return null;
  return gruppi.join("");
}
