import sqlite3

# Connect to SQLite database
conn = sqlite3.connect("FlightManagement.db")
cur = conn.cursor()

# Create Tables
cur.execute(
    """
CREATE TABLE IF NOT EXISTS Airports (
    airport_code VARCHAR(10) PRIMARY KEY,
    airport_name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL,
    timezone VARCHAR(50)
);
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS Aircraft (
    aircraft_id VARCHAR(20) PRIMARY KEY,
    model VARCHAR(50) NOT NULL,
    capacity INTEGER NOT NULL,
    manufacture_year INTEGER,
    last_maintenance_date DATE
);
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS Pilots (
    pilot_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    license_number VARCHAR(50) UNIQUE NOT NULL,
    qualification VARCHAR(100),
    contact_number VARCHAR(20),
    date_of_birth DATE,
    hire_date DATE
);
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS Flights (
    flight_id VARCHAR(20) PRIMARY KEY,
    departure_airport VARCHAR(10) NOT NULL,
    arrival_airport VARCHAR(10) NOT NULL,
    aircraft_id VARCHAR(20),
    flight_number VARCHAR(10) NOT NULL,
    scheduled_departure TIMESTAMP NOT NULL,
    scheduled_arrival TIMESTAMP NOT NULL,
    FOREIGN KEY (departure_airport) REFERENCES Airports(airport_code),
    FOREIGN KEY (arrival_airport) REFERENCES Airports(airport_code),
    FOREIGN KEY (aircraft_id) REFERENCES Aircraft(aircraft_id)
);
"""
)

cur.execute(
    """
CREATE TABLE IF NOT EXISTS PilotSchedules (
    schedule_id VARCHAR(20) PRIMARY KEY,
    flight_id VARCHAR(20) NOT NULL,
    pilot_id VARCHAR(20) NOT NULL,
    duty_start TIMESTAMP NOT NULL,
    duty_end TIMESTAMP NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES Flights(flight_id),
    FOREIGN KEY (pilot_id) REFERENCES Pilots(pilot_id)
);
"""
)

# Insert Sample Data
cur.executemany(
    """
INSERT INTO Airports VALUES ("airport_code", "airport_name", "city", "country", "timezone")
""",
    [
        ("JFK", "John F. Kennedy International", "New York", "USA", "EST"),
        ("LHR", "Heathrow Airport", "London", "UK", "GMT"),
        ("DXB", "Dubai International", "Dubai", "UAE", "GST"),
        ("HND", "Haneda Airport", "Tokyo", "Japan", "JST"),
        ("CDG", "Charles de Gaulle Airport", "Paris", "France", "CET"),
        ("LAX", "Los Angeles International", "Los Angeles", "USA", "PST"),
        ("ORD", "O'Hare International", "Chicago", "USA", "CST"),
        ("ATL", "Hartsfield-Jackson Atlanta", "Atlanta", "USA", "EST"),
        ("PEK", "Beijing Capital", "Beijing", "China", "CST"),
        ("SYD", "Sydney Kingsford Smith", "Sydney", "Australia", "AEST"),
    ],
)

cur.executemany(
    """
INSERT INTO Aircraft VALUES (?, ?, ?, ?, ?)
""",
    [
        ("A100", "Boeing 737", 180, 2015, "2023-06-10"),
        ("A200", "Airbus A320", 160, 2017, "2023-08-15"),
        ("A300", "Boeing 777", 350, 2012, "2022-12-01"),
        ("A400", "Airbus A350", 366, 2019, "2023-07-20"),
        ("A500", "Boeing 787", 296, 2018, "2023-05-30"),
    ],
)

cur.executemany(
    """
INSERT INTO Pilots VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""",
    [
        (
            "P001",
            "John",
            "Doe",
            "LN12345",
            "Captain",
            "123456789",
            "1975-05-20",
            "2005-09-15",
        ),
        (
            "P002",
            "Alice",
            "Smith",
            "LN67890",
            "First Officer",
            "987654321",
            "1980-07-11",
            "2010-03-25",
        ),
        (
            "P003",
            "Michael",
            "Brown",
            "LN54321",
            "Captain",
            "555666777",
            "1972-09-30",
            "2000-06-12",
        ),
        (
            "P004",
            "Sarah",
            "Johnson",
            "LN78901",
            "First Officer",
            "111222333",
            "1985-03-15",
            "2012-07-19",
        ),
    ],
)

cur.executemany(
    """
INSERT INTO Flights VALUES (?, ?, ?, ?, ?, ?, ?)
""",
    [
        (
            "F001",
            "JFK",
            "LHR",
            "A100",
            "AA101",
            "2024-02-05 08:00:00",
            "2024-02-05 20:00:00",
        ),
        (
            "F002",
            "LHR",
            "DXB",
            "A200",
            "BA202",
            "2024-02-06 10:00:00",
            "2024-02-06 22:00:00",
        ),
        (
            "F003",
            "DXB",
            "HND",
            "A300",
            "EK303",
            "2024-02-07 14:00:00",
            "2024-02-08 06:00:00",
        ),
        (
            "F004",
            "CDG",
            "JFK",
            "A400",
            "AF404",
            "2024-02-09 12:00:00",
            "2024-02-09 23:00:00",
        ),
        (
            "F005",
            "LAX",
            "ATL",
            "A500",
            "DL505",
            "2024-02-10 09:00:00",
            "2024-02-10 17:00:00",
        ),
    ],
)

cur.executemany(
    """
INSERT INTO PilotSchedules VALUES (?, ?, ?, ?, ?)
""",
    [
        ("S001", "F001", "P001", "2024-02-05 07:00:00", "2024-02-05 21:00:00"),
        ("S002", "F002", "P002", "2024-02-06 09:00:00", "2024-02-06 23:00:00"),
        ("S003", "F003", "P003", "2024-02-07 13:00:00", "2024-02-08 07:00:00"),
        ("S004", "F004", "P004", "2024-02-09 11:00:00", "2024-02-09 23:59:00"),
    ],
)

# Commit changes and close connection
conn.commit()
conn.close()
