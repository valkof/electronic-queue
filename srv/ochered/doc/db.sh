sqlite3 eq01.db "
CREATE TABLE IF NOT EXISTS ticket(
   queue_id INT,
   tick_id INT NOT NULL,
   tick_name TEXT,
   kiosk_id INT,
   tick_kiosk TIMESTAMP,
   tick_start TIMESTAMP,
   tick_stop TIMESTAMP,
   place_id INT
);
"
