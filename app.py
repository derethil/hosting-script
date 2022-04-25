from flask import Flask
app = Flask(__name__)

@app.route("/")
def index():
  return "<html><body><h1>Hello, world!</h1></body></html>"

if __name__ == "__main__":
  app.run(host='0.0.0.0',debug=True)