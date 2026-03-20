from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return """
    <h1>Hello, World!</h1>
    <p> This is a paragraph using html. </p>
    """
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


if __name__ == "__main__":
    app.run(debug=True)