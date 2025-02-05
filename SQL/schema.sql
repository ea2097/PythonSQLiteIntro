-- Create Tables
CREATE TABLE IF NOT EXISTS Airports (
    airport_code VARCHAR(10) PRIMARY KEY,
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    timezone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Aircraft (
    tail_number VARCHAR(10) PRIMARY KEY,
    msn VARCHAR(20) NOT NULL UNIQUE,
    model VARCHAR(50),
    capacity INTEGER,
    manufacture_year INTEGER,
    last_maintenance_date DATE
);

CREATE TABLE IF NOT EXISTS Pilots (
    license_number VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    qualification VARCHAR(100),
    contact_number VARCHAR(20),
    date_of_birth DATE,
    hire_date DATE
);

CREATE TABLE IF NOT EXISTS Flights (
    flight_number VARCHAR(10) PRIMARY KEY,
    departure_airport VARCHAR(10),
    arrival_airport VARCHAR(10),
    aircraft_tail_number VARCHAR(10),
    pilot_license VARCHAR(50),
    scheduled_departure TIMESTAMP,
    scheduled_arrival TIMESTAMP,
    FOREIGN KEY (departure_airport) REFERENCES Airports(airport_code) ON DELETE RESTRICT,
    FOREIGN KEY (arrival_airport) REFERENCES Airports(airport_code) ON DELETE RESTRICT,
    FOREIGN KEY (aircraft_tail_number) REFERENCES Aircraft(tail_number) ON DELETE RESTRICT,
    FOREIGN KEY (pilot_license) REFERENCES Pilots(license_number) ON DELETE RESTRICT
);

-- Create Views
-- FlightsView includes original Flight columns with additional calculated columns
CREATE VIEW IF NOT EXISTS FlightsView AS
SELECT
    *,
    CASE
        WHEN strftime('%Y-%m-%d %H:%M:%S', scheduled_departure) > '2025-02-13 13:50:00' THEN 'Scheduled'
        WHEN strftime('%Y-%m-%d %H:%M:%S', scheduled_departure) <= '2025-02-13 13:50:00'
        AND strftime('%Y-%m-%d %H:%M:%S', scheduled_arrival) >= '2025-02-13 13:50:00' THEN 'In Progress'
        WHEN strftime('%Y-%m-%d %H:%M:%S', scheduled_arrival) < '2025-02-13 13:50:00' THEN 'Completed'
        ELSE 'Not Scheduled'
    END AS status,
    time(
        (
            julianday(scheduled_arrival) - julianday(scheduled_departure)
        ) * 24 * 3600,
        'unixepoch'
    ) AS duration
FROM
    Flights;

-- PilotsView includes original Pilots columns with additional calculated columns
CREATE VIEW IF NOT EXISTS PilotsView AS WITH AvgDOB AS (
    SELECT
        avg(julianday(date_of_birth)) AS avg_dob_julian
    FROM
        Pilots
    WHERE
        date_of_birth IS NOT NULL
        AND date_of_birth != ''
)
SELECT
    p.*,
    p.first_name || ' ' || p.last_name AS pilot_name,
    CASE
        WHEN p.date_of_birth IS NULL THEN 'Unknown'
        WHEN p.date_of_birth = '' THEN 'Unknown'
        WHEN julianday(p.date_of_birth) >= a.avg_dob_julian THEN 'Below Average'
        WHEN julianday(p.date_of_birth) < a.avg_dob_julian THEN 'Above Average'
    END AS age_group,
    CAST(
        (julianday('now') - julianday(p.hire_date)) / 365.25 AS INTEGER
    ) || 'y ' || CAST(
        (
            (julianday('now') - julianday(p.hire_date)) / 30.4375
        ) % 12 AS INTEGER
    ) || 'm' AS service_years
FROM
    Pilots p
    CROSS JOIN AvgDOB a;

-- FlattenedFlightsView includes FlightsView columns with additional columns from related tables
CREATE VIEW IF NOT EXISTS FlattenedFlightsView AS
SELECT
    f.flight_number,
    f.scheduled_departure AS dep_time,
    f.scheduled_arrival AS arr_time,
    f.status,
    f.duration,
    dep.airport_code AS dep_airport,
    dep.country AS dep_country,
    arr.airport_code AS arr_airport,
    arr.country AS arr_country,
    a.model AS aircraft_model,
    p.pilot_name
FROM
    FlightsView f
    LEFT JOIN Airports dep ON f.departure_airport = dep.airport_code
    LEFT JOIN Airports arr ON f.arrival_airport = arr.airport_code
    LEFT JOIN Aircraft a ON f.aircraft_tail_number = a.tail_number
    LEFT JOIN PilotsView p ON f.pilot_license = p.license_number;

-- FlattenedPilotsView includes PilotsView columns with additional columns from related tables
CREATE VIEW IF NOT EXISTS FlattenedPilotsView AS
SELECT
    p.*,
    COUNT(f.flight_number) AS assigned_flights
FROM
    PilotsView p
    LEFT JOIN Flights f ON p.license_number = f.pilot_license
GROUP BY
    p.license_number;

-- FlattenedAirportsView includes Airports columns with additional columns from related tables
CREATE VIEW IF NOT EXISTS FlattenedAirportsView AS
SELECT
    a.*,
    f.status AS flights_status,
    COUNT(f.flight_number) AS flights_count,
    GROUP_CONCAT(f.flight_number, ', ') AS flights
FROM
    Airports a
    LEFT JOIN FlightsView f ON a.airport_code = f.departure_airport
    OR a.airport_code = f.arrival_airport
GROUP BY
    a.airport_code,
    f.status;