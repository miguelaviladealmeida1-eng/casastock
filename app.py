from flask import Flask, jsonify, render_template, request
from pathlib import Path
import sqlite3

app = Flask(__name__)
DB = Path(__file__).with_name("casastock.db")
CATEGORIES = ["Alimentos", "Bebidas", "Limpeza", "Higiene", "Outros"]

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'Outros',
            quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
            min_quantity INTEGER NOT NULL DEFAULT 2 CHECK(min_quantity >= 0),
            unit TEXT NOT NULL DEFAULT 'un.'
        )""")
        if db.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            db.executemany("INSERT INTO products(name,category,quantity,min_quantity,unit) VALUES(?,?,?,?,?)", [
                ("Farinha de trigo","Alimentos",3,2,"pacotes"),
                ("Arroz","Alimentos",1,2,"pacotes"),
                ("Refrigerante","Bebidas",4,2,"garrafas"),
                ("Detergente","Limpeza",2,2,"un."),
                ("Sabonete","Higiene",0,3,"un."),
                ("Macarrão","Alimentos",5,2,"pacotes")])

@app.get("/")
def home():
    return render_template("index.html", categories=CATEGORIES)

@app.get("/api/products")
def products():
    search=request.args.get("search","").strip()
    category=request.args.get("category","")
    status=request.args.get("status","")
    sql="SELECT * FROM products WHERE name LIKE ?"
    args=[f"%{search}%"]
    if category and category != "Todas":
        sql+=" AND category=?"; args.append(category)
    if status=="low": sql+=" AND quantity>0 AND quantity<=min_quantity"
    if status=="out": sql+=" AND quantity=0"
    sql+=" ORDER BY name COLLATE NOCASE"
    with connect() as db: rows=[dict(r) for r in db.execute(sql,args).fetchall()]
    return jsonify(rows)

@app.post("/api/products")
def add_product():
    d=request.get_json(silent=True) or {}
    name=str(d.get("name","")).strip()
    if not name: return jsonify(error="Informe o nome do produto."),400
    try:
        qty=int(d.get("quantity",0)); minimum=int(d.get("min_quantity",2))
    except (ValueError,TypeError): return jsonify(error="As quantidades devem ser números inteiros."),400
    if qty<0 or minimum<0: return jsonify(error="As quantidades não podem ser negativas."),400
    category=d.get("category","Outros")
    if category not in CATEGORIES: category="Outros"
    with connect() as db:
        cur=db.execute("INSERT INTO products(name,category,quantity,min_quantity,unit) VALUES(?,?,?,?,?)",
          (name,category,qty,minimum,str(d.get("unit","un.")).strip() or "un."))
        row=dict(db.execute("SELECT * FROM products WHERE id=?",(cur.lastrowid,)).fetchone())
    return jsonify(row),201

@app.patch("/api/products/<int:pid>")
def edit_product(pid):
    d=request.get_json(silent=True) or {}
    allowed={"name","category","quantity","min_quantity","unit"}
    fields={k:d[k] for k in allowed if k in d}
    if not fields: return jsonify(error="Nenhuma alteração informada."),400
    if "name" in fields and not str(fields["name"]).strip(): return jsonify(error="Nome inválido."),400
    for k in ("quantity","min_quantity"):
        if k in fields:
            try: fields[k]=int(fields[k])
            except (ValueError,TypeError): return jsonify(error="Quantidade inválida."),400
            if fields[k]<0: return jsonify(error="A quantidade não pode ser negativa."),400
    if "category" in fields and fields["category"] not in CATEGORIES: fields["category"]="Outros"
    if "name" in fields: fields["name"]=str(fields["name"]).strip()
    with connect() as db:
        db.execute("UPDATE products SET "+", ".join(k+"=?" for k in fields)+" WHERE id=?",[*fields.values(),pid])
        row=db.execute("SELECT * FROM products WHERE id=?",(pid,)).fetchone()
    if not row: return jsonify(error="Produto não encontrado."),404
    return jsonify(dict(row))

@app.delete("/api/products/<int:pid>")
def delete_product(pid):
    with connect() as db: cur=db.execute("DELETE FROM products WHERE id=?",(pid,))
    if not cur.rowcount: return jsonify(error="Produto não encontrado."),404
    return jsonify(ok=True)

@app.get("/api/summary")
def summary():
    with connect() as db:
        r=db.execute("""SELECT COUNT(*) total, COALESCE(SUM(quantity),0) units,
        SUM(CASE WHEN quantity>0 AND quantity<=min_quantity THEN 1 ELSE 0 END) low,
        SUM(CASE WHEN quantity=0 THEN 1 ELSE 0 END) out FROM products""").fetchone()
    return jsonify({k:r[k] or 0 for k in ("total","units","low","out")})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0",port=5000,debug=False)
