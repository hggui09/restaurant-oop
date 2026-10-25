import json
import xml.etree.ElementTree as ET

from enums import OrderStatus
from exceptions import StorageError, RestaurantError
from menu import Dish, Drink
from people import Customer, Waiter, Chef
from restaurant import Restaurant, Order


def _restore_status(order: Order, target: OrderStatus) -> None:
    for status in [OrderStatus.COOKING, OrderStatus.READY, OrderStatus.PAID]:
        if order.status == target:
            break
        order.set_status(status)


def save_json(restaurant: Restaurant, path: str) -> None:
    data = {
        "name": restaurant.name,
        "tables": [
            {"number": t.number, "seats": t.seats, "occupied": not t.is_free()}
            for t in restaurant.tables
        ],
        "staff": [_employee_to_dict(e) for e in restaurant.staff],
        "menu": [_item_to_dict(i) for i in restaurant.menu.items],
        "orders": [
            {
                "number": o.number,
                "table": o.table.number,
                "waiter": o.waiter.name,
                "customer": {"name": o.customer.name, "phone": o.customer.phone},
                "status": o.status.name,
                "items": [{"name": i.name, "quantity": q} for i, q in o.items.items()],
            }
            for o in restaurant.orders
        ],
    }
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise StorageError(f"Не удалось записать файл {path}: {e}")


def load_json(path: str) -> Restaurant:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError as e:
        raise StorageError(f"Файл {path} не найден")
    except json.JSONDecodeError as e:
        raise StorageError(f"Файл {path} поврежден: {e}")

    try:
        r = Restaurant(data["name"])
        for t in data["tables"]:
            table = r.add_table(t["seats"], t["number"])
            if t["occupied"]:
                table.occupy()
        for e in data["staff"]:
            r.hire(_employee_from_dict(e))
        for i in data["menu"]:
            r.menu.add(_item_from_dict(i))
        for o in data["orders"]:
            order = Order(
                number=o["number"],
                waiter=r.get_waiter(o["waiter"]),
                table=r.get_table(o["table"]),
                customer=Customer(o["customer"]["name"], o["customer"]["phone"]),
            )
            for it in o["items"]:
                order.add_item(r.menu.find(it["name"]), it["quantity"])
            _restore_status(order, OrderStatus[o["status"]])
            r.add_existing_order(order)
        return r
    except (KeyError, ValueError, TypeError, AttributeError, RestaurantError) as e:
        raise StorageError(f"Неверная структура данных в {path}: {e}")


def _employee_to_dict(e) -> dict:
    d = {"type": type(e).__name__, "name": e.name, "phone": e.phone,
         "salary": e.salary, "position": e.position}
    if isinstance(e, Waiter):
        d["tips_total"] = e.tips_total
    return d


def _employee_from_dict(d: dict):
    if d["type"] == "Waiter":
        w = Waiter(d["name"], d["phone"], d["salary"], d["position"])
        w.add_tips(d.get("tips_total", 0))
        return w
    if d["type"] == "Chef":
        return Chef(d["name"], d["phone"], d["salary"], d["position"])
    raise ValueError(f"Неизвестный тип сотрудника: {d['type']}")


def _item_to_dict(i) -> dict:
    if isinstance(i, Dish):
        return {"type": "Dish", "name": i.name, "price": i.price, "weight": i.weight}
    return {"type": "Drink", "name": i.name, "price": i.price,
            "volume": i.volume, "is_alcoholic": i.is_alcoholic}


def _item_from_dict(d: dict):
    if d["type"] == "Dish":
        return Dish(d["name"], d["price"], d["weight"])
    if d["type"] == "Drink":
        return Drink(d["name"], d["price"], d["volume"], d["is_alcoholic"])
    raise ValueError(f"Неизвестный тип позиции: {d['type']}")


def save_xml(restaurant: Restaurant, path: str) -> None:
    root = ET.Element("restaurant", name=restaurant.name)

    tables = ET.SubElement(root, "tables")
    for t in restaurant.tables:
        ET.SubElement(tables, "table", number=str(t.number), seats=str(t.seats),
                      occupied=str(not t.is_free()).lower())

    staff = ET.SubElement(root, "staff")
    for e in restaurant.staff:
        el = ET.SubElement(staff, type(e).__name__.lower(), name=e.name, phone=e.phone,
                           salary=str(e.salary), position=e.position)
        if isinstance(e, Waiter):
            el.set("tips_total", str(e.tips_total))

    menu = ET.SubElement(root, "menu")
    for i in restaurant.menu.items:
        if isinstance(i, Dish):
            ET.SubElement(menu, "dish", name=i.name, price=str(i.price), weight=str(i.weight))
        else:
            ET.SubElement(menu, "drink", name=i.name, price=str(i.price),
                          volume=str(i.volume), is_alcoholic=str(i.is_alcoholic).lower())

    orders = ET.SubElement(root, "orders")
    for o in restaurant.orders:
        oel = ET.SubElement(orders, "order", number=str(o.number), table=str(o.table.number),
                            waiter=o.waiter.name, status=o.status.name)
        ET.SubElement(oel, "customer", name=o.customer.name, phone=o.customer.phone)
        for item, qty in o.items.items():
            ET.SubElement(oel, "item", name=item.name, quantity=str(qty))

    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    try:
        tree.write(path, encoding="utf-8", xml_declaration=True)
    except OSError as e:
        raise StorageError(f"Не удалось записать файл {path}: {e}")


def load_xml(path: str) -> Restaurant:
    try:
        root = ET.parse(path).getroot()
    except FileNotFoundError as e:
        raise StorageError(f"Файл {path} не найден")
    except ET.ParseError as e:
        raise StorageError(f"Файл {path} поврежден: {e}")

    try:
        r = Restaurant(root.attrib["name"])
        for t in root.find("tables"):
            table = r.add_table(int(t.get("seats")), int(t.get("number")))
            if t.get("occupied") == "true":
                table.occupy()
        for e in root.find("staff"):
            if e.tag == "waiter":
                w = Waiter(e.get("name"), e.get("phone"), float(e.get("salary")), e.get("position"))
                w.add_tips(float(e.get("tips_total", 0)))
                r.hire(w)
            elif e.tag == "chef":
                r.hire(Chef(e.get("name"), e.get("phone"), float(e.get("salary")), e.get("position")))
            else:
                raise ValueError(f"Неизвестный тип сотрудника: {e.tag}")
        for i in root.find("menu"):
            if i.tag == "dish":
                r.menu.add(Dish(i.get("name"), float(i.get("price")), int(i.get("weight"))))
            elif i.tag == "drink":
                r.menu.add(Drink(i.get("name"), float(i.get("price")), int(i.get("volume")),
                                 i.get("is_alcoholic") == "true"))
            else:
                raise ValueError(f"Неизвестный тип позиции: {i.tag}")
        for o in root.find("orders"):
            c = o.find("customer")
            order = Order(
                number=int(o.get("number")),
                waiter=r.get_waiter(o.get("waiter")),
                table=r.get_table(int(o.get("table"))),
                customer=Customer(c.get("name"), c.get("phone")),
            )
            for it in o.findall("item"):
                order.add_item(r.menu.find(it.get("name")), int(it.get("quantity")))
            _restore_status(order, OrderStatus[o.get("status")])
            r.add_existing_order(order)
        return r
    except (KeyError, ValueError, TypeError, AttributeError, RestaurantError) as e:
        raise StorageError(f"Неверная структура данных в {path}: {e}")
