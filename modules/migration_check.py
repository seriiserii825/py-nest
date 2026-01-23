from classes.Command import Command


def migration_check():
    Command.run('npm run migration:check')
