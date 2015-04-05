CREATE USER 'web'@'localhost';
GRANT INSERT, SELECT ON theremometer.temperature_readings TO 'web'@'localhost';
