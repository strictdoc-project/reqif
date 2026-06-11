import logging
import os.path

__version__ = "0.0.50"

# Follow the standard library convention for logging in libraries: attach a
# NullHandler to the package root logger so that reqif emits no output unless
# the embedding application configures handlers for the "reqif" logger
# hierarchy.
# https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library
logging.getLogger("reqif").addHandler(logging.NullHandler())

PATH_TO_REQIF_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
