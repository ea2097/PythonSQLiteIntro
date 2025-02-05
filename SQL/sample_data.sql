-- Insert Sample Data
INSERT INTO
    Airports (
        airport_code,
        airport_name,
        city,
        country,
        timezone
    )
VALUES
    (
        'JFK',
        'John F. Kennedy International',
        'New York',
        'USA',
        'UTC-05'
    ),
    (
        'LHR',
        'Heathrow Airport',
        'London',
        'UK',
        'UTC+00'
    ),
    (
        'DXB',
        'Dubai International',
        'Dubai',
        'UAE',
        'UTC+04'
    ),
    (
        'HND',
        'Haneda Airport',
        'Tokyo',
        'Japan',
        'UTC+09'
    ),
    (
        'CDG',
        'Charles de Gaulle Airport',
        'Paris',
        'France',
        'UTC+01'
    ),
    (
        'LAX',
        'Los Angeles International',
        'Los Angeles',
        'USA',
        'UTC-08'
    ),
    (
        'ORD',
        'OHare International',
        'Chicago',
        'USA',
        'UTC-06'
    ),
    (
        'ATL',
        'Hartsfield-Jackson Atlanta',
        'Atlanta',
        'USA',
        'UTC-05'
    ),
    (
        'PEK',
        'Beijing Capital',
        'Beijing',
        'China',
        'UTC+08'
    ),
    (
        'SYD',
        'Sydney Kingsford Smith',
        'Sydney',
        'Australia',
        'UTC+10'
    ),
    (
        'SIN',
        'Singapore Changi',
        'Singapore',
        'Singapore',
        'UTC+08'
    ),
    (
        'FRA',
        'Frankfurt Airport',
        'Frankfurt',
        'Germany',
        'UTC+01'
    ),
    (
        'HKG',
        'Hong Kong International',
        'Hong Kong',
        'China',
        'UTC+08'
    ),
    (
        'YYZ',
        'Toronto Pearson',
        'Toronto',
        'Canada',
        'UTC-05'
    ),
    (
        'MEX',
        'Mexico City International',
        'Mexico City',
        'Mexico',
        'UTC-06'
    ),
    (
        'AMS',
        'Schiphol Airport',
        'Amsterdam',
        'Netherlands',
        'UTC+01'
    ),
    (
        'ICN',
        'Incheon International',
        'Seoul',
        'South Korea',
        'UTC+09'
    ),
    (
        'GRU',
        'Sao Paulo-Guarulhos',
        'Sao Paulo',
        'Brazil',
        'UTC-03'
    ),
    (
        'BKK',
        'Suvarnabhumi Airport',
        'Bangkok',
        'Thailand',
        'UTC+07'
    ),
    (
        'DEL',
        'Indira Gandhi International',
        'New Delhi',
        'India',
        'UTC+05:30'
    ),
    (
        'CAI',
        NULL,
        NULL,
        NULL,
        NULL
    ) ON CONFLICT(airport_code) DO NOTHING;

INSERT INTO
    Aircrafts (
        tail_number,
        model,
        capacity,
        manufacture_year,
        last_maintenance_date
    )
VALUES
    (
        'N737AB',
        'Boeing 737',
        180,
        2015,
        '2023-06-10'
    ),
    (
        'D-AINA',
        'Airbus A320',
        160,
        2017,
        '2023-08-15'
    ),
    (
        'N777BC',
        'Boeing 777',
        350,
        2012,
        '2022-12-01'
    ),
    (
        'F-WXWB',
        'Airbus A350',
        366,
        2019,
        '2023-07-20'
    ),
    (
        'JA787A',
        'Boeing 787',
        296,
        2018,
        '2023-05-30'
    ),
    (
        'G-BNLA',
        'Boeing 747',
        400,
        2010,
        '2023-09-20'
    ),
    (
        'A6-APB',
        'Airbus A380',
        555,
        2016,
        '2023-10-10'
    ),
    (
        'PP-XMA',
        'Embraer E190',
        114,
        2018,
        '2023-11-15'
    ),
    (
        'N767CX',
        'Boeing 767',
        250,
        2013,
        '2023-07-05'
    ),
    (
        'TC-JKR',
        'Airbus A321',
        190,
        2019,
        '2023-06-22'
    ),
    (
        'N757PW',
        'Boeing 757',
        243,
        2014,
        '2023-05-14'
    ),
    (
        'D-AKNF',
        'Airbus A319',
        156,
        2012,
        '2023-04-30'
    ),
    (
        'C-FCRJ',
        'Bombardier CRJ900',
        90,
        2020,
        '2023-03-12'
    ),
    (
        'N737MX',
        'Boeing 737 MAX',
        172,
        2021,
        '2023-02-18'
    ),
    (
        'C-GSTA',
        'Airbus A220',
        140,
        2022,
        '2023-01-25'
    ),
    (
        'TEST',
        NULL,
        NULL,
        NULL,
        NULL
    ) ON CONFLICT(tail_number) DO NOTHING;

INSERT INTO
    Pilots (
        license_number,
        first_name,
        last_name,
        qualification,
        contact_number,
        date_of_birth,
        hire_date
    )
VALUES
    (
        'ATP12345USA',
        'John',
        'Doe',
        'Captain',
        '123456789',
        '1985-05-20',
        '2015-09-15'
    ),
    (
        'ATP67890USA',
        'Alice',
        'Smith',
        'First Officer',
        '987654321',
        '1990-07-11',
        '2020-03-25'
    ),
    (
        'ATP54321USA',
        'Mike',
        'Brown',
        'Captain',
        '555666777',
        '1982-09-30',
        '2010-06-12'
    ),
    (
        'ATP78901UK',
        'Sarah',
        'John',
        'First Officer',
        '111222333',
        '1995-03-15',
        '2022-07-19'
    ),
    (
        'ATP45678CAN',
        'David',
        'Will',
        'Captain',
        '333444555',
        '1988-08-21',
        '2018-11-10'
    ),
    (
        'ATP56789AUS',
        'Emma',
        'Taylor',
        'First Officer',
        '444555666',
        '1993-12-05',
        '2021-04-23'
    ),
    (
        'ATP67812NZ',
        'James',
        'Anderson',
        'Captain',
        '777888999',
        '1980-10-17',
        '2008-07-09'
    ),
    (
        'ATP78923ESP',
        'Olivia',
        'Martin',
        'First Officer',
        '666777888',
        '1997-06-28',
        '2023-05-30'
    ),
    (
        'ATP89034MEX',
        'Will',
        'Garcia',
        'Captain',
        '555666777',
        '1979-04-02',
        '2005-02-18'
    ),
    (
        'ATP90145BRA',
        'Sophia',
        'Lopez',
        'First Officer',
        '111222444',
        '1992-09-11',
        '2019-09-07'
    ),
    (
        'Test',
        'Best',
        'Mike',
        NULL,
        NULL,
        NULL,
        NULL
    ) ON CONFLICT(license_number) DO NOTHING;

INSERT INTO
    Flights (
        flight_number,
        departure_airport,
        arrival_airport,
        aircraft_tail_number,
        pilot_license,
        scheduled_departure,
        scheduled_arrival
    )
VALUES
    (
        'AA101',
        'JFK',
        'LHR',
        'N737AB',
        'ATP12345USA',
        '2025-02-05 08:00:00',
        '2025-02-05 20:00:00'
    ),
    (
        'BA202',
        'LHR',
        'DXB',
        'D-AINA',
        'ATP12345USA',
        '2025-02-06 10:00:00',
        '2025-02-06 22:00:00'
    ),
    (
        'EK303',
        'DXB',
        'HND',
        'N777BC',
        'ATP12345USA',
        '2025-02-07 14:00:00',
        '2025-02-08 06:00:00'
    ),
    (
        'AF404',
        'CDG',
        'JFK',
        'F-WXWB',
        'ATP67890USA',
        '2025-02-09 12:00:00',
        '2025-02-09 23:00:00'
    ),
    (
        'DL505',
        'LAX',
        'ATL',
        'JA787A',
        'ATP54321USA',
        '2025-02-10 09:00:00',
        '2025-02-10 17:00:00'
    ),
    (
        'SQ600',
        'SIN',
        'FRA',
        'G-BNLA',
        'ATP67890USA',
        '2025-02-11 08:00:00',
        '2025-02-11 18:00:00'
    ),
    (
        'LH707',
        'FRA',
        'HKG',
        'A6-APB',
        'ATP54321USA',
        '2025-02-12 09:30:00',
        '2025-02-12 22:15:00'
    ),
    (
        'CX888',
        'HKG',
        'YYZ',
        'PP-XMA',
        'ATP12345USA',
        '2025-02-13 12:00:00',
        '2025-02-13 23:45:00'
    ),
    (
        'AC725',
        'YYZ',
        'MEX',
        'N767CX',
        'ATP78901UK',
        '2025-02-14 14:15:00',
        '2025-02-14 19:30:00'
    ),
    (
        'AM901',
        'MEX',
        'AMS',
        'TC-JKR',
        'ATP67812NZ',
        '2025-02-15 07:50:00',
        '2025-02-15 18:20:00'
    ),
    (
        'KL852',
        'AMS',
        'ICN',
        'N737AB',
        'ATP56789AUS',
        '2025-02-16 10:00:00',
        '2025-02-16 22:50:00'
    ),
    (
        'KE907',
        'ICN',
        'GRU',
        'D-AINA',
        'ATP78923ESP',
        '2025-02-17 05:30:00',
        '2025-02-17 20:45:00'
    ),
    (
        'JJ809',
        'GRU',
        'BKK',
        'N777BC',
        'ATP89034MEX',
        '2025-02-18 11:15:00',
        '2025-02-18 23:30:00'
    ),
    (
        'TG321',
        'BKK',
        'DEL',
        'F-WXWB',
        'ATP78901UK',
        '2025-02-19 06:45:00',
        '2025-02-19 12:10:00'
    ),
    (
        'AI223',
        'DEL',
        'SIN',
        'JA787A',
        'ATP56789AUS',
        '2025-02-20 15:00:00',
        '2025-02-20 23:20:00'
    ),
    (
        'AA700',
        'JFK',
        'CDG',
        'G-BNLA',
        'ATP89034MEX',
        '2025-02-21 08:10:00',
        '2025-02-21 20:30:00'
    ),
    (
        'BA303',
        'LHR',
        'ORD',
        'A6-APB',
        'ATP54321USA',
        '2025-02-22 09:20:00',
        '2025-02-22 19:50:00'
    ),
    (
        'EK555',
        'DXB',
        'ATL',
        'PP-XMA',
        'ATP67890USA',
        '2025-02-23 14:40:00',
        '2025-02-23 23:55:00'
    ),
    (
        'JL789',
        'HND',
        'SYD',
        'N767CX',
        'ATP45678CAN',
        '2025-02-24 13:30:00',
        '2025-02-24 22:40:00'
    ),
    (
        'CA101',
        'PEK',
        'JFK',
        'TC-JKR',
        'ATP90145BRA',
        '2025-02-25 06:00:00',
        '2025-02-25 18:50:00'
    ),
    (
        'TEST',
        NULL,
        NULL,
        NULL,
        NULL,
        NULL,
        NULL
    ) ON CONFLICT(flight_number) DO NOTHING;