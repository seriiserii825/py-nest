from classes.Command import Command


def migration_run():
    Command.run('npm run migration:run')
