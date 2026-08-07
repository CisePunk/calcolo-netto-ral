import { useEffect, useState } from "react";

/**
 * Controlli di leggibilità.
 *
 * Perché in un calcolatore fiscale non sono un accessorio. Questa pagina è
 * fatta di numeri lunghi, di segni «−» e «+» che ribaltano il significato di
 * una riga, e di differenze che stanno nell'ultima cifra. Chi fatica a leggere
 * non sbaglia "un po' di più": sbaglia in modo diverso, e su un importo che
 * finisce in un contratto.
 *
 * Tre leve indipendenti, perché servono a persone diverse: la dimensione del
 * testo, il contrasto, la trama nei grafici. Chi ha bisogno di caratteri più
 * grandi non ha necessariamente bisogno di più contrasto, e viceversa.
 *
 * Le stesse leve si attivano da sole quando il sistema operativo le richiede:
 * una preferenza già espressa altrove non va chiesta una seconda volta.
 */

// La chiave porta una versione: quando cambia il significato dei valori
// predefiniti, le preferenze salvate in precedenza vanno scartate invece che
// reinterpretate. Chi aveva "come il sistema" non l'aveva scelto — era il
// default di allora — e continuare a imporglielo sarebbe stato un bug.
const PREFERENZE = "leggibilita.v2";

// Valori ammessi per ciascuna leva. Non è una difesa contro un attacco — chi
// scrive nel localStorage di questa origine ha già eseguito codice qui, e a
// quel punto ha di meglio da fare. Serve contro il caso realistico: una chiave
// rimasta da una versione precedente, o modificata a mano per curiosità, che
// finisce in un attributo `data-` a cui nessuna regola CSS corrisponde. Il
// risultato non è un errore visibile, è una pagina senza tema — un guasto che
// si manifesta come «da me si vede strano» e non lascia tracce.
//
// Emerso dal controllo di sicurezza: la lettura si fidava di qualunque oggetto
// JSON, purché fosse JSON valido.
const VALORI_AMMESSI = {
  tema: ["chiaro", "scuro", "automatico"],
  testo: ["normale", "grande", "molto-grande"],
  contrasto: ["normale", "alto"],
  visione: ["standard", "rosso-verde", "senza-colore"],
};

const VALORI_INIZIALI = {
  tema: "chiaro",
  testo: "normale",
  contrasto: "normale",
  visione: "standard",
};

function leggiPreferenze() {
  let salvate;
  try {
    salvate = JSON.parse(localStorage.getItem(PREFERENZE));
  } catch {
    return VALORI_INIZIALI;
  }
  if (!salvate || typeof salvate !== "object") return VALORI_INIZIALI;

  // Ogni leva viene accettata da sola: una preferenza corrotta non deve
  // buttare via anche le altre tre.
  const scelte = { ...VALORI_INIZIALI };
  for (const [chiave, ammessi] of Object.entries(VALORI_AMMESSI)) {
    if (ammessi.includes(salvate[chiave])) scelte[chiave] = salvate[chiave];
  }
  return scelte;
}

export default function Leggibilita() {
  const [scelte, setScelte] = useState(leggiPreferenze);

  useEffect(() => {
    const radice = document.documentElement;
    radice.dataset.tema = scelte.tema;
    radice.dataset.testo = scelte.testo;
    radice.dataset.contrasto = scelte.contrasto;
    radice.dataset.visione = scelte.visione;
    // Le trame non sono una quarta scelta: sono la conseguenza delle prime.
    // Chi seleziona una modalità per daltonismo non deve doversi ricordare di
    // accendere anche il canale di riserva.
    radice.dataset.texture = scelte.visione === "standard" ? "no" : "si";
    try {
      localStorage.setItem(PREFERENZE, JSON.stringify(scelte));
    } catch {
      /* navigazione privata: le scelte valgono per questa sessione */
    }
  }, [scelte]);

  // Il tema EFFETTIVO si calcola qui invece che in CSS, per due motivi: la
  // scelta esplicita deve poter scavalcare il sistema operativo, e i valori del
  // tema scuro restano scritti in un posto solo invece di essere duplicati fra
  // media query e attributo — dove prima o poi divergerebbero.
  useEffect(() => {
    const scuroDiSistema = window.matchMedia("(prefers-color-scheme: dark)");
    const applica = () => {
      const effettivo =
        scelte.tema === "automatico"
          ? scuroDiSistema.matches
            ? "scuro"
            : "chiaro"
          : scelte.tema;
      document.documentElement.dataset.temaEffettivo = effettivo;
    };
    applica();
    scuroDiSistema.addEventListener("change", applica);
    return () => scuroDiSistema.removeEventListener("change", applica);
  }, [scelte.tema]);

  const imposta = (chiave, valore) =>
    setScelte((precedenti) => ({ ...precedenti, [chiave]: valore }));

  return (
    <details className="leggibilita">
      <summary>Leggibilità</summary>
      <div className="leggibilita-corpo">
        <Gruppo
          etichetta="Tema"
          valore={scelte.tema}
          onCambia={(v) => imposta("tema", v)}
          opzioni={[
            ["chiaro", "Chiaro"],
            ["scuro", "Scuro"],
            ["automatico", "Come il sistema"],
          ]}
        />

        <Gruppo
          etichetta="Dimensione del testo"
          valore={scelte.testo}
          onCambia={(v) => imposta("testo", v)}
          opzioni={[
            ["normale", "Normale"],
            ["grande", "Grande"],
            ["molto-grande", "Molto grande"],
          ]}
        />

        <Gruppo
          etichetta="Contrasto"
          valore={scelte.contrasto}
          onCambia={(v) => imposta("contrasto", v)}
          opzioni={[
            ["normale", "Normale"],
            ["alto", "Alto"],
          ]}
        />

        {/* Anteprima viva dei colori.
            Senza di questa, premere i pulsanti della visione non cambia NIENTE
            sullo schermo finché non è stato fatto un calcolo: le tinte
            governano solo il grafico, e il grafico compare dopo. Un controllo
            che non mostra il proprio effetto è un controllo rotto, anche
            quando funziona. */}
        <div className="anteprima-colori">
          <span aria-hidden="true" className="campioni">
            {[1, 2, 3, 4, 5].map((n) => (
              <span key={n} className={`campione campione-${n}`} />
            ))}
          </span>
          {/* La modalità attiva è scritta, non solo mostrata. Se i campioni non
              cambiano ma questa riga sì, il problema è nello schermo o in un
              filtro colore del sistema, non nell'applicazione: è una
              distinzione che da sola risparmia un'indagine. */}
          <span className="anteprima-nota">
            colori del grafico —{" "}
            <strong>
              {{
                standard: "standard",
                "rosso-verde": "daltonismo rosso-verde",
                "senza-colore": "senza colore",
              }[scelte.visione]}
            </strong>
          </span>
        </div>

        <Gruppo
          etichetta="Visione dei colori"
          valore={scelte.visione}
          onCambia={(v) => imposta("visione", v)}
          opzioni={[
            ["standard", "Standard"],
            ["rosso-verde", "Daltonismo rosso-verde"],
            ["senza-colore", "Senza colore"],
          ]}
        />

        <p className="leggibilita-nota">
          <strong>Rosso-verde</strong> usa una tavolozza pensata per protanopia e
          deuteranopia, che insieme sono la quasi totalità dei casi.{" "}
          <strong>Senza colore</strong> rinuncia del tutto alle tinte e affida la
          distinzione a trame e tonalità: serve alla tritanopia, alla visione
          monocromatica e alla stampa in bianco e nero. In entrambe le modalità
          le trame si accendono da sole.
        </p>
        <p className="leggibilita-nota">
          Le scelte restano salvate su questo dispositivo. Se il tuo sistema
          operativo chiede già più contrasto o meno animazioni, la pagina lo
          rispetta senza che tu debba dirlo qui.
        </p>
      </div>
    </details>
  );
}

function Gruppo({ etichetta, valore, opzioni, onCambia }) {
  return (
    <fieldset className="gruppo-leggibilita">
      <legend>{etichetta}</legend>
      {opzioni.map(([chiave, testo]) => (
        <button
          key={chiave}
          type="button"
          aria-pressed={valore === chiave}
          onClick={() => onCambia(chiave)}
        >
          {testo}
        </button>
      ))}
    </fieldset>
  );
}
