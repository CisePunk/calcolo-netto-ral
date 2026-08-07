/**
 * I testi della guida in linea.
 *
 * Stanno in un file a parte, e non sparsi nei componenti, per una ragione
 * precisa: sono il contenuto principale della modalità "alle prime armi", non
 * una decorazione dell'interfaccia. Riunirli permette di rileggerli tutti
 * insieme e accorgersi se una spiegazione contraddice un'altra.
 *
 * Regole di scrittura, applicate a tutte le voci:
 *   - si dice cosa vuol dire, non come funziona il codice;
 *   - si usa la parola che l'utente conosce prima di quella tecnica;
 *   - dove c'è un equivoco frequente, lo si nomina esplicitamente.
 */

export const aiutoCampi = {
  ral: {
    titolo: "Che cos'è la RAL",
    testo:
      "È lo stipendio ANNUO e LORDO scritto nel contratto: la somma di tutte " +
      "le mensilità, prima delle tasse e dei contributi. Non è quello che il " +
      "dipendente riceve sul conto, ed è più alta dello stipendio mensile che " +
      "si ha in mente.",
    equivoco:
      "Se stai pensando a una cifra come 1.800 € o 2.500 €, quello è uno " +
      "stipendio mensile: la RAL è circa dodici volte tanto.",
  },
  netto: {
    titolo: "Il netto che vuoi garantire",
    testo:
      "L'importo che il dipendente si trova effettivamente sul conto, dopo " +
      "tasse e contributi. Indica se è mensile o annuo: sono numeri molto " +
      "diversi e confonderli è l'errore più comune.",
  },
  territorio: {
    titolo: "Perché serve il comune",
    testo:
      "Le addizionali regionale e comunale cambiano da un territorio all'altro, " +
      "e non di poco: a parità di stipendio lordo la differenza fra due comuni " +
      "può superare i 600 € l'anno. Un calcolo senza il comune è un calcolo " +
      "incompleto.",
  },
  anno: {
    titolo: "Anno d'imposta",
    testo:
      "Le aliquote cambiano ogni anno. Il 2026 serve per le proiezioni; il 2025 " +
      "serve solo a confrontare i conti con documenti già emessi, come una " +
      "Certificazione Unica.",
  },
  ccnl: {
    titolo: "Contratto collettivo",
    testo:
      "Qui determina soltanto in quante mensilità viene diviso lo stipendio " +
      "(tredicesima, quattordicesima). Non cambia le tasse né il netto annuo: " +
      "cambia solo la cifra che si vede ogni mese.",
  },
  mensilita: {
    titolo: "Mensilità",
    testo:
      "In quante rate viene distribuito il netto annuo. Il netto ANNUO resta " +
      "identico con 12, 13 o 14 mensilità: cambia solo quanto si riceve ogni volta.",
  },
  giorni: {
    titolo: "Giorni di detrazione",
    testo:
      "I giorni di lavoro nell'anno. Con un rapporto iniziato o finito in corso " +
      "d'anno, detrazioni e bonus vengono ridotti in proporzione. Lascia 365 se " +
      "il rapporto copre tutto l'anno.",
  },
};

/**
 * Le voci del risultato. Ogni riga della tabella delle trattenute può essere
 * spiegata: è la differenza fra mostrare un numero e mostrare un calcolo.
 * Le chiavi corrispondono all'inizio dell'etichetta prodotta dal motore.
 */
export const aiutoVoci = [
  {
    chiave: "Retribuzione lorda",
    testo:
      "Il punto di partenza: quanto costa lo stipendio prima di qualunque " +
      "trattenuta. È la RAL che hai inserito, rapportata ai giorni di lavoro.",
  },
  {
    chiave: "Contributi INPS",
    testo:
      "La quota di contributi previdenziali a carico del dipendente, il 9,19% " +
      "della retribuzione. Non è una tassa: costruisce la pensione futura. " +
      "Si aggiunge un 1% sulla parte di stipendio oltre una soglia annuale.",
  },
  {
    chiave: "Imponibile fiscale",
    testo:
      "Quello su cui si calcolano le tasse: la retribuzione meno i contributi. " +
      "I contributi non vengono tassati, ed è il motivo per cui l'IRPEF non si " +
      "calcola sull'intera RAL.",
  },
  {
    chiave: "IRPEF lorda",
    testo:
      "L'imposta sul reddito prima delle detrazioni, calcolata a scaglioni: " +
      "ogni fascia di reddito ha la sua aliquota e paga solo sulla parte che " +
      "le compete. Guadagnare un euro in più non fa aumentare l'aliquota su tutto.",
  },
  {
    chiave: "Detrazione per lavoro dipendente",
    testo:
      "Uno sconto sull'IRPEF che spetta a tutti i lavoratori dipendenti. " +
      "Diminuisce al crescere del reddito e si azzera sopra i 50.000 €. " +
      "Sui redditi bassi arriva ad annullare l'imposta.",
  },
  {
    chiave: "Ulteriore detrazione",
    testo: "Uno sconto aggiuntivo di 65 € per i redditi fra 25.000 e 35.000 €.",
  },
  {
    chiave: "Detrazione taglio del cuneo",
    testo:
      "Fino a 1.000 € di sconto sull'IRPEF per i redditi fra 20.000 e 40.000 €. " +
      "Sopra i 32.000 € cala gradualmente fino ad azzerarsi a 40.000 €.",
  },
  {
    chiave: "IRPEF netta",
    testo:
      "L'imposta effettivamente dovuta: la lorda meno tutte le detrazioni. " +
      "Non può mai scendere sotto zero — se le detrazioni superano l'imposta, " +
      "l'IRPEF è semplicemente zero.",
  },
  {
    chiave: "Addizionale regionale",
    testo:
      "Un'imposta locale che va alla Regione. Alcune regioni la calcolano a " +
      "scaglioni come l'IRPEF, altre applicano una percentuale unica.",
  },
  {
    chiave: "Addizionale comunale",
    testo:
      "Un'imposta locale che va al Comune. Molti comuni prevedono una soglia " +
      "sotto la quale non si paga nulla — ma attenzione: superata la soglia si " +
      "paga sull'intero importo, non solo sulla parte eccedente.",
  },
  {
    chiave: "Somma esente",
    testo:
      "Denaro in più in busta paga per i redditi bassi, esente da tasse. " +
      "Non è uno sconto sull'imposta: è una somma che si aggiunge al netto.",
  },
  {
    chiave: "Trattamento integrativo",
    testo:
      "L'ex bonus di 100 € al mese, fino a 1.200 € l'anno per i redditi bassi. " +
      "Come la somma esente, si aggiunge al netto invece di ridurre le tasse.",
  },
];

export function aiutoPerVoce(etichetta) {
  const trovata = aiutoVoci.find((v) => etichetta.startsWith(v.chiave));
  return trovata ? trovata.testo : null;
}

export const spiegazioni = {
  gradino:
    "Superata la soglia di esenzione comunale l'addizionale si paga sull'intero " +
    "imponibile, non solo sulla parte eccedente. È il motivo per cui, appena " +
    "oltre quella soglia, un aumento di stipendio lordo può ridurre il netto.",
  nettoSopraLordo:
    "Il netto risulta superiore al lordo perché somma esente e trattamento " +
    "integrativo non sono sconti sulle tasse: sono somme che il datore eroga " +
    "in aggiunta allo stipendio. Su questi livelli di reddito superano le " +
    "trattenute.",
  mensilita:
    "Il netto annuo non cambia al variare delle mensilità: cambia solo in " +
    "quante rate viene distribuito.",
};

export const statiFonte = {
  primaria: {
    etichetta: "fonte primaria",
    descrizione: "letta sull'atto ufficiale (norma, circolare, tabella dell'Agenzia)",
  },
  secondaria: {
    etichetta: "fonte secondaria",
    descrizione: "concorde su più fonti specialistiche, non ancora sull'atto originale",
  },
  da_verificare: {
    etichetta: "da verificare",
    descrizione: "non ancora confermata",
  },
};
