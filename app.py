from flask import Flask
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = get_db_connection()
    all_runs = conn.execute("SELECT * FROM runs").fetchall() # Creates implicit cursor fetch all rows
    conn.close()

    output = "<h1> Speedrun Leaderboard</h1>"

    for run in all_runs:
        output += f"""
            <p>
            {run['game_name']} | {run['player_name']} | {run['time_seconds']} sec | {run['video_url']} | {run['submission_date']} | {run['verified']}
            </p>
        """

    return output
@app.route("/about")
def about():
    return """
    <h1>About </h1>
    <h2> Here's some info about this website! </h2>
    """

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