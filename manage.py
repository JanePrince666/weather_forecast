#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import time
from django.db import OperationalError
from django.core.management import execute_from_command_line


def wait_for_db():
    while True:
        try:
            from django.db import connection
            connection.ensure_connection()
            break
        except OperationalError:
            print("Database is not ready yet, waiting...")
            time.sleep(1)


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_forecast.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weather_forecast.settings")
    wait_for_db()  # Ожидание готовности базы данных
    execute_from_command_line(sys.argv)
