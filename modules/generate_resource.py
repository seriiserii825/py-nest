from classes.Command import Command
from classes.InputValidator import InputValidator


def generate_resource():
    resource_name = InputValidator.get_string(
        'Enter resource name, (user, category, review): ')
    Command.run(f'nest g res {resource_name} --no-spec')
