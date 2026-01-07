-- SQLite
DROP TABLE facturas;

SELECT name FROM sqlite_master WHERE type='table';
PRAGMA table_info(facturas_old);