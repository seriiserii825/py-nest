from classes.Command import Command


def migration_revert():
    Command.run('npm run migration:revert')
