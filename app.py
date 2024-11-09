from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_database():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Platos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plato_id INTEGER NOT NULL,
            mesa_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            FOREIGN KEY (plato_id) REFERENCES Platos(id),
            FOREIGN KEY (mesa_id) REFERENCES Mesas(id)
        )
    """)
    
    conn.commit()
    conn.close()

init_database()

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST" and "nombre_plato" in request.form:
        nombre = request.form["nombre_plato"]
        precio = float(request.form["precio_plato"])
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Platos (nombre, precio) VALUES (?, ?)", (nombre, precio))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    if request.method == "POST" and "numero_mesa" in request.form:
        numero = int(request.form["numero_mesa"])
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Mesas (numero) VALUES (?)", (numero,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    if request.method == "POST" and "plato_pedido" in request.form:
        plato_id = int(request.form["plato_pedido"])
        mesa_id = int(request.form["mesa_pedido"])
        cantidad = int(request.form["cantidad_pedido"])
        fecha = request.form["fecha_pedido"]
        conn = sqlite3.connect("restaurant.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Pedidos (plato_id, mesa_id, cantidad, fecha) VALUES (?, ?, ?, ?)", (plato_id, mesa_id, cantidad, fecha))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))


    conn = sqlite3.connect("restaurant.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Consultas para llenar las tablas
    cursor.execute("SELECT * FROM Platos")
    platos = cursor.fetchall()

    cursor.execute("SELECT * FROM Mesas")
    mesas = cursor.fetchall()

    cursor.execute("""
        SELECT Pedidos.id, Platos.nombre AS plato, Mesas.numero AS mesa, Pedidos.cantidad, Pedidos.fecha
        FROM Pedidos
        JOIN Platos ON Pedidos.plato_id = Platos.id
        JOIN Mesas ON Pedidos.mesa_id = Mesas.id
    """)
    pedidos = cursor.fetchall()

    conn.close()
    
    return render_template("index.html", platos=platos, mesas=mesas, pedidos=pedidos)

if __name__ == "__main__":
    app.run(debug=True)
