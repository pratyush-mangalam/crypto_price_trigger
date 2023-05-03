from .base import *

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    default="django-insecure-t^*4c12p%_^=1c75fm$nb-2bcp)osf&u78dtw#rh_b@+2+es#g",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1"]