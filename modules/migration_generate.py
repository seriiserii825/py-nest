from classes.Command import Command
from classes.FilesHandle import FilesHandle
from classes.InputValidator import InputValidator
from classes.PathHelper import PathHelper
from classes.Print import Print


def migration_generate():
    pt = PathHelper()
    entry_dir = pt.get_cwd
    migration_dir = entry_dir / 'src/migrations'
    if not migration_dir.exists():
        Print.error('Migrations directory not found')
        exit(1)
    fs = FilesHandle()
    fs.list_files(migration_dir)
    migration_file_name = InputValidator.get_string(
        'Enter migration file name (without extension): ')
    Command.run(
        f'npm run migration:generate src/migrations/{migration_file_name}')
