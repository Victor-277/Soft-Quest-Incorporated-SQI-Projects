CREATE DATABASE chinook;
USE chinook;

-- Artist
CREATE TABLE Artist (
    ArtistId INT PRIMARY KEY,
    Name VARCHAR(255)
);

-- Album
CREATE TABLE Album (
    AlbumId INT PRIMARY KEY,
    Title VARCHAR(255),
    ArtistId INT,
    FOREIGN KEY (ArtistId) REFERENCES Artist(ArtistId)
);

-- Customer
CREATE TABLE Customer (
    CustomerId INT PRIMARY KEY,
    FirstName VARCHAR(255),
    LastName VARCHAR(255),
    Company VARCHAR(255),
    Address VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    Country VARCHAR(255),
    PostalCode VARCHAR(255),
    Phone VARCHAR(255),
    Fax VARCHAR(255),
    Email VARCHAR(255),
    SupportRepId INT
);

-- Employee
CREATE TABLE Employee (
    EmployeeId INT PRIMARY KEY,
    LastName VARCHAR(255),
    FirstName VARCHAR(255),
    Title VARCHAR(255),
    ReportsTo INT,
    BirthDate DATETIME,
    HireDate DATETIME,
    Address VARCHAR(255),
    City VARCHAR(255),
    State VARCHAR(255),
    Country VARCHAR(255),
    PostalCode VARCHAR(255),
    Phone VARCHAR(255),
    Fax VARCHAR(255),
    Email VARCHAR(255)
);

-- Genre
CREATE TABLE Genre (
    GenreId INT PRIMARY KEY,
    Name VARCHAR(255)
);

-- Invoice
CREATE TABLE Invoice (
    InvoiceId INT PRIMARY KEY,
    CustomerId INT,
    InvoiceDate DATETIME,
    BillingAddress VARCHAR(255),
    BillingCity VARCHAR(255),
    BillingState VARCHAR(255),
    BillingCountry VARCHAR(255),
    BillingPostalCode VARCHAR(255),
    Total DECIMAL(10,2),
    FOREIGN KEY (CustomerId) REFERENCES Customer(CustomerId)
);

-- InvoiceLine
CREATE TABLE InvoiceLine (
    InvoiceLineId INT PRIMARY KEY,
    InvoiceId INT,
    TrackId INT,
    UnitPrice DECIMAL(10,2),
    Quantity INT,
    FOREIGN KEY (InvoiceId) REFERENCES Invoice(InvoiceId)
);

-- MediaType
CREATE TABLE MediaType (
    MediaTypeId INT PRIMARY KEY,
    Name VARCHAR(255)
);

-- Playlist
CREATE TABLE Playlist (
    PlaylistId INT PRIMARY KEY,
    Name VARCHAR(255)
);

-- Track
CREATE TABLE Track (
    TrackId INT PRIMARY KEY,
    Name VARCHAR(255),
    AlbumId INT,
    MediaTypeId INT,
    GenreId INT,
    Composer VARCHAR(255),
    Milliseconds INT,
    Bytes INT,
    UnitPrice DECIMAL(10,2),
    FOREIGN KEY (AlbumId) REFERENCES Album(AlbumId),
    FOREIGN KEY (MediaTypeId) REFERENCES MediaType(MediaTypeId),
    FOREIGN KEY (GenreId) REFERENCES Genre(GenreId)
);

-- PlaylistTrack
CREATE TABLE PlaylistTrack (
    PlaylistId INT,
    TrackId INT,
    PRIMARY KEY (PlaylistId, TrackId),
    FOREIGN KEY (PlaylistId) REFERENCES Playlist(PlaylistId),
    FOREIGN KEY (TrackId) REFERENCES Track(TrackId)
);
