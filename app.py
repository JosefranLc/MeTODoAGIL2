from flask import Flask, render_template, request, redirect, url_for, session
#respectivamente cria o "app", renderiza o nosso html, requisita os acessos aos formulários, redireciona os nossos caminhos
#monta o nosso url e guarda o nosso usuário no cache do navegador para poder acessar novamente.
import sqlite3
#importa o nosso banco de dados

def criar_banco(): #"a classe do nosso html" aqui é chamada de função usando o def
    conn = sqlite3.connect("database.db") # abre conexão com o banco (ou cria se não existir)
    cursor = conn.cursor() #cria o “controle” pra executar comandos SQL

    # cria tabela de usuários (login)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT,
        senha TEXT
    )
    """)
    #aqui fica um pouco mais complexo de entender, cria a tabela usuarios se não existir:
    #id → identificador automático
    #usuario → login
    #senha → senha

    conn.commit() #salva as alterações no banco
    conn.close() #fecha a conexão
criar_banco() #executa a função do criar banco anterior

app = Flask(__name__) #cria o app
app.secret_key = "123" #chave super secreta de login inquebrável

# conexão com banco
def conectar(): #função pra conectar no banco sempre que precisar
    return sqlite3.connect("database.db") #retorna a conexão

# =========================
# LOGIN
# =========================
@app.route("/", methods=["GET", "POST"])
#define rota para abrir a página [/ (página inicial)]
#aceita GET (abrir página) e POST (enviar formulário)
def login(): #função de login
    if request.method == "POST": #se o usuário enviou o formulário
        usuario = request.form["usuario"] #dados do usuário
        senha = request.form["senha"] #dados do usuario

        conn = conectar() #abre conexão com banco
        cursor = conn.cursor() #abre conexão com banco

        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND senha=?", (usuario, senha)) #Busca usuário no banco
        #Usa ? pra evitar SQL injection
        user = cursor.fetchone() #pega o resultado (um usuário ou nada)

        conn.close() #fecha a conexão

        if user: #se achou o usuário no banco de dados
            session["usuario"] = usuario #salva o login na sessão (usuário fica logado)
            return redirect(url_for("home")) #redireciona pra home
        else:
            return render_template("login.html", erro=True) #se falhou → volta pro login com erro

    return render_template("login.html") #se for GET → só abre a tela de login
    #vai reabrir a pagina pq está sem dados


# =========================
# HOME (index.html)
# =========================
@app.route("/home") #rota para abrir a home
def home(): #função denovo, isso facilita mt
    if "usuario" not in session: #se não estiver logado
        return redirect(url_for("login")) #manda de volta pro login

    return render_template("index.html")#se estiver logado → mostra página


# =========================
# CADASTRO
# =========================
@app.route("/cadastro", methods=["GET", "POST"]) #rota de cadastro
def cadastro(): #função
    if request.method == "POST": #se enviou formulário
        usuario = request.form["usuario"] #usa os dados
        senha = request.form["senha"] #usa os dados

        conn = conectar() #abre o banco
        cursor = conn.cursor() #conecta o banco

        cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, senha))
        #insere o novo usuário
        conn.commit() #salva no banco
        conn.close() #fecha a conexão

        return redirect(url_for("login")) #volta pro login depois de cadastrar

    return render_template("cadastro.html") #se GET → mostra página de cadastro


# =========================
# LOGOUT
# =========================
@app.route("/logout") #rota para deslogar
def logout(): #função
    session.pop("usuario", None) #remove usuário da sessão (desloga)
    return redirect(url_for("login")) #volta pro login

print("ESTOU RODANDO ESSE APP AQUI") #isso aqui foi pra testar o codigo e esqueci de tirar depois

if __name__ == "__main__": #verifica se tá rodando direto (não importado)
    #até hoje eu não se explicar em palavras isso aqui
    app.run(debug=True) #inicia servidor e debug=True → recarrega automático e mostra erro detalhado
