from flask import Flask, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
  <title>Synthia</title>
  <style>
    body { font-family: sans-serif; padding: 2em; background: #111; color: #eee; }
    h1 { color: #00e676; }
  </style>
</head>
<body>
  <h1>Welcome to Synthia 👋</h1>
  <p>This is your personal AI assistant running inside Home Assistant.</p>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8099)
