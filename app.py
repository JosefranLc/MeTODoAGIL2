from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

def criar_banco():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # cria tabela de usuários (login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        senha TEXT
    )
    """)

    conn.commit()
    conn.close()

criar_banco()

app = Flask(__name__)
app.secret_key = "123"

# conexão com banco
def conectar():
    return sqlite3.connect("database.db")

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha))
        user = cursor.fetchone()

        conn.close()

        if user:
            session["usuario"] = usuario
            return redirect(url_for("home"))
        else:
            return render_template("login.html", erro=True)

    return render_template("login.html")


# =========================
# HOME (index.html)
# =========================
@app.route("/home")
def home():
    if "usuario" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# =========================
# CADASTRO
# =========================
@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        senha = request.form["senha"]

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        conn.commit()
        conn.close()

        return redirect(url_for("login"))

    return render_template("cadastro.html")


# =========================
# LOGOUT
# =========================
@app.route("/logout")
def logout():
    session.pop("usuario", None)
    return redirect(url_for("login"))

print("ESTOU RODANDO ESSE APP AQUI")

if __name__ == "__main__":
    app.run(debug=True)
