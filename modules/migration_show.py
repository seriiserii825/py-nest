from py_libs.Command import Command


def migration_show():
    Command.run('npm run migration:show')
