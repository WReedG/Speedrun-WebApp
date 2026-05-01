import sqlite3
from datetime import datetime

conn = sqlite3.connect('runs.db')
cursor = conn.cursor()

query = """
INSERT INTO runs (game_name, player_name, time_seconds, video_url, submission_date, verified)
VALUES (?, ?, ?, ?, ?, ?)
"""

today = datetime.today().strftime("%m/%d/%Y")

sample_runs = [
    ("Minecraft", "Player1", 500, "https://www.twitch.tv/videos/2637822778", today, 1),
    ("Minecraft", "Player2", 650, "https://www.youtube.com/watch?v=rVs0EdiVefM", today, 0),
    ("Celeste", "Speedster", 300, "https://www.youtube.com/watch?v=b43KAaem61g", today, 1),
    ("Celeste", "RunnerX", 450, "https://www.youtube.com/watch?v=hoofTLBaTE8", today, 0),
    ("Hades", "FastGuy", 700, "https://www.youtube.com/watch?v=srG2gEikKu4", today, 1),
    ("Hades II", "FastGuy", 850, "https://www.youtube.com/watch?v=cpGZA4UtbNU", today, 1)
]

cursor.execute("DELETE FROM runs")
cursor.executemany(query, sample_runs)

conn.commit()
conn.close()