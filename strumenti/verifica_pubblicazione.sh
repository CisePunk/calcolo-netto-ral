#!/usr/bin/env bash
#
# Verifica che l'applicazione pubblicata risponda come deve, dall'esterno.
#
#   bash strumenti/verifica_pubblicazione.sh https://calcolo-netto-ral.onrender.com
#
# Perché non basta aprirla nel browser
# ------------------------------------
# Aprirla nel browser dice che c'è. Non dice se il calcolo è ancora giusto dopo
# la compilazione, se le intestazioni di sicurezza sono sopravvissute al proxy,
# né quanto aspetta chi arriva quando il servizio si è appena riacceso — che
# sul piano gratuito è la condizione normale, non un caso limite.
#
# Sono le tre cose che decidono se un link si può mandare a qualcuno.

set -uo pipefail

BASE="${1:-}"
[ -n "$BASE" ] || { echo "Uso: bash strumenti/verifica_pubblicazione.sh https://INDIRIZZO"; exit 1; }
BASE="${BASE%/}"

verde()  { printf '\033[1;32m%s\033[0m' "$1"; }
rosso()  { printf '\033[1;31m%s\033[0m' "$1"; }
ESITO=0

riga() { printf '  %-42s ' "$1"; }
ok()   { verde "ok"; printf '   %s\n' "${1:-}"; }
ko()   { rosso "NO"; printf '   %s\n' "${1:-}"; ESITO=1; }

echo
echo "  $BASE"
echo "  ────────────────────────────────────────────────────────────────"

# --- 1. Il risveglio a freddo -------------------------------------------------
# Va misurato per primo, perché la prima richiesta è quella che lo sveglia: se
# la misurassi dopo, troverei il servizio già caldo e otterrei un numero che
# nessun visitatore vedrà mai.
riga "primo caricamento (a freddo)"
INIZIO=$(date +%s)
CODICE=$(curl -s -o /dev/null -w '%{http_code}' --max-time 120 "$BASE/" || echo 000)
FREDDO=$(( $(date +%s) - INIZIO ))
if [ "$CODICE" = "200" ]; then
    if [ "$FREDDO" -le 5 ];   then ok "${FREDDO}s — era gia' sveglio"
    elif [ "$FREDDO" -le 20 ]; then ok "${FREDDO}s"
    else ko "${FREDDO}s — chi arriva aspetta troppo: serve un ping ogni 10 minuti"
    fi
else
    ko "HTTP $CODICE dopo ${FREDDO}s"
fi

# --- 2. Le pagine --------------------------------------------------------------
riga "la pagina risponde"
[ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$BASE/")" = "200" ] \
    && ok || ko

riga "controllo di salute"
[ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 30 "$BASE/api/salute")" = "200" ] \
    && ok || ko

riga "l'interfaccia compilata e' servita"
BUNDLE=$(curl -s --max-time 30 "$BASE/" | grep -oE 'assets/index-[A-Za-z0-9_-]+\.js' | head -1)
[ -n "$BUNDLE" ] && ok "$BUNDLE" || ko "nessun bundle nella pagina"

# --- 3. Il calcolo, che e' il motivo per cui esiste ---------------------------
riga "35.000 -> 26.032,22 netti"
RISPOSTA=$(curl -s --max-time 30 -X POST "$BASE/api/calcolo" \
           -H 'content-type: application/json' -d '{"ral":"35.000"}')
NETTO=$(printf '%s' "$RISPOSTA" | python3 -c \
    "import json,sys
try: print(f\"{json.load(sys.stdin)['netto_annuo']:.2f}\")
except Exception: print('errore')" 2>/dev/null)
[ "$NETTO" = "26032.22" ] && ok "$NETTO" || ko "ottenuto: $NETTO"

riga "formati italiani: 35.000 = 35000"
# Arrotondato allo stesso modo dell'altro controllo: la prima stesura
# confrontava 26032.22 con 26032.22420909091 e segnalava un guasto che non
# c'era. Un controllo che grida al lupo si impara a ignorarlo.
A=$(curl -s --max-time 30 -X POST "$BASE/api/calcolo" -H 'content-type: application/json' \
    -d '{"ral":"35000"}' | python3 -c \
    "import json,sys
try: print(f\"{json.load(sys.stdin)['netto_annuo']:.2f}\")
except Exception: print('errore')" 2>/dev/null)
[ "$A" = "$NETTO" ] && ok "identico a 35.000" || ko "ottenuto: $A, atteso $NETTO"

riga "minimo contrattuale: avviso su 10.000"
AVV=$(curl -s --max-time 30 -X POST "$BASE/api/calcolo" -H 'content-type: application/json' \
      -d '{"ral":"10.000"}' | grep -c "minimo-ccnl" || true)
[ "$AVV" -ge 1 ] && ok || ko "l'avviso non c'e'"

# --- 4. Le difese ---------------------------------------------------------------
INTESTAZIONI=$(curl -s -D - -o /dev/null --max-time 30 "$BASE/")
for h in "content-security-policy" "x-frame-options" "x-content-type-options" "referrer-policy"; do
    riga "intestazione $h"
    printf '%s' "$INTESTAZIONI" | grep -qi "^$h" && ok || ko "assente"
done

riga "https con certificato valido"
curl -s -o /dev/null --max-time 30 "$BASE/" && ok || ko "il certificato non regge"

# Qui contano i BYTE, non lo stato. Qualunque percorso sconosciuto restituisce
# index.html con un 200 — e' il ripiego della single-page, ed e' corretto. La
# prima stesura controllava lo stato e segnalava una fuga di dati che non c'era.
#
# `--path-as-is` serve perche' altrimenti curl normalizza `..` da solo e la
# richiesta ostile parte gia' innocua: si sarebbe provato il percorso sbagliato.
riga "nessuna fuga di file del progetto"
FUGA=0
for p in "/../dati_privati/LEGGIMI.md" "/../api/main.py" "/../dati/coefficienti.json" \
         "/%2e%2e/api/main.py" "/../../etc/passwd"; do
    CORPO=$(curl -s --path-as-is --max-time 30 "$BASE$p" | head -c 400)
    case "$CORPO" in
        *"<!doctype"*|*"<!DOCTYPE"*) ;;                      # la pagina: corretto
        *"root:"*|*"import "*|*"_fonte"*|*"Certificazione"*)  # contenuto vero
            FUGA=1; ULTIMO="$p" ;;
    esac
done
[ "$FUGA" -eq 0 ] && ok "cinque percorsi ostili, tutti sul ripiego" \
    || ko "$ULTIMO restituisce il file vero — non mandare il link"

echo "  ────────────────────────────────────────────────────────────────"
if [ "$ESITO" -eq 0 ]; then
    echo "  $(verde 'Il link si puo mandare.')"
else
    echo "  $(rosso 'Qualcosa non va: guarda le righe NO qui sopra.')"
fi
echo
exit "$ESITO"
