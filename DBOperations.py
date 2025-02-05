import os
import sqlite3
from Formatter import Formatter


class DBOperations:
    """Handles database operations and user interactions"""

    # SQL query constants
    sql_available_tables = "SELECT name FROM sqlite_master WHERE type='table';"
    sql_available_tables_views = (
        "SELECT name FROM sqlite_master WHERE type='table' or type='view';"
    )
    sql_table_info = "PRAGMA table_info({0})"
    sql_select_all = "SELECT {0} FROM {1}"
    sql_search = "SELECT {0} FROM {1} WHERE {2} = ?"
    sql_criteria_search = "SELECT {0} FROM {1} WHERE {2} ORDER BY {3}"
    sql_insert = "INSERT INTO {0} ({1}) VALUES ({2})"
    sql_update_data = "UPDATE {0} SET {1} WHERE {2}"
    sql_delete_data = "DELETE FROM {0} WHERE {1}"

    def __init__(self):
        try:
            self.conn = sqlite3.connect("FlightManagement.db")
            self.cur = self.conn.cursor()
            # Enable foreign key constraints
            self.conn.execute("PRAGMA foreign_keys = ON;")

            # Initialize schema and sample data
            self._initialize_database()

        except Exception as e:
            print(f"Database initialization failed: {str(e)}")

    def _initialize_database(self) -> None:
        """Initialize database schema and sample data"""
        try:
            with open(os.path.join("SQL", "schema.sql"), "r") as sql_script:
                self.conn.executescript(sql_script.read())
            with open(os.path.join("SQL", "views.sql"), "r") as sql_script:
                self.conn.executescript(sql_script.read())
            with open(os.path.join("SQL", "sample_data.sql"), "r") as sql_script:
                self.conn.executescript(sql_script.read())
            self.conn.commit()
        except Exception as e:
            print(f"Failed to initialize database: {str(e)}")

    def select_tables(self) -> None:
        """Main method to handle data selection workflow"""
        available_views = self.cur.execute(self.sql_available_tables_views).fetchall()

        while True:
            # Level 1: Display available views
            print("\nSelect the table of your interest to view records:")
            for index, view in enumerate(available_views, 1):
                print(f" {index}. {view[0]}")
            print(" *. < Back")

            view_choice = input("Enter your choice: ")

            if view_choice == "*":
                return

            if not view_choice.isdigit() or int(view_choice) > len(available_views):
                print("Invalid choice")
                continue

            view_name = available_views[int(view_choice) - 1][0]

            # Level 2: Handle view operations
            while True:
                print(f"\n[{view_name}] Select the data of your interest: ")
                print(" 1. All data")
                print(" 2. Filter by primary key")
                print(" 3. Filter by expression")
                print(" *. < Back")
                print(" **. << Main menu")

                criteria_choice = input("Enter your choice: ")

                if criteria_choice == "**":
                    return
                if criteria_choice == "*":
                    break

                # Level 3: Handle different criteria choices
                try:
                    if criteria_choice == "1":
                        # Show all data
                        cursor = self.cur.execute(
                            self.sql_select_all.format("*", view_name)
                        )
                        Formatter.print_formatted(cursor)

                    elif criteria_choice == "2":
                        # Filter by primary key
                        primary_key = self.cur.execute(
                            self.sql_table_info.format(view_name)
                        ).fetchone()[1]

                        pk_value = input(
                            f"\n[{view_name}] Enter the [{primary_key}] of the record you want to see: "
                        )
                        cursor = self.cur.execute(
                            self.sql_search.format("*", view_name, primary_key),
                            (pk_value,),
                        )
                        Formatter.print_formatted(cursor)

                    elif criteria_choice == "3":
                        # Filter by expression
                        columns = self.cur.execute(
                            self.sql_table_info.format(view_name)
                        )
                        print(f"\n[{view_name}] Available columns:")
                        print(", ".join(column[1] for column in columns))

                        expression = input(
                            f"\n[{view_name}] Enter the expression to filter the data: "
                        )
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*", view_name, expression, "1"
                            )
                        )
                        Formatter.print_formatted(cursor)

                    else:
                        print("Invalid choice")

                except sqlite3.OperationalError as e:
                    print(f"Database operation error: {e}")

    def select_views(self) -> None:

        while True:
            print("\nSelect the view of your interest: ")
            print(" 1. Flights Dashboards")
            print(" 2. Pilots Dashboards")
            print(" 3. Airports Dashboards")
            print(" *. < Back")

            view_choice = input("Enter your choice: ")

            if view_choice == "*":
                return

            if not view_choice.isdigit() or int(view_choice) > 3:
                print("Invalid choice")
                continue

            if view_choice == "1":
                while True:
                    print("\nSelect the view of your interest: ")
                    print(" 1. View In Progress Flights")
                    print(" 2. View Scheduled Flights")
                    print(" 3. View Flights with Missing Data")
                    print(" 4. View Top10 Longest Flights")
                    print(" 5. View All Flights")
                    print(" 6. More Custom Views!")
                    print(" *. < Back")
                    print(" **. << Main menu")

                    view_choice = input("Enter your choice: ")

                    if view_choice == "**":
                        return
                    elif view_choice == "*":
                        break
                    elif view_choice == "1":
                        # In Progress Flights
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedFlightsView",
                                "status = 'In Progress'",
                                "arr_time DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "2":
                        # Scheduled Flights
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedFlightsView",
                                "status = 'Scheduled'",
                                "dep_time DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "3":
                        # Flights with Missing Data
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedFlightsView",
                                "dep_airport IS NULL OR arr_airport IS NULL OR aircraft_model IS NULL OR pilot_name IS NULL OR dep_time IS NULL OR arr_time IS NULL",
                                "arr_time DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "4":
                        # Top10 Longest Flights
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedFlightsView",
                                "duration IS NOT NULL",
                                "duration DESC",
                            )
                            + " LIMIT 10"
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "5":
                        # All Flights
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*", "FlattenedFlightsView", "1", "status DESC"
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "6":
                        self.select_tables()
                    else:
                        print("Invalid choice")

            elif view_choice == "2":
                while True:
                    print("\nSelect the view of your interest: ")
                    print(" 1. View All Pilots by Assigned Flights")
                    print(" 2. View Pilots Schedules")
                    print(" 3. View Pilots with Missing Data")
                    print(" 4. More Custom Views!")
                    print(" *. < Back")
                    print(" **. << Main menu")

                    view_choice = input("Enter your choice: ")

                    if view_choice == "**":
                        return
                    elif view_choice == "*":
                        break
                    elif view_choice == "1":
                        # All Pilots by number of assigned flights
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedPilotsView",
                                "1",
                                "assigned_flights DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "2":
                        # Pilots Schedules
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "pilot_name, flight_number, dep_time, arr_time, duration, aircraft_model",
                                "FlattenedFlightsView",
                                "status = 'Scheduled'",
                                "pilot_name DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "3":
                        # Pilots with Missing Data
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "PilotsView",
                                "qualification IS NULL OR contact_number IS NULL OR date_of_birth IS NULL OR hire_date IS NULL",
                                "1",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "4":
                        self.select_tables()
                    else:
                        print("Invalid choice")

            elif view_choice == "3":
                while True:
                    print("\nSelect the view of your interest: ")
                    print(" 1. View All Airports by Flights Number")
                    print(" 2. View Airports with Scheduled Flights")
                    print(" 3. View Airports with Missing Data")
                    print(" 4. More Custom Views!")
                    print(" *. < Back")
                    print(" **. << Main menu")

                    view_choice = input("Enter your choice: ")

                    if view_choice == "**":
                        return
                    elif view_choice == "*":
                        break
                    elif view_choice == "1":
                        # All Airports by Flights Number
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedAirportsView",
                                "1",
                                "flights_count DESC, flights_status DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "2":
                        # Airports with scheduled flights
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedAirportsView",
                                "flights_status = 'Scheduled'",
                                "flights_count DESC",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "3":
                        # Airports with Missing Data
                        cursor = self.cur.execute(
                            self.sql_criteria_search.format(
                                "*",
                                "FlattenedAirportsView",
                                "airport_name IS NULL OR city IS NULL OR country IS NULL OR timezone IS NULL",
                                "1",
                            )
                        )
                        Formatter.print_formatted(cursor)
                    elif view_choice == "4":
                        self.select_tables()
            else:
                print("Invalid choice")

    def insert_data(self):
        available_tables = self.cur.execute(self.sql_available_tables).fetchall()

        while True:
            # Level 1: Display available table options
            print("\nSelect the table of your interest to add records:")
            for index, view in enumerate(available_tables, 1):
                print(f" {index}. {view[0]}")
            print(" *. < Back")

            view_choice = input("Enter your choice: ")

            if view_choice == "*":
                return

            if not view_choice.isdigit() or int(view_choice) > len(available_tables):
                print("Invalid choice")
                continue

            view_name = available_tables[int(view_choice) - 1][0]

            # Level 2: Handle view operations
            while True:
                print(f"\n[{view_name}] Enter the data to add: ")

                columns = self.cur.execute(
                    self.sql_table_info.format(view_name)
                ).fetchall()

                columns = [
                    (column[1], column[2], "Required" if column[3] == 1 else "Optional")
                    for column in columns
                ]

                data = {}
                for column in columns:
                    data[column] = input(f"Enter the value for {str(column)}: ")

                try:
                    columns_str = ", ".join(column[0] for column in columns)
                    values_str = ", ".join(
                        f"'{data[column]}'" for column in columns
                    ).replace("''", "NULL")

                    self.cur.execute(
                        self.sql_insert.format(view_name, columns_str, values_str)
                    )
                    self.conn.commit()
                    print("Record added successfully!")

                except Exception as e:
                    print(f"Error: {e}")

                add_more = input("Do you want to add more records? [Y/n]: ")
                if add_more.lower() != "y":
                    break

    def update_data(self):
        available_tables = self.cur.execute(self.sql_available_tables).fetchall()

        while True:
            # Level 1: Display available table options
            print("\nSelect the table of your interest to update records:")
            for index, view in enumerate(available_tables, 1):
                print(f" {index}. {view[0]}")
            print(" *. < Back")

            view_choice = input("Enter your choice: ")

            if view_choice == "*":
                return

            if not view_choice.isdigit() or int(view_choice) > len(available_tables):
                print("Invalid choice")
                continue

            view_name = available_tables[int(view_choice) - 1][0]

            # Level 2: Handle view operations
            while True:
                columns = self.cur.execute(
                    self.sql_table_info.format(view_name)
                ).fetchall()

                columns = [
                    [column[1], column[2], "Required" if column[3] == 1 else "Optional"]
                    for column in columns
                ]

                # Step one, ask for the primary key of target record
                pk_name = columns[0][0]
                pk_value = input(
                    f"\n[{view_name}] Enter the [{pk_name}] of the record you want to update: "
                )

                # Step two, get the target record
                selected_record = self.cur.execute(
                    self.sql_search.format("*", view_name, pk_name), (pk_value,)
                ).fetchone()

                if not selected_record:
                    print("Record not found!")
                    break

                # append current values to the columns list at the end
                columns = [
                    column + [selected_record[index]]
                    for index, column in enumerate(columns)
                ]

                print(f"\n[{view_name}] Enter the data to update [{pk_value}]: ")
                print(
                    "HINT: (column_name, data_type, Required/Optional, current_value)"
                )
                print("HINT: Hit enter to keep the current value\n")

                data = {}
                for column in columns:
                    data[column[0]] = input(f"Enter the value for {str(column)}: ")

                # Empty entries are kept as is
                for column in columns:
                    if data[column[0]] == "":
                        data[column[0]] = column[3]

                try:
                    update_str = ", ".join(
                        f"{column[0]} = '{data[column[0]]}'" for column in columns
                    )

                    self.cur.execute(
                        self.sql_update_data.format(
                            view_name, update_str, f"{pk_name} = '{pk_value}'"
                        )
                    )
                    self.conn.commit()
                    print("Record updated successfully!")

                except Exception as e:
                    print(f"Error: {e}")

                update_more = input("Do you want to update more records? [Y/n]: ")
                if update_more.lower() != "y":
                    break

    def delete_data(self):
        available_tables = self.cur.execute(self.sql_available_tables).fetchall()

        while True:
            # Level 1: Display available table options
            print("\nSelect the table of your interest to delete records:")
            for index, view in enumerate(available_tables, 1):
                print(f" {index}. {view[0]}")
            print(" *. < Back")

            view_choice = input("Enter your choice: ")

            if view_choice == "*":
                return

            if not view_choice.isdigit() or int(view_choice) > len(available_tables):
                print("Invalid choice")
                continue

            view_name = available_tables[int(view_choice) - 1][0]

            # Level 2: Handle view operations
            while True:
                columns = self.cur.execute(
                    self.sql_table_info.format(view_name)
                ).fetchall()

                columns = [
                    [column[1], column[2], "Required" if column[3] == 1 else "Optional"]
                    for column in columns
                ]

                # Step one, ask for the primary key of target record
                pk_name = columns[0][0]
                pk_value = input(
                    f"\n[{view_name}] Enter the [{pk_name}] of the record you want to delete: "
                )

                # Step two, get the target record
                cursor = self.cur.execute(
                    self.sql_search.format("*", view_name, pk_name), (pk_value,)
                )

                # Step three, confirm deletion
                try:
                    Formatter.print_formatted(cursor)
                    print(f"\nAre you sure you want to delete this record?")
                    delete_confirm = input("Confirm deletion? [y/N]: ")
                    if delete_confirm.lower() == "y":
                        self.cur.execute(
                            self.sql_delete_data.format(
                                view_name, f"{pk_name} = '{pk_value}'"
                            )
                        )
                        self.conn.commit()
                        print("Record deleted successfully!")
                except Exception as e:
                    print(f"Error: {e}")

                delete_more = input("Do you want to delete more records? [Y/n]: ")
                if delete_more.lower() != "y":
                    break
