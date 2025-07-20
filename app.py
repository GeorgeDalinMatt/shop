from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize DB
def init_db():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price TEXT,
            img TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()
    cart = session.get("cart", [])
    return render_template("index.html", items=items, cart=cart)

@app.route("/add_to_cart/<int:item_id>")
def add_to_cart(item_id):
    cart = session.get("cart", [])
    cart.append(item_id)
    session["cart"] = cart
    return redirect(url_for("index"))

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]
        img = request.form["img"]
        conn = sqlite3.connect('shop.db')
        c = conn.cursor()
        c.execute("INSERT INTO items (name, price, img) VALUES (?, ?, ?)", (name, price, img))
        conn.commit()
        conn.close()
        return redirect(url_for("admin"))
    conn = sqlite3.connect('shop.db')
    c = conn.cursor()
    c.execute("SELECT * FROM items")
    items = c.fetchall()
    conn.close()
    return render_template("admin.html", items=items)

if __name__ == "__main__":
    app.run(debug=True)

@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    conn = sqlite3.connect("shop.db")
    c = conn.cursor()
    c.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

