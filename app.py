from flask import Flask, request, redirect, url_for
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
        verified = None
        if run['verified']:
            verified = "&#x2705;"
        else:
            verified = "&#x274C;"

        output += f"""
            <div>
            {run['game_name']} |
            {run['player_name']} |
            {run['time_seconds']} sec | 
            <a href="{run['video_url']}" target="_blank">Video</a> |
            {run['submission_date']} |
            {verified} |
            <form action="/delete/{run['run_id']}" method="POST" style="display: inline;">
                <button type="submit">Delete</button>
            </form> |
            <a href="/edit/{run['run_id']}">Edit</a>
            </div>
        """

    return output

@app.route("/add", methods=["GET", "POST"])
def add_run():
    if request.method == "GET":
        # HTML form to allow user's to submit information for a run
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
        # Confirmation message for a submitted run
        conn = get_db_connection()
        cursor = conn.cursor()
        query = ("INSERT INTO runs (game_name, player_name, time_seconds, video_url, submission_date, verified) "
                 "VALUES (?, ?, ?, ?, ?, ?)")
        cur_date = datetime.now().strftime("%m/%d/%Y")
        video_url = request.form.get("video_url")
        if not video_url.startswith(("http://", "https://")):
            video_url = "https://" + video_url
        data = (
            request.form.get("game_name"),
            request.form.get("player_name"),
            int(request.form.get("time_seconds")),
            video_url,
            cur_date,
            0
        )
        cursor.execute(query, data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

@app.route("/delete/<int:run_id>", methods=["POST"])
def delete_run(run_id):
    # Delete the corresponding id that was input to the form
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM runs WHERE run_id = ?", (run_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route("/edit/<int:run_id>", methods=["GET", "POST"])
def edit_run(run_id):
    if request.method == "GET":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM runs WHERE run_id = ?", (run_id,))
        data = cursor.fetchone()
        conn.close()
        checkmark = "checked" if data['verified'] else ""
        output = f"""
            <form action="/edit/{run_id}" method="POST">
                <label for="game_name">Game Name:</label>
                <input type="text" name="game_name" id="game_name" value="{data['game_name']}"><br><br>

                <label for="player_name">Player Username:</label>
                <input type="text" name="player_name" id="player_name" value="{data['player_name']}"><br><br>

                <label for="time_seconds">Time (in seconds):</label>
                <input type="text" name="time_seconds" id="time_seconds" value="{data['time_seconds']}"><br><br>

                <label for="video_url">Video Link:</label>
                <input type="text" name="video_url" id="video_url" value="{data['video_url']}"><br><br>
                
                <label for="verified">Verified Run:</label>
                <input type="checkbox" name="verified" id="verified" {checkmark}><br><br>

                <input type="submit" value="Submit">
            </form>
            <p>Click <a href="/">here</a> to return to the main page. </p>
        """
        return output
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
        UPDATE runs 
        SET game_name = ?, player_name = ?, time_seconds = ?, video_url = ? , verified = ?
        WHERE run_id = ?
        """
        video_url = request.form.get("video_url")
        if not video_url.startswith(("http://", "https://")):
            video_url = "https://" + video_url
        if request.form.get("verified") is not None:
            verified = 1
        else:
            verified = 0

        data = (
            request.form.get("game_name"),
            request.form.get("player_name"),
            int(request.form.get("time_seconds")),
            video_url,
            verified,
            run_id
        )
        cursor.execute(query, data)
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

 # Helper funtion to create a connection to the main db.
def get_db_connection():
    conn = sqlite3.connect("runs.db")
    conn.row_factory = sqlite3.Row # Allows columns to be accessed by either name or index
    return conn

if __name__ == "__main__":
    app.run(debug=True)