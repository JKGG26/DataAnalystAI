IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DANE_DB')
BEGIN
    CREATE DATABASE DANE_DB;
END;