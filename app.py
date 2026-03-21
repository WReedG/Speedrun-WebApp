from flask import Flask, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    conn = get_db_connection()
    all_runs = conn.execute("SELECT * FROM runs").fetchall() # Creates implicit cursor fetch all rows
    conn.close()

    output = "<h1> Speedrun Leaderboard</h1><p></p>"
    output += """<p> Submit a run <a href="/add">here!</a></p> """

    for run in all_runs:
        output += f"""
            <p>
            {run['game_name']} | {run['player_name']} | {run['time_seconds']} sec | 
            <a href="https:{run['video_url']}" target="_blank">Video</a> | {run['submission_date']} | {run['verified']}
            </p>
        """

    return output

@app.route("/add", methods=["GET", "POST"])
def add_run():
    if request.method == "GET":
        output = """
        <form action="/add" method="POST">
        <label for="game_name">Game Name:</label>
        <input type="text" name="game_name" id="game_name"><br><br>
        <label for="player_name">Player Username:</label>
        <input type="text" name="player_name" id="player_name"><br><br>
        <label for="time_seconds">Time (in seconds):</label>
        <input type="text" name="time_seconds" id="time_seconds"><br><br>
        <label for="video_url">Video Link:</label>
        <input type="text" name="video_url" id="video_url"><br><br>
        <input type="submit" value="Submit">
        </form>
        <p>Click <a href="/">here</a> to return to the main page. </p>
        """
        return output
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "INSERT INTO runs (game_name, player_name, time_seconds, video_url, submission_date, verified) VALUES (?, ?, ?, ?, ?, ?)"
        cur_date = datetime.now().strftime("%m/%d/%Y")
        data = (request.form.get("game_name"), request.form.get("player_name"), int(request.form.get("time_seconds")),
                request.form.get("video_url"), cur_date, "False")
        cursor.execute(query, data)
        conn.commit()
        conn.close()
        output = "<p>Run submitted! Thank you for submitting a run, please return to the home page to view it.</p>"
        output += """<p> Click <a href="/">here</a> to return to the main page! </p>"""
        return output

@app.route("/<name>")
def hello_name(name):
    return f"""
    <h1> Hello, {name}!</h1>
    <p> You seem to be somewhere you shouldn't, return to the main page. </p>
    """

 # Helper funtion to create a connection to the main db.
def get_db_connection():
    conn = sqlite3.connect("runs.db")
    conn.row_factory = sqlite3.Row # Allows columns to be accessed by either name or index
    return conn

if __name__ == "__main__":
    app.run(debug=True)