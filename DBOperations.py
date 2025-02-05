import os
import sqlite3
from Flights import Flights
from Formatter import Formatter


class DBOperations:
    """Handles database operations and user interactions"""

    # SQL query constants
    sql_available_tables_views = (
        "SELECT name FROM sqlite_master WHERE type='table' or type='view';"
    )
    sql_table_info = "PRAGMA table_info({0})"
    sql_select_all = "SELECT {0} FROM {1}"
    sql_search = "SELECT {0} FROM {1} WHERE {2} = ?"
    sql_criteria_search = "SELECT {0} FROM {1} WHERE {2} ORDER BY {3}"

    sql_insert = ""
    sql_alter_data = ""
    sql_update_data = ""
    sql_delete_data = ""

    def __init__(self):
        try:
            self.conn = sqlite3.connect("FlightManagement.db")
            self.cur = self.conn.cursor()

            # Initialize schema and sample data
            self._initialize_database()

            # Enable foreign key constraints
            self.conn.execute("PRAGMA foreign_keys = ON;")

        except Exception as e:
            print(f"Database initialization failed: {str(e)}")

    def _initialize_database(self) -> None:
        """Initialize database schema and sample data"""
        try:
            with open(os.path.join("SQL", "schema.sql"), "r") as sql_script:
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
            print("\nSelect the table of your interest: ")
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
            print(" 3. Destinations Dashboards")
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
                    print(" 1. View All Destinations by Flights Number")
                    print(" 2. View Destinations with Scheduled Flights")
                    print(" 3. View Destinations with Missing Data")
                    print(" 4. More Custom Views!")
                    print(" *. < Back")
                    print(" **. << Main menu")

                    view_choice = input("Enter your choice: ")

                    if view_choice == "**":
                        return
                    elif view_choice == "*":
                        break
                    elif view_choice == "1":
                        # All Destinations by Flights Number
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
                        # Destinations with scheduled flights
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
                        # Destinations with Missing Data
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
        try:
            self.get_connection()

            flight = Flights()
            flight.set_flight_id(int(input("Enter FlightID: ")))

            self.cur.execute(self.sql_insert, tuple(str(flight).split("\n")))

            self.conn.commit()
            print("Inserted data successfully")
        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def select_all(self):
        try:
            self.get_connection()
            self.cur.execute(self.sql_select_all)
            result = self.cur.fetchall()

            # think how you could develop this method to show the records

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def search_data(self):
        try:
            self.get_connection()
            flightID = int(input("Enter FlightNo: "))
            self.cur.execute(self.sql_search, tuple(str(flightID)))
            result = self.cur.fetchone()
            if type(result) == type(tuple()):
                for index, detail in enumerate(result):
                    if index == 0:
                        print("Flight ID: " + str(detail))
                    elif index == 1:
                        print("Flight Origin: " + detail)
                    elif index == 2:
                        print("Flight Destination: " + detail)
                    else:
                        print("Status: " + str(detail))
            else:
                print("No Record")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    def update_data(self):
        try:
            self.get_connection()

            # Update statement

            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()

    # Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.

    def delete_data(self):
        try:
            self.get_connection()

            if result.rowcount != 0:
                print(str(result.rowcount) + "Row(s) affected.")
            else:
                print("Cannot find this record in the database")

        except Exception as e:
            print(e)
        finally:
            self.conn.close()
