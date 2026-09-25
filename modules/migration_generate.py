from py_libs.Command import Command
from py_libs.FilesHandle import FilesHandle
from py_libs.InputValidator import InputValidator
from py_libs.Print import Print

from classes.PathHelper import PathHelper


def migration_generate():
    pt = PathHelper()
    entry_dir = pt.get_cwd
    migration_dir = entry_dir / 'src/migrations'
    if not migration_dir.exists():
        Print.error('Migrations directory not found')
        exit(1)
    fs = FilesHandle()
    fs.list_files(migration_dir, mtime=True)
    migration_file_name = InputValidator.get_string(
        'Enter migration file name (without extension): ')
    Command.run(
        f'npm run migration:generate src/migrations/{migration_file_name}')
