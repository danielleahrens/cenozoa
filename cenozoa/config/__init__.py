from .config import Config

import os

config = Config(os.environ['CONFIG_PATH'], os.environ['SECRETS_PATH'])
