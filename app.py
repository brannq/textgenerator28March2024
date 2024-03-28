# !pip install flask
# !pip install textblob
import google.generativeai as palm
from flask import Flask, request, render_template, redirect, url_for


palm.configure(api_key= "AIzaSyDQcl6y7PITgoWesNf2w0fDHv43v01NxYg")
# os.getenvironment to hide API key from public

model = {
    "model":"models/chat-bison-001",
}
name = ""
flag = 1
#%%

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    global name, flag
    if flag == 1:
        name = request.form.get("q")
        flag = 0
    return render_template("main.html", r=name)

@app.route("/text", methods=["GET", "POST"])
def text():
    return render_template("text.html")

@app.route("/text_generator", methods=["GET", "POST"])
def text_generator():
    if request.method == "POST":
        q = request.form.get("q")
        if q:
            # Assuming palm.chat requires messages as a list
            r = palm.chat(**model, messages=[q])
            return render_template("text_generator.html", r=r.last)
        else:
            # Handle case where input message is missing
            error_message = "Input message is missing."
            return render_template("error.html", error_message=error_message)
    else:
        # Handle GET requests to /text_generator
        return redirect(url_for("index"))

@app.route("/end", methods=["GET", "POST"])
def end():
    print("ending process....")
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
