import sqlite3
import argparse

def select_orders(order_ids):
    with sqlite3.connect('db/mydb.db') as conn:
        cursor = conn.cursor()

        order_data_list = []
        for order_id in order_ids:
            cursor.execute('''
                SELECT products.name, products.id, orders.number, orders.amount
                FROM products
                JOIN orders ON orders.product_id = products.id
                WHERE orders.number = ?
            ''', (order_id,))
            rows = cursor.fetchall()
            order_data_list.append(rows)
        return select_racks(order_data_list)


def select_racks(order_data_list):
    with sqlite3.connect('db/mydb.db') as conn:
        cursor = conn.cursor()

        result_dict = {}
        for item in order_data_list:
            for gitems in item:
                product_name, product_id, order_number, order_amount = gitems
                cursor.execute('''
                        SELECT main_racks.name,
                            side_racks.name, main_racks_dop.name
                        FROM products
                        LEFT JOIN location_products ON location_products.products_id = products.id
                        LEFT JOIN side_racks ON location_products.side_racks_id = side_racks.id
                        LEFT JOIN main_racks ON location_products.main_racks_id = main_racks.id
                        LEFT JOIN main_racks AS main_racks_dop ON side_racks.main_racks_id = main_racks_dop.id
                        WHERE products.name = ?
                    ''', (product_name,))
                grows = cursor.fetchall()

                if grows:
                    main_rack_name = grows[0][0]
                    if main_rack_name not in result_dict:
                        result_dict[main_rack_name] = []
                    for row in grows:
                        if row[1] and row[2]:  # Если есть и основной и дополнительный стеллаж
                            result_dict[main_rack_name].append(f'{product_name} (id={product_id})\nзаказ {order_number}, {order_amount} шт\nдоп стеллаж: {row[1]}, {row[2]}')
                        elif row[1]:  # Если есть только основной стеллаж
                            result_dict[main_rack_name].append(f'{product_name} (id={product_id})\nзаказ {order_number}, {order_amount} шт\nосновной стеллаж: {row[1]}')
                        else:
                            result_dict[main_rack_name].append(f'{product_name} (id={product_id})\nзаказ {order_number}, {order_amount} шт')
        return result_data(result_dict)


def result_data(result_dict):
    # Вывод результатов
    print(f'Страница сборки заказов {main_rack}')
    for main_rack, items in result_dict.items():
        print(f'===Стеллаж {main_rack}')
        for item in items:
            print(item)
        print()



def main():
    parser = argparse.ArgumentParser(
        description="File System Analyzer with File Type Categorization"
    )

    # Устанавливаем значение для определения файлов с размером выше этого значения
    parser.add_argument("invalue", nargs='+', type=int, help="Set size value: (default is byte)")
    args = parser.parse_args()

    # Получаем список чисел из аргументов командной строки
    values_list = args.invalue

    # Преобразуем список чисел в кортеж
    values_tuple = tuple(values_list)
    select_orders(values_tuple)


if __name__ == "__main__":
    main()