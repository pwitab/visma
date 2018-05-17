from importlib import import_module
from os import environ


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    Inspired by Django
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path
                          ) from err

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "{0}" does not define a "{1}" attribute/class'.format(
             module_path, class_name)
        ) from err


def get_api_settings_from_env():
    settings = {'token_path': environ.get('VISMA_API_TOKEN_PATH'),
                'client_id': environ.get('VISMA_API_CLIENT_ID'),
                'client_secret': environ.get('VISMA_API_CLIENT_SECRET')}

    if environ.get('VISMA_API_ENV') == 'test':
        settings['test'] = True

    if environ.get('VISMA_API_ENV') == 'production':
        settings['test'] = False


    return settings
