import sqlite3

conn = sqlite3.connect("runs.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS runs (
        run_id INTEGER PRIMARY KEY AUTOINCREMENT,
        game_name TEXT,
        player_name TEXT,
        time_seconds INTEGER,
        video_url TEXT,
        submission_date TEXT,
        verified INTEGER
    )
""")

cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_game_verified
ON runs(game_name, verified)
""")

conn.commit()
conn.close()

print("Database initialized")