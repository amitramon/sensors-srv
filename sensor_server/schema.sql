DROP TABLE IF EXISTS sensor;

CREATE TABLE sensor (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sensor_id INTEGER NOT NULL,
  reading_type TEXT NOT NULL,
  value REAL NOT NULL,
  read_time REAL NOT NULL
);
