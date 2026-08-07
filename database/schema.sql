-- ---------------------------------------------------------------------------
-- Registro dei coefficienti fiscali e previdenziali
-- ---------------------------------------------------------------------------
--
-- Perche' un database, per un calcolatore che e' in fondo una funzione pura.
--
-- Il problema vero di questo dominio non e' calcolare: e' che i coefficienti
-- cambiano ogni anno, cambiano da comune a comune, e vanno tracciati con la
-- fonte da cui provengono. Un numero fiscale senza provenienza e senza data non
-- e' verificabile, e la prima stesura di questo progetto ne conteneva sei
-- sbagliati su sette proprio perche' erano scritti "a senso" nel codice.
--
-- Il registro rende quel problema esplicito: ogni valore ha un anno, un ambito
-- territoriale, una fonte e uno stato di verifica dichiarato.
--
-- Da dove arrivano i dati.
-- La fonte di verita' resta dati/coefficienti.json, versionato in git: le
-- modifiche ai coefficienti si leggono in una diff, si discutono e si
-- rivedono come il codice. Da li' viene generato il seed di questo database
-- (strumenti/genera_seed.py). Il database non e' l'originale: e' la copia
-- interrogabile che serve all'applicazione.
--
-- Due forme di addizionale, non una.
-- Analizzando la tabella dell'Agenzia delle Entrate su tutti i 7.792 comuni
-- italiani e' emerso che l'85% usa un'aliquota unica e il 15% usa scaglioni;
-- che il 36% ha una soglia di esenzione e il 64% non ne ha nessuna. Uno schema
-- costruito guardando solo Milano sarebbe stato sbagliato per la maggioranza
-- dei comuni. Da qui le colonne opzionali e i vincoli che le governano.
-- ---------------------------------------------------------------------------

SET NAMES utf8mb4;

DROP TABLE IF EXISTS scaglione;
DROP TABLE IF EXISTS addizionale_comunale;
DROP TABLE IF EXISTS addizionale_regionale;
DROP TABLE IF EXISTS parametro;
DROP TABLE IF EXISTS ccnl;
DROP TABLE IF EXISTS territorio;
DROP TABLE IF EXISTS anno_imposta;
DROP TABLE IF EXISTS fonte;


-- ---------------------------------------------------------------------------
-- Provenienza
-- ---------------------------------------------------------------------------
-- Sta in una tabella sua perche' la stessa norma giustifica piu' coefficienti:
-- la Legge di Bilancio 2026 fissa un'aliquota e insieme una riduzione delle
-- detrazioni. Ripeterne il testo su ogni riga significherebbe poterlo
-- correggere in un posto e dimenticarlo in un altro.
CREATE TABLE fonte (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    riferimento    VARCHAR(500) NOT NULL COMMENT 'Norma, circolare o documento ufficiale',
    stato          ENUM('primaria', 'secondaria', 'da_verificare') NOT NULL
                   COMMENT 'primaria = letta sull''atto ufficiale; secondaria = concorde su piu'' fonti specialistiche',
    data_verifica  DATE NOT NULL,
    nota           TEXT NULL,
    UNIQUE KEY uk_fonte (riferimento(255), stato, data_verifica)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
  COMMENT='Da dove viene ogni numero, e quanto e'' solido';


-- ---------------------------------------------------------------------------
-- Anni d'imposta
-- ---------------------------------------------------------------------------
CREATE TABLE anno_imposta (
    anno                 SMALLINT PRIMARY KEY,
    descrizione          VARCHAR(255) NOT NULL,
    -- Un anno passato serve a confrontarsi con documenti gia' emessi, non a
    -- proiettare stipendi futuri. Tenerli distinti evita di calcolare
    -- un'offerta del 2026 con le aliquote del 2025.
    ammesso_proiezioni   BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Territori
-- ---------------------------------------------------------------------------
CREATE TABLE territorio (
    codice       CHAR(2) PRIMARY KEY COMMENT 'Sigla provincia, usata come chiave breve',
    comune       VARCHAR(64) NOT NULL,
    regione      VARCHAR(64) NOT NULL,
    predefinito  BOOLEAN NOT NULL DEFAULT FALSE,
    nota         TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Contratti collettivi
-- ---------------------------------------------------------------------------
-- Il CCNL NON entra nel calcolo fiscale: la RAL e' annua, quindi le mensilita'
-- cambiano solo il divisore del netto mensile, mai il netto annuo. E' una
-- tabella di presentazione, e va detto per non far credere il contrario.
CREATE TABLE ccnl (
    codice       VARCHAR(32) PRIMARY KEY,
    nome         VARCHAR(128) NOT NULL,
    mensilita    TINYINT UNSIGNED NOT NULL,
    predefinito  BOOLEAN NOT NULL DEFAULT FALSE,
    fonte_id     INT NOT NULL,
    CONSTRAINT fk_ccnl_fonte FOREIGN KEY (fonte_id) REFERENCES fonte(id),
    CONSTRAINT ck_ccnl_mensilita CHECK (mensilita BETWEEN 12 AND 14)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Parametri scalari nazionali
-- ---------------------------------------------------------------------------
-- Aliquote, soglie e importi che non hanno struttura a scaglioni: aliquota
-- INPS, massimale, importi delle detrazioni, soglie del cuneo fiscale.
-- Il raggruppamento per `gruppo` tiene insieme i valori che condividono la
-- stessa fonte e che si leggono insieme.
CREATE TABLE parametro (
    anno      SMALLINT NOT NULL,
    gruppo    VARCHAR(64) NOT NULL COMMENT 'inps, detrazioni_lavoro_dipendente, cuneo_somma_esente, ...',
    chiave    VARCHAR(64) NOT NULL,
    valore    DECIMAL(14,5) NOT NULL,
    fonte_id  INT NOT NULL,
    PRIMARY KEY (anno, gruppo, chiave),
    CONSTRAINT fk_parametro_anno  FOREIGN KEY (anno) REFERENCES anno_imposta(anno),
    CONSTRAINT fk_parametro_fonte FOREIGN KEY (fonte_id) REFERENCES fonte(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Scaglioni progressivi
-- ---------------------------------------------------------------------------
-- Stessa meccanica per l'IRPEF e per le addizionali regionali che la usano:
-- ogni aliquota si applica solo alla quota di reddito che ricade nello
-- scaglione. Una tabella sola, distinta dall'ambito.
CREATE TABLE scaglione (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    ambito            ENUM('irpef', 'addizionale_regionale') NOT NULL,
    anno              SMALLINT NOT NULL,
    territorio        CHAR(2) NULL COMMENT 'NULL per gli scaglioni nazionali (IRPEF)',
    ordine            TINYINT UNSIGNED NOT NULL COMMENT 'Progressivo dal piu'' basso',
    limite_superiore  DECIMAL(12,2) NULL COMMENT 'NULL = ultimo scaglione, senza limite',
    aliquota          DECIMAL(7,6) NOT NULL,
    fonte_id          INT NOT NULL,

    -- Colonna generata, indispensabile per la chiave unica qui sotto.
    --
    -- In SQL due NULL non sono considerati uguali, quindi una UNIQUE che
    -- includa `territorio` NON impedisce righe duplicate quando territorio e'
    -- NULL — cioe' proprio per gli scaglioni IRPEF. Provandolo, il database
    -- accettava due scaglioni identici: nel calcolo sarebbero stati sommati
    -- entrambi, raddoppiando un pezzo di imposta senza alcun segnale.
    --
    -- Sostituendo NULL con un valore convenzionale il confronto torna a
    -- funzionare e il duplicato viene respinto.
    territorio_chiave CHAR(2) GENERATED ALWAYS AS (COALESCE(territorio, '--')) STORED,

    UNIQUE KEY uk_scaglione (ambito, anno, territorio_chiave, ordine),
    CONSTRAINT fk_scaglione_anno       FOREIGN KEY (anno) REFERENCES anno_imposta(anno),
    CONSTRAINT fk_scaglione_territorio FOREIGN KEY (territorio) REFERENCES territorio(codice),
    CONSTRAINT fk_scaglione_fonte      FOREIGN KEY (fonte_id) REFERENCES fonte(id),
    CONSTRAINT ck_scaglione_aliquota   CHECK (aliquota >= 0 AND aliquota <= 1),
    -- L'IRPEF e' nazionale, l'addizionale regionale no: il vincolo impedisce
    -- di inserire uno scaglione IRPEF legato a un comune, o viceversa.
    CONSTRAINT ck_scaglione_ambito CHECK (
        (ambito = 'irpef' AND territorio IS NULL) OR
        (ambito = 'addizionale_regionale' AND territorio IS NOT NULL)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Addizionale regionale
-- ---------------------------------------------------------------------------
-- Due forme possibili: aliquota unica (Sicilia) oppure scaglioni (Lombardia).
-- Il vincolo impedisce di riempirle entrambe o nessuna delle due.
CREATE TABLE addizionale_regionale (
    territorio  CHAR(2) NOT NULL,
    anno        SMALLINT NOT NULL,
    tipo        ENUM('unica', 'scaglioni') NOT NULL,
    aliquota    DECIMAL(7,6) NULL COMMENT 'Valorizzata solo se tipo = unica',
    fonte_id    INT NOT NULL,
    nota        TEXT NULL,
    PRIMARY KEY (territorio, anno),
    CONSTRAINT fk_reg_territorio FOREIGN KEY (territorio) REFERENCES territorio(codice),
    CONSTRAINT fk_reg_anno       FOREIGN KEY (anno) REFERENCES anno_imposta(anno),
    CONSTRAINT fk_reg_fonte      FOREIGN KEY (fonte_id) REFERENCES fonte(id),
    CONSTRAINT ck_reg_forma CHECK (
        (tipo = 'unica'     AND aliquota IS NOT NULL AND aliquota BETWEEN 0 AND 1) OR
        (tipo = 'scaglioni' AND aliquota IS NULL)
    )
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Addizionale comunale
-- ---------------------------------------------------------------------------
-- Aliquota unica, con soglia di esenzione FACOLTATIVA.
--
-- `soglia_esenzione` NULL significa "questo comune non prevede esenzione", che
-- e' il caso del 64% dei comuni italiani — non un dato mancante. Zero
-- significherebbe un'altra cosa, ed e' il motivo per cui la colonna e'
-- nullable invece che DEFAULT 0.
--
-- Dove esiste, e' una SOGLIA e non una franchigia: superata, l'addizionale si
-- paga sull'intero imponibile. A Milano questo produce un gradino di 184 euro
-- per un centesimo di imponibile in piu'.
CREATE TABLE addizionale_comunale (
    territorio        CHAR(2) NOT NULL,
    anno              SMALLINT NOT NULL,
    aliquota          DECIMAL(7,6) NOT NULL,
    soglia_esenzione  DECIMAL(12,2) NULL COMMENT 'NULL = nessuna esenzione prevista',
    fonte_id          INT NOT NULL,
    nota              TEXT NULL,
    PRIMARY KEY (territorio, anno),
    CONSTRAINT fk_com_territorio FOREIGN KEY (territorio) REFERENCES territorio(codice),
    CONSTRAINT fk_com_anno       FOREIGN KEY (anno) REFERENCES anno_imposta(anno),
    CONSTRAINT fk_com_fonte      FOREIGN KEY (fonte_id) REFERENCES fonte(id),
    CONSTRAINT ck_com_aliquota   CHECK (aliquota >= 0 AND aliquota <= 1),
    CONSTRAINT ck_com_soglia     CHECK (soglia_esenzione IS NULL OR soglia_esenzione > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------------------------------------------
-- Viste
-- ---------------------------------------------------------------------------

-- Tutti i coefficienti con la loro provenienza, in un elenco solo: e' quello
-- che alimenta la pagina /coefficienti e la modalita' esperto dell'interfaccia.
CREATE OR REPLACE VIEW v_coefficienti AS
    SELECT p.anno, 'nazionale' AS ambito, p.gruppo AS voce,
           p.chiave, CAST(p.valore AS CHAR) AS valore,
           f.riferimento AS fonte, f.stato, f.data_verifica
      FROM parametro p JOIN fonte f ON f.id = p.fonte_id
    UNION ALL
    SELECT s.anno,
           COALESCE(s.territorio, 'nazionale') AS ambito,
           s.ambito AS voce,
           CONCAT('scaglione ', s.ordine,
                  ' fino a ', COALESCE(CAST(s.limite_superiore AS CHAR), 'oltre')) AS chiave,
           CAST(s.aliquota AS CHAR) AS valore,
           f.riferimento, f.stato, f.data_verifica
      FROM scaglione s JOIN fonte f ON f.id = s.fonte_id
    UNION ALL
    SELECT r.anno, r.territorio, 'addizionale_regionale',
           CONCAT('tipo: ', r.tipo),
           COALESCE(CAST(r.aliquota AS CHAR), 'a scaglioni'),
           f.riferimento, f.stato, f.data_verifica
      FROM addizionale_regionale r JOIN fonte f ON f.id = r.fonte_id
    UNION ALL
    SELECT c.anno, c.territorio, 'addizionale_comunale',
           CONCAT('aliquota; esenzione: ',
                  COALESCE(CAST(c.soglia_esenzione AS CHAR), 'nessuna')),
           CAST(c.aliquota AS CHAR),
           f.riferimento, f.stato, f.data_verifica
      FROM addizionale_comunale c JOIN fonte f ON f.id = c.fonte_id;


-- Quante voci poggiano su una fonte primaria e quante no. E' la domanda che
-- rende onesta la ricerca: un calcolatore che dichiara quanto e' sicuro di se'
-- e' piu' utile di uno che finge una certezza uniforme.
CREATE OR REPLACE VIEW v_stato_verifiche AS
    SELECT anno, ambito, stato, COUNT(*) AS voci
      FROM v_coefficienti
     GROUP BY anno, ambito, stato;
