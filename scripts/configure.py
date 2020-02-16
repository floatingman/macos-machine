#!/usr/bin/env python
"""Configure local settings"""

import sys
from pathlib import Path

# Add project root to to sys.path
FILE = Path(__file__).resolve()
SCRIPTS_DIR, PROJECT_ROOT = FILE.parent, FILE.parents[1]
sys.path.append(str(PROJECT_ROOT))
# Remove the current scripts/ directory from sys.path
try:
    sys.path.remove(str(SCRIPTS_DIR))
except ValueError:  # Already removed
    pass

# pylint: disable=wrong-import-position
from machine import settings  # noqa: E402
# pylint: disable=unused-import
import machine.config  # noqa: E402,F401
# pylint: enable=unused-import
# pylint: enable=wrong-import-position


def display_usage(command):
    """Display usage help"""
    print("Usage: %s [option] [value]" % command)
    sys.exit(1)


def display_option(name):
    """Display current option value"""
    value = settings.get_option(name)
    print("%s: %s" % (name, value))


def update_option(name, new_value):
    """Update option value"""
    value = settings.get_option(name)
    if new_value in settings.TRUTHY:
        if not value:
            settings.enable_option(name)
            print("%s is now enabled" % name)
    elif new_value in settings.FALSY:
        if value:
            settings.disable_option(name)
            print("%s is now disabled" % name)
    else:
        if value != new_value:
            value = settings.set_option(name, new_value)
            print("%s: %s" % (name, value))


if __name__ == '__main__':
    if len(sys.argv) == 3:
        update_option(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        display_option(sys.argv[1])
    else:
        display_usage(sys.argv[0])
