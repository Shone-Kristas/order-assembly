import sqlite3

conn = sqlite3.connect('mydb.db')

cursor = conn.cursor()


products = [('Ноутбук',), ('Телевизор',), ('Телефон',), ('Системный блок',), ('Часы',), ('Микрофон',)]
cursor.executemany('INSERT INTO products (name) VALUES (?)', products)

orders = [
    (10, 2, conn.execute("SELECT id FROM products WHERE name='Ноутбук'").fetchone()[0]),
    (10, 1, conn.execute("SELECT id FROM products WHERE name='Телефон'").fetchone()[0]),
    (10, 1, conn.execute("SELECT id FROM products WHERE name='Микрофон'").fetchone()[0]),
    (11, 3, conn.execute("SELECT id FROM products WHERE name='Телевизор'").fetchone()[0]),
    (14, 3, conn.execute("SELECT id FROM products WHERE name='Ноутбук'").fetchone()[0]),
    (14, 4, conn.execute("SELECT id FROM products WHERE name='Системный блок'").fetchone()[0]),
    (15, 1, conn.execute("SELECT id FROM products WHERE name='Часы'").fetchone()[0])
]
cursor.executemany('INSERT INTO orders (number, amount, product_id) VALUES (?, ?, ?)', orders)

main_racks = [('А',), ('Б',), ('Ж',)]
cursor.executemany('INSERT INTO main_racks (name) VALUES (?)', main_racks)


side_racks = [('А', conn.execute("SELECT id FROM main_racks WHERE id=3").fetchone()[0]),
              ('З', conn.execute("SELECT id FROM main_racks WHERE id=2").fetchone()[0]),
              ('В', conn.execute("SELECT id FROM main_racks WHERE id=2").fetchone()[0])
]
cursor.executemany('INSERT INTO side_racks (name, main_racks_id) VALUES (?, ?)', side_racks)

location_products = [(conn.execute("SELECT id FROM products WHERE name='Ноутбук'").fetchone()[0], conn.execute("SELECT id FROM main_racks WHERE id=1").fetchone()[0], 'none'),
                     (conn.execute("SELECT id FROM products WHERE name='Телевизор'").fetchone()[0], conn.execute("SELECT id FROM main_racks WHERE id=1").fetchone()[0], 'none'),
                     (conn.execute("SELECT id FROM products WHERE name='Телефон'").fetchone()[0], 'none', conn.execute("SELECT id FROM side_racks WHERE id=2").fetchone()[0]),
                     (conn.execute("SELECT id FROM products WHERE name='Телефон'").fetchone()[0], 'none', conn.execute("SELECT id FROM side_racks WHERE id=3").fetchone()[0]),
                     (conn.execute("SELECT id FROM products WHERE name='Системный блок'").fetchone()[0], conn.execute("SELECT id FROM main_racks WHERE id=3").fetchone()[0], 'none'),
                     (conn.execute("SELECT id FROM products WHERE name='Часы'").fetchone()[0], 'none', conn.execute("SELECT id FROM side_racks WHERE id=1").fetchone()[0]),
                     (conn.execute("SELECT id FROM products WHERE name='Микрофон'").fetchone()[0], conn.execute("SELECT id FROM main_racks WHERE id=3").fetchone()[0], 'none')
]

cursor.executemany('INSERT INTO location_products (products_id, main_racks_id, side_racks_id) VALUES (?, ?, ?)', location_products)

conn.commit()
conn.close()