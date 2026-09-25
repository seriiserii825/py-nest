from py_libs.Command import Command


def migration_revert():
    Command.run('npm run migration:revert')
