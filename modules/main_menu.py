from classes.Menu import Menu
from modules.generate_resource import generate_resource
from modules.migration_check import migration_check
from modules.migration_generate import migration_generate
from modules.migration_revert import migration_revert
from modules.migration_run import migration_run
from modules.migration_show import migration_show


def main_menu():
    options = [
        "0).Migration Generate",
        "1).Migration Run",
        "2).Migration Revert",
        "3).Migration Show",
        "4).Migration Check",
        "5).Generate Resource",
        "6).Exit",
    ]
    Menu.display("Main Menu", ["Options"], [[opt] for opt in options])
    choice = Menu.choose_option()
    if choice == 0:
        migration_generate()
        main_menu()
    elif choice == 1:
        migration_run()
        main_menu()
    elif choice == 2:
        migration_revert()
        main_menu()
    elif choice == 3:
        migration_show()
        main_menu()
    elif choice == 4:
        migration_check()
        main_menu()
    elif choice == 5:
        generate_resource()
        main_menu()
    else:
        print("Exiting...")
        exit(0)
