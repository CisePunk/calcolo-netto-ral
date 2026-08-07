"""
Genera il seed SQL del registro a partire da dati/coefficienti.json.

Perche' generato e non scritto a mano
-------------------------------------
I coefficienti esistono in un posto solo: dati/coefficienti.json, versionato in
git. Una modifica a un'aliquota si legge in una diff, si discute e si rivede
come una modifica al codice.

Se il seed SQL fosse scritto a mano, esisterebbero due copie degli stessi
numeri, e prima o poi divergerebbero: si aggiorna il JSON, ci si dimentica del
SQL, e il database serve all'applicazione un'aliquota vecchia. E' esattamente
il tipo di errore silenzioso che questo progetto cerca di rendere impossibile.

Generandolo, la divergenza non puo' avvenire: il seed e' una funzione del JSON.

Uso
---
    python3 strumenti/genera_seed.py            # scrive database/seed.sql
    python3 strumenti/genera_seed.py --stdout   # lo stampa e basta
"""

import json
import pathlib
import sys

RADICE = pathlib.Path(__file__).resolve().parent.parent
REGISTRO = RADICE / "dati" / "coefficienti.json"
USCITA = RADICE / "database" / "seed.sql"

# Chiavi che non sono coefficienti ma metadati.
META = ("_fonte", "_stato", "_nota")


def testo(valore) -> str:
    """Letterale SQL per una stringa, con gli apostrofi raddoppiati.

    L'italiano e' pieno di apostrofi ('dell'imposta', 'l'aliquota') e ognuno,
    non protetto, chiuderebbe la stringa a meta' frase.
    """
    if valore is None:
        return "NULL"
    return "'" + str(valore).replace("\\", "\\\\").replace("'", "''") + "'"


def numero(valore) -> str:
    return "NULL" if valore is None else repr(float(valore))


class Fonti:
    """Raccoglie le fonti deduplicate e assegna a ognuna un identificativo.

    La stessa norma giustifica piu' coefficienti — la Legge di Bilancio 2026
    fissa un'aliquota e insieme una riduzione delle detrazioni — quindi il testo
    va scritto una volta sola.
    """

    def __init__(self, data_verifica):
        self.data_verifica = data_verifica
        self._per_chiave = {}
        self.righe = []

    def id_di(self, sezione: dict) -> int:
        riferimento = sezione.get("_fonte") or "non dichiarata"
        stato = sezione.get("_stato") or "da_verificare"
        nota = sezione.get("_nota")
        chiave = (riferimento, stato)
        if chiave not in self._per_chiave:
            identificativo = len(self._per_chiave) + 1
            self._per_chiave[chiave] = identificativo
            self.righe.append(
                f"({identificativo}, {testo(riferimento)}, {testo(stato)}, "
                f"{testo(self.data_verifica)}, {testo(nota)})"
            )
        return self._per_chiave[chiave]


def genera(registro: dict) -> str:
    meta = registro["_meta"]
    fonti = Fonti(meta["data_ultima_verifica"])

    anni, territori, ccnl = [], [], []
    parametri, scaglioni, regionali, comunali = [], [], [], []

    # --- anni ---------------------------------------------------------------
    for anno in sorted(registro["nazionale"]):
        recente = anno == max(registro["nazionale"])
        descrizione = ("anno corrente, usato per le proiezioni" if recente
                       else "anno chiuso, usato solo per il confronto con documenti gia' emessi")
        anni.append(f"({anno}, {testo(descrizione)}, {'TRUE' if recente else 'FALSE'})")

    # --- parametri e scaglioni nazionali ------------------------------------
    for anno, gruppi in sorted(registro["nazionale"].items()):
        for gruppo, sezione in sorted(gruppi.items()):
            fonte_id = fonti.id_di(sezione)
            for chiave, valore in sezione.items():
                if chiave in META:
                    continue

                # Gli scaglioni progressivi hanno una tabella propria: la loro
                # struttura (ordine, limite, aliquota) e' informazione, non un
                # dettaglio di serializzazione.
                if chiave == "scaglioni":
                    for ordine, (limite, aliquota) in enumerate(valore, start=1):
                        scaglioni.append(
                            f"('irpef', {anno}, NULL, {ordine}, "
                            f"{numero(limite)}, {numero(aliquota)}, {fonte_id})")
                    continue

                # Le fasce della somma esente NON sono scaglioni: non si sommano
                # per quote, se ne applica una sola all'intero reddito. Appiattirle
                # in parametri evita di suggerire una meccanica che non c'e'.
                if chiave == "fasce":
                    for indice, (limite, percentuale) in enumerate(valore, start=1):
                        parametri.append(
                            f"({anno}, {testo(gruppo)}, {testo(f'fascia_{indice}_limite')}, "
                            f"{numero(limite)}, {fonte_id})")
                        parametri.append(
                            f"({anno}, {testo(gruppo)}, {testo(f'fascia_{indice}_percentuale')}, "
                            f"{numero(percentuale)}, {fonte_id})")
                    continue

                if isinstance(valore, (int, float)):
                    parametri.append(
                        f"({anno}, {testo(gruppo)}, {testo(chiave)}, "
                        f"{numero(valore)}, {fonte_id})")

    # --- territori e addizionali --------------------------------------------
    for codice, dati in sorted(registro["territori"].items()):
        territori.append(
            f"({testo(codice)}, {testo(dati['comune'])}, {testo(dati['regione'])}, "
            f"{'TRUE' if dati.get('predefinito') else 'FALSE'}, {testo(dati.get('_nota'))})")

        for anno, per_anno in sorted(dati["anni"].items()):
            regionale = per_anno["regionale"]
            fonte_id = fonti.id_di(regionale)
            if regionale["tipo"] == "scaglioni":
                for ordine, (limite, aliquota) in enumerate(regionale["scaglioni"], start=1):
                    scaglioni.append(
                        f"('addizionale_regionale', {anno}, {testo(codice)}, {ordine}, "
                        f"{numero(limite)}, {numero(aliquota)}, {fonte_id})")
                aliquota_unica = None
            else:
                aliquota_unica = regionale["aliquota"]
            regionali.append(
                f"({testo(codice)}, {anno}, {testo(regionale['tipo'])}, "
                f"{numero(aliquota_unica)}, {fonte_id}, {testo(regionale.get('_nota'))})")

            comunale = per_anno["comunale"]
            fonte_id = fonti.id_di(comunale)
            comunali.append(
                f"({testo(codice)}, {anno}, {numero(comunale['aliquota'])}, "
                f"{numero(comunale.get('soglia_esenzione'))}, {fonte_id}, "
                f"{testo(comunale.get('_nota'))})")

    # --- contratti ----------------------------------------------------------
    for contratto in registro["ccnl"]["contratti"]:
        fonte_id = fonti.id_di(contratto)
        ccnl.append(
            f"({testo(contratto['codice'])}, {testo(contratto['nome'])}, "
            f"{contratto['mensilita']}, "
            f"{'TRUE' if contratto.get('predefinito') else 'FALSE'}, {fonte_id})")

    def blocco(tabella, colonne, righe):
        if not righe:
            return ""
        valori = ",\n    ".join(righe)
        return (f"INSERT INTO {tabella} ({colonne}) VALUES\n    {valori};\n\n")

    return "".join([
        "-- ---------------------------------------------------------------\n",
        "-- GENERATO AUTOMATICAMENTE da dati/coefficienti.json\n",
        "-- Non modificare a mano: le modifiche vanno fatte nel JSON e poi\n",
        "--     python3 strumenti/genera_seed.py\n",
        f"-- Ultima verifica dei coefficienti: {meta['data_ultima_verifica']}\n",
        "-- ---------------------------------------------------------------\n\n",
        "SET NAMES utf8mb4;\n\n",
        "DELETE FROM scaglione;\n",
        "DELETE FROM addizionale_comunale;\n",
        "DELETE FROM addizionale_regionale;\n",
        "DELETE FROM parametro;\n",
        "DELETE FROM ccnl;\n",
        "DELETE FROM territorio;\n",
        "DELETE FROM anno_imposta;\n",
        "DELETE FROM fonte;\n\n",
        blocco("fonte", "id, riferimento, stato, data_verifica, nota", fonti.righe),
        blocco("anno_imposta", "anno, descrizione, ammesso_proiezioni", anni),
        blocco("territorio", "codice, comune, regione, predefinito, nota", territori),
        blocco("ccnl", "codice, nome, mensilita, predefinito, fonte_id", ccnl),
        blocco("parametro", "anno, gruppo, chiave, valore, fonte_id", parametri),
        blocco("scaglione", "ambito, anno, territorio, ordine, limite_superiore, aliquota, fonte_id", scaglioni),
        blocco("addizionale_regionale", "territorio, anno, tipo, aliquota, fonte_id, nota", regionali),
        blocco("addizionale_comunale", "territorio, anno, aliquota, soglia_esenzione, fonte_id, nota", comunali),
    ])


def main():
    registro = json.loads(REGISTRO.read_text(encoding="utf-8"))
    sql = genera(registro)

    if "--stdout" in sys.argv:
        print(sql)
        return 0

    USCITA.parent.mkdir(exist_ok=True)
    USCITA.write_text(sql, encoding="utf-8")

    conteggi = {
        "fonti": sql.count("INSERT INTO fonte"),
        "righe totali": sql.count("),\n") + sql.count(");\n"),
    }
    print(f"Scritto {USCITA.relative_to(RADICE)}")
    print(f"  righe di INSERT generate: {conteggi['righe totali']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
