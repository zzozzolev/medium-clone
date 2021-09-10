#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    if 'SECRET_KEY' not in os.environ:
        set_secret_key()

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def set_secret_key():
    env_file_path = '../docker/.env'
    if os.path.isfile(env_file_path):
        with open(env_file_path) as f:
            for line in f:
                key, value = line.split('=')
                if key == 'SECRET_KEY':
                    os.environ['SECRET_KEY'] = value.strip()


if __name__ == '__main__':
    main()
