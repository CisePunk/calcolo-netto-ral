import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// In sviluppo il frontend gira su 5173 e l'API su 8000: il proxy fa sì che il
// codice usi sempre percorsi relativi (/api/...), gli stessi che funzioneranno
// in produzione, dove è l'API a servire anche la pagina. Così non esiste una
// configurazione "di sviluppo" che differisce da quella reale.
export default defineConfig({
  plugins: [react()],
  // Un contrassegno della compilazione, mostrato nel piè di pagina. Serve a
  // rispondere in due secondi alla domanda «quale versione sto guardando?»,
  // che durante lo sviluppo è costata un giro di verifiche su codice già
  // corretto: il browser serviva una pagina vecchia.
  define: {
    __COMPILAZIONE__: JSON.stringify(
      new Date().toISOString().slice(0, 16).replace("T", " ")
    ),
  },
  server: {
    proxy: {
      "/api": {
        target: process.env.API_URL ?? "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
