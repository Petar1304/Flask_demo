from flask import Flask, render_template, request, url_for, make_response, session, redirect

app = Flask(__name__)
app.secret_key = b"\x86\xcd\x08@\x8bv6K\x0bmol\xa1\xcb\xae'91^G\xdan\x9c\xce"
# generate secret key with os.urandom(24)


@app.route('/home')
def home():
  return render_template('home.html')


@app.route('/search')
def search():
  vrsta = request.args.get('vrsta', 'svi proizvodi')
  max_cena = request.args.get('max_cena', float('inf'), type=float)
  return render_template("search.html", vrsta=vrsta, max_cena=max_cena)
# http://localhost:8080/search?vrsta=tv&max_cena=300


@app.route('/table')
def table():
  n = request.args.get("n", 0, type=int)
  return render_template("table.html", n=n)


@app.route('/sum')
def sum():
  num1 = request.args.get('num1', 0, float)
  num2 = request.args.get('num2', 0, float)
  try:
    sum = float(num1) + float(num2)
  except:
    sum = None
  return render_template("sum.html", sum=sum)


@app.route('/pizza')
def pizza():
  if "naruci" in request.args:
        # print(request.args)
        ime = request.args.get("ime")
        adresa = request.args.get("adresa")
        vrsta = request.args.get("vrsta")
        velicina = request.args.get("velicina")
        dodaci = []
        if "kecap" in request.args:
            dodaci.append(request.args.get("kecap"))
        if "origano" in request.args:
            dodaci.append(request.args.get("origano"))
            
        return render_template("narudzbina.html", ime=ime,
                               adresa=adresa, vrsta=vrsta,
                               velicina=velicina, dodaci=dodaci)
  else:
    return render_template("formular.html")


# POST metoda
@app.route('/post_request', methods=['GET', 'POST'])
def post():
  if request.method == "POST":
    name = request.form.get('name')
  if request.method == "GET":
    name = request.args.get('name')


# putanja sa parametrima
@app.route("/pozdrav/<ime>")
def pozdravi(ime):
    return f'<h2>Pozdrav { ime }</h2>'


# SESSION
@app.route('/session')
def session_page():
  if 'username' in session:
    print(session)
    username = session['username']
    return render_template("session.html", username=username)
  else:
    return render_template("session.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    session['username'] = request.form.get('username')
   #  session['username'] = request.form['username']
  return redirect(url_for('session_page'))

@app.route('/logout')
def logout():
  session.pop('username', None)
  return redirect(url_for("session_page"))


# COOKIE
@app.route('/cookie')
def cookie_page():
  if 'name' in request.cookies:
    name = request.cookies.get('name')
    return render_template("cookie.html", name=name)
  else:
    return render_template('cookie.html')


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
  if request.method == 'POST':
    name = request.form.get('name')
    response = make_response(redirect( url_for('cookie_page') ))
    response.set_cookie('name', name)
    return response


@app.route('/resetcookie')
def resetcookie():
  response = make_response(redirect(url_for('cookie_page')))
  response.set_cookie('name', '', expires=0)
  return response


# RUN APP
if __name__ == '__main__':
  app.run(debug=True, port=8080)







