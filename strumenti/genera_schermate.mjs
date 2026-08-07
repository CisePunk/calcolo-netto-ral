/**
 * Rigenera le schermate del prototipo per il progetto Figma.
 *
 * Perché esiste
 * -------------
 * Le prime diciannove erano state fatte a mano. Poi tre difetti dell'interfaccia
 * sono stati corretti — la frase di conferma spezzata in colonne, gli importi
 * fuori schermo sul telefono, l'avviso sul minimo contrattuale — e le immagini
 * sono rimaste quelle di prima.
 *
 * Un'immagine vecchia non ha l'aria di essere vecchia. Sarebbero finite nella
 * presentazione mostrando esattamente i difetti che erano stati sistemati, e
 * nessuno se ne sarebbe accorto guardandole.
 *
 * Da qui uno script: rifarle costa un comando invece di mezz'ora, quindi si
 * rifanno davvero ogni volta che l'interfaccia cambia.
 *
 * Come si usa
 * -----------
 *     # in un terminale: l'applicazione deve girare
 *     .venv/bin/python -m uvicorn api.main:app --port 8000
 *
 *     # in un altro, dalla radice del progetto
 *     node strumenti/genera_schermate.mjs
 *
 * Playwright non è fra le dipendenze del pacchetto ed è voluto: serve solo a
 * generare immagini, non a far funzionare il prodotto. Chi non ce l'ha
 * installa `npm i -D playwright` e poi lo toglie.
 */

import { mkdir } from "node:fs/promises";
import { createRequire } from "node:module";

// Playwright vive in web/node_modules, e la risoluzione dei moduli segue la
// posizione DI QUESTO FILE, non la cartella da cui lo lanci: importarlo per
// nome fallisce anche stando dentro web/. Da qui l'aggancio esplicito.
const richiedi = createRequire(new URL("../web/package.json", import.meta.url));
const { chromium } = richiedi("playwright");

const BASE = "http://127.0.0.1:8000";
const USCITA = "documenti/ux/design/schermate";

const SCRIVANIA = { width: 1280, height: 1200 };
const TELEFONO = { width: 390, height: 900 };

await mkdir(USCITA, { recursive: true });
const browser = await chromium.launch();

/** Una pagina nuova per ogni scatto: nessuno stato che si trascina. */
async function pagina(viewport = SCRIVANIA) {
  const p = await browser.newPage({ viewport, deviceScaleFactor: 2 });
  await p.goto(BASE, { waitUntil: "networkidle" });
  return p;
}

const campo = (p) => p.locator("input[type=text], input[inputmode]").first();
const calcola = (p) => p.locator("button[type=submit]").first();

async function scatta(p, nome, selettore) {
  const dove = `${USCITA}/${nome}.png`;
  if (selettore) await p.locator(selettore).screenshot({ path: dove });
  else await p.screenshot({ path: dove, fullPage: true });
  console.log(`  ${nome}`);
  await p.close();
}

/** Preme un pulsante trovandolo dal testo dell'etichetta. */
async function premi(p, testo) {
  await p.getByRole("button", { name: testo, exact: false }).first().click();
  await p.waitForTimeout(150);
}

// --- lo stato di partenza -------------------------------------------------
{
  const p = await pagina();
  await scatta(p, "01-vuoto-neofita-scrivania");
}
{
  const p = await pagina(TELEFONO);
  await scatta(p, "04-vuoto-neofita-telefono");
}

// --- l'eco dell'input: come lo strumento dice di aver capito --------------
{
  const p = await pagina();
  await campo(p).fill("35.000");
  await p.waitForTimeout(250);
  await scatta(p, "02-eco-input");
}

// --- il risultato ---------------------------------------------------------
for (const [nome, viewport] of [
  ["03-risultato-neofita-scrivania", SCRIVANIA],
  ["05-risultato-neofita-telefono", TELEFONO],
]) {
  const p = await pagina(viewport);
  await campo(p).fill("35.000");
  await calcola(p).click();
  await p.waitForSelector(".risultato", { timeout: 8000 });
  await p.waitForTimeout(400);
  await scatta(p, nome);
}

// --- gli stati d'errore e di avviso ---------------------------------------
{
  const p = await pagina();
  await campo(p).fill("trentacinquemila");
  await calcola(p).click();
  await p.waitForTimeout(600);
  await scatta(p, "06-input-non-interpretabile");
}
{
  const p = await pagina();
  await campo(p).fill("1800");
  await calcola(p).click();
  await p.waitForSelector(".risultato", { timeout: 8000 });
  await p.waitForTimeout(300);
  await scatta(p, "07-avviso-sembra-mensile");
}
// NUOVA: l'avviso sul minimo contrattuale, che prima non esisteva.
{
  const p = await pagina();
  await campo(p).fill("10.000");
  await calcola(p).click();
  await p.waitForSelector(".risultato", { timeout: 8000 });
  await p.waitForTimeout(300);
  await scatta(p, "20-avviso-minimo-ccnl");
}

// --- modalità esperto -----------------------------------------------------
{
  const p = await pagina();
  await premi(p, "Esperto");
  await scatta(p, "08-esperto-parametri");
}
{
  const p = await pagina();
  await premi(p, "Esperto");
  await campo(p).fill("35.000");
  await calcola(p).click();
  await p.waitForSelector(".risultato", { timeout: 8000 });
  await p.waitForTimeout(400);
  await scatta(p, "09-esperto-risultato-e-fonti");
}

// --- leggibilità: le quattro leve ------------------------------------------
async function conPannello(fn) {
  const p = await pagina();
  await campo(p).fill("35.000");
  await calcola(p).click();
  await p.waitForSelector(".risultato", { timeout: 8000 });
  await p.locator(".leggibilita summary").click();
  await p.waitForTimeout(200);
  if (fn) await fn(p);
  await p.waitForTimeout(300);
  return p;
}

await scatta(await conPannello(), "10-pannello-leggibilita");

for (const [nome, etichetta] of [
  ["11-visione-standard", "Standard"],
  ["12-visione-rosso-verde", "Daltonismo rosso-verde"],
  ["13-visione-senza-colore", "Senza colore"],
  ["14-alto-contrasto", "Alto"],
  ["15-testo-molto-grande", "Molto grande"],
  ["16-tema-scuro", "Scuro"],
]) {
  await scatta(await conPannello((p) => premi(p, etichetta)), nome);
}

// --- calcolo inverso: i tre esiti ------------------------------------------
async function inverso(netto, mensile = true) {
  const p = await pagina();
  // Il selettore di direzione ha `role="tab"`, non `button`: cercarlo come
  // pulsante fallisce con un timeout di trenta secondi e nessuna spiegazione
  // utile. Vale la pena guardare il markup invece di indovinare il ruolo.
  await p.getByRole("tab", { name: /netto/i }).last().click();
  await p.waitForTimeout(250);
  await p.locator("input[type=text], input[inputmode]").first().fill(netto);
  // "mensile" e "annuo" sono due radio nello stesso fieldset, nell'ordine.
  const radio = p.locator("input[type=radio]");
  if ((await radio.count()) >= 2) await radio.nth(mensile ? 0 : 1).check();
  await calcola(p).click();
  await p.waitForTimeout(1500);
  return p;
}

await scatta(await inverso("1.800"), "17-inverso-netto-mensile");
await scatta(await inverso("9.500", false), "18-netto-ambiguo");
await scatta(await inverso("9.200", false), "19-netto-impossibile");

await browser.close();
console.log("\n  Fatto. Ricordati di rilanciare anche genera_curva.py se sono");
console.log("  cambiate le discontinuità.");
