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
    try:
        return int(text)
    except ValueError:
        raise ValueError(f"«{text}» — не целое число") from None


def ask_float(prompt: str) -> float:
    text = input(prompt).strip().replace(",", ".")
    try:
        return float(text)
    except ValueError:
        raise ValueError(f"«{text}» — не число") from None


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
        print("Этот стол свободен — сначала посадите гостей (пункт 3)")
        return
    print("Официанты:", ", ".join(w.name for w in r.waiters()))
    waiter = r.get_employee(input("Имя официанта: "), Waiter)
    customer = Customer(input("Имя гостя: "), input("Телефон гостя: "))
    order = r.take_order(table, waiter, customer)
    print(f"Создан заказ №{order.number}")


def add_to_order(r: Restaurant) -> None:
    order = r.get_order(ask_int("Номер заказа: "))
    item = r.menu.find(input("Название позиции: "))
    qty = ask_int("Количество: ")
    order.add_item(item, qty)
    print(f"Добавлено: {item.name} x{qty}. Сумма заказа: {order.total():.0f} ₽")


def cook_order(r: Restaurant) -> None:
    order = r.get_order(ask_int("Номер заказа: "))
    if not order.items:
        print("В заказе нет ни одной позиции")
        return
    print("Повара:", ", ".join(c.name for c in r.chefs()))
    chef = r.get_employee(input("Имя повара: "), Chef)
    order.set_status(OrderStatus.COOKING)
    chef.cook(order)
    print(f"{chef} приготовил заказ №{order.number}")


def pay_order(r: Restaurant) -> None:
    order = r.get_order(ask_int("Номер заказа: "))
    print(order.print_bill())
    choice = input("Способ оплаты (1 — карта, 2 — наличные): ").strip()
    methods = {"1": PaymentMethod.CARD, "2": PaymentMethod.CASH}
    if choice not in methods:
        raise ValueError("Нужно ввести 1 или 2")
    tip = ask_float("Чаевые, %: ")
    payment = Payment(order, methods[choice], tip)
    payment.pay()
    print(f"Оплачено {payment.total_with_tips():.0f} ₽ ({payment.method.value}), "
          f"чаевые {payment.tips_amount():.0f} ₽ — официанту {order.waiter.name}")


def show_orders(r: Restaurant) -> None:
    if not r.orders:
        print("Заказов пока нет")
    for o in r.orders:
        print(f"  №{o.number}: стол {o.table.number}, {o.waiter.name}, "
              f"{o.status.value}, {o.total():.0f} ₽")


def show_revenue(r: Restaurant) -> None:
    print(f"Выручка: {r.revenue():.0f} ₽")
    for w in r.waiters():
        print(f"  Чаевые {w.name}: {w.tips_total:.0f} ₽")


def main() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    r = create_demo_restaurant()

    actions = {
        "1": ("Показать меню", show_menu),
        "2": ("Показать столы", show_tables),
        "3": ("Посадить гостей", seat_guests),
        "4": ("Создать заказ", create_order),
        "5": ("Добавить позицию в заказ", add_to_order),
        "6": ("Приготовить заказ", cook_order),
        "7": ("Оплатить заказ", pay_order),
        "8": ("Список заказов", show_orders),
        "9": ("Выручка и чаевые", show_revenue),
    }

    while True:
        print(f"\n===== {r.name} =====")
        for key, (title, _) in actions.items():
            print(f"{key}. {title}")
        print("10. Сохранить в JSON    11. Загрузить из JSON")
        print("12. Сохранить в XML     13. Загрузить из XML")
        print("0. Выход")

        try:
            choice = input("> ").strip()
            if choice == "0":
                print("До свидания!")
                break
            elif choice in actions:
                actions[choice][1](r)
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
