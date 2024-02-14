import sys

from itdagene.settings.base import *

TESTING = "test" in sys.argv  # Check if manage.py test has been run
COLLECTING_STATIC = "collectstatic" in sys.argv  # Check if collecting static files

if COLLECTING_STATIC:
    SECRET_KEY = "no-secret"
elif TESTING:
    from itdagene.settings.test import *
# else:
#     from itdagene.settings.local import *
