from flask import render_template, redirect, Flask
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("/WebInterfaceV2/dashboard.html")

@app.route("/devices")
def devices():
    return render_template("/WebInterfaceV2/devices.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)