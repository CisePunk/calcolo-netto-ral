# Immagine di pubblicazione.
#
# Perché Docker e non il runtime Python di Render
# -----------------------------------------------
# Il servizio è uno solo — l'API serve anche l'interfaccia compilata — ma per
# costruirlo servono due mondi: Node per compilare React, Python per eseguire
# FastAPI. Un servizio Python su Render non ha `npm`, e un servizio Node non ha
# `uvicorn`: qualunque dei due si scegliesse, il build fallirebbe a metà.
#
# Con due stadi il problema sparisce: il primo compila, il secondo esegue, e
# nell'immagine finale Node non c'è nemmeno. È anche più onesto — quello che
# gira in produzione è la stessa immagine che si può costruire qui.

# --- stadio 1: compila l'interfaccia -----------------------------------------
FROM node:22-slim AS interfaccia
WORKDIR /web

# Prima i manifest, poi il resto: se le dipendenze non cambiano, Docker riusa
# il livello e non riscarica niente.
COPY web/package.json web/package-lock.json ./
RUN npm ci

COPY web/ ./
RUN npm run build


# --- stadio 2: esegue ---------------------------------------------------------
FROM python:3.13-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Il motore, il registro dei coefficienti e l'API. Il database NON entra qui: a
# runtime il registro è il JSON versionato, e MySQL resta uno strumento di
# verifica. Vedi README.
COPY motore/ ./motore/
COPY api/ ./api/
COPY dati/ ./dati/

# L'interfaccia compilata, presa dallo stadio precedente.
COPY --from=interfaccia /web/dist ./web/dist

# Render assegna la porta con la variabile PORT; in locale vale 8000, così
# `docker run -p 8000:8000` funziona senza altro.
ENV PORT=8000
EXPOSE 8000

# Serve una shell per espandere $PORT, ma `exec` fa diventare uvicorn il
# processo numero uno: così riceve i segnali di arresto e si ferma con ordine
# invece di essere ucciso dopo il timeout. Senza, ogni riavvio costa dieci
# secondi di attesa e le richieste in corso vengono troncate.
CMD ["sh", "-c", "exec uvicorn api.main:app --host 0.0.0.0 --port ${PORT}"]
