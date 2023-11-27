import multiprocessing
import os


GAE_ENV = os.environ.get('GAE_ENV')

workers = multiprocessing.cpu_count() * 2 + 1
# if GAE_ENV and GAE_ENV == 'standard':
#     workers = 1

##############################
##############################
from pathlib import Path
import environ

ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent.parent

env = environ.Env()

print(f'ROOT_DIR: {ROOT_DIR}')
env.read_env(str('/Users/selochanlee/___Project/weapon/.env'))
os.environ['PORT'] = '8081'
os.environ['IS_RUN_LOCAL'] = 'True'
workers = 1
##############################
##############################

print(f'* NUM OF WORKERS: {workers}')
