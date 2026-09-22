from classes.Print import Print
from classes.Select import Select
from modules.seed import seed
from modules.generate_nest import generate_nest
from modules.migration_check import migration_check
from modules.migration_generate import migration_generate
from modules.migration_revert import migration_revert
from modules.migration_run import migration_run
from modules.migration_show import migration_show
from modules.show_package_json_migrations import show_package_json_migrations


def main_menu():
    options = [
        "Seed",
        "Migration Generate",
        "Migration Run",
        "Migration Revert",
        "Migration Show",
        "Migration Check",
        "Generate (nest g)",
        "Show package json migrations",
        "Exit",
    ]
    selected = Select.select_with_fzf(options, multi=False)
    choice = selected[0] if selected else "Exit"

    try:
        if choice == "Seed":
            seed()
        elif choice == "Migration Generate":
            migration_generate()
            migration_run()
        elif choice == "Migration Run":
            migration_run()
        elif choice == "Migration Revert":
            migration_revert()
        elif choice == "Migration Show":
            migration_show()
        elif choice == "Migration Check":
            migration_check()
        elif choice == "Generate (nest g)":
            generate_nest()
        elif choice == "Show package json migrations":
            show_package_json_migrations()
        else:
            print("Exiting...")
            exit(0)
    except RuntimeError as e:
        Print.error(str(e))

    main_menu()
