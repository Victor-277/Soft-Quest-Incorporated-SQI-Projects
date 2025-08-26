-- Return the date/time, station name and the highest recorded 
-- value of nitrogen oxide (NOx) found in the dataset for the year 2022.
USE pollution_db2;
SET SQL_SAFE_UPDATES = 0;
UPDATE measurement SET DateTime = STR_TO_DATE(DateTime, '%Y-%m-%d %H:%i:%s');
SET SQL_SAFE_UPDATES = 1;
SELECT DateTime, Location AS StationName, NOx AS HighestNOx FROM measurement WHERE DateTime >= '2022-01-01' AND
 DateTime < '2023-01-01' ORDER BY NOx DESC LIMIT 1;
