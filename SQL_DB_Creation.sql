IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'DANE_DB')
BEGIN
    CREATE DATABASE DANEDB;
END;