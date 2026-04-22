import sqlite3
from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "supersecreto123"

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

def crear_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    correo TEXT UNIQUE,
    password TEXT,
    rol TEXT DEFAULT 'cliente'
)
    """)

    con.commit()
    con.close()

crear_db()

productos = [
    {"id":1,"nombre":"iPhone 14","precio":4200000,"imagen":"https://m.media-amazon.com/images/I/61cwywLZR-L._AC_SL1500_.jpg","categoria":"Celulares"},
    {"id":2,"nombre":"Samsung Galaxy S23","precio":3500000,"imagen":"https://m.media-amazon.com/images/I/71OXmy3NMCL._AC_SL1500_.jpg","categoria":"Celulares"},
    {"id":3,"nombre":"Redmi Note 14 pro 4G","precio":1200000,"imagen":"https://m.media-amazon.com/images/I/71K+7dkoanL._AC_UY218_.jpg","categoria":"Celulares"},
    {"id":4,"nombre":"iPhone 13","precio":3800000,"imagen":"https://m.media-amazon.com/images/I/61VuVU94RnL._AC_SL1500_.jpg","categoria":"Celulares"},
    {"id":5,"nombre":"Portátil HP","precio":3200000,"imagen":"https://m.media-amazon.com/images/I/71jQbkYw5KL._AC_UY218_.jpg","categoria":"Computadores"},
    {"id":6,"nombre":"Portátil Lenovo","precio":3000000,"imagen":"https://m.media-amazon.com/images/I/61uX-zajiXL._AC_SX208_CB1169409_QL70_.jpg","categoria":"Computadores"},
    {"id":7,"nombre":"MacBook Air","precio":5200000,"imagen":"https://m.media-amazon.com/images/I/71TPda7cwUL._AC_SL1500_.jpg","categoria":"Computadores"},
    {"id":8,"nombre":"Teclado Gamer","precio":150000,"imagen":"https://m.media-amazon.com/images/I/71kr3WAj1FL._AC_SL1500_.jpg","categoria":"Accesorios"},
    {"id":9,"nombre":"Mouse Gamer","precio":90000,"imagen":"https://m.media-amazon.com/images/I/61UxfXTUyvL._AC_SL1500_.jpg","categoria":"Accesorios"},
    {"id":10,"nombre":"Audífonos Bluetooth","precio":180000,"imagen":"https://m.media-amazon.com/images/I/51Yya2WtvkL._AC_UY218_.jpg","categoria":"Accesorios"},
    {"id":11,"nombre":"Monitor 24\"","precio":850000,"imagen":"https://m.media-amazon.com/images/I/81QpkIctqPL._AC_SL1500_.jpg","categoria":"Monitores"},
    {"id":12,"nombre":"Tablet Samsung","precio":1300000,"imagen":"https://m.media-amazon.com/images/I/51hix7Z18SL._AC_UY218_.jpg","categoria":"Tablets"},
    {"id":13,"nombre":"Smartwatch","precio":250000,"imagen":"https://m.media-amazon.com/images/I/61ZjlBOp+rL._AC_SL1500_.jpg","categoria":"Wearables"},
    {"id":14,"nombre":"Router WiFi","precio":220000,"imagen":"https://m.media-amazon.com/images/I/51NPaIorJiL._AC_UY218_.jpg","categoria":"Redes"},
    {"id":15,"nombre":"Disco SSD 1TB","precio":350000,"imagen":"https://m.media-amazon.com/images/I/51ZuYxUAmPL._AC_UY218_.jpg","categoria":"Almacenamiento"},
    {"id":16,"nombre":"iPhone 14 pro max","precio":4200000,"imagen":"https://m.media-amazon.com/images/I/61dJHCFo1oL._AC_UY218_.jpg","categoria":"Celulares"},
    {"id":17,"nombre":"Samsung Galaxy S24","precio":4500000,"imagen":"https://m.media-amazon.com/images/I/71-EnPs+uQL._AC_UY218_.jpg","categoria":"Celulares"},
    {"id":18,"nombre":"Redmi Note 15 pro 5G","precio":2400000,"imagen":"https://m.media-amazon.com/images/I/713x7we4IhL._AC_UY218_.jpg","categoria":"Celulares"},
    {"id":19,"nombre":"iPhone 13 pro max","precio":4800000,"imagen":"https://m.media-amazon.com/images/I/71n-nparKcL._AC_UY218_.jpg","categoria":"Celulares"},
    {"id":20,"nombre":"Portátil HP Gamer","precio":4200000,"imagen":"https://m.media-amazon.com/images/I/7160S1idIuL._AC_UY218_.jpg","categoria":"Computadores"},
    {"id":21,"nombre":"Portátil Lenovo Gamer","precio":4000000,"imagen":"https://m.media-amazon.com/images/I/71Qmg0W9QuL._AC_UY218_.jpg","categoria":"Computadores"},
    {"id":22,"nombre":"MacBook Air Full","precio":6200000,"imagen":"https://m.media-amazon.com/images/I/71Ej6sIsNaL._AC_UY218_.jpg","categoria":"Computadores"},
    {"id":23,"nombre":"Teclado Gamer Mecanico","precio":250000,"imagen":"https://m.media-amazon.com/images/I/71Bk2A2WmOL._AC_UY218_.jpg","categoria":"Accesorios"},
    {"id":24,"nombre":"Mouse Gamer Inalambrico","precio":100000,"imagen":"https://m.media-amazon.com/images/I/619DIEev8fL._AC_UY218_.jpg","categoria":"Accesorios"},
    {"id":25,"nombre":"Audífonos Bluetooth Gamer","precio":280000,"imagen":"https://m.media-amazon.com/images/I/71epDZgbjQL._AC_UY218_.jpg","categoria":"Accesorios"},
    {"id":26,"nombre":"Monitor Gamer 27\"","precio":950000,"imagen":"https://m.media-amazon.com/images/I/71-Bv5z6UTL._AC_UY218_.jpg","categoria":"Monitores"},
    {"id":27,"nombre":"Tablet Samsung Gamer","precio":2300000,"imagen":"https://m.media-amazon.com/images/I/61d0nRJ7UJL._AC_UY218_.jpg","categoria":"Tablets"},
    {"id":28,"nombre":"Smartwatch avanzado","precio":350000,"imagen":"https://m.media-amazon.com/images/I/51GeUyZUB9L._AC_UY218_.jpg","categoria":"Wearables"},
    {"id":29,"nombre":"Router WiFi avanzado","precio":320000,"imagen":"https://m.media-amazon.com/images/I/41VlTprOFdL._AC_UY218_.jpg","categoria":"Redes"},
    {"id":30,"nombre":"Disco SSD 2TB","precio":450000,"imagen":"https://m.media-amazon.com/images/I/51zhuXxYuRL._AC_UY218_.jpg","categoria":"Almacenamiento"},
]

@app.route("/")
def index():
    return render_template("inicio.html")

@app.route("/productos")
def productos_page():
    return render_template("productos.html", productos=productos)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form["correo"]
        password = request.form["password"]

        if correo == "admin@techstore.com" and password == "admin123":
            session["usuario"] = "Administrador"
            session["rol"] = "admin"
            return redirect("/productos")

        con = sqlite3.connect("database.db")
        cur = con.cursor()

        cur.execute("SELECT * FROM usuarios WHERE correo=? AND password=?", (correo, password))
        user = cur.fetchone()

        con.close()

        if user:
            session["usuario"] = user[0]
            if correo == "admin@techstore.com":
                session["rol"] = "admin"
            else:
                session["rol"] = "cliente"
            return redirect("/productos")
        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"]
        correo = request.form["correo"]
        password = request.form["password"]

        try:

            con = sqlite3.connect("database.db")
            cur = con.cursor()

            cur.execute(
                "INSERT INTO usuarios (nombre, correo, password) VALUES (?,?,?)",
                (nombre, correo, password)
            )

            con.commit()
            con.close()

            return redirect("/login")

        except:
            return "Este correo ya está registrado"

    return render_template("registro.html")

@app.route("/admin")
def admin():

    if "usuario" not in session:
        return redirect("/login")

    if session.get("rol") != "admin":
        return "No tienes permiso para entrar aquí"

    return render_template("admin.html")

@app.route("/carrito")
def carrito():

    if "usuario" not in session:
        return redirect("/login")

    return render_template("carrito.html")

@app.route("/subir")
def subir():

    if "usuario" not in session:
        return redirect("/login")

    return render_template("subir_producto.html")


app.run(debug=True)
