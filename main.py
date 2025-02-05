from DBOperations import DBOperations

db_ops = DBOperations()

while True:
    print("\n Menu:")
    print("**********")
    print(" 1. View Dashboards")
    print(" 2. View Data by Criteria")
    print(" 3. Add Records")
    print(" 4. Edit Records")
    print(" 5. Delete Records")
    print(" *. Exit\n")

    try:
        __choose_menu = input("Enter your choice: ")
        if __choose_menu == "1":
            db_ops.select_views()
        elif __choose_menu == "2":
            db_ops.select_tables()
        elif __choose_menu == "3":
            db_ops.insert_data()
        elif __choose_menu == "4":
            db_ops.update_data()
        elif __choose_menu == "5":
            db_ops.delete_data()
        elif __choose_menu == "*":
            exit(0)
        else:
            print("Invalid Choice")
    except Exception as e:
        print(e)
        print("Invalid Choice")
        continue
