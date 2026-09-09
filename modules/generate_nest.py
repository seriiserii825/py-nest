from classes.Command import Command
from classes.InputValidator import InputValidator
from classes.Print import Print
from classes.Select import Select

SCHEMATICS = [
    ("application", "application", "Generate a new application within a monorepo"),
    ("class", "cl", "Generate a new class"),
    ("configuration", "config", "Generate a CLI configuration file"),
    ("controller", "co", "Generate a controller declaration"),
    ("decorator", "d", "Generate a custom decorator"),
    ("filter", "f", "Generate a filter declaration"),
    ("gateway", "ga", "Generate a gateway declaration"),
    ("guard", "gu", "Generate a guard declaration"),
    ("interceptor", "in", "Generate an interceptor declaration"),
    ("interface", "interface", "Generate an interface"),
    ("middleware", "mi", "Generate a middleware declaration"),
    ("module", "mo", "Generate a module declaration"),
    ("pipe", "pi", "Generate a pipe declaration"),
    ("provider", "pr", "Generate a provider declaration"),
    ("resolver", "r", "Generate a GraphQL resolver declaration"),
    ("resource", "res", "Generate a new CRUD resource"),
    ("service", "s", "Generate a service declaration"),
    ("library", "lib", "Generate a new library within a monorepo"),
    ("sub-app", "app", "Generate a new application within a monorepo"),
]


def generate_nest():
    options = [f"{name} - {desc}" for name, _, desc in SCHEMATICS]
    selected = Select.select_with_fzf(options, multi=False)
    if not selected:
        Print.error("Nothing selected")
        return
    choice = options.index(selected[0])
    schematic, alias, _ = SCHEMATICS[choice]

    name = InputValidator.get_string(f"Enter name for {schematic}: ")

    add_spec = InputValidator.get_string(
        "Generate spec files for tests? (y/N): ", allow_empty=True
    ).strip().lower() in ("y", "yes")
    spec_flag = "--spec" if add_spec else "--no-spec"

    Command.run(f"nest g {alias} {name} {spec_flag}")
