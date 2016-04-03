#!/usr/bin/env python
import os
import sys
import fabfile

if __name__ == "__main__":
    if fabfile.env("check"):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings_development")

        from django.core.management import execute_from_command_line

        execute_from_command_line(sys.argv)
