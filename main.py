
from database import (
    init_db,
    add_employee,
    get_employees,
    add_location,
    get_locations,
    add_shift,
    get_shifts
)


# =====================================
# ВЫВОД СОТРУДНИКОВ
# =====================================

def show_employees():

    employees = get_employees()

    print("\n=== СПИСОК СОТРУДНИКОВ ===")

    if not employees:
        print("Сотрудников пока нет.")
        return

    for employee in employees:
        print(
            f"ID: {employee['id']} | "
            f"Имя: {employee['full_name']} | "
            f"Должность: {employee['position']} | "
            f"Телефон: {employee['phone']}"
        )


# =====================================
# ВЫВОД РАБОЧИХ ТОЧЕК
# =====================================

def show_locations():

    locations = get_locations()

    print("\n=== РАБОЧИЕ ТОЧКИ ===")

    if not locations:
        print("Рабочих точек пока нет.")
        return

    for location in locations:
        print(
            f"ID: {location['id']} | "
            f"Название: {location['name']} | "
            f"Адрес: {location['address']}"
        )


# =====================================
# ВЫВОД РАСПИСАНИЯ СМЕН
# =====================================

def show_shifts():

    shifts = get_shifts()

    print("\n=== РАСПИСАНИЕ СМЕН ===")

    if not shifts:
        print("Смен пока нет.")
        return

    for shift in shifts:
        print(
            f"\nСмена №{shift['id']}"
            f"\nСотрудник: {shift['employee_name']}"
            f"\nКофейня: {shift['location_name']}"
            f"\nДата: {shift['shift_date']}"
            f"\nВремя: {shift['start_time']} - "
            f"{shift['end_time']}"
        )


# =====================================
# ДОБАВЛЕНИЕ СОТРУДНИКА
# =====================================

def create_employee():

    print("\n=== ДОБАВЛЕНИЕ СОТРУДНИКА ===")

    full_name = input("ФИО: ").strip()
    position = input("Должность: ").strip()
    phone = input("Телефон: ").strip()
    hire_date = input("Дата приёма (ГГГГ-ММ-ДД): ").strip()

    if not full_name or not position:
        print("ФИО и должность обязательны!")
        return

    try:
        add_employee(
            full_name,
            position,
            phone,
            hire_date
        )

        print("Сотрудник успешно добавлен!")

    except Exception as error:
        print(f"Ошибка: {error}")


# =====================================
# ДОБАВЛЕНИЕ РАБОЧЕЙ ТОЧКИ
# =====================================

def create_location():

    print("\n=== ДОБАВЛЕНИЕ РАБОЧЕЙ ТОЧКИ ===")

    name = input("Название кофейни: ").strip()
    address = input("Адрес: ").strip()

    if not name:
        print("Название обязательно!")
        return

    try:
        add_location(name, address)
        print("Рабочая точка добавлена!")

    except Exception as error:
        print(f"Ошибка: {error}")


# =====================================
# ДОБАВЛЕНИЕ СМЕНЫ
# =====================================

def create_shift():

    print("\n=== ДОБАВЛЕНИЕ СМЕНЫ ===")

    employees = get_employees()
    locations = get_locations()

    if not employees:
        print("Сначала добавьте сотрудников!")
        return

    if not locations:
        print("Сначала добавьте рабочие точки!")
        return

    print("\nСотрудники:")

    for employee in employees:
        print(
            f"{employee['id']} - "
            f"{employee['full_name']}"
        )

    try:
        employee_id = int(
            input("\nВведите ID сотрудника: ")
        )

        if not any(
            employee["id"] == employee_id
            for employee in employees
        ):
            print("Такого сотрудника нет!")
            return

        print("\nРабочие точки:")

        for location in locations:
            print(
                f"{location['id']} - "
                f"{location['name']}"
            )

        location_id = int(
            input("\nВведите ID рабочей точки: ")
        )

        if not any(
            location["id"] == location_id
            for location in locations
        ):
            print("Такой рабочей точки нет!")
            return

        shift_date = input(
            "Дата смены (ГГГГ-ММ-ДД): "
        ).strip()

        start_time = input(
            "Начало смены (ЧЧ:ММ): "
        ).strip()

        end_time = input(
            "Окончание смены (ЧЧ:ММ): "
        ).strip()

        add_shift(
            employee_id,
            location_id,
            shift_date,
            start_time,
            end_time
        )

    except ValueError as error:
        print(f"Ошибка: {error}")

    except Exception as error:
        print(f"Ошибка: {error}")


# =====================================
# ГЛАВНОЕ МЕНЮ
# =====================================

def main():

    init_db()

    print("\nБаза данных успешно подключена!")

    while True:

        print("\n==============================")
        print(" СИСТЕМА УПРАВЛЕНИЯ КОФЕЙНЕЙ")
        print("==============================")

        print("1. Добавить сотрудника")
        print("2. Показать сотрудников")
        print("3. Добавить рабочую точку")
        print("4. Показать рабочие точки")
        print("5. Добавить смену")
        print("6. Показать расписание смен")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "1":
            create_employee()

        elif choice == "2":
            show_employees()

        elif choice == "3":
            create_location()

        elif choice == "4":
            show_locations()

        elif choice == "5":
            create_shift()

        elif choice == "6":
            show_shifts()

        elif choice == "0":
            print("\nПрограмма завершена!")
            break

        else:
            print("Неверный пункт меню!")


if __name__ == "__main__":
    main()
