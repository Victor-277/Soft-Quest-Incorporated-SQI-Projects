-- Return the mean values of PM2.5 (particulate matter <2.5 micron diameter) & VPM2.5 
-- (volatile particulate matter <2.5 micron diameter) by each station for the year 2019 
--  for readings taken at 08:00 hours (peak traffic intensity).
USE pollution_db2;
SELECT Location as StationName, AVG(PM2_5) AS MeanPM2_5, AVG(VPM2_5) AS MeanVPM2_5 FROM measurement
WHERE DateTime >= '2019-01-01' AND DateTime < '2020-01-01' AND HOUR(DateTime) = 8 GROUP BY Location;