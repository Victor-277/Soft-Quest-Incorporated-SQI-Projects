-- Extend the previous query to show these values for all stations in the years 2010 to 2022.
USE pollution_db2;
SELECT Location AS StationName, AVG(PM2_5) AS MeanPM2_5, AVG(VPM2_5) AS MeanVPM2_5 FROM measurement
	WHERE DateTime >= '2010-01-01' AND DateTime < '2023-01-01' AND HOUR(DateTime) = 8 GROUP BY Location;