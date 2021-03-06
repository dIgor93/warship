import os
from os.path import join

RPS = float(os.environ.get('RPS') or 0.02)
AREA_WIDTH = 3000
AREA_HEIGHT = 3000
BOTS_COUNT = 10
ENTITY_PATH = 'entities'
STATICS_PATH = join(ENTITY_PATH, 'statics')
MODELS_PATH = join(ENTITY_PATH, 'dynamics')

REDIS_HOST = os.environ.get('REDIS_HOST') or 'localhost'
REDIS_PORT = os.environ.get('REDIS_PORT') or 6379
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD') or ''
