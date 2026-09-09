from rich.console import Console
from rich.syntax import Syntax

PACKAGE_JSON_MIGRATIONS = """\
{
  "scripts": {
    "migration:check": "typeorm-ts-node-commonjs migration:generate -d src/data-source.ts src/migrations/TempCheck && echo 'Changes detected!' || echo 'No changes'",
    "migration:to_check": "npx typeorm-ts-node-commonjs schema:log -d src/data-source.ts",
    "migration:generate": "typeorm-ts-node-commonjs migration:generate -d src/data-source.ts",
    "migration:create": "typeorm-ts-node-commonjs migration:create",
    "migration:run": "typeorm-ts-node-commonjs migration:run -d src/data-source.ts",
    "migration:revert": "typeorm-ts-node-commonjs migration:revert -d src/data-source.ts",
    "migration:show": "typeorm-ts-node-commonjs migration:show -d src/data-source.ts"
  }
}
"""


def show_package_json_migrations():
    console = Console(soft_wrap=True)
    syntax = Syntax(PACKAGE_JSON_MIGRATIONS, "json", theme="ansi_dark", line_numbers=False)
    console.print(syntax)
