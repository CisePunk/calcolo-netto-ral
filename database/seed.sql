-- ---------------------------------------------------------------
-- GENERATO AUTOMATICAMENTE da dati/coefficienti.json
-- Non modificare a mano: le modifiche vanno fatte nel JSON e poi
--     python3 strumenti/genera_seed.py
-- Ultima verifica dei coefficienti: 2026-08-06
-- ---------------------------------------------------------------

SET NAMES utf8mb4;

DELETE FROM scaglione;
DELETE FROM addizionale_comunale;
DELETE FROM addizionale_regionale;
DELETE FROM parametro;
DELETE FROM ccnl;
DELETE FROM territorio;
DELETE FROM anno_imposta;
DELETE FROM fonte;

INSERT INTO fonte (id, riferimento, stato, data_verifica, nota) VALUES
    (1, 'L. 207/2024 art. 1 commi 4-5; circolare Agenzia delle Entrate n. 4/E del 16 maggio 2025', 'secondaria', '2026-08-06', 'La percentuale si applica al reddito da LAVORO DIPENDENTE, ma la soglia di accesso guarda il reddito COMPLESSIVO. La somma non concorre a formare il reddito: incide solo sul netto. Non e'' a scaglioni: si sceglie una sola percentuale in base alla fascia.'),
    (2, 'L. 207/2024 art. 1 comma 6', 'primaria', '2026-08-06', 'Da 20.000,01 a 32.000: 1.000 euro fissi. Da 32.000,01 a 40.000: 1.000 * (40.000 - R) / 8.000. Oltre 40.000: nulla. Rapportata ai giorni.'),
    (3, 'Art. 13 comma 1 TUIR', 'secondaria', '2026-08-06', 'Fascia 2: 1.910 + 1.190 * (28.000 - R) / 13.000. Fascia 3: 1.910 * (50.000 - R) / 22.000. Rapportate ai giorni di lavoro nell''anno.'),
    (4, 'INPS, circolare n. 26 del 30 gennaio 2025 (minimali e massimali 2025); aliquota aggiuntiva: art. 3-ter D.L. 384/1992', 'secondaria', '2026-08-06', 'Il massimale si applica ai soli iscritti per la prima volta dal 1/1/1996: fuori dal caso semplice, implementato ma dichiarato.'),
    (5, 'Art. 11 TUIR, assetto a tre aliquote vigente per l''anno d''imposta 2025 (D.Lgs. 216/2023)', 'primaria', '2026-08-06', 'Seconda aliquota al 35%: e'' il valore corretto per il 2025 e quello che compare nel 730/2026.'),
    (6, 'Art. 1 D.L. 3/2020, convertito con L. 21/2020, e successive modifiche', 'secondaria', '2026-08-06', 'Fino a 15.000: importo pieno, se c''e'' capienza (IRPEF lorda sui redditi da lavoro STRETTAMENTE maggiore delle detrazioni art. 13). Da 15.000 a 28.000: ridotto, pari alla differenza tra detrazioni spettanti e IRPEF lorda, con tetto di 1.200. CUMULABILE con il cuneo fiscale: non e'' stato abrogato dalla L. 207/2024.'),
    (7, 'Art. 13 comma 1.1 TUIR', 'primaria', '2026-08-06', 'Spetta se il reddito complessivo e'' SUPERIORE a 25.000 e NON superiore a 35.000. Il comma 1-bis, spesso citato per errore, e'' stato abrogato dal D.L. 3/2020.'),
    (8, 'L. 207/2024 art. 1 commi 4-5, confermata per il 2026', 'secondaria', '2026-08-06', NULL),
    (9, 'L. 207/2024 art. 1 comma 6, confermata per il 2026', 'secondaria', '2026-08-06', NULL),
    (10, 'INPS, minimali e massimali 2026; aliquota aggiuntiva: art. 3-ter D.L. 384/1992', 'secondaria', '2026-08-06', 'Aliquota FPLD complessiva 33%: 23,81% al datore, 9,19% al lavoratore.'),
    (11, 'L. 199/2025 (Legge di Bilancio 2026), che rende strutturale il taglio della seconda aliquota dal 35% al 33% dal 1 gennaio 2026', 'primaria', '2026-08-06', 'Attenzione: il 730/2026 applica ancora il 35% perche'' riguarda i redditi 2025. Il 33% si vede in busta paga nel 2026.'),
    (12, 'L. 199/2025 (Legge di Bilancio 2026)', 'secondaria', '2026-08-06', 'Fuori dal caso semplice e standard. Non implementata nel motore, dichiarata nelle ASSUNZIONI.'),
    (13, 'Art. 1 D.L. 3/2020 e successive modifiche, in vigore nel 2026', 'secondaria', '2026-08-06', NULL),
    (14, 'Regione Lombardia, addizionale regionale IRPEF; banca dati MEF (codice regione 10)', 'secondaria', '2026-08-06', NULL),
    (15, 'Agenzia delle Entrate, tabella addizionali comunali modulistica 2026 (anno d''imposta 2025), riga F205 MILANO MI', 'primaria', '2026-08-06', 'SOGLIA, non franchigia: superati i 23.000 di imponibile si paga lo 0,8% sull''intero importo. Genera un gradino di circa 184 euro.'),
    (16, 'Regione Lombardia; la L. 199/2025 consente di mantenere i quattro scaglioni preesistenti fino al 2028', 'secondaria', '2026-08-06', 'La Lombardia non si e'' allineata alle tre aliquote statali.'),
    (17, 'Comune di Milano, aliquota invariata rispetto al 2025', 'secondaria', '2026-08-06', 'La tabella ufficiale AdE che confermera'' il 2026 (modulistica 2027) non e'' ancora pubblicata. Esiste una proposta comunale di portare la soglia a 25.000 e l''aliquota massima allo 0,9%: NON in vigore.'),
    (18, 'Regione Siciliana, portale tributi, addizionale regionale IRPEF', 'secondaria', '2026-08-06', 'Aliquota unica, nessuno scaglione: forma diversa dalla Lombardia.'),
    (19, 'Agenzia delle Entrate, tabella addizionali comunali modulistica 2026 (anno d''imposta 2025), riga G273 PALERMO PA', 'primaria', '2026-08-06', 'NESSUNA soglia di esenzione: si paga da subito. Aumentata dall''1,002% dell''anno d''imposta 2024 per effetto del piano di riequilibrio finanziario. E'' l''aliquota da usare per il confronto con la CU.'),
    (20, 'Regione Siciliana, portale tributi', 'secondaria', '2026-08-06', NULL),
    (21, 'Deliberazione del Consiglio comunale di Palermo, misura correttiva imposta dal piano di riequilibrio finanziario concordato con lo Stato', 'secondaria', '2026-08-06', 'Aumento di 0,374 punti rispetto al 2025. Non ancora presente nelle tabelle ufficiali AdE.'),
    (22, 'CCNL Terziario Distribuzione e Servizi: tredicesima a dicembre, quattordicesima a luglio', 'secondaria', '2026-08-06', NULL),
    (23, 'CCNL Metalmeccanici industria', 'da_verificare', '2026-08-06', NULL),
    (24, 'CCNL Studi professionali', 'da_verificare', '2026-08-06', NULL),
    (25, 'CCNL Edilizia industria', 'da_verificare', '2026-08-06', NULL);

INSERT INTO anno_imposta (anno, descrizione, ammesso_proiezioni) VALUES
    (2025, 'anno chiuso, usato solo per il confronto con documenti gia'' emessi', FALSE),
    (2026, 'anno corrente, usato per le proiezioni', TRUE);

INSERT INTO territorio (codice, comune, regione, predefinito, nota) VALUES
    ('MI', 'Milano', 'Lombardia', TRUE, 'Territorio dell''esempio del task. Preselezionato ma sempre dichiarato in interfaccia, mai assunto in silenzio.'),
    ('PA', 'Palermo', 'Sicilia', FALSE, 'Territorio di controllo, usato per il confronto con una Certificazione Unica reale. Ha forma diversa da Milano su entrambe le addizionali: e'' la prova che il registro non puo'' essere una semplice tabella territorio -> aliquota.');

INSERT INTO ccnl (codice, nome, mensilita, predefinito, fonte_id) VALUES
    ('commercio', 'Terziario, Distribuzione e Servizi (Confcommercio)', 14, TRUE, 22),
    ('metalmeccanici', 'Metalmeccanici industria', 13, FALSE, 23),
    ('studi_professionali', 'Studi professionali', 14, FALSE, 24),
    ('edilizia', 'Edilizia industria', 13, FALSE, 25);

INSERT INTO parametro (anno, gruppo, chiave, valore, fonte_id) VALUES
    (2025, 'cuneo_somma_esente', 'limite_reddito_complessivo', 20000.0, 1),
    (2025, 'cuneo_somma_esente', 'fascia_1_limite', 8500.0, 1),
    (2025, 'cuneo_somma_esente', 'fascia_1_percentuale', 0.071, 1),
    (2025, 'cuneo_somma_esente', 'fascia_2_limite', 15000.0, 1),
    (2025, 'cuneo_somma_esente', 'fascia_2_percentuale', 0.053, 1),
    (2025, 'cuneo_somma_esente', 'fascia_3_limite', 20000.0, 1),
    (2025, 'cuneo_somma_esente', 'fascia_3_percentuale', 0.048, 1),
    (2025, 'cuneo_ulteriore_detrazione', 'reddito_minimo_escluso', 20000.0, 2),
    (2025, 'cuneo_ulteriore_detrazione', 'reddito_soglia_piena', 32000.0, 2),
    (2025, 'cuneo_ulteriore_detrazione', 'reddito_massimo', 40000.0, 2),
    (2025, 'cuneo_ulteriore_detrazione', 'importo_pieno', 1000.0, 2),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_1_limite', 15000.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_1_importo', 1955.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_1_minimo', 690.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_2_limite', 28000.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_2_base', 1910.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_2_quota', 1190.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_2_divisore', 13000.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_3_limite', 50000.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_3_base', 1910.0, 3),
    (2025, 'detrazioni_lavoro_dipendente', 'fascia_3_divisore', 22000.0, 3),
    (2025, 'inps', 'aliquota_dipendente', 0.0919, 4),
    (2025, 'inps', 'aliquota_aggiuntiva', 0.01, 4),
    (2025, 'inps', 'soglia_prima_fascia', 55448.0, 4),
    (2025, 'inps', 'massimale_annuo', 120607.0, 4),
    (2025, 'trattamento_integrativo', 'soglia_importo_pieno', 15000.0, 6),
    (2025, 'trattamento_integrativo', 'soglia_massima', 28000.0, 6),
    (2025, 'trattamento_integrativo', 'importo', 1200.0, 6),
    (2025, 'ulteriore_detrazione_65', 'reddito_minimo_escluso', 25000.0, 7),
    (2025, 'ulteriore_detrazione_65', 'reddito_massimo_incluso', 35000.0, 7),
    (2025, 'ulteriore_detrazione_65', 'importo', 65.0, 7),
    (2026, 'cuneo_somma_esente', 'limite_reddito_complessivo', 20000.0, 8),
    (2026, 'cuneo_somma_esente', 'fascia_1_limite', 8500.0, 8),
    (2026, 'cuneo_somma_esente', 'fascia_1_percentuale', 0.071, 8),
    (2026, 'cuneo_somma_esente', 'fascia_2_limite', 15000.0, 8),
    (2026, 'cuneo_somma_esente', 'fascia_2_percentuale', 0.053, 8),
    (2026, 'cuneo_somma_esente', 'fascia_3_limite', 20000.0, 8),
    (2026, 'cuneo_somma_esente', 'fascia_3_percentuale', 0.048, 8),
    (2026, 'cuneo_ulteriore_detrazione', 'reddito_minimo_escluso', 20000.0, 9),
    (2026, 'cuneo_ulteriore_detrazione', 'reddito_soglia_piena', 32000.0, 9),
    (2026, 'cuneo_ulteriore_detrazione', 'reddito_massimo', 40000.0, 9),
    (2026, 'cuneo_ulteriore_detrazione', 'importo_pieno', 1000.0, 9),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_1_limite', 15000.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_1_importo', 1955.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_1_minimo', 690.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_2_limite', 28000.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_2_base', 1910.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_2_quota', 1190.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_2_divisore', 13000.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_3_limite', 50000.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_3_base', 1910.0, 3),
    (2026, 'detrazioni_lavoro_dipendente', 'fascia_3_divisore', 22000.0, 3),
    (2026, 'inps', 'aliquota_dipendente', 0.0919, 10),
    (2026, 'inps', 'aliquota_aggiuntiva', 0.01, 10),
    (2026, 'inps', 'soglia_prima_fascia', 56224.0, 10),
    (2026, 'inps', 'massimale_annuo', 122295.0, 10),
    (2026, 'riduzione_detrazioni_redditi_alti', 'soglia_reddito', 200000.0, 12),
    (2026, 'riduzione_detrazioni_redditi_alti', 'importo_riduzione', 440.0, 12),
    (2026, 'trattamento_integrativo', 'soglia_importo_pieno', 15000.0, 13),
    (2026, 'trattamento_integrativo', 'soglia_massima', 28000.0, 13),
    (2026, 'trattamento_integrativo', 'importo', 1200.0, 13),
    (2026, 'ulteriore_detrazione_65', 'reddito_minimo_escluso', 25000.0, 7),
    (2026, 'ulteriore_detrazione_65', 'reddito_massimo_incluso', 35000.0, 7),
    (2026, 'ulteriore_detrazione_65', 'importo', 65.0, 7);

INSERT INTO scaglione (ambito, anno, territorio, ordine, limite_superiore, aliquota, fonte_id) VALUES
    ('irpef', 2025, NULL, 1, 28000.0, 0.23, 5),
    ('irpef', 2025, NULL, 2, 50000.0, 0.35, 5),
    ('irpef', 2025, NULL, 3, NULL, 0.43, 5),
    ('irpef', 2026, NULL, 1, 28000.0, 0.23, 11),
    ('irpef', 2026, NULL, 2, 50000.0, 0.33, 11),
    ('irpef', 2026, NULL, 3, NULL, 0.43, 11),
    ('addizionale_regionale', 2025, 'MI', 1, 15000.0, 0.0123, 14),
    ('addizionale_regionale', 2025, 'MI', 2, 28000.0, 0.0158, 14),
    ('addizionale_regionale', 2025, 'MI', 3, 50000.0, 0.0172, 14),
    ('addizionale_regionale', 2025, 'MI', 4, NULL, 0.0173, 14),
    ('addizionale_regionale', 2026, 'MI', 1, 15000.0, 0.0123, 16),
    ('addizionale_regionale', 2026, 'MI', 2, 28000.0, 0.0158, 16),
    ('addizionale_regionale', 2026, 'MI', 3, 50000.0, 0.0172, 16),
    ('addizionale_regionale', 2026, 'MI', 4, NULL, 0.0173, 16);

INSERT INTO addizionale_regionale (territorio, anno, tipo, aliquota, fonte_id, nota) VALUES
    ('MI', 2025, 'scaglioni', NULL, 14, NULL),
    ('MI', 2026, 'scaglioni', NULL, 16, 'La Lombardia non si e'' allineata alle tre aliquote statali.'),
    ('PA', 2025, 'unica', 0.0123, 18, 'Aliquota unica, nessuno scaglione: forma diversa dalla Lombardia.'),
    ('PA', 2026, 'unica', 0.0123, 20, NULL);

INSERT INTO addizionale_comunale (territorio, anno, aliquota, soglia_esenzione, fonte_id, nota) VALUES
    ('MI', 2025, 0.008, 23000.0, 15, 'SOGLIA, non franchigia: superati i 23.000 di imponibile si paga lo 0,8% sull''intero importo. Genera un gradino di circa 184 euro.'),
    ('MI', 2026, 0.008, 23000.0, 17, 'La tabella ufficiale AdE che confermera'' il 2026 (modulistica 2027) non e'' ancora pubblicata. Esiste una proposta comunale di portare la soglia a 25.000 e l''aliquota massima allo 0,9%: NON in vigore.'),
    ('PA', 2025, 0.01014, NULL, 19, 'NESSUNA soglia di esenzione: si paga da subito. Aumentata dall''1,002% dell''anno d''imposta 2024 per effetto del piano di riequilibrio finanziario. E'' l''aliquota da usare per il confronto con la CU.'),
    ('PA', 2026, 0.01404, NULL, 21, 'Aumento di 0,374 punti rispetto al 2025. Non ancora presente nelle tabelle ufficiali AdE.');

