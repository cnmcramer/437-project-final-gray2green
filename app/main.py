from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/services")
def services_page():
    return render_template("services.html")

@app.route("/gallery")
def gallery_page():
    return render_template("gallery.html")

@app.route("/quote")
def quote_page():
    return render_template("quote.html")

@app.route("/contact")
def contact_page():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
