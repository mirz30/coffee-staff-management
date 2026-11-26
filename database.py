
import sqlite3
from datetime import datetime


DB_NAME = "coffee_staff.db"


# =====================================
# ПОДКЛЮЧЕНИЕ К БАЗЕ ДАННЫХ
# =====================================

def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row

    # Включаем проверку внешних ключей
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# =====================================
# СОЗДАНИЕ ТАБЛИЦ
# =====================================

def init_db():
    with get_connection() as connection:

        # Таблица сотрудников
        connection.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                position TEXT NOT NULL,
                phone TEXT,
                hire_date TEXT
            )
        """)

        # Таблица рабочих точек
        connection.execute("""
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                address TEXT
            )
        """)

        # Таблица смен
        connection.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER NOT NULL,
                location_id INTEGER NOT NULL,
                shift_date TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,

                FOREIGN KEY (employee_id)
                    REFERENCES employees(id),

                FOREIGN KEY (location_id)
                    REFERENCES locations(id),

                CHECK (start_time < end_time)
            )
        """)


# =====================================
# РАБОТА С СОТРУДНИКАМИ
# =====================================

def add_employee(full_name, position, phone, hire_date):

    with get_connection() as connection:
        connection.execute("""
            INSERT INTO employees (
                full_name,
                position,
                phone,
                hire_date
            )
            VALUES (?, ?, ?, ?)
        """, (
            full_name,
            position,
            phone,
            hire_date
        ))


def get_employees():

    with get_connection() as connection:
        employees = connection.execute("""
            SELECT * FROM employees
            ORDER BY id
        """).fetchall()

        return [dict(employee) for employee in employees]


# =====================================
# РАБОТА С РАБОЧИМИ ТОЧКАМИ
# =====================================

def add_location(name, address):

    with get_connection() as connection:
        connection.execute("""
            INSERT OR IGNORE INTO locations (
                name,
                address
            )
            VALUES (?, ?)
        """, (name, address))


def get_locations():

    with get_connection() as connection:
        locations = connection.execute("""
            SELECT * FROM locations
            ORDER BY id
        """).fetchall()

        return [dict(location) for location in locations]


# =====================================
# ПРОВЕРКА КОНФЛИКТОВ СМЕН
# =====================================

def check_shift_conflict(
    employee_id,
    location_id,
    shift_date,
    start_time,
    end_time
):

    with get_connection() as connection:

        conflict = connection.execute("""
            SELECT
                shifts.id,
                shifts.employee_id,
                shifts.location_id,
                shifts.shift_date,
                shifts.start_time,
                shifts.end_time,
                employees.full_name AS employee_name,
                locations.name AS location_name

            FROM shifts

            JOIN employees
                ON shifts.employee_id = employees.id

            JOIN locations
                ON shifts.location_id = locations.id

            WHERE shifts.shift_date = ?

            AND (
                shifts.employee_id = ?
                OR shifts.location_id = ?
            )

            AND shifts.start_time < ?
            AND shifts.end_time > ?

            LIMIT 1
        """, (
            shift_date,
            employee_id,
            location_id,
            end_time,
            start_time
        )).fetchone()

        return dict(conflict) if conflict else None


# =====================================
# ДОБАВЛЕНИЕ СМЕНЫ
# =====================================

def add_shift(
    employee_id,
    location_id,
    shift_date,
    start_time,
    end_time
):

    # Проверяем формат даты и времени
    try:
        datetime.strptime(shift_date, "%Y-%m-%d")

        start = datetime.strptime(
            start_time, "%H:%M"
        )

        end = datetime.strptime(
            end_time, "%H:%M"
        )

    except ValueError:
        raise ValueError(
            "Неверный формат даты или времени!"
        )

    # Проверяем последовательность времени
    if start >= end:
        raise ValueError(
            "Время окончания должно быть позже начала!"
        )

    # Проверяем конфликты
    conflict = check_shift_conflict(
        employee_id,
        location_id,
        shift_date,
        start_time,
        end_time
    )

    if conflict:

        if conflict["employee_id"] == employee_id:
            raise ValueError(
                f"Сотрудник {conflict['employee_name']} "
                f"уже имеет смену в это время!"
            )

        if conflict["location_id"] == location_id:
            raise ValueError(
                f"Рабочая точка {conflict['location_name']} "
                f"уже занята в это время!"
            )

    # Добавляем смену
    with get_connection() as connection:

        connection.execute("""
            INSERT INTO shifts (
                employee_id,
                location_id,
                shift_date,
                start_time,
                end_time
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            employee_id,
            location_id,
            shift_date,
            start_time,
            end_time
        ))

    print("Смена успешно добавлена!")


# =====================================
# ПОЛУЧЕНИЕ ВСЕХ СМЕН
# =====================================

def get_shifts():

    with get_connection() as connection:

        shifts = connection.execute("""
            SELECT
                shifts.id,
                shifts.employee_id,
                shifts.location_id,
                employees.full_name AS employee_name,
                locations.name AS location_name,
                shifts.shift_date,
                shifts.start_time,
                shifts.end_time

            FROM shifts

            JOIN employees
                ON shifts.employee_id = employees.id

            JOIN locations
                ON shifts.location_id = locations.id

            ORDER BY
                shifts.shift_date,
                shifts.start_time
        """).fetchall()

        return [dict(shift) for shift in shifts]
