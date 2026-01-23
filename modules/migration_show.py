from classes.Command import Command


def migration_show():
    Command.run('npm run migration:show')
