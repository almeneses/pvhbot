import sys
import os
import logging
from dotenv import dotenv_values


def load_config(app):
    config = dotenv_values()
    app.config.update(config)
