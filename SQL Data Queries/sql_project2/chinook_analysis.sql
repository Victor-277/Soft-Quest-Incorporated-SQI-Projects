-- 1. Top-Selling Products
SELECT t.Name AS Product, SUM(il.Quantity) AS Total_Units_Sold, SUM(il.UnitPrice * il.Quantity) AS Total_Revenue
FROM InvoiceLine il JOIN Track t ON il.TrackId = t.TrackId GROUP BY t.TrackId ORDER BY Total_Units_Sold DESC
LIMIT 10;

-- 2. Revenue by Country
SELECT c.Country, ROUND(SUM(i.Total), 2) AS Revenue FROM Invoice i JOIN Customer c ON i.CustomerId = c.CustomerId
GROUP BY c.Country ORDER BY Revenue DESC;

-- 3. Monthly Revenue Performance
SELECT DATE_FORMAT(i.InvoiceDate, '%Y-%m') AS Month, ROUND(SUM(i.Total), 2) AS Monthly_Revenue
FROM Invoice i GROUP BY Month ORDER BY Month;

-- 4. Top Customers by Total Spending
SELECT  CONCAT(c.FirstName, ' ', c.LastName) AS Customer, c.Country, ROUND(SUM(i.Total), 2) AS Total_Spent
FROM Customer c JOIN  Invoice i ON c.CustomerId = i.CustomerId
GROUP BY  c.CustomerId ORDER BY  Total_Spent DESC LIMIT 10;

-- 5. Most Popular Music Genres Sold
SELECT g.Name AS Genre, COUNT(il.InvoiceLineId) AS Total_Tracks_Sold
FROM InvoiceLine il JOIN Track t ON il.TrackId = t.TrackId
JOIN  Genre g ON t.GenreId = g.GenreId GROUP BY g.GenreId
ORDER BY Total_Tracks_Sold DESC;

-- 6. Latest Purchased Tracks with Customer Info
SELECT c.FirstName, c.LastName, t.Name AS Track, il.UnitPrice, il.Quantity, i.InvoiceDate
FROM Customer c JOIN nvoice i ON c.CustomerId = i.CustomerId
JOIN  InvoiceLine il ON i.InvoiceId = il.InvoiceId JOIN Track t ON il.TrackId = t.TrackId
ORDER BY i.InvoiceDate DESC LIMIT 20;

-- 7. Top-Selling Tracks by Genre (using RANK window function)
SELECT g.Name AS Genre,t.Name AS Track, SUM(il.Quantity) AS Total_Units_Sold,
RANK() OVER (PARTITION BY g.GenreId ORDER BY SUM(il.Quantity) DESC) AS TrackRank
FROM InvoiceLine il JOIN Track t ON il.TrackId = t.TrackId
JOIN Genre g ON t.GenreId = g.GenreId
GROUP BY g.GenreId, g.Name, t.TrackId, t.Name
ORDER BY g.Name, TrackRank;
