from py_libs.Command import Command


def migration_run():
    Command.run('npm run migration:run')
