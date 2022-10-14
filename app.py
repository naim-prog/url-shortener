from hashlib import sha512
from urllib import request
from flask import Flask, redirect, render_template, request, flash
import secrets, os, json

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
BASE_DIR = os.getcwd()

@app.route("/")
def home():
    # No hay url_key en el URL
    if not request.args.get('url_key'):
        # redirigir a shortner
        return redirect("/shortner/")

    # Abrir el fichero
    url_json = dict(json.loads(open(os.path.join(BASE_DIR, "urls.json"), "r", encoding='utf-8').read()))

    url_key_user = request.args.get('url_key')

    redirect_url = url_json.get(url_key_user)

    # No está el url
    if not redirect_url: 
        flash("Your URL is not shorted")
        return redirect("/shortner/")

    # Redirigir a la url
    return redirect(redirect_url)
    

@app.get("/shortner/")
def shortner_get():
    return render_template('shortner-get.html')


@app.post("/shortner/")
def shortner_post():
    # No ha introducido URL
    if not request.form.get('url'):
        flash("Introduce una URL")
        return redirect("/shortner/")
    
    url_req = request.form.get('url')

    if not url_req.startswith('http'):
        url_req = 'https://' + url_req

    redirect_url_sha = sha512(url_req.encode('utf-8')).hexdigest()

    data = json.load(open("urls.json", "r"))

    data[redirect_url_sha] = url_req

    json.dump(data, open("urls.json", "w"), indent=4)

    return render_template('shortner-post.html', redirect_url = f"/?url_key={redirect_url_sha}")


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
