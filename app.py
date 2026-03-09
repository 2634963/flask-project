import flask

app = flask.Flask(__name__)

@app.route("/")
@app.route("/index.html")
def mainPage():
    return """\
<!doctype html>
<head>
    <title>
        Hello, World!
    </title>
</head>
<body>
    <p>
        Hello from Flask!
    </p>
</body>"""
