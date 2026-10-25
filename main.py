import os

from enums import OrderStatus, PaymentMethod
from exceptions import RestaurantError, StorageError
from menu import Dish, Drink
from people import Customer, Waiter, Chef
from restaurant import Restaurant, Payment
import storage

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
JSON_PATH = os.path.join(DATA_DIR, "restaurant.json")
XML_PATH = os.path.join(DATA_DIR, "restaurant.xml")


def create_demo_restaurant() -> Restaurant:
    r = Restaurant("У Анастасии")
    for seats in (2, 2, 4, 4, 6):
        r.add_table(seats)
    r.hire(Waiter("Анна", "+7 900 111-11-11", 45000))
    r.hire(Waiter("Олег", "+7 900 222-22-22", 45000))
    r.hire(Chef("Иван", "+7 900 333-33-33", 80000, "Шеф-повар"))
    r.hire(Chef("Мария", "+7 900 444-44-44", 60000))
    r.menu.add(Dish("Борщ", 350, 300))
    r.menu.add(Dish("Паста с грибами", 520, 280))
    r.menu.add(Dish("Стейк", 1200, 250))
    r.menu.add(Drink("Морс", 180, 300))
    r.menu.add(Drink("Вино красное", 450, 150, is_alcoholic=True))
    return r


def ask_int(prompt: str) -> int:
    text = input(prompt).strip()
    if not text.isdigit():
        raise ValueError(f"'{text}' - не целое число")
    return int(text)


def ask_float(prompt: str) -> float:
    text = input(prompt).strip().replace(",", ".")
    if not text.replace(".", "", 1).isdigit():
        raise ValueError(f"'{text}' - не число")
    return float(text)


def show_menu(r: Restaurant) -> None:
    print(r.menu.show())


def show_tables(r: Restaurant) -> None:
    for t in r.tables:
        state = "свободен" if t.is_free() else "занят"
        print(f"  Стол №{t.number}: {t.seats} мест, {state}")


def seat_guests(r: Restaurant) -> None:
    guests = ask_int("Сколько гостей? ")
    table = r.seat_customer(guests)
    print(f"Гости посажены за стол №{table.number}")


def create_order(r: Restaurant) -> None:
    table = r.get_table(ask_int("Номер стола: "))
    if table.is_free():
        print("Этот стол свободен - сначала посадите гостей (пункт 3)")
        return
    print("Официанты:", ", ".join(w.name for w in r.waiters()))
    waiter = r.get_waiter(input("Имя официанта: "))
    customer = Customer(input("Имя гостя: "), input("Телефон гостя: "))
    order = r.take_order(table, waiter, customer)
    print(f"Создан заказ №{order.number}")


def add_to_order(r: Restaurant) -> None:
    order = r.get_order(ask_int("Номер заказа: "))
    item = r.menu.find(input("Название позиции: "))
    qty = ask_int("Количество: ")
    order.add_item(item, qty)
    print(f"Добавлено: {item.name} x{qty}. Сумма заказа: {order.total():.0f} руб")


def cook_order(r: Restaurant) -> None:
    order = r.get_order(ask_int("Номер заказа: "))
    if not order.items:
        print("В заказе нет ни одной позиции")
        return
    print("Повара:", ", ".join(c.name for c in r.chefs()))
    chef = r.get_chef(input("Имя повара: "))
    order.set_status(OrderStatus.COOKING)
    chef.cook(order)
    print(f"{chef} приготовил заказ №{order.number}")


def pay_order(r: Restaurant) -> None:
    order = r.get_order(ask_int("Номер заказа: "))
    print(order.print_bill())
    choice = input("Способ оплаты (1 - карта, 2 - наличные): ").strip()
    methods = {"1": PaymentMethod.CARD, "2": PaymentMethod.CASH}
    if choice not in methods:
        raise ValueError("Нужно ввести 1 или 2")
    tip = ask_float("Чаевые, %: ")
    payment = Payment(order, methods[choice], tip)
    payment.pay()
    print(f"Оплачено {payment.total_with_tips():.0f} руб ({payment.method.value}), "
          f"чаевые {payment.tips_amount():.0f} руб - официанту {order.waiter.name}")


def show_orders(r: Restaurant) -> None:
    if not r.orders:
        print("Заказов пока нет")
    for o in r.orders:
        print(f"  №{o.number}: стол {o.table.number}, {o.waiter.name}, "
              f"{o.status.value}, {o.total():.0f} руб")


def show_revenue(r: Restaurant) -> None:
    print(f"Выручка: {r.revenue():.0f} руб")
    for w in r.waiters():
        print(f"  Чаевые {w.name}: {w.tips_total:.0f} руб")


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    r = create_demo_restaurant()

    while True:
        print(f"\n===== {r.name} =====")
        print("1. Показать меню")
        print("2. Показать столы")
        print("3. Посадить гостей")
        print("4. Создать заказ")
        print("5. Добавить позицию в заказ")
        print("6. Приготовить заказ")
        print("7. Оплатить заказ")
        print("8. Список заказов")
        print("9. Выручка и чаевые")
        print("10. Сохранить в JSON    11. Загрузить из JSON")
        print("12. Сохранить в XML     13. Загрузить из XML")
        print("0. Выход")

        try:
            choice = input("> ").strip()
            if choice == "0":
                print("До свидания!")
                break
            elif choice == "1":
                show_menu(r)
            elif choice == "2":
                show_tables(r)
            elif choice == "3":
                seat_guests(r)
            elif choice == "4":
                create_order(r)
            elif choice == "5":
                add_to_order(r)
            elif choice == "6":
                cook_order(r)
            elif choice == "7":
                pay_order(r)
            elif choice == "8":
                show_orders(r)
            elif choice == "9":
                show_revenue(r)
            elif choice == "10":
                storage.save_json(r, JSON_PATH)
                print(f"Сохранено в {JSON_PATH}")
            elif choice == "11":
                r = storage.load_json(JSON_PATH)
                print("Данные загружены из JSON")
            elif choice == "12":
                storage.save_xml(r, XML_PATH)
                print(f"Сохранено в {XML_PATH}")
            elif choice == "13":
                r = storage.load_xml(XML_PATH)
                print("Данные загружены из XML")
            else:
                print("Нет такого пункта меню")

        except StorageError as e:
            print(f"Ошибка файла: {e}")
        except RestaurantError as e:
            print(f"Ошибка: {e}")
        except ValueError as e:
            print(f"Неверный ввод: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из программы")
            break
        except Exception as e:
            print(f"Непредвиденная ошибка: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
