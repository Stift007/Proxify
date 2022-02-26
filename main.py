
from react.app import ReactApp, ReactBuiltinServer, render_template, secure_html
from flask import flash, redirect, request
import requests

app = ReactBuiltinServer(__name__)
app.config["SECRET_KEY"] = "E"
react = ReactApp(app)

@react.component()
def searchengine(props):
    return """
    <form action="/proxify" method="POST">
            
        <div class="mb-3">
            <label for="query" class="form-label">Search Query</label>
            <input type="text" class="form-control" id="query" name="query" aria-describedby="emailHelp">
            <div id="emailHelp" class="form-text">We'll never share your search Queries with anyone else.</div>
        </div>
        
        <button type="submit" class="btn btn-primary">Submit</button>
    </form>
    """

@app.route("/")
def main():
    return render_template("index.html",react)

@app.route("/proxify", methods=["GET","POST"])
def proxifier():
    print(request.form)
    url = request.form.get("query","https://google.com")
    return redirect(f"/localproxy?url={url}")

@app.route("/localproxy")
def prx():
    try:
        url = request.args.get("url")
        r = requests.get(url)
        page = r.text.replace(f'"{url}',f'"http://127.0.0.1:5000/localproxy?url={url}').replace('"/',f'"http://127.0.0.1:5000/localproxy?url={url}/')
        return page
    except Exception as error:
        flash(error)
        return redirect("/")
app.run(debug=True)
    