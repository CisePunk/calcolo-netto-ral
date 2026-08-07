/**
 * Chiamate all'API.
 *
 * Nessun calcolo qui dentro, e nessun elenco di anni, comuni o contratti:
 * l'interfaccia non conosce nessun dato fiscale. Se un giorno il registro
 * cambia, la pagina lo scopre chiedendolo, non perché qualcuno si è ricordato
 * di aggiornarla.
 */

const BASE = "/api";

async function chiama(percorso, opzioni = {}) {
  const risposta = await fetch(`${BASE}${percorso}`, {
    headers: { "Content-Type": "application/json" },
    ...opzioni,
  });

  if (!risposta.ok) {
    // L'API restituisce messaggi già scritti per essere letti da una persona:
    // vanno mostrati così come sono, non tradotti una seconda volta.
    let messaggio = "Qualcosa non ha funzionato. Riprova fra un momento.";
    try {
      const corpo = await risposta.json();
      if (corpo?.detail) messaggio = corpo.detail;
    } catch {
      /* la risposta non era JSON: resta il messaggio generico */
    }
    throw new Error(messaggio);
  }
  return risposta.json();
}

export const opzioni = () => chiama("/opzioni");

export const calcola = (dati) =>
  chiama("/calcolo", { method: "POST", body: JSON.stringify(dati) });

export const inverso = (dati) =>
  chiama("/inverso", { method: "POST", body: JSON.stringify(dati) });

export const coefficienti = (anno, territorio) =>
  chiama(`/coefficienti?anno=${anno}&territorio=${territorio}`);

/** 26032.22 -> "26.032,22 €" */
export function euro(valore, decimali = 2) {
  if (valore === null || valore === undefined) return "—";
  return new Intl.NumberFormat("it-IT", {
    style: "currency",
    currency: "EUR",
    minimumFractionDigits: decimali,
    maximumFractionDigits: decimali,
    // Senza questo, la formattazione italiana OMETTE il separatore sui numeri
    // di quattro cifre: "1859,44 €" accanto a "26.032,22 €". In una colonna di
    // importi che si leggono per confronto, due convenzioni diverse nella
    // stessa tabella sono un invito a sbagliare riga.
    useGrouping: "always",
  }).format(valore);
}

/** 74.4 -> "74,4%" — `toFixed` non conosce la virgola decimale italiana. */
export function percentuale(valore, decimali = 1) {
  if (valore === null || valore === undefined) return "—";
  return new Intl.NumberFormat("it-IT", {
    style: "percent",
    minimumFractionDigits: decimali,
    maximumFractionDigits: decimali,
  }).format(valore);
}
