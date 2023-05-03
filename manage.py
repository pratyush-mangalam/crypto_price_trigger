#!/usr/bin/env python
import os
import sys
from pathlib import Path

import environ

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django  # noqa
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )

        raise

    # This allows easy placement of apps within the interior
    # todo directory.
    current_path = Path(__file__).parent.resolve()
    sys.path.append(os.path.join(current_path, "todo"))
    if os.environ["DJANGO_SETTINGS_MODULE"] != "config.settings.test":
        env = environ.Env()
        # OS environment variables take precedence over variables from .env
        env.read_env(os.path.join(current_path, ".env"))

    execute_from_command_line(sys.argv)
