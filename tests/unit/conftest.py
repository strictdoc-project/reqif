import os
import sys

REQIF_ROOT_PATH = os.path.abspath(os.path.join(__file__, "../../../../reqif"))
assert os.path.exists(REQIF_ROOT_PATH), "does not exist: {}".format(
    REQIF_ROOT_PATH
)
sys.path.append(REQIF_ROOT_PATH)
