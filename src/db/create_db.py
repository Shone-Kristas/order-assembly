import sqlite3

conn = sqlite3.connect('mydb.db')

conn.execute("""
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

conn.execute("""
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number INTEGER NOT NULL,
    amount INTEGER NOT NULL,
    product_id INTEGER,
    FOREIGN KEY (product_id)  REFERENCES products (id)
);
""")

conn.execute("""
CREATE TABLE main_racks (   
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);
""")

conn.execute("""
CREATE TABLE side_racks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    main_racks_id INTEGER,
    FOREIGN KEY (main_racks_id) REFERENCES main_racks (id)
);
""")

conn.execute("""
CREATE TABLE location_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    products_id INTEGER,
    main_racks_id INTEGER,
    side_racks_id INTEGER,
    FOREIGN KEY (products_id) REFERENCES products (id)
    FOREIGN KEY (main_racks_id) REFERENCES main_racks (id)
    FOREIGN KEY (side_racks_id) REFERENCES side_racks (id)
);
""")

conn.commit()
conn.close()
