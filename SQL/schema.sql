CREATE TABLE IF NOT EXISTS Airports (
    airport_code VARCHAR(10) PRIMARY KEY NOT NULL CHECK(LENGTH(airport_code) = 3),
    airport_name VARCHAR(100),
    city VARCHAR(50),
    country VARCHAR(50),
    timezone VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS Aircrafts (
    tail_number VARCHAR(10) PRIMARY KEY NOT NULL CHECK(LENGTH(tail_number) > 0),
    model VARCHAR(50),
    capacity INTEGER,
    manufacture_year INTEGER,
    last_maintenance_date DATE
);

CREATE TABLE IF NOT EXISTS Pilots (
    license_number VARCHAR(50) PRIMARY KEY NOT NULL CHECK(LENGTH(license_number) > 0),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    qualification VARCHAR(100),
    contact_number VARCHAR(20),
    date_of_birth DATE,
    hire_date DATE
);

CREATE TABLE IF NOT EXISTS Flights (
    flight_number VARCHAR(10) PRIMARY KEY NOT NULL CHECK(LENGTH(flight_number) > 0),
    departure_airport VARCHAR(10),
    arrival_airport VARCHAR(10),
    aircraft_tail_number VARCHAR(10),
    pilot_license VARCHAR(50),
    scheduled_departure TIMESTAMP,
    scheduled_arrival TIMESTAMP,
    FOREIGN KEY (departure_airport) REFERENCES Airports(airport_code) ON DELETE RESTRICT,
    FOREIGN KEY (arrival_airport) REFERENCES Airports(airport_code) ON DELETE RESTRICT,
    FOREIGN KEY (aircraft_tail_number) REFERENCES Aircrafts(tail_number) ON DELETE RESTRICT,
    FOREIGN KEY (pilot_license) REFERENCES Pilots(license_number) ON DELETE RESTRICT
);