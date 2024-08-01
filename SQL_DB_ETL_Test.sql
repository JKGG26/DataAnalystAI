USE DANE_DB
GO
---------------------------------------------
----------------- VARIABLES -----------------
---------------------------------------------
-- Set file path to load
DECLARE @test_file_path nvarchar(350);
SET @test_file_path = 'C:\Users\JhormanDavidGonzŠlez\Documents\Projects\DataAnalystAI\data\test_send.csv';

-- DECLARE SQL command to do BULK INSERT
DECLARE @SQL NVARCHAR(MAX)
SET @SQL = '
	BULK INSERT #TempTableStageTest
	FROM ''' + @test_file_path + '''
	WITH (
		FORMAT = ''CSV'',
		FIRSTROW = 2,
		ROWTERMINATOR = ''\n'',
		FIELDTERMINATOR = ''|''
	);'
---------------------------------------------
---------------- PREPARATION ----------------
---------------------------------------------
-- Check if temporal staging tabel already exists and drop it
IF OBJECT_ID('tempdb..#TempTableStageTest') IS NOT NULL
BEGIN
    DROP TABLE #TempTableStageTest;
END
------------------------------------------------
----- Load Train_A data into stating table -----
------------------------------------------------
-- Create temporal Staging table for TrainA data
-- Declare variable to keep file path to load
CREATE TABLE #TempTableStageTest (
    ID nvarchar(5) NOT NULL,
	X_1 nvarchar(25) NULL,
	X_2 nvarchar(25) NULL,
	X_3 nvarchar(25) NULL,
	X_4 nvarchar(25) NULL,
	X_5 nvarchar(25) NULL,
	X_6 nvarchar(25) NULL,
	X_7 nvarchar(25) NULL,
	X_8 nvarchar(25) NULL,
	X_9 nvarchar(25) NULL,
	X_10 nvarchar(25) NULL,
	X_11 nvarchar(25) NULL,
	X_12 nvarchar(25) NULL,
	X_13 nvarchar(25) NULL,
	X_14 nvarchar(25) NULL,
	X_15 nvarchar(25) NULL,
	X_16 nvarchar(25) NULL,
	X_17 nvarchar(25) NULL,
	X_18 nvarchar(25) NULL,
	X_19 nvarchar(25) NULL,
	X_20 nvarchar(25) NULL,
	X_21 nvarchar(25) NULL,
	X_22 nvarchar(25) NULL,
	X_23 nvarchar(25) NULL,
	X_24 nvarchar(25) NULL,
	X_25 nvarchar(25) NULL,
	X_26 nvarchar(25) NULL,
	X_27 nvarchar(25) NULL,
	X_28 nvarchar(25) NULL,
	X_29 nvarchar(25) NULL,
	X_30 nvarchar(25) NULL
);
-- Select temporal table and do
EXEC sp_executesql @SQL;
-----------------------------------------------------
-- Move data to table with rigth columns datatypes --
-----------------------------------------------------
-- Create destination table [dbo].[t_data_train]
IF NOT EXISTS (
	SELECT * FROM INFORMATION_SCHEMA.TABLES
	WHERE TABLE_SCHEMA = 'dbo'
	AND TABLE_NAME = 't_data_test'
)
BEGIN
	CREATE TABLE [DANE_DB].[dbo].[t_data_test](
		[ID] [nvarchar](5) NOT NULL UNIQUE,
		[X_1] [decimal](20, 18) NULL,
		[X_2] [decimal](20, 18) NULL,
		[X_3] [decimal](20, 18) NULL,
		[X_4] [decimal](20, 18) NULL,
		[X_5] [decimal](20, 18) NULL,
		[X_6] [decimal](20, 18) NULL,
		[X_7] [decimal](20, 18) NULL,
		[X_8] [decimal](20, 18) NULL,
		[X_9] [decimal](20, 18) NULL,
		[X_10] [decimal](20, 18) NULL,
		[X_11] [decimal](20, 18) NULL,
		[X_12] [decimal](20, 18) NULL,
		[X_13] [decimal](20, 18) NULL,
		[X_14] [decimal](20, 18) NULL,
		[X_15] [decimal](20, 18) NULL,
		[X_16] [decimal](20, 18) NULL,
		[X_17] [decimal](20, 18) NULL,
		[X_18] [decimal](20, 18) NULL,
		[X_19] [decimal](20, 18) NULL,
		[X_20] [decimal](20, 18) NULL,
		[X_21] [decimal](20, 18) NULL,
		[X_22] [decimal](20, 18) NULL,
		[X_23] [decimal](20, 18) NULL,
		[X_24] [decimal](20, 18) NULL,
		[X_25] [decimal](20, 18) NULL,
		[X_26] [decimal](20, 18) NULL,
		[X_27] [decimal](20, 18) NULL,
		[X_28] [decimal](20, 18) NULL,
		[X_29] [decimal](20, 18) NULL,
		[X_30] [decimal](20, 18) NULL,
		[Y] [tinyint] NULL
	)
END;
-- COPY data from #TempTableStageTrain INTO [dbo].[t_data_test]
INSERT INTO [DANE_DB].[dbo].[t_data_test]
SELECT 
	ID,
	TRY_CONVERT(DECIMAL(20, 18), X_1) AS X_1,
	TRY_CONVERT(DECIMAL(20, 18), X_2) AS X_2,
	TRY_CONVERT(DECIMAL(20, 18), X_3) AS X_3,
	TRY_CONVERT(DECIMAL(20, 18), X_4) AS X_4,
	TRY_CONVERT(DECIMAL(20, 18), X_5) AS X_5,
	TRY_CONVERT(DECIMAL(20, 18), X_6) AS X_6,
	TRY_CONVERT(DECIMAL(20, 18), X_7) AS X_7,
	TRY_CONVERT(DECIMAL(20, 18), X_8) AS X_8,
	TRY_CONVERT(DECIMAL(20, 18), X_9) AS X_9,
	TRY_CONVERT(DECIMAL(20, 18), X_10) AS X_10,
	TRY_CONVERT(DECIMAL(20, 18), X_11) AS X_11,
	TRY_CONVERT(DECIMAL(20, 18), X_12) AS X_12,
	TRY_CONVERT(DECIMAL(20, 18), X_13) AS X_13,
	TRY_CONVERT(DECIMAL(20, 18), X_14) AS X_14,
	TRY_CONVERT(DECIMAL(20, 18), X_15) AS X_15,
	TRY_CONVERT(DECIMAL(20, 18), X_16) AS X_16,
	TRY_CONVERT(DECIMAL(20, 18), X_17) AS X_17,
	TRY_CONVERT(DECIMAL(20, 18), X_18) AS X_18,
	TRY_CONVERT(DECIMAL(20, 18), X_19) AS X_19,
	TRY_CONVERT(DECIMAL(20, 18), X_20) AS X_20,
	TRY_CONVERT(DECIMAL(20, 18), X_21) AS X_21,
	TRY_CONVERT(DECIMAL(20, 18), X_22) AS X_22,
	TRY_CONVERT(DECIMAL(20, 18), X_23) AS X_23,
	TRY_CONVERT(DECIMAL(20, 18), X_24) AS X_24,
	TRY_CONVERT(DECIMAL(20, 18), X_25) AS X_25,
	TRY_CONVERT(DECIMAL(20, 18), X_26) AS X_26,
	TRY_CONVERT(DECIMAL(20, 18), X_27) AS X_27,
	TRY_CONVERT(DECIMAL(20, 18), X_28) AS X_28,
	TRY_CONVERT(DECIMAL(20, 18), X_29) AS X_29,
	TRY_CONVERT(DECIMAL(20, 18), X_30) AS X_30,
	NULL
FROM #TempTableStageTest;

-- Visualize data
--SELECT * FROM [dbo].[t_data_test];

-- DROP Temporal tables
DROP TABLE #TempTableStageTest;