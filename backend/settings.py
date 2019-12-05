import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent
config_path = BASE_DIR / 'config' / 'market.yaml'

def get_config():
    with open(config_path) as f:
        config = yaml.safe_load(f)
    return config

config = get_config()
